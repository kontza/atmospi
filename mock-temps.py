#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import glob
import time
import sqlite3 as lite
import re
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if __name__=="__main__":
    month_in_seconds = 30 * 24 * 3600
    timestamps = range(int(time.time()-month_in_seconds), int(time.time()), 300)
    device = '28-000000000001'
    temps = []
    con = None
    for ts in timestamps:
        gm = time.gmtime(ts)
        temp_c = gm[3] + gm[4]/60
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        temps.append((ts, temp_c, temp_f))
    try:
        con = lite.connect('log.db')
        db = con.cursor()

        # Iterate through the devices.
        db.execute("delete from Temperature;")
        for timestamp, temp_c, temp_f in temps:
            db.execute("INSERT INTO Temperature (DeviceID, Timestamp, C, F) VALUES(" + str(1) + ", " + str(timestamp) + ", " + str(temp_c) + ", " + str(temp_f) + ")")

        # Commit the changes to the database.
        con.commit()

    except lite.Error as e:
        if con:
            con.rollback()
        logger.error("Error {}:".format(e.args[0]))
        sys.exit(1)

    finally:
        if con:
            con.close()
