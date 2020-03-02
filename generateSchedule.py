# -*- coding: utf-8 -*-
import sys, getopt
import argparse

from skyfield import api
from skyfield.api import EarthSatellite
from skyfield.api import Topos, load

MAXDISTANCE = 1000000000.0

def findVisibility(satellite, site, times, passes, trajectory):

    satellitePasses = []
    aboveHorizon = False
    ts = load.timescale()
    riseTime = 0.
    setTime = 0.
    maxEl = 0.
    maxDistance = 0.
    minDistance = MAXDISTANCE

    difference = satellite - site
    topocentric = difference.at(times)
    geocentric = satellite.at(times)

    el, az, distance = topocentric.altaz()

    for i in range(len(el.degrees[:])):
        if el.degrees[i] > 0.0:
            if(trajectory):
                print("Visible: ", f"{satellite.model.satnum:6d}", times[i].utc_iso(), \
                    f"{distance.km[i]:10.3f}", f"{az.degrees[i]:7.2f}", f"{el.degrees[i]:7.2f}", \
                    times[i], geocentric.position.km[:,i])
            if el.degrees[i] > maxEl:
                maxEl = el.degrees[i]
                maxEl_az = az.degrees[i]
                maxEl_range = distance.km[i]
            if aboveHorizon == False:
                # Satellite just rose above horizon
                riseTime = times[i]
                riseAz = az.degrees[i]
            aboveHorizon = True
            if distance.km[i] < minDistance:
                minDistance = distance.km[i]
            if distance.km[i] > maxDistance:
                maxDistance = distance.km[i]
        else:
            if aboveHorizon == True:
                # Satellite just set
                setTime = times[i]
                setAz = az.degrees[i]
                if riseAz > 90 and riseAz < 270 and (setAz < 90 or setAz > 270):
                    direction = 'NB'
                elif setAz > 90 and setAz < 270 and (riseAz < 90 or riseAz > 270):
                    direction = 'SB'
                else:
                    direction = 'NA'
                satellitePasses.append((satellite.model.satnum, \
                                        riseTime, (setTime-riseTime), \
                                        direction, \
                                        int(maxEl+0.5), int(maxEl_az+0.5),\
                                        int(maxEl_range), int(riseAz+0.5), \
                                        int(setAz+0.5), int(minDistance), \
                                        int(maxDistance)))

                if(passes):
                    print("Pass:    ", f"{satellite.model.satnum:6d}", riseTime.utc_iso(), \
                        f"{1440*(setTime-riseTime):7.2f}", \
                        direction, \
                        int(maxEl+0.5), int(maxEl_az+0.5),\
                        int(maxEl_range), int(riseAz+0.5), \
                        int(setAz+0.5), int(minDistance), \
                        int(maxDistance))

                riseTime = 0.
                setTime = 0.
                maxEl = 0.
                aboveHorizon = False
                maxDistance = 0.
                minDistance = MAXDISTANCE
    return satellitePasses

def computeSchedule(catalog,groundStation, times, passes, trajectory):
    passes = []
    for i in range(len(catalog)):
        passes.append(findVisibility(catalog[i],groundStation, times, passes, trajectory))
    return passes

def readTLE(tleFilename):
    # Open TLE filename
    tleFile = open(tleFilename,'r')
    print("Opened TLE file: ",tleFilename)
    # Read TLEs into catalog
    catalog = []

    line0 = None
    line1 = None
    line2 = None

    for line in tleFile:
        if line[0] == '0':
            line0 = line
        elif line[0] == '1':
            line1 = line
        elif line[0] == '2':
            line2 = line
        else:
            # Error - TLE lines start with 0, 1 or 2
            print("Error: line does not start with 0, 1 or 2: ",line)

        if line1 and line2:
            # Check if object number is same in both line 1 and 2
            if line1[1:6] == line2[1:6]:
                catalog.append(EarthSatellite(line1,line2))
                line1 = None;
                line2 = None;
            else:
                print("Error: Satnumber in line 1 not equal to line 2",line1,line2)
    print("Read ", len(catalog), "TLEs into catalog")
    return catalog

def main(argv):

    # Defaults
    inputFile = 'catalogTest.txt'
    outputFile = 'scheduleTest.txt'
    start = '01012020'
    duration = 1        # one day
    observerLatitude = 0.0
    observerLongitude = 0.0
    passes = True
    trajectory = False

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('generateSchedule.py -i <inputFile> -o <outputFile>', \
            ' -start <data> -duration <days>', \
            ' -obslat <observerLatitude> -obslon <observerLongitude>',\
            ' -passes -trajectory')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('generateSchedule.py -i <inputFile> -o <outputFile>', \
                ' -start <mmddyyyy> -duration <hours>', \
                ' -obslat <observerLatitude> -obslon <observerLongitude>',\
                ' -passes -trajectory')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFile = arg
        elif opt in ("-o", "--ofile"):
            outputFile = arg
        elif opt in ['-start']:
            start = arg
        elif opt in ['-duration']:
            duration = arg
        elif opt in ['-obslat']:
            observerLatitude = arg
        elif opt in ['-obslon']:
            observerLongitude = arg
        elif opt in ['-passes']:
            passes = True
        elif opt in ['-trajectory']:
            trajectory = True

    groundStation = Topos(observerLatitude, observerLongitude)

    ts = load.timescale()
    times = ts.utc(int(start[4:8]), int(start[0:2]), int(start[2:4]), 0, range(0,1440*duration))

    catalog = readTLE(inputFile)
    schedule = computeSchedule(catalog, groundStation, times, passes, trajectory)

    print("Schedule length:",len(schedule))

if __name__ == "__main__":
   main(sys.argv[1:])
