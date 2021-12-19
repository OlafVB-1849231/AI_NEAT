from Genome import Genome 
from Gene import Gene
from Neuron import Neuron
from Connection import Connection

AMOUNT_INPUTS = 6
AMOUNT_OUTPUTS = 1
MAX_HIDDEN = 100

def generateNetwork(genome):
    neurons = []
    for i in range(0, AMOUNT_INPUTS + AMOUNT_OUTPUTS + MAX_HIDDEN):
        neurons.append(None)

    for i in range(0, AMOUNT_INPUTS):
        neurons[i] = Neuron()    

    for gene in genome.genes:
        if gene.enabled:

            if neurons[gene.to_neuron_id] == None:
                neurons[gene.to_neuron_id] = Neuron([])

            if neurons[gene.from_neuron_id] == None: 
                neurons[gene.from_neuron_id] == Neuron([])


            # TODO: find out why try except is necessary
            try:
                connection = Connection(gene.from_neuron_id, gene.weight)
                neurons[gene.to_neuron_id].incoming.append(connection)
            except:
                pass

    return neurons 


def eval(inputs, network):
    for i in range(0, len(inputs)):
        network[i].value = inputs[i] 
    
    
    for i in range(AMOUNT_INPUTS, MAX_HIDDEN + AMOUNT_INPUTS + AMOUNT_OUTPUTS):
        if network[i] != None:
            network[i].calc_value(network) 

    outputs = []

    for i in range(AMOUNT_INPUTS + MAX_HIDDEN, AMOUNT_INPUTS + MAX_HIDDEN + AMOUNT_OUTPUTS):
        if network[i] == None:
            outputs.append(None)
            continue 
        outputs.append(network[i].value) 

    for i in range(0, AMOUNT_INPUTS + MAX_HIDDEN + AMOUNT_OUTPUTS):
        if network[i] != None:
            network[i].value = 0

    return outputs

# testGenome = Genome(AMOUNT_INPUTS, AMOUNT_OUTPUTS, MAX_HIDDEN)
# # testGenome.print_genes()
# # testGenome.mutate()
# # testGenome.print_genes()

# for i in range(0, 1):
#     testGenome.mutate()
#     print("--------------------")
#     testGenome.print_genes()

# network = generateNetwork(testGenome) 


# for lol in range(0, 10):
#     network[0].value = 0.05 * lol 
#     network[1].value = 0.05 * lol 
#     network[2].value = 0.05 * lol

#     for i in range(AMOUNT_INPUTS, MAX_HIDDEN + AMOUNT_INPUTS + AMOUNT_OUTPUTS):
#         if network[i] != None:
#             network[i].calc_value(network) 

#     print(network[103].value)