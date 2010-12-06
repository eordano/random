import random
import config

from generation import Generation
from individual import Individual

bs = [[lambda x: 'A', 'Always A'], [lambda x: 'B', 'Always B'], [lambda x: 'A' if x and x[-1][0] > x[-1][1] else 'B', 'Most crowded'], [lambda x: 'A' if x and x[-1][0] < x[-1][1] else 'B', 'Least crowded'], [lambda x: 'A' if len(x) % 2 else 'B', 'A, B'], [lambda x: 'A' if len(x) % 3 < 2 else 'B', 'A, A, B'], [lambda x: 'A' if x and (700/x[-1][0] if x[-1][0] else 1000) > (300/x[-1][1] if x[-1][1] else 1000) else 'B', 'Most $$$ of Last Round'], [lambda x: 'A' if x and (700/x[-1][0] if x[-1][0] else 1000) < (300/x[-1][1] if x[-1][1] else 1000) else 'B', 'Less $$$ of Last Round'], [lambda x: 'A' if random.randint(0, 2) % 2 else 'B', 'Random']]

class f20(Individual):
	def __init__(self, string):
		self.string = string
		self.fit = None
		
	@classmethod
	def random_individual(cls):
		return f20(''.join(['A' if random.randrange(2) else 'B' for i in xrange(config.string_length)]))
	
	def random_mutant(self):
		newstr = [i for i in self.string]
		for i in xrange(config.genes_mutated):
			a = random.randrange(len(self.string))
			newstr[a] = 'A' if self.string[a] == 'B' else 'B'
		return f20(''.join(newstr))
	
	def mate(self, friend):
		newstr = ''
		for i in xrange(len(self.string)):
			newstr += self.string[i] if random.randrange(2) else friend.string[i]
		return f20(newstr)
	
	def fitness(self):
		if self.fit:
			return self.fit
		score = 0.0
		for J in xrange(config.simulations_per_individual):
			players = [[lambda x: self.string[len(x)], 'Individual']]
			players += [random.choice(bs) for i in xrange(6)]
			x = []
			record = []
			points = [0 for i in xrange(7)]
			for I in xrange(20):
				what = [p[0](x) for p in players]
				x.append([sum([1 if j == 'A' else 0 for j in what]), sum([1 if j == 'B' else 0 for j in what])])
				money = [700/x[-1][0] if j == 'A' else 300/x[-1][1] for j in what]
				points = [sum(a) for a in zip(points, money)]
				record.append(points)
			score += (float(record[-1][0])/float(max(record[-1])))**config.value_power
		self.fit = score
		return score
	
	def get_description(self):
		return " - (%s), fitness ~ %f\n"%(self.string, self.fitness())
		
if __name__ == '__main__':
	G = Generation(f20)
	cont = 0
	while True:
		print "Generation #%d"%cont
		cont += 1
		G = G.spawn_new_gen(Debug=True)