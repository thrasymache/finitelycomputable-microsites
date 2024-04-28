import falcon
from jinja2 import Environment, PackageLoader
from os import environ
from posixpath import join
from finitelycomputable.idtrust_db.controller import (
        dialog_from_id, journey_from_id, create_dialog, interact_core
)
from finitelycomputable.idtrust_common.strategies import Strategy
from finitelycomputable.idtrust_falcon import App


def urlfor_new_dialog(app_path, blind, journey_id=None):
    if journey_id is None:
        if blind:
            return app_path
        else:
            return join(app_path, f'choose_miscommunication')
    else:
        if blind:
            return join(app_path, f'journey/{journey_id}')
        else:
            return join(app_path,
                f'journey/{journey_id}/choose_miscommunication')

def urlfor_interact(app_path, pk, blind):
    if blind:
        return join(app_path, f'interact/{pk}')
    else:
        return join(app_path, f'interact/{pk}/reveal_miscommunication')

env = Environment(
    loader=PackageLoader('finitelycomputable.idtrust_common', 'templates')
)

class Home(object):
    template = env.get_template('interaction_begin.html')

    def __init__(self, app_path):
        self.app_path = app_path

    def on_get(self, req, resp, blind):
        resp.text = self.template.render(**{
            'blind': blind,
            'journey': None,
            'form': None,
            'blind_toggle_url': urlfor_new_dialog(self.app_path, not blind),
        })
        resp.status = falcon.HTTP_200

    def on_get_blind(self, req, resp):
        return self.on_get(req, resp, True)

    def on_get_reveal(self, req, resp):
        return self.on_get(req, resp, False)

    def on_post(self, req, resp, blind):
        media = req.get_media()
        obj = create_dialog(
                None,
                media.get('user_miscommunication'),
                media.get('foil_miscommunication'),
        )
        interact_core(obj, blind, media.get('user_intent'))
        raise falcon.HTTPFound(urlfor_interact(self.app_path, obj.id, blind))

    def on_post_blind(self, req, resp):
        return self.on_post(req, resp, True)

    def on_post_reveal(self, req, resp):
        return self.on_post(req, resp, False)


class Journey(object):
    template = env.get_template('interaction_begin.html')

    def __init__(self, app_path):
        self.app_path = app_path

    def get_resource(self, pk):
        try:
            return journey_from_id(pk)
        except:
            raise falcon.HTTPNotFound(description=f"Journey {pk} not found.")

    def on_get(self, req, resp, pk, blind):
        journey = self.get_resource(pk)
        resp.text = self.template.render(**{
            'blind': blind,
            'journey': journey,
            'form': None,
            'blind_toggle_url': urlfor_new_dialog(self.app_path, not blind, pk),
        })
        resp.status = falcon.HTTP_200

    def on_get_blind(self, req, resp, pk):
        return self.on_get(req, resp, pk, True)

    def on_get_reveal(self, req, resp, pk):
        return self.on_get(req, resp, pk, False)

    def on_post(self, req, resp, pk, blind):
        journey = self.get_resource(pk)
        media = req.get_media()
        obj = create_dialog(
                journey,
                media.get('user_miscommunication'),
                media.get('foil_miscommunication'),
        )
        interact_core(obj, blind, media.get('user_intent'))
        raise falcon.HTTPFound(urlfor_interact(self.app_path, obj.id, blind))

    def on_post_blind(self, req, resp, pk):
        return self.on_post(req, resp, pk, True)

    def on_post_reveal(self, req, resp, pk):
        return self.on_post(req, resp, pk, False)


class Interact(object):
    template = env.get_template('interaction.html')

    def __init__(self, app_path):
        self.app_path = app_path

    def get_resource(self, pk):
        try:
            return dialog_from_id(pk)
        except:
            raise falcon.HTTPNotFound(description=f"Dialog {pk} not found.")

    def on_get(self, req, resp, pk, blind):
        interaction = self.get_resource(pk)
        resp.text = self.template.render(
            new_partner_url=urlfor_new_dialog(self.app_path,
                    blind=blind,
                    journey_id=interaction.journey_id,
            ),
            new_journey_url=urlfor_new_dialog(self.app_path, blind=blind),
            blind_toggle_url=urlfor_interact(self.app_path, pk, blind=not blind),
            **interact_core(interaction, blind, None, None)
        )
        resp.status = falcon.HTTP_200

    def on_get_blind(self, req, resp, pk):
        return self.on_get(req, resp, pk, True)

    def on_get_reveal(self, req, resp, pk):
        return self.on_get(req, resp, pk, False)

    def on_post(self, req, resp, pk, blind):
        interaction = self.get_resource(pk)
        media = req.get_media()
        resp.text = self.template.render(
            new_partner_url=urlfor_new_dialog(
                    self.app_path,
                    blind=blind,
                    journey_id=interaction.journey_id,
            ),
            new_journey_url=urlfor_new_dialog(
                self.app_path, blind=blind),
            blind_toggle_url=urlfor_interact(self.app_path, pk, blind=not blind),
            **interact_core(
                interaction,
                blind,
                media.get('user_intent'),
                media.get('user_guess'),
        ))
        resp.status = falcon.HTTP_200

    def on_post_blind(self, req, resp, pk):
        return self.on_post(req, resp, pk, True)

    def on_post_reveal(self, req, resp, pk):
        return self.on_post(req, resp, pk, False)


def add_routes(app, app_path):
    home = Home(app_path)
    app.add_route(app_path, home, suffix='blind')
    app.add_route(
            join(app_path, 'choose_miscommunication'), home, suffix='reveal')
    journey = Journey(app_path)
    app.add_route(join(app_path, 'journey/{pk}'), journey, suffix='blind')
    app.add_route(
            join(app_path, 'journey/{pk}/choose_miscommunication'),
            journey, suffix='reveal'
    )
    interact = Interact(app_path)
    app.add_route(join(app_path, 'interact/{pk}'), interact, suffix='blind')
    app.add_route(join(app_path, 'interact/{pk}/reveal_miscommunication'),
        interact, suffix='reveal')


application = App(media_type=falcon.MEDIA_HTML)
application.req_options.strip_url_path_trailing_slash = True
base_path = join('/', environ.get('BASE_PATH', ''))

add_routes(application, base_path)


def run():
    from sys import argv, exit, stderr
    from wsgiref import simple_server
    if len(argv) < 2 or argv[1] != 'run':
        stderr.write(f'usage: {argv[0]} run [port]\n')
        exit(1)
    try:
        port=int(argv[2])
    except IndexError:
        port=8080
    simple_server.make_server('0.0.0.0', port, application).serve_forever()
