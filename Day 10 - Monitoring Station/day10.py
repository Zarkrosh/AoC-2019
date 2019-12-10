import math
# For graphical part
import sys
import platform
import os
import time

PLATFORM = platform.system()

ASTEROID = "#"
VOID = "."

def calculateAngles((x, y)):
	result = {}
	for coord in viewsMap[station]:
		result[coord] = angle2Points(station, coord)
	return result

def angle2Points((x1,y1), (x2,y2)):
	res = (math.atan2(y2-y1, x2-x1) * 180 / math.pi) + 90
	if res < 0: res = 360 + res
	return res

def mcd(a, b):
	if b == 0:
		return a
	else:
		return mcd(b, a % b)

def getCoordinatesBetweenPoints((x1, y1), (x2, y2)):
	result = []

	vector = [x2 - x1, y2 - y1]
	div = abs(mcd(vector[0], vector[1]))
	vector[0] /= div
	vector[1] /= div
	point = [x1 + vector[0], y1 + vector[1]]
	while point != [x2, y2]:
		result.append((point[0], point[1]))
		# Next point
		point[0] += vector[0]
		point[1] += vector[1]

	return result

def updateViews(point, views, asteroids):
	for y in range(len(asteroids)):
		for x in range(len(asteroids[0])):
			if (x,y) != point and asteroids[y][x] == ASTEROID:
				# Get list of coordinates between the points
				coords = getCoordinatesBetweenPoints((x,y), point)
				# Checks if any has an asteroid
				if ASTEROID in "".join(asteroids[cy][cx] for (cx, cy) in coords):
					continue
				# Direct line of sight
				if point not in views: views[point] = [(x,y)] 
				else: views[point].append((x,y)) 

def calculateViewsMap(asteroids):
	viewsMap = {}
	for y in range(len(asteroids)):
		for x in range(len(asteroids[0])):
			if asteroids[y][x] == ASTEROID:
				# Calculates which other asteroids can see it
				updateViews((x,y), viewsMap, asteroids)
	return viewsMap

def printAsteroidMap(asteroids, station, solution, destroyed, angle):
	outputs = [list(row) for row in asteroids]
	outputs[station[1]][station[0]] = '\033[96m' + '@' + '\033[0m'
	if destroyed != None:
		outputs[destroyed[1]][destroyed[0]] = '\033[91m' + 'X' + '\033[0m'
	if solution != None:
		outputs[solution[1]][solution[0]] = '\033[92m' + 'O' + '\033[0m'
	print "".join("".join(row) + "\n" for row in outputs) 
	print "Angle:", angle
	
# Reads challenge input
with open("input10", "r") as file:
	asteroids = [line.rstrip() for line in file.readlines()]

# Calculates view map
viewsMap = calculateViewsMap(asteroids)
station = max(viewsMap, key=lambda k: len(viewsMap[k]))
print "[*] Solution 1:", station, "->", len(viewsMap[station]), "asteroids"

# Part 2
NTH_ASTEROID = 200

graphicMode = False
if len(sys.argv) > 1:
	SLEEP = float(sys.argv[1]) / 1000
	graphicMode = True
	if PLATFORM == "Windows": clear = lambda: os.system('cls') 
	elif PLATFORM == "Linux": clear = lambda: os.system('clear')
	else: clear = lambda: None
	# Prints initial map
	raw_input("\nPress to start graphical solution")

angles = calculateAngles(station)
destroyed = []
while len(angles) > 0:
	# Finds next asteroid to destroy
	toDestroy = min(angles, key=angles.get)
	destroyed.append(toDestroy)
	# Updates asteroid map
	asteroids[toDestroy[1]] = asteroids[toDestroy[1]][:toDestroy[0]] + VOID + asteroids[toDestroy[1]][toDestroy[0]+1:]
	if graphicMode:
		clear()
		solution = None if len(destroyed) < NTH_ASTEROID else destroyed[NTH_ASTEROID-1]
		printAsteroidMap(asteroids, station, solution, toDestroy, angles[toDestroy])
		time.sleep(SLEEP)
	# Deletes angle of destroyed asteroid 
	del angles[toDestroy]
	if len(angles) == 0:
		# Lap completed, recalculates views of remaining asteroids
		viewsMap = calculateViewsMap(asteroids)
		if len(viewsMap) > 0:
			angles = calculateAngles(station)


solution2 = destroyed[NTH_ASTEROID-1][0] * 100 + destroyed[NTH_ASTEROID-1][1] 
print "[*] Solution 2:", solution2
