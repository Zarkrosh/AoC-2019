import copy

def executeInstruction(memory, ip):
	opcode = memory[ip]
	if opcode == 1:
		# 1 - Add
		num1 = memory[memory[ip+1]]
		num2 = memory[memory[ip+2]]
		memory[memory[ip+3]] = num1 + num2
		return True
	elif opcode == 2:
		# 2 - Multiply
		num1 = memory[memory[ip+1]]
		num2 = memory[memory[ip+2]]
		memory[memory[ip+3]] = num1 * num2
		return True
	elif opcode == 99:
		# 99 - End of program
		return False
	else:
		# Unexpected opcode
		print "[*] Unexpected opcode at ip ", ip, "->", opcode
		return False

def executeProgram(memory):
	ip = 0
	while executeInstruction(memory, ip):
		ip += 4 # Next instruction


# Reads challenge input
with open("input2", "r") as file:
	line = "".join(l.rstrip() for l in file.readlines())

# Set memory
memory = map(int, line.split(","))

# Makes a backup of memory for the 2nd part
backupMemory = copy.deepcopy(memory)

# Explicit replacement for the challenge
memory[1] = 12
memory[2] = 2

########## FIRST PART ########## 
executeProgram(memory)
print "[*] Solution 1:", memory[0]

########## SECOND PART  ##########
toFind = 19690720
found = False
noun = 0
verb = 0
solution = ()
while not found:
	ip = 0
	memory = copy.deepcopy(backupMemory)
	memory[1] = noun
	memory[2] = verb
	executeProgram(memory)
	if toFind == memory[0]:
		solution = (noun, verb)
		found = True

	verb += 1
	if verb >= 99:
		verb = 0
		noun += 1
	if noun >= 99:
		break

if len(solution) > 0:
	print "[*] Solution 2:", (100 * solution[0] + solution[1])
else:
	print "[!] Solution 2: not found"