# Group 8
# Amalnnath Parameswaran - 100585138
# Zeerak Siddiqu - 100554495
# Ali Khan - 100526718


import random
import matplotlib.pyplot as plt
import math
from array import *

# Global Vars
citiesNo = 20
populationNo = 20
iterations = 10000

class city():
	x = 0
	y = 0

	# Assign set values
	def assign(self, x, y, name):
		self.x = x
		self.y = y
		self.name = name

	# Retrieve coordinates
	def get_coord(self):
		return self.x, self.y

	# Assign Random values
	def random(self, name):
		self.x = random.randint(0, 50)
		self.y = random.randint(0, 50)
		self.name = name

	# Return X
	def returnx(self):
		return self.x

	# Return Y
	def returny(self):
		return self.y

	# Return Name of City
	def returnName(self):
		return self.name

	# Calculate distance between 2 cities
	def distance(self, city):
		xDist = abs(self.returnx() - city.returnx())
		yDist = abs(self.returny() - city.returny())
		dist = math.sqrt((xDist * xDist) + (yDist * yDist))
		return dist

class cityArray():

	cities = []

	# Add city into city-array
	def addCity(self, city):
		self.cities.append(city)

	# Get city from City Array
	def getCity(self, index):
		return self.cities[index]

	# Populate city array with given domain
	def populate(self):
		for x in range(citiesNo):
			self.cities.append(city())
		self.cities[0].assign(20, 20, 0)
		self.cities[1].assign(20, 40, 1)
		self.cities[2].assign(20, 160, 2)
		self.cities[3].assign(40, 120, 3)
		self.cities[4].assign(60, 20, 4)
		self.cities[5].assign(60, 80, 5)
		self.cities[6].assign(60, 200, 6)
		self.cities[7].assign(80, 180, 7)
		self.cities[8].assign(100, 40, 8)
		self.cities[9].assign(100, 120, 9)
		self.cities[10].assign(100, 160, 10)
		self.cities[11].assign(120, 80, 11)
		self.cities[12].assign(140, 140, 12)
		self.cities[13].assign(140, 180, 13)
		self.cities[14].assign(160, 20, 14)
		self.cities[15].assign(180, 60, 15)
		self.cities[16].assign(180, 100, 16)
		self.cities[17].assign(180, 200, 17)
		self.cities[18].assign(200, 40, 18)
		self.cities[19].assign(200, 160, 19)

	# Populate array with random cities
	def populateRandom(self):
		index = 0
		for x in range(citiesNo):
			self.cities.append(city())
		for acity in self.cities:
			acity.random(index)
			index = index + 1

	# array of all x values in city array
	def xCoord(self):
		x = []
		for acity in self.cities:
			x.append(acity.returnx())
		return x

	# Array of all y values in city array
	def yCoord(self):
		y = []
		for acity in self.cities:
			y.append(acity.returny())
		return y

class order():
	def __init__(self):
		self.order = []
	
	# Create an empty order
	def empty(self):
		for i in range(0, citiesNo):
			a = city()
			a.random(-1)
			self.order.append(a)
			self.fitnessNorm = 1

	# Create a standard order (Ex. 0, 1, 2, 3...)
	def default(self, cityArray):
		for i in cityArray.cities:
			self.order.append(i)

	# Random order
	def shuffle(self, cityArray):
		self.default(cityArray)
		random.shuffle(self.order)

	# Return order array
	def getOrder(self):
		return self.order

	# Get a value, given an index
	def getVal(self, i):
		return self.order[i]

	# Set a value in order given index and value
	def setVal(self, i, val):
		self.order[i] = val

	# Print order to the console
	def printOrder(self):
		print("")
		for i in self.order:
			print i.returnName(),
		print self.getFit(),

	# Set the normalized fitness value (%)
	def setFitNorm(self, fit):
		self.fitnessNorm = fit

	# Get normalized fitness value (%)
	def getFitNorm(self):
		return self.fitnessNorm

	# Get calculated fitness values
	def getFit(self):
		return self.fit

	# Calculate fitness
	def fitness(self):
		self.a = city()
		self.b = city()
		total = 0
		for i in self.order:
			if i.returnName() == 0:
				self.b = i
			else:
				total = total + i.distance(self.a) 
			self.a = i
		total = total + self.a.distance(self.b)
		fit = 1/total
		self.fit = fit
		return fit

	# Crossover 2 orders into this order
	def crossover(self, ordA, ordB):
		a = random.randint(0, citiesNo-1)
		if a == citiesNo-1:
			b = random.randint(a - 1, citiesNo-1)
		else:
			b = random.randint(a + 1, citiesNo-1)

		used = []
		modB = []
	
		c = order()
		c.empty()

		count = 0
		for x in xrange(a, b):
		 	c.setVal(count,ordA.getVal(x))
		 	count = count + 1
		 	used.append(ordA.getVal(x).returnName())

		for i in xrange(0, citiesNo):
			check = 0
			temp = ordB.getVal(i)
			for x in used:
				if x == ordB.getVal(i).returnName():
					check = check + 1	
			if check == 0:
				modB.append(temp)

		count = 0
		for x in xrange(0, citiesNo):
			if(c.getVal(x).returnName() == -1):
				c.setVal(x, modB[count])
				count = count + 1
		return c

	# Mutate this order
	def mutate(self):
		a = random.randint(0, citiesNo-1)
		b = random.randint(0, citiesNo-1)

		c = self.order[a]
		d = self.order[b]

		self.order[b] = c
		self.order[a] = d

