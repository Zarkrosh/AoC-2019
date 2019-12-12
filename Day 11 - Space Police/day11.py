from intcodecomp import IntCodeComputer

UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)
TURNS = [LEFT, UP, RIGHT, DOWN]

def getFacing(facing, turn):
	i = TURNS.index(facing) + (-1 if turn == 0 else 1)
	if i < 0: i = len(TURNS) - 1
	elif i >= len(TURNS): i = 0
	return TURNS[i]

def startPaintingRobot(panels):
	[x, y] = 0, 0
	facing = UP
	robot = IntCodeComputer(program)
	robot.muteOutput(True)
	while not robot.hasFinished():
		currentColor = 0 if (x,y) not in panels else panels[(x,y)]
		robot.addInputs([currentColor])
		robot.executeProgramAndPauseOnOutput(2) # Pauses every 2 outputs
		outputs = robot.getOutputs()
		if len(outputs) > 0:
			# Paints panel
			panels[(x,y)] = outputs[0]
			# Moves
			facing = getFacing(facing, outputs[1])
			x += facing[0]
			y += facing[1]

# Reads challenge input
with open("input11", "r") as file:
	program = map(int, file.read().split(","))

# Part 1
panels = {} # Map of panels (coords) -> color
startPaintingRobot(panels)
print "[*] Solution 1:", len(panels)

# Part 2: starts on white panel
panels = {(0,0): 1}
startPaintingRobot(panels)
# Graphical output
print "[*] Solution 2:"
minX = min(panels.keys(), key=lambda k: k[0])[0]
maxX = max(panels.keys(), key=lambda k: k[0])[0]
minY = min(panels.keys(), key=lambda k: k[1])[1]
maxY = max(panels.keys(), key=lambda k: k[1])[1]
for i in range(minY, maxY+1):
	p = ""
	for j in range(minX, maxX+1):
		p += " " if (j,i) not in panels else (" " if panels[(j,i)] == 0 else "#")
	print p
