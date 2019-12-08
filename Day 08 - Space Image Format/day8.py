import sys

WIDTH = 25
HEIGHT = 6

with open("input8", "r") as file:
	raw = "".join(line.rstrip() for line in file.readlines())

layers = [raw[i:i + WIDTH*HEIGHT] for i in range(0, len(raw), WIDTH*HEIGHT)]

# Part 1
minZeroesLayer = None
minZeroes = sys.maxint
for l in layers:
	c = l.count("0")
	if c < minZeroes:
		minZeroesLayer = l
		minZeroes = c

solution1 = minZeroesLayer.count("1") * minZeroesLayer.count("2")
print "[*] Solution 1:", solution1

# Part 2
# Creates empty image
finalImage = len(layers[0]) * [""]

# Iterates layers generating the final image
for layer in layers:
	# Iterates the final image and gets values from the current layer
	for i in range(len(finalImage)):
		if len(finalImage[i]) == 0:
			# Empty position
			if layer[i] != "2":
				finalImage[i] = layer[i]

print "[*] Solution 2:"
for i in range(HEIGHT):
	s = ""
	for j in range(WIDTH):
		if finalImage[i * WIDTH + j] == "0":
			s += "#"
		else:
			s += " "
	print s
