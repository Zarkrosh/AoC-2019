import sys

# Returns Manhattan distance between 2 points (P and Q)
def manhattanDistance((pX, pY), (qX, qY)):
	return (abs(pX - qX) + abs(pY - qY))

# Reads challenge input
with open("input3", "r") as file:
	sCables = file.readlines()

# { (COORDINATES): (<CABLE'S ID>, <1st cable steps>), ... }
mapped = {
	(0, 0): (-1, -1)
}

# [ (COORDINATES, <stepSum>), ... ]
intersections = []

# TESTS
# Output 1st part: 6   | Output 2nd part: 30
#sCables = ["R8,U5,L5,D3", "U7,R6,D4,L4"]
# Output 1st part: 159 | Output 2nd part: 610 
#sCables = ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]
# Output 1st part: 135 | Output 2nd part: 410
#sCables = ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]

idCable = 0
for s in sCables:
	mapX, mapY = (0, 0)

	segments = s.split(",")
	totalLength = 1
	for segment in segments:
		direction = segment[0]
		length = int(segment[1:])
		if direction == "U":
			# Up
			difX, difY = (0, -1)
		elif direction == "R":
			# Right
			difX, difY = (1, 0)
		elif direction == "D":
			# Down
			difX, difY = (0, 1)
		elif direction == "L":
			# Left
			difX, difY = (-1, 0)
		else:
			print "[!] Unknown direction:", direction
			exit()

		# Generates the cable checking for intersections
		for i in range(length):
			# Updates map pointers
			mapX += difX
			mapY += difY
			point = (mapX, mapY)

			if point in mapped:
				# Already mapped
				if mapped[point][0] != idCable:
					# Crosses with another cable
					stepSum = mapped[point][1]
					intersections.append((point, stepSum + totalLength))
			else:
				# First mapping
				mapped[point] = (idCable, totalLength)

			totalLength += 1

	idCable += 1

# 1st solution: gets the closest intersection (Manhattan distance)
minDistance = sys.maxsize
for inter in intersections:
	currDist = manhattanDistance((0,0), inter[0])
	if currDist < minDistance:
		minDistance = currDist

# 2nd solution: gets the intersection with the lowest step sum
minSteps = sys.maxsize
for inter in intersections:
	stepSum = inter[1]
	if stepSum < minSteps:
		minSteps = stepSum

print "[*] Solution 1:", minDistance
print "[*] Solution 2:", minSteps
