import numpy as np 

class Neuron:


    def __init__(self, incoming=None):
        self.incoming = incoming
        self.outgoing = []
        self.value = 0


    def calc_value(self, neuron_list):
        value = 0

        for connection in self.incoming:
            # Bias neuron
            if connection.neuron_id < 0:
                value += connection.weight
            else: 
                # Note: connection.neuron_id might not exist if for example the genes are:
                # 0 -> 5 and 5 -> 103 and the 0 -> 5 gene is disabled while the 5 -> 103 gene is enabled
                try:
                    value +=  neuron_list[connection.neuron_id].value * connection.weight
                except:
                    pass
        self.value = self.activation_function(value)


    def activation_function(self, value):
        # Sigmoid 
        return 1/(1 + np.exp(-value))



    