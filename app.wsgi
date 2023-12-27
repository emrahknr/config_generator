#! /usr/bin/python3.6

import logging
import sys

logging.basicConfig(stream=sys.stderr)

sys.path.insert(0,"/var/www/html/ne80_config_generator")

from app import app as application
