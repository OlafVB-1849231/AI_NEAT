import Main 
from Pool import Individual,Species,Pool
import random
import Visualize

AMOUNT_INPUTS = 3
AMOUNT_OUTPUTS = 1
MAX_HIDDEN = 100

pool = Pool(AMOUNT_INPUTS, MAX_HIDDEN, AMOUNT_OUTPUTS)
pool.initialize(100)

print(len(pool.species_list))

for species in pool.species_list:
    for individual in species.population:
        individual.fitness = random.random() * 1000

pool.new_generation()


Visualize.visualize(pool.species_list[0].population[0].genome)