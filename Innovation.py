class Innovation:

    def __init__(self, start = 1):
        self.value = start


    def new_innovation(self):
        temp = self.value 

        self.value += 1
        return temp