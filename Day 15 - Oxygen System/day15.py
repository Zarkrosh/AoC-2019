from intcodecomp import IntCodeComputer

NORTH = (0, -1) 
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)
MOVEMENTS = [NORTH,EAST,SOUTH,WEST]
OUTPUTS = {NORTH: 1, SOUTH: 2, WEST: 3, EAST: 4}

# Map
WALL = 0
EMPTY = 1
OXYGEN = 2
mapped = {(0,0): EMPTY}

# Robot
posX = 0
posY = 0
currLen = 0 # Length of the current route from (0,0)
history = [(posX,posY)] # History of movements
lastLook = None # NORTH, EAST, SOUTH, WEST
backtracking = False

# Oxygen system location
solution1 = None
oxX = oxY = None

def getRemainingMoves(x,y):
	global mapped
	rem = []
	for m in MOVEMENTS:
		dX = m[0] + 0
		dY = m[1] + 0
		if (x + dX, y + dY) not in mapped:
			rem.append(((x + dX, y + dY), OUTPUTS[m]))
	return rem

def nextMove():
	global posX, posY, lastLook, history, currLen, backtracking
	backtracking = False
	remainingMoves = getRemainingMoves(posX, posY)
	#print "Remaining:", remainingMoves
	if len(remainingMoves) > 0:
		# Next move on current position
		lastLook = remainingMoves[0][0] + () # Deep copy
		#print "Looking at", lastLook
		return remainingMoves[0][1] + 0
	else:
		# No more moves -> backtrack
		if len(history) > 0:
			backtracking = True
			preX, preY = history.pop()
			lastLook = (preX, preY)
			return OUTPUTS[(preX-posX, preY-posY)]
		else:
			print "[!] No more backtracks"
			exit()

def checkOutput(output):
	# Shitty globals, I know :(
	global posX, posY, lastLook, mapped, history, currLen, oxX, oxY, solution1
	ret = False
	nX = lastLook[0]
	nY = lastLook[1]
	mapped[(nX,nY)] = output
	if output != WALL:
		if not backtracking:
			history.append((posX, posY))
			currLen += 1
		else:
			currLen -= 1
		posX = nX
		posY = nY
		if output == OXYGEN:
			# Bingo
			oxX = posX
			oxY = posY
			solution1 = currLen

	return ret

def printMap(mapped):
	minX = min(mapped.keys(), key=lambda k: k[0])[0]
	maxX = max(mapped.keys(), key=lambda k: k[0])[0]
	minY = min(mapped.keys(), key=lambda k: k[1])[1]
	maxY = max(mapped.keys(), key=lambda k: k[1])[1]
	for i in range(minY, maxY+1):
		p = ""
		for j in range(minX, maxX+1):
			if (j,i) in mapped:
				if mapped[(j,i)] == WALL: p += "#"
				elif mapped[(j,i)] == EMPTY: p += "."
				else: p += "O"
			else:
				p += " "
		print p

# Reads challenge input
with open("input15", "r") as file:
	program = map(int, file.read().split(","))

control = IntCodeComputer(program)
control.muteOutput(True)
control.setInputFromFunction(nextMove)
found = False
try:
	while not found:
		control.executeProgramAndPauseOnOutput(1)
		found = checkOutput(int(control.getOutputs()[0]))
except KeyError:
	# Map scan completed when backtrack to origin
	pass

print "Map:"
printMap(mapped)
print "[*] Solution 1:", solution1

# Part 2: oxygen filling
def oxygenFill((x, y), mapped, time):
	res = time
	mapped[(x,y)] = OXYGEN
	emptyNeighbours = []
	for m in MOVEMENTS:
		nX = x + m[0]
		nY = y + m[1]
		if (nX,nY) in mapped:
			if mapped[(nX,nY)] == EMPTY:
				emptyNeighbours.append((nX,nY))

	if len(emptyNeighbours) > 0:
		res = max(oxygenFill(neigh, mapped, time+1) for neigh in emptyNeighbours)
	
	return res

print "[*] Solution 2:", oxygenFill((oxX,oxY),mapped, 0)
