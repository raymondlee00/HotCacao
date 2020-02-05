#!/usr/bin/python3
import sys
sys.path.insert(0,"/var/www/hotcocoa/")
sys.path.insert(0,"/var/www/hotcocoa/hotcocoa/")

import logging
logging.basicConfig(stream=sys.stderr)

from hotcocoa import app as application
