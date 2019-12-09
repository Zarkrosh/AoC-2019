import copy
import itertools
from intcodecomp import IntCodeComputer

# Reads challenge input
with open("input7", "r") as file:
	line = "".join(l.rstrip() for l in file.readlines())

# Set memory
program = map(int, line.split(","))

solution1 = 0
# Iterates all permutations of the phase settings
for perm in list(itertools.permutations([0,1,2,3,4], 5)):
	signal = 0
	for i in range(5):
		memory = copy.deepcopy(program)
		module = IntCodeComputer(memory)
		module.addInputs([perm[i], signal])
		module.muteOutput(True)
		module.executeProgram()
		signal = module.getOutputs()[0]
	
	if signal > solution1:
		solution1 = signal
	
print "[*] Solution 1:", solution1

solution2 = 0
# Iterates all permutations of the phase settings (loopback mode)
for perm in list(itertools.permutations([5,6,7,8,9], 5)):
	signal = 0
	# Generates the 5 independent modules
	modules = []
	for i in range(5):
		module = IntCodeComputer(memory)
		module.addInputs([perm[i]])
		module.muteOutput(True)
		modules.append(module)

	while not modules[-1].hasFinished():
		for module in modules:
			module.addInputs([signal])
			module.executeProgramAndPauseOnOutput()
			signal = module.getOutputs()[-1]

	if signal > solution2:
		solution2 = signal

print "[*] Solution 2:", solution2
