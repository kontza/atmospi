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

def read_temps():
    temps = {}
    for file in device_files:
        lines = read_temp_raw(file)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.5)
            lines = read_temp_raw(file)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0

            # Round all measurements to the precision defined in settings.
            temp_c = round(temp_c, settings['precision'])
            temp_f = round(temp_f, settings['precision'])

            # Get the unique name of the device.
            device = file
            device = re.sub('/sys/bus/w1/devices/', '', device)
            device = re.sub('/w1_slave', '', device)

            # Add the measurement to the temps array.
            temps[device] = {'C': temp_c, 'F': temp_f}
    return temps

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
        print("Error {}:".format(e.args[0]))
        sys.exit(1)

    finally:
        if con:
            con.close()
