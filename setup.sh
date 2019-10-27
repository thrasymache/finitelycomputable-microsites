#! /bin/sh
# setuputils and distutils make an impressive fraud of being able to simply
# configure multiple distributions (which are the smallest
# independently-installable unit) to be built from the same directory, but back
# in the 70s they understood how to do this sort of thing.
python id_trust/setup.py $*
python omnibus/setup.py $*
