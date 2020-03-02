import argparse

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

def plotTLE(catalog, tlePlotFilename):
    xdata = [0.]*len(catalog)
    ydata = [0.]*len(catalog)
    zdata = [0.]*len(catalog)
    print('length catalog',len(catalog))
    i = 0
    for satellite in catalog:
        xdata[i] = satellite.model.inclo
        ydata[i] = satellite.model.ecco
        zdata[i] = satellite.model.no
        print(i,xdata[i],ydata[i],zdata[i])
        i = i+1

    #TODO: add histogram plots of inclination, eccentricty and mean motion
    #TODO: add 2d plots of inclination vs mean motion, inclination vs eccentricity
    fig = plt.figure()
    fig.suptitle('Catalog 3D Plot')
    ax = plt.axes(projection='3d')
    ax.set_xlabel('Inclination')
    ax.set_ylabel('Eccentricity')
    ax.set_zlabel('Mean Motion')
    ax.scatter3D(xdata, ydata, zdata, c=zdata);
    plt.show()

parser = argparse.ArgumentParser(description='Read TLE files')
parser.add_argument("--tleFilename")
args = parser.parse_args()

tleDefaultFilename = 'catalogTest'
if args.tleFilename:
    tleFilename = args.tleFilename + '.txt'
    tlePlotFilename = args.tleFilename + '.plt'
else:
    tleFilename = tleDefaultFilename + '.txt'
    tlePlotFilename = tleDefaultFilename + '.plt'

catalog = readTLE(tleFilename)
plotTLE(catalog, tlePlotFilename)
