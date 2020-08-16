def run():
    from sys import argv
    from django.core.management import execute_from_command_line

    if len(argv) <= 1:
        argv.append('help')
    elif len(argv) > 1 and argv[1] == 'run':
        argv[1] = 'runserver'
    command_line = (
        argv[0:2] +
        ['--settings', 'finitelycomputable.django_apps.settings.dev'] +
        argv[2:]
    )
    execute_from_command_line(command_line)
