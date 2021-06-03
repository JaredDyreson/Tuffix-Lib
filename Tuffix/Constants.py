##########################################################################
# constants
# AUTHOR: Kevin Wortman
##########################################################################

import packaging.version
import pathlib

VERSION = packaging.version.parse('0.1.0')

STATE_PATH = pathlib.Path('/var/lib/tuffix/state.json')
PICKLE_PATH = pathlib.Path('/var/lib/tuffix/pickle_jar')
JSON_PATH = pathlib.Path('/var/lib/tuffix/json_payloads')

KEYWORD_MAX_LENGTH = 8
