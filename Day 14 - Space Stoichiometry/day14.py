def setLeftover(quantity, chemical, leftovers):
	if chemical in leftovers:
		leftovers[chemical] += quantity
	else:
		leftovers[chemical] = quantity

def checkLeftover(quantity, chemical, leftovers):
	consumed = 0
	if chemical in leftovers:
		if leftovers[chemical] >= quantity:
			leftovers[chemical] -= quantity
			consumed = quantity
	return consumed

def getCostOfProducing(quantity, chemical, reactions, leftovers):
	cost = 0
	if chemical in reactions:
		reaction = reactions[chemical]
		qResult = reaction[0]
		sources = reaction[1]
		produced = checkLeftover(quantity, chemical, leftovers)
		while produced < quantity:
			for source in sources:
				qSource = source[0]
				cSource = source[1]
				cost += getCostOfProducing(qSource, cSource, reactions, leftovers)
			produced += qResult
		setLeftover((produced-quantity), chemical, leftovers)
	else: cost = quantity

	return cost


# Reads challenge input
with open("input14", "r") as file:
	inp = file.readlines()

# Test
# 31
#inp = ["10 ORE => 10 A","1 ORE => 1 B","7 A, 1 B => 1 C","7 A, 1 C => 1 D","7 A, 1 D => 1 E","7 A, 1 E => 1 FUEL"]
# 165
#inp = ["9 ORE => 2 A","8 ORE => 3 B","7 ORE => 5 C","3 A, 4 B => 1 AB","5 B, 7 C => 1 BC","4 C, 1 A => 1 CA","2 AB, 3 BC, 4 CA => 1 FUEL"]
# 180697 
#inp = ["2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG","17 NVRVD, 3 JNWZP => 8 VPVL","53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL","22 VJHF, 37 MNCFX => 5 FWMGM","139 ORE => 4 NVRVD","144 ORE => 7 JNWZP","5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC","5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV","145 ORE => 6 MNCFX","1 NVRVD => 8 CXFTF","1 VJHF, 6 MNCFX => 4 RFSQX","176 ORE => 6 VJHF"]
# 2210736 
inp = ["171 ORE => 8 CNZTR","7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL","114 ORE => 4 BHXH","14 VRPVC => 6 BMBT","6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL","6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT","15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW","13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW","5 BMBT => 4 WPTQ","189 ORE => 9 KTJDG","1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP","12 VRPVC, 27 CNZTR => 2 XDBXC","15 KTJDG, 12 BHXH => 5 XCVML","3 BHXH, 2 VRPVC => 7 MZWV","121 ORE => 7 VRPVC","7 XCVML => 6 RJRHP","5 BHXH, 4 VRPVC => 5 LTCX"]

reactions = {}
for i in inp:
	parts = [p.strip() for p in i.rstrip().split("=>")]
	result = parts[1].split() # ["quantity", "chemical"]
	lSources = [p.strip() for p in parts[0].split(",")]
	lSources = [s.split() for s in lSources]
	sources = []
	for s in lSources:
		sources.append((int(s[0]), s[1]))
	# "result": [qty, [(list of sources)]]
	reactions[result[1]] = [int(result[0]), sources]

print reactions
leftovers = {}
print "[*] Solution 1:", getCostOfProducing(1, "FUEL", reactions, leftovers)
print leftovers
