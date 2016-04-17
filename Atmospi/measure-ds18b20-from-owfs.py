#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import os
import os.path
import sqlite3
import syslog
import time

# Import settings.
try:
    from settings import settings
except ImportError:
    from default_settings import settings


def store_temp(sensor_name, temp_c):
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    try:
        con = sqlite3.connect(settings['db'])
        db = con.cursor()

        # Get the current timestamp as an integer.
        timestamp = int(time.time())

        # Retrieve the device ID from the Devices table.
        db.execute("SELECT DeviceID FROM Devices WHERE Type = 'ds18b20' AND SerialID = ?", (sensor_name, ))
        result = db.fetchone()

        # If the ID wasn't found, add it automatically.
        if result is None:
            db.execute("INSERT INTO Devices (DeviceID, Type, SerialID, Label) VALUES (NULL, 'ds18b20', ?, ?)",
                       (sensor_name, sensor_name,))
            id = db.lastrowid

        # Otherwise, use the returned ID.
        else:
            id = result[0]

        # Record the temperatures to the database.
        db.execute("INSERT INTO Temperature (DeviceID, Timestamp, C, F) VALUES(?,?,?,?)",
                   (id, timestamp, temp_c, temp_f, ))

        # Commit the changes to the database.
        con.commit()

    except sqlite3.Error, e:
        if con:
            con.rollback()
        syslog.syslog(syslog.LOG_ERR, "Error : {}".format(e.args[0]))

    finally:
        if con:
            con.close()


def read_temp_from_dir(temp_sensor_path):
    with open(os.path.join(temp_sensor_path, 'temperature')) as f:
        temp = float(f.readlines()[0])
        sensor_name = os.path.basename(temp_sensor_path)
        syslog.syslog(syslog.LOG_INFO, "Reading {}: {}".format(sensor_name, temp))
        store_temp(sensor_name, temp)

if __name__ == "__main__":
    syslog.openlog('atmospi')
    for entry in glob.glob("/media/1-wire/10.*"):
        read_temp_from_dir(entry)
    syslog.closelog()
