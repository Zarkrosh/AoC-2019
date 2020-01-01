DEAL_INC = "deal with increment"
DEAL_NEW = "deal into new stack"
CUT = "cut"

def shuffle(shuffling, deck_size):
	# "Factory order"
	deck = [i for i in range(deck_size)]
	for s in shuffling:
		if DEAL_INC in s:
			# Deal with increment N: circular buffer popping the leftmost card every N
			nDeck = [-1] * deck_size
			n = int(s.split()[-1])
			pos = 0
			while len(deck) > 0:
				nDeck[pos % deck_size] = deck.pop(0)
				pos += n
			deck = nDeck
		elif DEAL_NEW in s:
			# Deal new deck: reverse deck
			deck.reverse()
		elif CUT in s:
			# Cut N cards
			n = int(s.split()[-1])
			deck = deck[n:] + deck[:n]
		else:
			print "[!] Error parsing shuffling:", s
			exit()
	return deck

with open("input22", "r") as file:
	shuffling = file.readlines()

deck = shuffle(shuffling, 10007)
print "[*] Solution 1:", deck.index(2019)

# Part 2: I hate maths
# I liked this neat solution ->
# 	https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbtugcu
NEW_SIZE = 119315717514047
TIMES = 101741582076661
POSITION = 2020

shuffles = { 
	'deal with increment ': lambda x, m, a, b: (a * x % m, b * x % m),
	'deal into new stack': lambda _, m, a, b: (-a % m, (m - 1 - b) % m),
	'cut ': lambda x,m,a,b: (a, (b - x) % m) 
}

a, b = 1, 0
for s in shuffling:
	for op, fn in shuffles.items():
		if s.startswith(op):
			arg = int(s[len(op):]) if op[-1] == ' ' else 0
			a,b = fn(arg, NEW_SIZE, a, b)
			break

r = (b * pow(1 - a, NEW_SIZE - 2, NEW_SIZE)) % NEW_SIZE
print "[*] Solution 2:", ((POSITION - r) * pow(a, TIMES * (NEW_SIZE - 2), NEW_SIZE) + r) % NEW_SIZE
