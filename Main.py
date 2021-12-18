from Genome import Genome 
from Gene import Gene


AMOUNT_INPUTS = 3
AMOUNT_OUTPUTS = 1




def generateNetwork(genome):

    neurons = []

    for i in range(0, AMOUNT_INPUTS):
        neurons.append(Neuron())    






testGenome = Genome(3, 3, 100)
# testGenome.print_genes()
# testGenome.mutate()
# testGenome.print_genes()

for i in range(0, 4):
    testGenome.mutate()
    print("--------------------")
    testGenome.print_genes()


