import networkx as nx

UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)
DIRECTIONS = [RIGHT, DOWN, LEFT, UP]

WALL = "#"
PASSAGE = "."

START = "AA"
END = "ZZ"

def addPortal(dictionary, name, coords):
	if name in dictionary:
		dictionary[name].append(coords)
	else:
		dictionary[name] = [coords]

# Reads challenge input
with open("input20", "r") as file:
	lines = [line.rstrip("\r\n") for line in file.readlines()]
	if len(lines[-1].split()) == 0: lines.pop() # Removes last element

# Dictionary of portals: {"AA":[(0,0), (1,1)]}
portals = {}

# Find portals positions
# Top portals
for i in range(len(lines[0])):
	if lines[0][i].isalpha():
		p = lines[0][i] + lines[1][i]
		addPortal(portals, p, (i,2))
# Bottom portals
maxY = len(lines)-1
for i in range(len(lines[-1])):
	if lines[maxY-1][i].isalpha():
		p = lines[maxY-1][i] + lines[maxY][i]
		addPortal(portals, p, (i, maxY-2)) 
# Left portals
for i in range(len(lines)):
	if lines[i][0].isalpha():
		p = lines[i][0] + lines[i][1]
		addPortal(portals, p, (2, i))
# Right portals
maxX = len(lines[0])-1
for i in range(len(lines)):
	if lines[i][maxX-1].isalpha():
		p = lines[i][maxX-1] + lines[i][maxX]
		addPortal(portals, p, (maxX-2, i))
# Middle portals
for i in range(2, maxY-1):
	for j in range(2, maxX-1):
		if lines[i][j].isalpha():
			if lines[i+1][j].isalpha():
				# Vertical
				p = lines[i][j] + lines[i+1][j]
				if lines[i-1][j] == PASSAGE:
					# Top
					addPortal(portals, p, (j, i-1))
				elif lines[i+2][j] == PASSAGE:
					# Bottom
					addPortal(portals, p, (j, i+2))
			elif lines[i][j+1].isalpha():
				# Horizontal
				p = lines[i][j] + lines[i][j+1]
				if lines[i][j-1] == PASSAGE:
					# Left
					addPortal(portals, p, (j-1, i))
				elif lines[i][j+2] == PASSAGE:
					# Right
					addPortal(portals, p, (j+2, i))

# Mapping of the maze
maze = nx.Graph()
for i in range(2, maxY-1):
	for j in range(2, maxX-1):
		if lines[i][j] == PASSAGE:
			c = (j, i, 0)
			maze.add_node(c)
			# Finds neigbours passages
			for d in DIRECTIONS:
				if lines[i + d[1]][j + d[0]] == PASSAGE:
					n = (j + d[0], i + d[1], 0)
					maze.add_node(n)
					maze.add_edge(c, n)

# Copy plain graph for part 2
mazeRec = maze.copy()

# Part 1
# Applies portals connections
for portal in portals.items():
	values = portal[1]
	if len(values) > 1:
		maze.add_edge(values[0] + (0,), values[1] + (0,))


paths = [len(path)-1 for path in nx.all_simple_paths(maze, portals[START][0] + (0,), portals[END][0] + (0,))]
print "Part 1 - Paths from AA to ZZ:"
for lPath in paths:
	print "  ", lPath
print "[*] Solution 1:", "not found" if len(paths) == 0 else min(paths)

# Part 2
# Removes start and exit from recursive (they are walls now)
recursive = mazeRec.copy()
recursive.remove_node(portals[START][0] + (0,))
recursive.remove_node(portals[END][0] + (0,))

solution2 = None
DEPTH = 25
print "Trying to find 2nd solution with", DEPTH, "levels of recursivity..."
for i in range(DEPTH):
	# Copy nodes at depth level
	for node in recursive.nodes():
		mazeRec.add_node((node[0], node[1], i+1))
	# Copy edges
	for edge in recursive.edges():
		nEdge1 = (edge[0][0], edge[0][1], i+1)
		nEdge2 = (edge[1][0], edge[1][1], i+1)
		mazeRec.add_edge(nEdge1, nEdge2)
	# Applies portals logic
	for portal in portals.items():
		if len(portal[1]) > 1:
			outer = portal[1][0]
			inner = portal[1][1]
			# Outer portal is connected to the inner of the upper level
			mazeRec.add_edge((outer[0], outer[1], i+1), (inner[0], inner[1], i))

paths = [len(path)-1 for path in nx.all_simple_paths(mazeRec, portals[START][0] + (0,), portals[END][0] + (0,))]
print "Part 2 - Paths from AA to ZZ (with recursivity):"
for lPath in paths:
	print "  ", lPath
print "[*] Solution 2:", "not found" if len(paths) == 0 else min(paths)
