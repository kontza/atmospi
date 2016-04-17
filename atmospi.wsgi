#!/usr/bin/python
import os
import os.path
import sys
import logging

logging.basicConfig(stream=sys.stderr)

atmospi_dir = os.path.split(__file__)[0]
sys.path.insert(0, atmospi_dir)
print >>sys.stderr, "Atmospi home: {}".format(atmospi_dir)
from Atmospi import app as application
