#!/usr/bin/python
# -*- coding: utf-8 -*-

# Takes data from measData file, increments it by some amount,
# writes a JSON file with the timestamp and the data JSON file 
# is named netta_data-deviceID-[ISO 8601 timestamp].json

import sys
import json 
import time
import random

def randomValue(value):
    return value + (value / 10) * random.random()
def newValues(values):
    return [randomValue(item) for item in values]

def makeMeasurementValues(data):
    measValues = dict()
    measValues['measurepA'] = data[0]
    measValues['measuremg'] = data[1]
    measValues['measureN'] = data[2]
    measValues['zeroLevel'] = data[3]
    measValues['coronaI'] = data[4]
    measValues['coronaU'] = data[5]
    measValues['trapU'] = data[6]
    measValues['tempAmbient'] = data[7]
    measValues['tempProcess'] = data[8]
    measValues['tempSensor'] = data[9]
    measValues['tempInlet'] = data[10]
    measValues['tempElectronics'] = data[11]
    measValues['systemPressure'] = data[12]
    measValues['filterPressure'] = data[13]
    measValues['fanRPM'] = data[14]
    measValues['coronaStability'] = data[15]
    measValues['coronaStabilityMax'] = data[16]
    measValues['ambientHumidity'] = data[17]
    measValues['errorMaster'] = 0.0
    measValues['errorPressure'] = 0.0
    measValues['errorTempAmbient'] = 0.0
    measValues['errorTempSensorHeater'] = 0.0
    measValues['errorTempInletHeater'] = 0.0
    measValues['errorTempProcess'] = 0.0
    measValues['errorFanRPM'] = 0.0
    measValues['errorSensorOffset'] = 0.0
    measValues['errorSensorCorona'] = 0.0
    measValues['errorSensorTrap'] = 0.0
    measValues['errorElectronicsTemp'] = 0.0
    measValues['errorSensorImpedance'] = 0.0
    
    return measValues

def makeJsonFile(amount, deviceID, location):
    # ISO 8601 timestamp eg. '2015-01-28T16:24:48Z' 

    amount = int(amount)
    unixTimestamp = time.time()
    

    with open("measData") as f:
        data = map(float, f)

    for i in xrange(amount):
        unixTimestamp += i * 60
        ISOTimestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(unixTimestamp))
        data = newValues(data)    
        measValuesDict = makeMeasurementValues(data)
        deviceDict = dict([('deviceID', deviceID), ('firmwareVersion', '0.01b'),
            ('locationCoordinates', '60.2194,24.8139'), ('locationTxt', location),
            ('measurementValues', measValuesDict)])
        devTimeDict = dict([('timestamp', ISOTimestamp), ('device', deviceDict)]) 
        wholeThingDict = dict([('nettaData', devTimeDict)])

        filename = "netta_data-" + deviceID + "-" + str(int(unixTimestamp)) + ".json"
        f = open(filename, 'w+')

        json.dump(wholeThingDict, f, indent=4, separators=(',', ': '), sort_keys=True)
        f.close()

def main(argv):
    # get amount, deviceID, location from command line arguments
    if len(argv) == 0:
        print("Making one json file using default parameters")
        makeJsonFile(1, "0114", "Leppavaara")
    elif len(argv) == 3:
        print("Making " + argv[0] + " data json files")
        makeJsonFile(argv[0], argv[1], argv[2])
    else:
        print("Invalid arguments:\n")
        print("Correct usage: python json_maker.py [amount] [deviceID] [location]")

if __name__ == "__main__":
    main(sys.argv[1:])    