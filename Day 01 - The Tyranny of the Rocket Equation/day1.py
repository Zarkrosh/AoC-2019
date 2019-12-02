# Dynamic programming
calculated = {}

def getFuel(massFuel, recursive):
	result = 0

	if massFuel > 0:
		if massFuel in calculated:
			# Result already calculated
			result = calculated[massFuel]
		else:
			result = max(int(massFuel/3) - 2, 0)
			calculated[massFuel] = result

		if recursive:
			result += getFuel(result, recursive)

	return result


with open("input1", "r") as file:
	lines = file.readlines()

solution1 = 0
solution2 = 0
for line in lines:
	if len(line) > 0:
		mass = int(line.rstrip())
		solution1 += getFuel(mass, False)
		solution2 += getFuel(mass, True)

print "[*] Solution 1:", solution1
print "[*] Solution 2:", solution2
