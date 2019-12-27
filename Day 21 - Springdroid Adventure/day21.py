from intcodecomp import IntCodeComputer

# Droid takes input as ASCII codes, ending with newline
def genInput(instrs):
	inp = []
	for inst in instrs:
		inp += [ord(c) for c in inst]
		inp += [ord('\n')]
	return inp

def getOutput(program, inp):
	droid = IntCodeComputer(program)
	droid.muteOutput(True)
	droid.addInputs(genInput(inp))
	droid.executeProgram()
	return droid.getOutputs()

# Reads challenge input
with open("input21", "r") as file:
	program = map(int, file.read().split(","))

# Part 1
instP1 = [
	"NOT A T",
    "NOT B J",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND D J",
    "WALK"]

out = getOutput(program, instP1)
if out[-1] > 127:
	print "[*] Solution 1:", out[-1]
else:
	print "".join(chr(o) if o < 127 else str(o) for o in out)

# Part 2
instP2 = [
	"NOT A T",
    "NOT B J",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND D J",
    "NOT E T",
    "NOT T T",
    "OR H T",
    "AND T J",
    "RUN"]

out = getOutput(program, instP2)
if out[-1] > 127:
	print "[*] Solution 2:", out[-1]
else:
	print "".join(chr(o) if o < 127 else str(o) for o in out)
