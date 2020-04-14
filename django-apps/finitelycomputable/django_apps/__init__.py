def run():
    from sys import argv
    from django.core.management import execute_from_command_line
    execute_from_command_line([
        argv[0],
        'runserver',
        '--settings', 'finitelycomputable.django_apps.settings',
    ])
