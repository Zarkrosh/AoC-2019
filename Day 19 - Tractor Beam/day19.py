from intcodecomp import IntCodeComputer

def angle2Points((x1,y1), (x2,y2)):
	return (math.atan2(y2-y1, x2-x1) * 180 / math.pi) 

def printMap(mapped):
	minX = min(mapped.keys(), key=lambda k: k[0])[0]
	maxX = max(mapped.keys(), key=lambda k: k[0])[0]
	minY = min(mapped.keys(), key=lambda k: k[1])[1]
	maxY = max(mapped.keys(), key=lambda k: k[1])[1]
	for i in range(minY, maxY+1):
		p = ""
		for j in range(minX, maxX+1):
			if (j,i) in mapped:
				if mapped[(j,i)] == 1:
					p += "#"
				else:
					p += "."
			else:
				p += "."
		print p

# Reads challenge input
with open("input19", "r") as file:
	program = map(int, file.read().split(","))

# First part
mapped = {}
for y in range(50):
	for x in range(50):
		drone = IntCodeComputer(program)
		drone.muteOutput(True)
		drone.addInputs([x, y])
		drone.executeProgram()
		out = drone.getOutputs()[0]
		if out == 1: mapped[(x,y)] = 1

print "[*] Solution 1:", sum(c for c in mapped.values()) 

printMap(mapped)
# Second part
# Calculate the angles of the beam
maxX = max(mapped.keys(), key=lambda k: k[0])[0]
maxY = max(mapped.keys(), key=lambda k: k[1])[1]
minYmaxX = min(filter(lambda k: k[0][0] == maxX, mapped.items()), key=lambda k2: k2[0][1])[0][1]

upper = angle2Points((0,0), (maxX, minYmaxX))
lower = angle2Points((0,0), (maxX, maxY))


print maxX, maxY, minYmaxX