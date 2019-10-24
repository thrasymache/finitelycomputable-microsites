#! /usr/bin/env python3
# For other options in running bjoern see https://github.com/jonashaag/bjoern

from omnibus.wsgi import application
import bjoern
import sys

if __name__ == '__main__':
    try:
        bjoern.run(application, "127.0.0.1", 8000)
    except KeyboardInterrupt:
        sys.exit(1)
