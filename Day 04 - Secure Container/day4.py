# Valid password:
#  1: 6 digit number
#  2: The value is within the range given
#  3: Adjacent digits are the same
#  4: Going from left to right, de digits never decrease
# (2nd part) 
#  5: the two adjacent digits are not part of a larger group of matching digits

lowLimit = 357253
highLimit = 892942

def isValidPassword1(password):
	res = True
	sameAdjacent = False
	lastCharOrd = 0
	for ch in str(password):
		if ord(ch) < lastCharOrd:
			res = False
			break
		elif ord(ch) == lastCharOrd:
			sameAdjacent = True
		lastCharOrd = ord(ch)

	res &= sameAdjacent

	return res

def isValidPassword2(password):
	res = True
	lastCharOrd = 0
	lastAdjacentLen = 0
	adjacents = []
	for ch in str(password):
		if ord(ch) < lastCharOrd:
			res = False
			break
		elif ord(ch) == lastCharOrd:
			lastAdjacentLen += 1
		elif lastAdjacentLen > 0:
			adjacents.append(lastAdjacentLen+1)
			lastAdjacentLen = 0
		lastCharOrd = ord(ch)

	if res and lastAdjacentLen > 0:
		adjacents.append(lastAdjacentLen+1)

	return res and (2 in adjacents)

possibles1 = []
possibles2 = []
for i in range(lowLimit, highLimit + 1):
	if isValidPassword1(i):
		possibles1.append(i)
	if isValidPassword2(i):
		possibles2.append(i)

print "[*] Solution 1:", len(possibles1)
print "[*] Solution 2:", len(possibles2)
