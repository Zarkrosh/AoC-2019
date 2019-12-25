from intcodecomp import IntCodeComputer
import copy
import sys

SCAFFOLD = "#"
VOID = "."

UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]
CURR_DIR = UP

def getNextPositions(currX, currY, mapp, inters, currPath):
	possibles = []
	for d in DIRECTIONS:
		nX = currX + d[0]
		nY = currY + d[1]
		if nX >= 0 and nX < len(mapp[0]):
			if nY >= 0 and nY < len(mapp):
				if (nX,nY) not in currPath or ((nX,nY) in inters and currPath[-1] != (nX,nY) and currPath[-2] != (nX,nY)):
					if mapp[nY][nX] == SCAFFOLD:
						possibles.append((nX,nY))
	#print "Getting next for", (currX, currY), possibles
	return possibles

def getAllPaths(initX, initY, mapping, intersections, currentPath):
	paths = []
	currentX = initX
	currentY = initY

	currentPath.append((initX, initY))

	exit = False
	while not exit:
		nextP = getNextPositions(currentX, currentY, mapping, intersections, currentPath)
		if len(nextP) > 1:
			# Path splitting
			for n in nextP:
				for path in getAllPaths(n[0], n[1], mapping, intersections, copy.deepcopy(currentPath)):
					paths.append(path)
		elif len(nextP) == 1:
			# Keep going
			#print "Keep going", nextP[0]
			currentPath.append(nextP[0])
			currentX = nextP[0][0]
			currentY = nextP[0][1]
		else:
			# The end
			#print "#####"
			exit = True
	return paths

sys.setrecursionlimit(10000)

# Reads challenge input
with open("input17", "r") as file:
	program = map(int, file.read().split(","))
program2 = copy.deepcopy(program)

control = IntCodeComputer(program)
control.muteOutput(True)
control.executeProgram()
output = "".join(chr(c) for c in control.getOutputs()).split()
print "".join(c + "\n" for c in output)

intersections = []
for i in range(len(output)):
	for j in range(len(output[0])):
		if i > 0 and j > 0 and i < len(output)-1 and j < len(output[0])-1:
			if output[i][j] == SCAFFOLD and output[i-1][j] == SCAFFOLD and output[i+1][j] == SCAFFOLD and output[i][j-1] == SCAFFOLD and output[i][j+1] == SCAFFOLD:
				intersections.append((j,i))

# Part 1
print "[*] Solution 1:", sum(x * y for (x,y) in intersections)

# Part 2
posX = posY = 0
# Finds initial position of the robot
for i in range(len(output)):
	if "^" in output[i]: 
		posX = output[i].index("^")
		posY = i
		break

print "[*] Initial position:", (posX,posY)

paths = getAllPaths(posX, posY, output, intersections, [])
print paths

program2[0] = 2
control = IntCodeComputer(program)

solution2 = None
print "[*] Solution 2:", solution2