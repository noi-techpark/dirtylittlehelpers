#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Ignoring warnings about "Used * or ** magic (star-args)"

# Author: Peter Moser <p.moser@noi.bz.it>)

import echo
import requests
import json
import unit


IGNORE_ACTIVE = True
IGNORE = [
    r'"_t": ".*it\.bz\.idm\.bdp\.dto.*"',
    r'"origin": ".*"',
    r'"coordinateReferenceSystem": ".*"',
    r'"crs": ".*"',
    r'"parentStation": ".*"',
    r'"linegeometry": ".*"',
    r'"aquisitionIntervalls"',
    r'"acquisitionIntervals"',
    r'"desc"',
    r'"en": ".*"',
    r'"default". ".*"',
    r'"unit": null',
    r'"unit": ""',
    r'}',
    r'{'
]

VERBOSE = True
URL_READER_1 = "http://52.214.47.112:8080/reader"
URL_READER_2 = "http://127.0.0.1:8081/reader"
REPEATS = 1
MAX_STATIONS = 1

def main():

    resp = requests.get(URL_READER_2 + "/stations")
    if resp.status_code != 200:
        echo.outred("ERROR: Cannot get station names\n")
        echo.outred("ERROR: Code = " + str(resp.status_code) + "\n")
        echo.outred("ERROR: Msg  = " + resp.text + "\n")
        
        return
    
    stationTypes = json.loads(resp.text)

    stations = {}
    for stationType in stationTypes:
        resp = requests.get(URL_READER_2 + "/stations",
                            params={'stationType': stationType})
        stations[stationType] = json.loads(resp.text)

    urls = []
    params = []
    stations2ignore = ['TrafficStreetFactor']
    for stype in stations:
        if len(stations[stype]) == 0:
            continue
        if stype in stations2ignore:
            print("IGNORED /station-details for " + stype)
            continue
        
        urls.append("/station-details")
        params.append({'stationType': stype})        
        
        for i, station in enumerate(stations[stype]):
            if MAX_STATIONS > 0 and i >= MAX_STATIONS:
                break
            urls.append("/station-details")
            params.append({'stationType': stype, 'stationId': station})
            
    output(urls, params)
    return
        
    urls = []
    params = []
    stations2ignore = ['TrafficStreetFactor']
    for stype in stations:
        if len(stations[stype]) == 0:
            continue
        if stype in stations2ignore:
            print("IGNORED /stations for " + stype)
            continue

        urls.append("/stations")
        params.append({'stationType': stype})
        
        for i, station in enumerate(stations[stype]):
            if MAX_STATIONS > 0 and i >= MAX_STATIONS:
                break
            urls.append("/stations")
            params.append({'stationType': stype, 'stationId': station})
            
    output(urls, params)
    return        

#    urls = []
#    params = []
#    stations2ignore = ['TrafficStreetFactor', 'Mobilestation', 'ParkingStation']
#    for stype in stations:
#        if not stations[stype]:  #list empty
#            continue
#        if stype in stations2ignore:
#            print("IGNORED /station-details for " + stype)
#            continue
#        
#        for i, station in enumerate(stations[stype]):
#            if MAX_STATIONS > 0 and i >= MAX_STATIONS:
#                break
#            urls.append("/types")
#            params.append({'stationType': stype, 'stationId': station})
#
#    urls = ["/types"]
#    params = [{'stationType': 'Linkstation'}]
#            
#    output(urls, params)
#    return

#    urls = [
#        "/stations",
#        "/stations?stationType=EChargingStation"
#        ]

#    urls = ["/station-details"]
#    params = [{'stationType': 'EChargingStation', 'stationId': 'DW-000027'}]


    urls = []
    params = []
    stations2ignore = ['TrafficStreetFactor', 'TrafficSensor', 'Mobilestation']
    for stype in stations:
        if not stations[stype]:  #list empty
            continue
        if stype in stations2ignore:
            print("IGNORED /station-details for " + stype)
            continue
        
        for i, station in enumerate(stations[stype]):
            if MAX_STATIONS > 0 and i >= MAX_STATIONS:
                break
            urls.append("/data-types")
            params.append({'stationType': stype, 'stationId': station})

#    urls = ["/data-types"]
#    params = [{'stationType': 'Bluetoothstation', 'stationId': 'meinstein'}]
        
    output(urls, params)
    return        
        
#    urls = ["/stations"]
#    params = [{'stationType': 'BikesharingStation'}]        
        
#    urls = []
#    params = []        
#    for s in stations:
#        if not stations[s]:
#            continue
#        urls.append("/last-record")
#        params.append({'stationType': s, 'stationId': stations[s][0]})

#    urls = []
#    params = []        
#    for s in stations:
#        if not stations[s]:
#            continue
#        resp = requests.get(URL_READER_2 + "/types", params={'stationType': s, 'stationId': stations[s][0]})
#        if resp.status_code != 200:
#            continue
#        resp = json.loads(resp.text)
#        if not resp:
#            continue
#        datatype = resp[0]['id']
#        
#        urls.append("/records")
#        params.append({'stationType': s, 
#                       'stationId': stations[s][0], 
#                       'typeId': datatype, 
#                       'start': 1450000000000, 
#                       'end':   1500000000000})

    output(urls, params)



def output(urls, params):
    for url in zip(urls, params):
        
        try:
            result = unit.test(URL_READER_1, URL_READER_2, url, REPEATS, IGNORE, IGNORE_ACTIVE)
        except Exception as e:
            echo.outred("ERROR  ")
            echo.outred(url)
            print()
            raise e
            
        if result['status']:
            echo.outgreen("SUCCESS")
        else:
            echo.outred("FAILED ")
            
        echo.out(" {} {}\n".format(result['path'], result['params']))
        
        if VERBOSE:
            print(result['diff']['A'])
            print("------------------------------")
            print(result['diff']['B'])

        
        if not result['status']:
            echo.outdiff(result['diff']['output'])


if __name__ == '__main__':
    main()
