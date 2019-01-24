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
    r'"acquisitionIntervals"'
]

VERBOSE = False
URL_READER_1 = "https://tomcatsec.testingmachine.eu/reader"
URL_READER_2 = "http://127.0.0.1:8081/reader"
REPEATS = 1

def main():

    resp = requests.get(URL_READER_2 + "/stations")
    stationTypes = json.loads(resp.text)

    stations = {}
    for stationType in stationTypes:
        resp = requests.get(URL_READER_2 + "/stations",
                            params={'stationType': stationType})
        stations[stationType] = json.loads(resp.text)

#    urls = []
#    params = []
#    for s in stations:
#        if len(stations[s]) == 0:
#            continue
#        urls.append("/station-details")
#        params.append({'stationType': s, 'stationId': stations[s][0]})
#        if len(stations[s]) > 1:
#            urls.append("/station-details")
#            params.append({'stationType': s, 'stationId': stations[s][-1]})
#            
#    output(urls, params)

    urls = []
    params = []
    for s in stations:
        if not stations[s]:  #list empty
            continue
        urls.append("/types")
        params.append({'stationType': s, 'stationId': stations[s][0]})
        if len(stations[s]) > 1:
            urls.append("/types")
            params.append({'stationType': s, 'stationId': stations[s][-1]})
            

#    urls = [
#        "/stations",
#        "/stations?stationType=EChargingStation"
#        ]

#    urls = ["/station-details"]
#    params = [{'stationType': 'EChargingStation', 'stationId': 'DW-000027'}]

    urls = ["/types"]
    params = [{'stationType': 'TrafficSensor'}]

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
