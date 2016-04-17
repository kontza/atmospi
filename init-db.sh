#!/bin/sh
rm log.db
sqlite3 log.db << EOF
CREATE TABLE Devices(DeviceID INTEGER PRIMARY KEY, Type TEXT, SerialID TEXT, Label TEXT);
CREATE TABLE Temperature(DeviceID INT, Timestamp INT, C REAL, F REAL);
CREATE TABLE Humidity(DeviceID INT, Timestamp INT, H REAL);
CREATE TABLE Flag(DeviceID INT, Timestamp INT, Value TEXT);
CREATE INDEX temperature_dt ON Temperature(DeviceID, Timestamp);
CREATE INDEX humidity_dt ON Humidity(DeviceID, Timestamp);
CREATE INDEX flag_dt ON Flag(DeviceID, Timestamp);
EOF
python ./mock-temps.py
