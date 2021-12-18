class Gene:

    def __init__(self, innovation_number, from_neuron_id, to_neuron_id, weight = 1, enabled = True):
        self.innovation_number = innovation_number
        self.from_neuron_id = from_neuron_id
        self.to_neuron_id = to_neuron_id
        self.weight = weight
        self.enabled = enabled

    def print(self):
        print("Gene: innovation number - from - to - weight - enabled")
        print("            " + str(self.innovation_number) + " - " + str(self.from_neuron_id) + " - " + str(self.to_neuron_id) + " - " + str(self.weight) + " - " + str(self.enabled))
