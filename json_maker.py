#!/usr/bin/python
# -*- coding: utf-8 -*-

# Takes data from measData file, increments it by some amount,
# writes a JSON file with the timestamp and the data JSON file 
# is named netta_data-[device_id]-[unix-timestamp].json

import json 
import time
import random

DEVICE_ID = "0114"

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

# ISO 8601 timestamp eg. '2015-01-28T16:24:48Z' 

unixTimestamp = time.time()
ISOTimestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(unixTimestamp))


with open("measData") as f:
    data = map(float, f)

data = newValues(data)
measValuesDict = makeMeasurementValues(data)

deviceDict = dict([('deviceID', DEVICE_ID), ('firmwareVersion', '0.01b'),
    ('locationCoordinates', '60.2194,24.8139'), ('locationTxt', 'Leppavaara'),
    ('measurementValues', measValuesDict)])

devTimeDict = dict([('timestamp', ISOTimestamp), ('device', deviceDict)]) 
wholeThingDict = dict([('nettaData', devTimeDict)])

filename = "netta_data-" + DEVICE_ID + "-" + str(int(unixTimestamp)) + ".json"
f = open(filename, 'w+')

json.dump(wholeThingDict, f, indent=4, separators=(',', ': '), sort_keys=True)
f.close()
