def getPattern(position):
	base = [0,1,0,-1]
	res = []
	for b in base: res += [b] * (position + 1)
	return res

def FFT(inputSignal, iterations):
	nSignal = [0] * len(inputSignal)
	for it in range(iterations):
		for i in range(len(inputSignal)):
			patt = getPattern(i)
			iPatt = 1
			res = 0
			for j in range(len(inputSignal)):
				res += inputSignal[j] * patt[iPatt]
				iPatt += 1
				if iPatt == len(patt): iPatt = 0
			nSignal[i] = abs(res) % 10
		inputSignal = nSignal
	return inputSignal

def FFT2(inputSignal, iterations):
	length = len(inputSignal)
	nSignal = [0] * length
	for it in range(iterations):
		nSignal[-1] = inputSignal[-1]
		# The offset is in the last half of the data, so I can omit the first half calculations
		for i in range(length - 2,length // 2, -1):
			nSignal[i] = abs(inputSignal[i] + nSignal[i+1]) % 10
		inputSignal = nSignal
		nSignal = [0] * len(inputSignal)
	return inputSignal

# Reads challenge input
with open("input16", "r") as file:
	inp = [int(c) for c in file.read().rstrip()]

prevInp = int("".join(str(c) for c in inp))
result = FFT(inp,100)
print "[*] Solution 1:", "".join(str(c) for c in result)[:8]

# Part 2
# Reads challenge input (again)
with open("input16", "r") as file:
	inp = [int(c) for c in file.read().rstrip()]

inp = inp * 10000
offset = int("".join(str(c) for c in inp[:7]))
result = FFT2(inp, 100)
print "[*] Solution 2:", "".join(str(r) for r in result[offset:offset+8])