class population():

	def __init__(self):
		self.population = []
		self.recordDist = 0
		self.best = order()
		
	# Create an initial population given a cityarray
	def createPop(self, gen, cityArray):
		for i in range(populationNo):
			self.population.append(order())
		for i in self.population:
			i.shuffle(cityArray)
		if gen == 0:
			self.population[0].default(cityArray)

	# Print the population
	def printPop(self):
		print "\nPop:"
		for i in self.population:
			i.printOrder()

	# Find fitness of orders within population
	def findFit(self):
		total = 0
		for i in self.population:
			i.fitness()
			a = i.getFit()
			if a > self.recordDist:
				self.recordDist = a
				self.best = i
			total = total + i.getFit()
		for i in self.population:
			a = i.getFit()
			b = a / total
			i.setFitNorm(b)

	# Order with best fitness in current population
	def getBest(self):
		return best

	# Pick values from previous population and add to self
	def pick(self, pop):
		a = order()
		self.pop = pop
		total = 0
		prob = []

		num = random.randint(0, 100)*0.01
		#print num
		for i in pop.population:
			total = i.getFitNorm() + total
			prob.append(total)
			if num < total:
				return i 
			a = i
		return a

	# Create the next generation population
	def nextGen(self, popu, mutationRate, crossRate):
		self.popu =  popu

		for i in range(populationNo):
				self.population.append(self.pick(popu))

		for i in range(populationNo):
			if random.randint(0, 11) < mutationRate:
				self.population[i].mutate()
			elif random.randint(0, 11) < crossRate:
				self.population[i] = self.population[i].crossover(self.population[random.randint(0, citiesNo-1)], self.population[random.randint(0, citiesNo-1)])

def main():
	cityArr = cityArray()
	cityArr.populate()
	atbest = order()
	atbestfit = 0

	pop = population()
	pop.createPop(0, cityArr)
	#pop.printPop()
	pop.findFit()
	#pop.printPop()
	pops = []
	i = 0

	for i in xrange(iterations):
	#while atbestfit < 0.0075:
		pops.append(population())
		pops[i].nextGen(pop, 1, 5)
		pops[i].findFit()
		pops[i].printPop()
		if pops[i].recordDist > atbestfit:
			print(atbestfit)
			atbestfit = pops[i].recordDist
			atbest = pops[i].best
			atbest.printOrder()
			print(atbestfit)

			# Save best order
			pop = pops[i]
			i = i + 1

			x_best = []
			y_best = []

			first = city()
			a = 0
			for j in atbest.order:
				if a == 0:
					first = j
					a=1
				x_best.append(j.returnx())
				y_best.append(j.returny())

		
	# Plot best order
	atbest.printOrder()
	xcord = cityArr.xCoord()
	ycord = cityArr.yCoord()

	x_best.append(first.returnx())
	y_best.append(first.returny())

	plt.plot(x_best, y_best, linewidth=3)
	plt.plot(xcord, ycord, 'ro')
	plt.show()

if __name__ == "__main__":
    main()