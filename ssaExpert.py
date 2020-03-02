import json
import time
import random

nSensors = 10
sensorMissedPassCount = [0]*(nSensors+1)
nObjects = 300
objectMissedPassCount = [0]*(nObjects+1)
runningMissedPassCount = 0
minSize = -60   # dBsm: 1 square millimeter
maxSize = 60    # dBsm: 1 million square meters

# Expert system approach to monitoring SSA events and
# generating recommendations to the SSA operator to be used
# for creating training data for machine learning algorithm

# Message types
# 1. Observation
#   - correlates with known object
#   - does not correlate with known object
#
# 2. Missed pass
#   - one missed pass is not a trend, but...
#   - if multiple missed passes for a specific object
#       then initiate lost object procedure
#   - if multiple missed passes from a specific sensor
#       then request a sensor status check
#

# Initialize
def initialize():
    # Any initialization...
    pass


def uctImportance(size, orbit):
    # Size is an estimated area in dB square meters
    # Orbit is a dictionary of where period, inclination and eccentricity
    #   are the key values
    # Importance is a logrithmic value where 0 is "normal priority"
    importance = 20 + size
    # Compute period in revs per day
    #   - if the UCT is in the crowded zone raise the importance 10 dB
    if(period > 13.5 and period < 15.5):
        importance += 10
    if ( period > 0.9 and period < 1.1):
        importance += 10
    return importance

def rsoImportance(rsoIdentifier):
    # General level of importance for known objects
    #   1. occupied spacecraft
    #   2. allied operational spacecraft
    #   3. non-allied operational spacecraft
    #   4. large debris
    #   5. small debris
    return random.randint(1,5) # Just return a random for now

# Read message
def readMessage(msgDict):
    runningMissedPassCount = 0 # ?
    recommendations = []
    if msgDict['type'] == 'missedPass':
        sensorID = int(msgDict['sensorID'])
        objectID = int(msgDict['objectID'])
        sensorMissedPassCount[sensorID] += 1
        if sensorMissedPassCount[sensorID] > 1:
            # Sensor has missed 3 observations in a row
            recommendations.append({'Request sensor status from:',\
                msgDict['sensorID']})
        if runningMissedPassCount > 1:
            recommendations.append('Request network status update')
        if objectMissedPassCount[objectID] >1:
            # There have been at least 3 missed passes on this object
            objectMissedPassCount[objectID] += 1
            recommendations.append({'Request lost object search for: ',\
                msgDict['objectID']})
    if msgDict['type'] == 'observation':
        runningMissedPassCount = 0
        sensorID = int(msgDict['sensorID'])
        objectID = int(msgDict['objectID'])
        sensorMissedPassCount[sensorID] = 0
        objectMissedPassCount[objectID] = 0
        if msgDict['objectType'] == 'known':
            recommendations.append({'Request catalog update for object:',\
                msgDict['objectID']})
        elif msgDict['objectType'] == 'unknown':
            # New/unknown object detected
            # Search for possible sources
            objectSize = int(msgDict['objectSize'])
            if objectSize > -30:
                recommendations.append({'Request source analysis for object:',\
                    msgDict['objectID']})
                # Evaluate potential collision risk
                recommendations.append({'Request collision risk assessment for object:',\
                    msgDict['objectID']})
                if objectSize > 0:
                    recommendations.append({'Request notification for significant uncataloged object:',\
                        msgDict['objectID']})
    return recommendations

def validateRecommendations(recommendations):
    print('Validation recommendations: ',len(recommendations))
    for recommendation in recommendations:
        print('Recommendation: ',recommendation)
        pass

# Test logic
def demoSsaExpert():

    initialize()
    print('Initialized')

    # There are two primary types of sensor messages
    #   1. Observations
    #   2. Missed satellitePasses
    # Observations are used to keep the catalog of known objects
    #   up to date
    # Missed satellite passes provide a notification that a
    #   sensor did not detect an object when expected.  Missed
    #   passes can be due to a sensor issue or because the
    #   object is not where it was expected
    # Test 1: Missed pass
    #   One pass missed, do nothing unless priority target
    #       then generate tasking readMessage
    sensorID = random.randint(1,nSensors)
    objectID = random.randint(1,nObjects)
    message = {'type':'missedPass', 'time':time.time(), \
        'sensorID':sensorID, 'objectID':objectID, 'priority':'low'}
    recommendations = readMessage(message)
    validateRecommendations(recommendations)
    print('Test 1: Missed Pass',message,recommendations)

    # Test 2: Multiple consecutive missed passes for an object
    #   Generate alert
    #       if new UCT detected in similar orbit, possible maneuver alert
    #       if multiple new UCTs detected in similar orbit, possible breakup alert
    #       other possibilities - dock with other RSO, re-enter atmosphere

    # Test 3: Multiple or all targets missed from a single sensor
    #   Request status update from sensor

    # Test 4: No updates sensors
    #   Request network status updates after timeout period

    # Test 5: UCT detected
    #   Generate tasking to compare orbit against known orbits of known objects to
    #       - estimate importance of UCT (size, orbit)
    #       - evaluate probability of collision
    #       - determine potential origin
    sensorID = random.randint(1,nSensors)
    objectSize = random.randint(minSize,maxSize)
    message = {'type':'observation', 'time':time.time(), \
        'sensorID':sensorID, 'objectType':'unknown',\
        'objectID':str(random.randint(200,299)),\
        'objectSize':objectSize}
    recommendations = readMessage(message)
    validateRecommendations(recommendations)
    print('Test 5: UCT detected ',message,recommendations)

    # Test 6: Normal pass
    #   Generate tasking to evaluate data quality and update catalog
    sensorID = random.randint(1,nSensors)
    objectSize = random.randint(minSize,maxSize)
    message = {'type':'observation', 'time':time.time(), \
        'sensorID':sensorID, 'objectType':'known',\
        'objectID':str(random.randint(100,199)),\
        'objectSize':objectSize}
    recommendations = readMessage(message)
    validateRecommendations(recommendations)
    print('Test 6: Normal pass',message,recommendations)

    # Test 7: Launch notification
    #   Generate sensor tasking to support Launch
    message = {'type':'launchNotification', 'time':time.time(), \
        'launchTime':(time.time()-random.randint(1,10)),\
        'launchPoint':[random.randint(0,90),random.randint(-180,180)],\
        'objectType':'unknown',\
        'objectID':str(random.randint(100,199)),\
        'objectSize':objectSize}
    recommendations = readMessage(message)
    validateRecommendations(recommendations)
    print('Test 7: Launch notification',message,recommendations)

if __name__== "__main__":
  demoSsaExpert()
