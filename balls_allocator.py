# import scipy
import numpy as np

class Bins:
    def __init__(self, m=2):
        assert m>=1
        self.m = m
        self.array = [0 for _ in range(self.m)]
        self.__n_acum = 0
        self.n = None
        self.beta = None
    
    def simulate_random_1(self):
        pos = np.random.randint(0, self.m)
        self.array[pos] +=1

    def simulate_random_2(self):
        pos1 = np.random.randint(0, self.m)
        pos2 = np.random.randint(0, self.m)
        if self.array[pos1] < self.array[pos2]:
            self.array[pos1] += 1
        else:
            ### as we draw pos1 and pos2 randomly do we need to make another random in case of tie or is this enough?
            self.array[pos2] += 1

    def simulate_random_beta(self):
        b = (np.random.random() < self.beta)
        if b:
            self.simulate_random_2()
        else:
            self.simulate_random_1()

    def simulate_n_random_1(self):
        for _ in range(self.n):
            self.simulate_random_1()

    def simulate_n_random_2(self):
        for _ in range(self.n):
            self.simulate_random_2()

    def simulate_n_random_beta(self):
        for _ in range(self.n):
            self.simulate_random_beta()
            

    def simulate(self, method="one-choice", n=10, beta=0.05):
        assert beta<=1
        assert beta>=0

        self.n = n
        self.beta = beta
        if method == "one-choice":
            self.simulate_n_random_1()
        elif method == "two-choice":
            self.simulate_n_random_2()
        elif method == "beta-choice":
            self.simulate_n_random_beta()
        else:
            print("kheeeeeeeeeee")
            # raise Exception
        self.__n_acum += n

    
    def maximum_load(self):
        return max(self.array)
    
    def gap(self):
        return self.maximum_load - (self.__n_acum/self.m)
    
    def gap_new(self):
        return self.maximum_load - (self.n/self.m)
    
    def reset(self, new_m=None):
        if new_m:
            self.m = new_m
        self.array = [0 for _ in range(self.m)]
        self.__n_acum = 0
        self.n = None
        self.beta = None
    

if __name__ == "__main__":

    ### TODO: do it with numpy

    bins = Bins(m=15)
    bins.simulate(method="beta-choice", n=10000, beta=0.5)
    print(bins.array)
    print(bins.maximum_load())
