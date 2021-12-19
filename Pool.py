import random
from Genome import Genome
import math
from Innovation import Innovation

DELTA_DISJOINT = 2.0
DELTA_WEIGHTS = 0.4
DELTA_THRESHOLD = 1.0

# TODO: check if this sorts from low to high or high to low
def compare_individual_fitness(item1):
    return item1.fitness

# individual 1 should have highest fitness
def crossover(individual1, individual2):

    genome1 = individual1.genome
    genome2 = individual2.genome 

    new_genes = []

    for gene1 in genome1.genes:

        gene1_innovation_number = gene1.innovation_number

        gene2 = genome2.get_gene_with_innovation_number(gene1_innovation_number)

        if gene2 != None and math.random < 0.5 and gene2.enabled:
            new_genes.append(gene2.deepcopy())
        else:
            new_genes.append(gene1.deepcopy())

    new_amount_neurons = max(genome1.amount_neurons, genome2.amount_neurons)

    new_genome = Genome(genome1.amount_inputs, genome1.amount_outputs, genome1.max_hidden_neurons, genome1.innovation)
    new_genome.genes = new_genes
    new_genome.amount_neurons = new_amount_neurons

    new_individual = Individual(new_genome, -1)

    return new_individual
    
# Combination of disjoint and excess genes
# As
def disjoint(genome1, genome2):
    disjoint = set()

    for gene in genome1.genes: 
        disjoint.add(gene.innovation_number)
    for gene in genome2.genes:
        disjoint.add(gene.innovation_number)

    max_genes = max(len(genome1.genes), len(genome2.genes))
    try:
        return len(disjoint) / max_genes
    except:
        return 0

def weights(genome1, genome2):

    sum = 0
    matches = 0 

    for gene1 in genome1.genes:
        for gene2 in genome2.genes: 
            if gene1.innovation_number == gene2.innovation_number:
                matches += 1
                sum = sum + abs(gene1.weight - gene2.weight)

    try:
        return sum / matches
    except:
        return 0


# Combines disjoint and excess genes (not seperate as in paper)
def same_species(genome1, genome2):
    dd = DELTA_DISJOINT * disjoint(genome1, genome2)
    dw = DELTA_WEIGHTS * weights(genome1, genome2)

    return dd + dw < DELTA_THRESHOLD


class Individual:
    def __init__(self, genome, species):
        self.genome = genome
        self.species = species 
        self.fitness = 0

    def deepcopy(self):
        new_genome = self.genome.deepcopy()

        new_individual = Individual(new_genome, self.species)
        new_individual.fitness = self.fitness 

        return new_individual


class Species: 
    CROSSOVER_CHANCE = 0.75


    def __init__(self):
        # List of individuals
        self.population = []
        self.initial_staleness = 15
        self.staleness = self.initial_staleness
        self.max_fitness = 0
        self.current_fitness = 0 

    def calculate_average_fitness(self):
        total_fitness = 0

        for individual in self.population:
            total_fitness += individual.fitness 

        self.current_fitness = total_fitness / len(self.population)


    def cull(self, cull_to_one=False):

        if cull_to_one:
            max_fitness = 0 
            best_individual = None

            for individual in self.population: 
                if individual.fitness > max_fitness:
                    max_fitness = individual.fitness 
                    best_individual = individual

            if best_individual != None: 
                self.population = [best_individual]
        else:
            # Kill half
            amount_remaining = math.ceil(len(self.population) / 2)

            self.population.sort(key=compare_individual_fitness, reverse=True)
            self.population = self.population[0:amount_remaining]

    def breed(self):
        child = None 

        if random.random() < self.CROSSOVER_CHANCE and len(self.population) > 1:
            individual1, individual2 = random.sample(self.population, 2)

            if individual1.fitness > individual2.fitness:
                child = crossover(individual1, individual2)
            else:
                child = crossover(individual2, individual1)

        elif len(self.population) > 0:
            individual = random.sample(self.population, 1)[0]
            child = individual.deepcopy()
        else:
            return 

        child.genome.mutate()

        return child 



class Pool:

    def __init__(self, amount_inputs, max_hidden_neurons, amount_outputs):
        # List of species
        self.species_list = []
        
        
        self.global_population_size = 0
        self.amount_inputs = amount_inputs
        self.amount_outputs = amount_outputs
        self.max_hidden_neurons = max_hidden_neurons


    def total_average_fitness(self):
        total_fitness_sum = 0

        for species in self.species_list:
            species.calculate_average_fitness()
            total_fitness_sum += species.current_fitness

        total_fitness_sum = total_fitness_sum  

        return total_fitness_sum
    

    def remove_stale_species(self):
        new_species_list = []

        for species in self.species_list:
            species.calculate_average_fitness()
            if species.current_fitness <= species.max_fitness:
                species.staleness -= 1
            else:
                species.staleness = species.initial_staleness

            if species.staleness > 0:
                new_species_list.append(species)

        self.species_list = new_species_list

    def remove_weak_species(self):
        i = 0 

        total_average_fitness = self.total_average_fitness()

        while(i < len(self.species_list)):
            if (self.species_list[i].current_fitness / total_average_fitness) * self.global_population_size < 1:
                del self.species_list[i]

            i += 1

    # @arg child: Individual
    def add_to_species(self, child):
        found_species = False
        
        for species in self.species_list:
            if same_species(child.genome, species.population[0].genome):
                species.population.append(child)
                found_species = True 
                break 

        if not found_species:
            new_species = Species()
            new_species.population.append(child) 
            self.species_list.append(new_species)


    def new_generation(self):   
        new_children = []
        # cull species
        for species in self.species_list:
            species.cull()

        self.remove_stale_species()
        self.remove_weak_species()

        total_average_fitness = self.total_average_fitness()

        for species in self.species_list:
            breed_amount = math.ceil((species.current_fitness / total_average_fitness) * self.global_population_size)

            for i in range(0, breed_amount):
                new_children.append(species.breed())
        
        for species in self.species_list:
            species.cull(True)

        while len(new_children) + len(self.species_list) < self.global_population_size:
            new_children.append(random.sample(self.species_list, 1)[0].breed())
        
        # print("lol")
        # print(self.global_population_size)
        # print(len(new_children))

        for child in new_children:
            self.add_to_species(child)


    def get_best_individual(self):
        max_individual = None 
        max_fitness = 0

        for species in self.species_list:
            for individual in species.population: 
                if individual.fitness > max_fitness:
                    max_individual = individual 
                    max_fitness = individual.fitness

        return max_individual


    def initialize(self, global_population_size):
        innovation = Innovation(1)
        self.global_population_size = global_population_size
        for i in range(0, global_population_size):
            new_genome = Genome(self.amount_inputs, self.amount_outputs, self.max_hidden_neurons, innovation)
            new_genome.mutate()
            individual = Individual(new_genome, -1)
            self.add_to_species(individual)

        