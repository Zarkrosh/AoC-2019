import networkx as nx

def getNumAllOrbits(depth, node, graph):
	result = depth
	for s in graph.successors(node):
		result += getNumAllOrbits(depth + 1, s, graph)
	return result

with open("input6", "r") as file:
	orbits = file.readlines()

grOrbits = nx.DiGraph()
for orbit in orbits:
	nodes = orbit.rstrip().split(")")
	grOrbits.add_edge(nodes[0], nodes[1])

print "[*] Solution 1:", getNumAllOrbits(0, "COM", grOrbits)
print "[*] Solution 2:", len(nx.shortest_path(grOrbits.to_undirected(), "YOU", "SAN")) - 3
