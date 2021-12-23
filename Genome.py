import random 
from Gene import Gene 
from Innovation import Innovation

class Genome:

    mutate_connection_chance = 0.6
    perturb_chance = 0.90
    crossover_chance = 0.75
    link_mutate_chance = 0.15
    node_mutation_chance = 0.05
    bias_mutation_chance = 0.05
    disable_mutation_chance = 0.06
    enable_mutation_chance = 0.05
    step = 0.05


    def __init__(self, amount_inputs, amount_outputs, max_hidden_neurons, innovation):
        self.genes = [] 
        self.current_inovation = 1  
        self.amount_inputs = amount_inputs
        self.amount_outputs = amount_outputs
        self.amount_neurons = amount_inputs
        self.max_hidden_neurons = max_hidden_neurons
        self.innovation = innovation
    

    def new_innovation(self):
        return self.innovation.new_innovation()


    def new_neuron_number(self):
        temp = self.amount_neurons
        self.amount_neurons += 1 
        return temp


    def point_mutate(self):
        for gene in self.genes:

            if random.random() < self.perturb_chance:
                gene.weight = gene.weight + random.uniform(-1, 1) * self.step 
            else:
                gene.weight = random.uniform(-1, 1)


    def random_neuron(self, allow_input):
        possibilities = set()

        # Add inputs
        if allow_input:
            for i in range(0, self.amount_inputs):
                possibilities.add(i)

        # Add outputs
        for i in range(self.max_hidden_neurons + self.amount_inputs, self.max_hidden_neurons + self.amount_inputs + self.amount_outputs):
            possibilities.add(i)

        # Add hidden
        for gene in self.genes:
            if allow_input or gene.from_neuron_id > self.amount_inputs - 1:
                possibilities.add(gene.from_neuron_id)
            if allow_input or gene.to_neuron_id > self.amount_inputs - 1:
                possibilities.add(gene.to_neuron_id)

        # Return a random node
        if len(possibilities) >= 1: 
            return random.sample(list(possibilities), 1)[0]

        else:
            return None


    def contains_link(self, from_id, to_id):
        for gene in self.genes:
            if gene.from_neuron_id == from_id and gene.to_neuron_id == to_id:
                return True

        return False



    def link_mutate_bias(self):
        from_neuron = -1
        to_neuron = self.random_neuron(False)

        if to_neuron != None: 
            if not self.contains_link(from_neuron, to_neuron):
                new_gene = Gene(self.new_innovation(), -1, to_neuron, random.uniform(-1, 1))
                self.genes.append(new_gene)


    def is_output_neuron(self, neuron_id):
        if neuron_id >= self.amount_inputs + self.max_hidden_neurons:
            return True
        return False

    def is_input_neuron(self, neuron_id):
        if neuron_id < self.amount_inputs:
            return True 
        
        return False

    # Try to add a new link
    # TODO: add explicit bias node option
    def link_mutate(self):
        from_neuron = self.random_neuron(True) 
        to_neuron = self.random_neuron(False)

        # If both inputs
        if self.is_input_neuron(from_neuron) and self.is_input_neuron(to_neuron):
            return

        # No self loops
        if from_neuron == to_neuron:
            return

        # Swap 
        if self.is_input_neuron(to_neuron): 
            temp = to_neuron 
            from_neuron = to_neuron 
            to_neuron = temp 

        # Output neuron can have no outgoing arrows
        if self.is_output_neuron(from_neuron):
            return

        if not self.contains_link(from_neuron, to_neuron):
            new_gene = Gene(self.new_innovation(), from_neuron, to_neuron, random.uniform(-1, 1))
            self.genes.append(new_gene)

    # Add a new node (inbetween an existing link)
    def node_mutate(self):
        
        # If no genes can't do anything
        if len(self.genes) <= 0: 
            return 

        
        random_gene = random.sample(self.genes, 1)[0]

        if not random_gene.enabled:
            return 

        random_gene.enabled = False
        new_neuron_num = self.new_neuron_number()

        first_new_gene = Gene(self.new_innovation(), random_gene.from_neuron_id, new_neuron_num)
        second_new_gene = Gene(self.new_innovation(), new_neuron_num, random_gene.to_neuron_id, random_gene.weight)


        self.genes.append(first_new_gene)
        self.genes.append(second_new_gene)


    def enable_disable_mutate(self, mutate_to):
        genes_to_mutate = []

        for i in range(0, len(self.genes)):
            if self.genes[i].enabled != mutate_to:
                genes_to_mutate.append(i)

        if len(genes_to_mutate) < 1:
            return 

        random_gene = random.sample(genes_to_mutate, 1)[0]
        self.genes[random_gene].enabled = mutate_to



    def mutate(self):
        if random.random() < self.mutate_connection_chance:
            self.point_mutate()

        if random.random() < self.link_mutate_chance:
            self.link_mutate()

        if random.random() < self.node_mutation_chance:
            self.node_mutate()   

        if random.random() < self.bias_mutation_chance:
            self.link_mutate_bias()

        if random.random() < self.disable_mutation_chance:
            self.enable_disable_mutate(False)

        if random.random() < self.enable_mutation_chance:
            self.enable_disable_mutate(True)


        # # Temp: 
        # new_genes = []
        # for gene in self.genes:
        #     if gene.enabled:
        #         new_genes.append(gene) 
        #     else: 
        #         self.amount_neurons -= 1
        #         if self.amount_neurons < 0:
        #             self.amount_neurons = 0

        # self.genes = new_genes

    def print_genes(self):
        print("Amount genes: " + str(len(self.genes)))
        for gene in self.genes:
            gene.print()

    
    def deepcopy(self):
        new_gene_list = []

        for gene in self.genes:
            new_gene_list.append(gene.deepcopy())

        new_genome = Genome(self.amount_inputs, self.amount_outputs, self.max_hidden_neurons, self.innovation)
        new_genome.genes = new_gene_list 
        new_genome.current_inovation = self.current_inovation
        new_genome.amount_neurons = self.amount_neurons


        return new_genome


    def get_gene_with_innovation_number(self, innovation_number):
        for gene in self.genes:
            if gene.innovation_number == innovation_number:
                return gene 

        return None