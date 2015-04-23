#!/usr/bin/python
# -*- coding: utf-8 -*-

# Takes data from measData file, increments it by some amount,
# writes a JSON file with the timestamp and the data JSON file 
# is named sensor_data-deviceID-[ISO 8601 timestamp].json

import sys
import json 
import time
import datetime

def splitdata(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines(True)

    return data[1:-1]
def makeJsonFile(dataline):
    # ISO 8601 timestamp eg. '2015-01-28T16:24:48' 
    deviceID = "4577"

    year = int(dataline[0][:4])
    month = int(dataline[0][5:7])
    day = int(dataline[0][-2:])

    hours = int(dataline[1][:2])
    minutes = int(dataline[1][3:5])
    seconds = int(dataline[1][6:8])

    unixTimestamp = time.mktime(datetime.datetime(year, month, day, hours, minutes, seconds).timetuple())

    deviceID = "4577"

    measValues = dict()
    measValues['measurepA'] = dataline[3]
    measValues['measuremg'] = dataline[2]
    measValues['measureN'] = dataline[4]

    ISOTimestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(unixTimestamp))  
    deviceDict = dict([('deviceID', deviceID), ('firmwareVersion', '0'),
        ('locationCoordinates', "-"),s ('locationTxt', location),
        ('measurementValues', measValues)])
    devTimeDict = dict([('timestamp', ISOTimestamp), ('device', deviceDict)]) 
    wholeThingDict = dict([('nettaData', devTimeDict)])

    filename = "sensor_data-" + deviceID + "-" + str(int(unixTimestamp)) + ".json"
    f = open(filename, 'w+')

    json.dump(wholeThingDict, f, indent=4, separators=(',', ': '), sort_keys=True)
    f.close()
    return filename

def main(argv):
    # get deviceID and location from command line arguments
    if len(argv) == 1:
        if (argv[0][-3:] == "txt"):
            print("Sending data from file to cloud")
            data = splitdata(argv[0])
            for line in data:
                jsonfile = makeJsonFile(line.split())
                # TÄSSÄ LÄHETETÄÄN JSON PILVEEN
                # TÄSSÄ POISTATAAN JSON
        else:
            print("invalid file")
    else:
        print("Invalid arguments")
        print("Correct usage: python json_maker.py [filename]")

if __name__ == "__main__":
    main(sys.argv[1:]) 
