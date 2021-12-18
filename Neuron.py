import numpy as np 

class Neuron:


    def __init__(self, incoming=None):
        self.incoming = incoming
        self.outgoing = []


    def calc_value(self, neuron_list):
        value = 0

        for connection in incoming:
            value +=  neuron_list[connection.neuron_id].value * connection.weight

        self.value = self.activation_function(value)


    def activation_function(self, value):
        # Sigmoid 
        return 1/(1 + np.exp(-value))



    