def executeProgram(memory):
	ip = 0
	exit = False
	while not exit and ip < len(memory):
		# Extracts opcode and parameter modes
		instruction = str(memory[ip]).zfill(5)
		opcode = int(instruction[3:])
		modP1  = int(instruction[2])
		modP2  = int(instruction[1])
		modP3  = int(instruction[0])

		if opcode == 1 or opcode == 2:
			# Add / Multiply
			param1 = (memory[memory[ip+1]] if modP1 == 0 else memory[ip+1])
			param2 = (memory[memory[ip+2]] if modP2 == 0 else memory[ip+2])
			memory[memory[ip+3]] = (param1 + param2) if opcode == 1 else (param1 * param2)
			ip += 4
		elif opcode == 3:
			# Takes integer from input and save
			memory[memory[ip+1]] = int(raw_input("> "))
			ip += 2
		elif opcode == 4:
			# Output
			print memory[memory[ip+1]] if modP1 == 0 else memory[ip+1]
			ip += 2
		elif opcode == 5 or opcode == 6:
			# Jump if true | false
			param1 = (memory[memory[ip+1]] if modP1 == 0 else memory[ip+1])
			param2 = (memory[memory[ip+2]] if modP2 == 0 else memory[ip+2])
			if opcode == 5 and param1 != 0:
				# If true
				ip = param2
			elif opcode == 6 and param1 == 0:
				# If false
				ip = param2
			else:
				# Nothing
				ip += 3 
		elif opcode == 7 or opcode == 8:
			# Less than | Equals 
			param1 = (memory[memory[ip+1]] if modP1 == 0 else memory[ip+1])
			param2 = (memory[memory[ip+2]] if modP2 == 0 else memory[ip+2])
			if opcode == 7:
				if param1 < param2:
					memory[memory[ip+3]] = 1
				else:
					memory[memory[ip+3]] = 0
			else:
				if param1 == param2:
					memory[memory[ip+3]] = 1
				else:
					memory[memory[ip+3]] = 0
			ip += 4
		elif opcode == 99:
			# 99 - End of program
			exit = True
		else:
			# Unexpected opcode
			print "[*] Unexpected opcode at ip ", ip, "->", opcode
			print "[*] Memory state:", memory
			exit = True


# Reads challenge input
with open("input5", "r") as file:
	line = "".join(l.rstrip() for l in file.readlines())

# Set memory
memory = map(int, line.split(","))

# Execute program:
#  > enter '1' for 1st part solution
#  > enter '5' for 2nd part solution
executeProgram(memory)
