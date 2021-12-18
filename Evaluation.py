import Main

class Evaluation():
    
    def __init__(self, individual):
        self.individual = individual
        self.individual.fitness = 0
        self.network = Main.generateNetwork(self.individual.genome)

    def eval(self, inputs):
        return Main.eval(inputs, self.network)
    
    def increase_fitness(self, amount):
        self.individual.fitness += amount