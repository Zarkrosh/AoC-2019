class Moon:
	def __init__(self, (x, y, z)):
		self.x = x
		self.y = y
		self.z = z
		self.vX = self.vY = self.vZ = 0

	def move(self, step=0):
		self.x += self.vX
		self.y += self.vY
		self.z += self.vZ

	def potentialEnergy(self):
		return abs(self.x) + abs(self.y) + abs(self.z)

	def kineticEnergy(self):
		return abs(self.vX) + abs(self.vY) + abs(self.vZ)

	def totalEnergy(self):
		return self.potentialEnergy() * self.kineticEnergy()

def updateVelocity(moon1, moon2):
	if moon1.x != moon2.x:
		moon1.vX += 1 if moon1.x < moon2.x else -1
		moon2.vX += 1 if moon2.x < moon1.x else -1
	if moon1.y != moon2.y:
		moon1.vY += 1 if moon1.y < moon2.y else -1
		moon2.vY += 1 if moon2.y < moon1.y else -1
	if moon1.z != moon2.z:
		moon1.vZ += 1 if moon1.z < moon2.z else -1
		moon2.vZ += 1 if moon2.z < moon1.z else -1	

def gcd(a, b):
	if b == 0: return a
	else: return gcd(b, a % b)

def lcm(x, y):
	return (x * y) / gcd(x, y)

# Reads challenge input
with open("input12", "r") as file:
	lines = file.readlines()

# Parses moons' data
moons = [Moon([int(c.split("=")[1]) for c in l.translate(None, "<> ").split(",")]) for l in lines]

for steps in range(1000):
	# Updates velocity for each pair of moons
	for i in range(len(moons)):
		cMoon = moons[i]
		for j in range(i+1, len(moons)):
			oMoon = moons[j]
			# For every axis
			updateVelocity(cMoon, oMoon)
	# Applies velocity
	for m in moons: m.move()

print "[*] Solution 1:", sum(m.totalEnergy() for m in moons)

# Part 2
# Parses moons' data (again)
moons = [Moon([int(c.split("=")[1]) for c in l.translate(None, "<> ").split(",")]) for l in lines]

# Initial positions and velocities
initX = [[m.x, m.vX] for m in moons]
initY = [[m.y, m.vY] for m in moons]
initZ = [[m.z, m.vZ] for m in moons]

# Cycle flags
cycleX = None
cycleY = None
cycleZ = None

solution2 = None
steps = 1
while cycleX == None or cycleY == None or cycleZ == None:
	# Updates velocity for each pair of moons
	for i in range(len(moons)):
		cMoon = moons[i]
		for j in range(i+1, len(moons)):
			oMoon = moons[j]
			# For every axis
			updateVelocity(cMoon, oMoon)
	# Applies velocity
	for m in moons: m.move()
	# Checks for cycles on each axis
	if cycleX == None and [[m.x, m.vX] for m in moons] == initX:
		cycleX = steps
	if cycleY == None and [[m.y, m.vY] for m in moons] == initY:
		cycleY = steps
	if cycleZ == None and [[m.z, m.vZ] for m in moons] == initZ:
		cycleZ = steps
	# Next step
	steps += 1
 
lcmXY = lcm(cycleX, cycleY)
solution2 = lcm(lcmXY, cycleZ)
print "[*] Solution 2:", solution2

# ;)
import webbrowser
webbrowser.open_new_tab("https://www.youtube.com/watch?v=7QVeSEz1M_Q")
