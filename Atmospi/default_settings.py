# Atmospi settings.
import os.path
import sys

atmospi_dir = os.path.split(__file__)[0]

settings = {

    # Absolute path to the SQLite database file.
    'db': os.path.normpath(os.path.join(atmospi_dir, '..', 'log.db')),

    # How far into the past should data be loaded (in seconds)?
    # Default to 1 week.
    'range_seconds': 60 * 60 * 24 * 7,

    # The number of digits after the decimal place that will be stored.
    'precision': 2,

    # Temperature unit of measure (C or F).
    't_unit': 'C',
}

print >>sys.stderr, "DB PATH: {}".format(settings['db'])
