from intcodecomp import IntCodeComputer

# Reads challenge input
with open("input9", "r") as file:
	line = "".join(l.rstrip() for l in file.readlines())

# Set memory
program = map(int, line.split(","))

IntCodeComputer(program).executeProgram()
