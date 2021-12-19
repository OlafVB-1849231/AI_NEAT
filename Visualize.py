import graphviz 
from Genome import Genome



def visualize(genome):
    dot = graphviz.Digraph('round-table', comment='The Round Table', edge_attr={'fontsize': '5'})  


    added_nodes = set()

    for i in range(0, genome.amount_inputs):
        added_nodes.add(i)
        dot.node(str(i), str(i))

    for gene in genome.genes:
        if gene.from_neuron_id not in added_nodes:
            added_nodes.add(gene.from_neuron_id)
            dot.node(str(gene.from_neuron_id), str(gene.from_neuron_id))

        if gene.to_neuron_id not in added_nodes:
            added_nodes.add(gene.to_neuron_id)
            dot.node(str(gene.to_neuron_id), str(gene.to_neuron_id))

        dot.edge(str(gene.from_neuron_id), str(gene.to_neuron_id), label=str("%.5f" % gene.weight))


    #doctest_mark_exe()
    dot.render(directory='doctest-output', view=True) 