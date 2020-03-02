import argparse
import csv

from skyfield import api
from skyfield.api import EarthSatellite
from skyfield.constants import AU_KM, AU_M
from skyfield.sgp4lib import TEME_to_ITRF
from skyfield.api import Topos, load


# Read TLE file and write key parameters in CSV format
def readTLE(tleFilename):
    # Open TLE filename
    tleFile = open(tleFilename,'r')
    # print("Opened TLE file: ",tleFilename)
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
            catalog.append(EarthSatellite(line1,line2))
            line1 = None;
            line2 = None;
    # print("Read ", len(catalog), "TLEs into catalog")
    return catalog

def writeSatelliteCSV(catalog, tleDefaultCSVFilename):
    with open(tleDefaultCSVFilename, 'w', newline='') as csvfile:

        fieldnames = ['satnum', 'epochyr', 'epochdays', 'jdsatepoch', 'ndot', \
            'nddot', 'bstar', 'inclination', 'rightascension', 'eccentricity', \
            'argofperigee', 'meanmotion', 'meananomaly']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for satellite in catalog:
            writer.writerow({\
                'satnum':satellite.model.satnum, \
                'epochyr':satellite.model.epochyr, \
                'epochdays':satellite.model.epochdays, \
                'jdsatepoch':satellite.model.jdsatepoch, \
                'ndot':satellite.model.ndot, \
                'nddot':satellite.model.nddot, \
                'bstar':satellite.model.bstar, \
                'inclination':satellite.model.inclo, \
                'rightascension':satellite.model.nodeo, \
                'eccentricity':satellite.model.ecco, \
                'argofperigee':satellite.model.argpo, \
                'meananomaly':satellite.model.mo, \
                'meanmotion':satellite.model.no})

parser = argparse.ArgumentParser(description='Read TLE files')
parser.add_argument("--tleFilename")
args = parser.parse_args()


tleDefaultFilename = 'catalogTest.txt'
tleDefaultCSVFilename = 'catalogTest.csv'
if args.tleFilename:
    tleFilename = args.tleFilename
else:
    tleFilename = tleDefaultFilename

catalog = readTLE(tleFilename)
writeSatelliteCSV(catalog,tleDefaultCSVFilename)
