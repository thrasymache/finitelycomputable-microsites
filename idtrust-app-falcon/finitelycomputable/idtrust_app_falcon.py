import falcon
from jinja2 import Environment, PackageLoader
from os import environ
from posixpath import join
from finitelycomputable.idtrust_db.controller import (
        dialog_from_id, journey_from_id, create_dialog, interact_core
)
from finitelycomputable.idtrust_common.strategies import Strategy
from finitelycomputable.idtrust_falcon import App


def urlfor_new_dialog(blind, journey_id=None):
    if journey_id is None:
        if blind:
            return join(base_path, '')
        else:
            return join(base_path, 'choose_miscommunication')
    else:
        if blind:
            return join(base_path, f'journey/{journey_id}')
        else:
            return join(base_path,
                    f'journey/{journey_idk}/choose_miscommunication')

def urlfor_interact(pk, blind):
    if blind:
        return join(base_path, f'interact/{pk}')
    else:
        return join(base_path, f'interact/{pk}/choose_miscommunication')

env = Environment(
    loader=PackageLoader('finitelycomputable.idtrust_common', 'templates')
)

class HomeBlind(object):
    template = env.get_template('interaction_begin.html')

    def on_get(self, req, resp):
        resp.text = self.template.render(**{
            'blind': True,
            'journey': None,
            'form': None,
            'blind_toggle_url': urlfor_new_dialog(False),
        })
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        media = req.get_media()
        obj = create_dialog(
                None,
                media.get('user_miscommunication'),
                media.get('foil_miscommunication'),
        )
        interact_core(obj, True, media.get('user_intent'))
        raise falcon.HTTPFound(urlfor_interact(obj.id, True))


class HomeReveal(object):
    template = env.get_template('interaction_begin.html')

    def on_get(self, req, resp):
        resp.text = self.template.render(**{
            'blind': False,
            'journey': None,
            'form': None,
            'blind_toggle_url': urlfor_new_dialog(True),
        })
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        media = req.get_media()
        obj = create_dialog(
                None,
                media.get('user_miscommunication'),
                media.get('foil_miscommunication'),
        )
        interact_core(obj, True, media.get('user_intent'))
        raise falcon.HTTPFound(urlfor_interact(obj.id, True))


class JourneyBlind(object):
    template = env.get_template('interaction_begin.html')

    def on_get(self, req, resp, pk):
        try:
            journey = journey_from_id(pk)
        except:
            raise falcon.HTTPNotFound(description=f"Journey {pk} not found.")
        resp.text = self.template.render(**{
            'blind': True,
            'journey': journey,
            'form': None,
            'blind_toggle_url': urlfor_new_dialog(True),
        })
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, pk):
        try:
            journey = journey_from_id(pk)
        except:
            raise falcon.HTTPNotFound(description=f"Journey {pk} not found.")
        media = req.get_media()
        obj = create_dialog(
                journey,
                media.get('user_miscommunication'),
                media.get('foil_miscommunication'),
        )
        interact_core(obj, True, media.get('user_intent'))
        raise falcon.HTTPFound(urlfor_interact(obj.id, True))


class JourneyReveal(object):
    template = env.get_template('interaction_begin.html')

    def on_get(self, req, resp, pk):
        try:
            journey = journey_from_id(pk)
        except:
            raise falcon.HTTPNotFound(description=f"Journey {pk} not found.")
        resp.text = self.template.render(**{
            'blind': False,
            'journey': journey,
            'form': None,
            'blind_toggle_url': urlfor_new_dialog(True),
        })
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, pk):
        try:
            journey = journey_from_id(pk)
        except:
            raise falcon.HTTPNotFound(description=f"Journey {pk} not found.")
        media = req.get_media()
        obj = create_dialog(
                journey,
                media.get('user_miscommunication'),
                media.get('foil_miscommunication'),
        )
        interact_core(obj, False, media.get('user_intent'))
        raise falcon.HTTPFound(urlfor_interact(obj.id, False))


class InteractBlind(object):
    template = env.get_template('interaction.html')

    def on_get(self, req, resp, pk):
        try:
            interaction = dialog_from_id(pk)
        except:
            raise falcon.HTTPNotFound(description=f"Dialog {pk} not found.")
        resp.text = self.template.render(
            new_partner_url=urlfor_new_dialog(
                    blind=True,
                    journey_id=interaction.journey_id,
            ),
            new_journey_url=urlfor_new_dialog(blind=True),
            **interact_core(interaction, True, None, None)
        )
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, pk):
        try:
            interaction = dialog_from_id(pk)
        except:
            raise falcon.HTTPNotFound(description=f"Dialog {pk} not found.")
        media = req.get_media()
        resp.text = self.template.render(
            new_partner_url=urlfor_new_dialog(
                    blind=True,
                    journey_id=interaction.journey_id,
            ),
            new_journey_url=urlfor_new_dialog(blind=True),
            **interact_core(
                interaction,
                True,
                media.get('user_intent'),
                media.get('user_guess'),
        ))
        resp.status = falcon.HTTP_200


application = App(media_type=falcon.MEDIA_HTML)
application.req_options.strip_url_path_trailing_slash = True
base_path = join('/', environ.get('BASE_PATH', ''))
application.add_route(join(base_path, ''), HomeBlind())
application.add_route(join(base_path, 'choose_miscommunication'), HomeReveal())
application.add_route(join(base_path, 'journey/{pk}'), JourneyBlind())
application.add_route(
        join(base_path, 'journey/{pk}/choose_miscommunication'),
        JourneyReveal()
)
application.add_route(join(base_path, 'interact/{pk}'), InteractBlind())


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
