from intcodecomp import IntCodeComputer

def joystickLogic():
	if paddX < ballX: return 1
	elif paddX > ballX: return -1
	else: return 0
	
# Reads challenge input
with open("input13", "r") as file:
	program = map(int, file.read().split(","))

# Part 1
screen = {}
game = IntCodeComputer(program)
game.muteOutput(True)
while not game.hasFinished():
	game.executeProgramAndPauseOnOutput(3) # Pauses every 3 outputs
	out = game.getOutputs()
	if len(out) == 3: screen[(int(out[0]),int(out[1]))] = int(out[2])

print "[*] Solution 1:", sum(1 if screen[k] == 2 else 0 for k in screen)

# Part 2
screen = {}
program[0] = 2 # 0MG_U_SO_H4X0R
game = IntCodeComputer(program)
game.muteOutput(True)
game.setInputFromFunction(joystickLogic) # Takes input from this function

score = 0
ballX = paddX = -1 # I'm only interested in the X axis positions
joystick = 0
while not game.hasFinished():
	game.executeProgramAndPauseOnOutput(3) # Pauses every 3 outputs
	out = game.getOutputs()
	if len(out) < 3:
		continue
	elif int(out[0]) == -1 and int(out[1]) == 0:
		# New score
		score = out[2]
	else:
		# Tile
		x = int(out[0])
		y = int(out[1])
		tID = int(out[2])
		screen[(x,y)] = tID
		if tID == 3: paddX = x   # Paddle
		elif tID == 4: ballX = x # Ball

print "[*] Solution 2:", score