class IntCodeComputer:
	MOD_POS = 0
	MOD_INM = 1
	MOD_REL = 2

	def __init__(self, memory):
		self.memory = memory + 3000 * [0]
		self.ip = 0
		self.relativeBase = 0
		self.finished = False
		self.outputs = []
		self.inputs = []
		self.mutedOutput = False # True to not output to stdout
		self.pauseOnNOutputs = 0 # Don't stop on output
		self.inputFunction = None # Take input from function

	def getOutputs(self):
		return self.outputs

	def muteOutput(self, value):
		self.mutedOutput = value

	def addInputs(self, inputs):
		self.inputs += inputs

	def setInputFromFunction(self, inputFunction):
		self.inputFunction = inputFunction

	def hasFinished(self):
		return self.finished

	def executeProgramAndPauseOnOutput(self, numOutputs=1):
		self.pauseOnNOutputs = numOutputs
		self.currentOutputs = 0
		self.outputs = []
		self.executeProgram()

	def getValueByMode(self, position, mode, literal):
		value = None

		if not literal:
			# Default mode
			if mode == self.MOD_POS:
				# By position
				value = self.memory[self.memory[position]]
			elif mode == self.MOD_INM:
				# Inmediate
				value = self.memory[position]
			elif mode == self.MOD_REL:
				# Relative
				value = self.memory[self.relativeBase + self.memory[position]]
			else:
				print "[*] Invalid mode:", mode
				exit()
		else:
			# Literal mode: for writings
			if mode == self.MOD_POS or mode == self.MOD_INM:
				value = self.memory[position]
			elif mode == self.MOD_REL:
				value = self.relativeBase + self.memory[position]
			else:
				print "[*] Invalid mode:", mode
				exit()

		return value

	def executeProgram(self):
		exit = False
		while not exit:
			# Extracts opcode and parameter modes
			instruction = str(self.memory[self.ip]).zfill(5)
			opcode = int(instruction[3:])
			modP1  = int(instruction[2])
			modP2  = int(instruction[1])
			modP3  = int(instruction[0])

			if opcode == 1 or opcode == 2:
				# Add / Multiply
				param1 = self.getValueByMode(self.ip+1, modP1, False)
				param2 = self.getValueByMode(self.ip+2, modP2, False)
				dest = self.getValueByMode(self.ip+3, modP3, True)
				self.memory[dest] = (param1 + param2) if opcode == 1 else (param1 * param2)
				self.ip += 4
			elif opcode == 3:
				if self.inputFunction != None:
					# Takes input from a function
					inp = self.inputFunction()
				else:
					# Takes integer from input and save
					if len(self.inputs) > 0:
						# Takes input from parameters
						inp = int(self.inputs.pop(0))
					else:
						# Takes input from standard input
						inp = int(raw_input("> "))
				dest = self.getValueByMode(self.ip+1, modP1, True)
				self.memory[dest] = inp
				self.ip += 2
			elif opcode == 4:
				# Output
				output = self.getValueByMode(self.ip+1, modP1, False)
				if not self.mutedOutput:
					print output
				self.outputs.append(output)
				self.ip += 2
				if self.pauseOnNOutputs > 0:
					# Pauses on output
					if self.currentOutputs+1 >= self.pauseOnNOutputs:
						exit = True
					else:
						self.currentOutputs += 1
			elif opcode == 5 or opcode == 6:
				# Jump if true | false
				param1 = self.getValueByMode(self.ip+1, modP1, False)
				param2 = self.getValueByMode(self.ip+2, modP2, False)
				if opcode == 5 and param1 != 0:
					# If true
					self.ip = param2
				elif opcode == 6 and param1 == 0:
					# If false
					self.ip = param2
				else:
					# Nothing
					self.ip += 3 
			elif opcode == 7 or opcode == 8:
				# Less than | Equals 
				param1 = self.getValueByMode(self.ip+1, modP1, False)
				param2 = self.getValueByMode(self.ip+2, modP2, False)
				dest = self.getValueByMode(self.ip+3, modP3, True)
				if opcode == 7:
					value = 1 if param1 < param2 else 0
				else:
					value = 1 if param1 == param2 else 0
				self.memory[dest] = value
				self.ip += 4
			elif opcode == 9:
				# Relative base adjust
				self.relativeBase += self.getValueByMode(self.ip+1, modP1, False)
				self.ip += 2
			elif opcode == 99:
				# 99 - End of program
				exit = True
				self.finished = True	
			else:
				# Unexpected opcode
				print "[*] Unexpected opcode at ip ", self.ip, "->", opcode
				print "[*] Memory state:", self.memory
				exit = True
				self.finished = True
