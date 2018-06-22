#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # this is an unusable default - a specifc settings MUST be selected
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omnibus.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
