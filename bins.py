# import scipy
import numpy as np
import time

class Bins:
    def __init__(self, m=2, seed=42):
        assert m>=1
        self.m = m
        self.array = np.zeros(self.m, dtype=int)
        # self.__aux_array = np.zeros(self.m, dtype=int)  # auxiliary array for batch purposes
        self.__n_acum = 0
        self.n = None
        self.d = None
        self.beta = None
        self.b_size=None
        # self.k = None
        self.__seed=seed
        self.rng = np.random.default_rng(seed)
        

    def choose_d(self, d=1):
        return self.rng.integers(0, self.m, d)
    
    def mask(self, idxs):
        """make a numpy array of False for positions in idxs and True for the rest"""
        mask = np.ones(self.m, dtype=bool)
        mask[idxs] = False
        return mask
    
    def argmin(self, mask):
        """argmin of a numpy array after applying a mask"""
        masked_values = np.where(mask, np.inf, self.array)
        # masked_array = np.ma.array(self.array, mask=~mask)
        return np.argmin(masked_values)
    

    def simulate_random(self):
        """simulate a batch of size self.b_size (single ball for ==1)"""
        aux_array=np.zeros(self.m, dtype=int)
        for _ in range(self.b_size):
            b = (self.rng.random() < self.beta)
            d_choice = self.d if b else 1
            idxs = self.choose_d(d=d_choice)
            mask = self.mask(idxs=idxs)
            minimum_idx = self.argmin(mask=mask) #If tie, we choose the first
            aux_array[minimum_idx] += 1
        return aux_array
        

    def simulate_n_random(self):
        """
        simulate all n balls by batches
        if n//b is not integer, then last batch is smaller
        """
        full_batch_iterations = self.n//self.b_size
        lose_balls = self.n%self.b_size
        for _ in range(full_batch_iterations):
            self.array+=self.simulate_random()

        if lose_balls:
            b_size=self.b_size
            self.b_size=lose_balls
            self.array+=self.simulate_random()
            self.b_size=b_size
            

    def simulate(self, d=1, n=10, beta=0.05, b_size=1):
        assert beta<=1
        assert beta>=0
        assert d>=1
        assert n>=1
        assert b_size>=1

        self.d = d
        self.n = n
        self.beta = beta
        self.b_size = b_size
        self.simulate_n_random()
        self.__n_acum += n

    def le_value(self, idxs, value):
        # idxs_below_value = []
        # for idx in idxs:
        #     if self.array[idx] < value:
        #         idxs_below_value.append(idx)

        mask = self.mask(idxs=idxs)
        masked_values = np.where(mask, np.inf, self.array)
        mask_below_value = masked_values <= value
        idxs_below_value_np = np.where(mask_below_value)[0]
        # print(sorted(list(set(idxs_below_value))))
        # print(idxs_below_value_np)
        # print(sorted(list(set(idxs_below_value)))==idxs_below_value_np)
        # print()
        # assert all(sorted(list(set(idxs_below_value)))==idxs_below_value_np)

        return idxs_below_value_np

    def simulate_random_uncertainty(self):
        """simulate a batch of size self.b_size with uncertainty queries (single ball for ==1)"""
        aux_array=np.zeros(self.m, dtype=int)
        m = np.median(self.array)
        q25 = np.percentile(self.array, 25)  # better outside if big batch sizes
        q75 = np.percentile(self.array, 75)

        for _ in range(self.b_size):
            b = (self.rng.random() < self.beta)  # use for k = 2 if b else 1
            idxs = self.choose_d(d=self.d)
            idxs_below_median = self.le_value(idxs=idxs, value=m)
            num_below_median = len(idxs_below_median)

            if num_below_median==1:
                minimum_idx = idxs_below_median[0]
            elif num_below_median>1:
                if b:
                    
                    idxs_below_q25 = self.le_value(idxs=idxs_below_median, value=q25)
                    if len(idxs_below_q25)==0:
                        minimum_idx = self.rng.choice(idxs_below_median)
                    else:
                        minimum_idx = self.rng.choice(idxs_below_q25)
                else:
                    minimum_idx = self.rng.choice(idxs_below_median)
            elif num_below_median==0:
                if b: 
                    
                    idxs_below_q75 = self.le_value(idxs=idxs, value=q75)
                    if len(idxs_below_q75)==0:
                        minimum_idx = self.rng.choice(idxs)
                    else:
                        minimum_idx = self.rng.choice(idxs_below_q75)
                else:
                    minimum_idx = self.rng.choice(idxs)
            
            aux_array[minimum_idx] += 1
        return aux_array


    def simulate_n_random_uncertainty(self):
        """
        simulate all n balls by batches with uncertainty
        if n//b is not integer, then last batch is smaller
        """
        full_batch_iterations = self.n//self.b_size
        lose_balls = self.n%self.b_size
        for _ in range(full_batch_iterations):
            self.array+=self.simulate_random_uncertainty()

        if lose_balls:
            b_size=self.b_size
            self.b_size=lose_balls
            self.array+=self.simulate_random_uncertainty()
            self.b_size=b_size

    def simulate_uncertainty(self, d=1, n=10, beta=0.05, b_size=1):
        assert beta<=1
        assert beta>=0
        assert d>=1
        assert n>=1
        assert b_size>=1
        # assert (k==1 or k==2)

        self.d = d
        # self.k = k  # with beta we do not need k
        self.n = n
        self.b_size = b_size
        self.beta=beta
        self.simulate_n_random_uncertainty()
        self.__n_acum += n

    
    def maximum_load(self):
        return np.max(self.array)
    
    def gap(self):
        return self.maximum_load() - (self.__n_acum/self.m)
    
    def gap_new(self):
        return self.maximum_load() - (self.n/self.m)
    
    def reset(self, new_m=None, seed=None):
        if new_m:
            self.m = new_m
        if seed:
            self.__seed=seed
            self.rng = np.random.default_rng(seed)
        self.array = np.zeros(self.m, dtype=int)
        # self.__aux_array = np.zeros(self.m, dtype=int)
        self.__n_acum = 0
        self.n = None
        self.d = None
        self.beta = None
        self.b_size=None
        # self.k = None

    # def __call__(self, *args, **kwargs):
    #     """Allow instance to be called directly to run simulate()"""
    #     return self.simulate(*args, **kwargs)

    def __repr__(self):
        return f"Bins(m={self.m}, n_acum={self.__n_acum}, d={self.d}, beta={self.beta}, b_size={self.b_size}, seed={self.__seed})"
    
    def __str__(self):
        return f"{self.array}"
    

def time_it(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    return result, end - start

if __name__ == "__main__":

    # This file is meant to be imported and used
    # the following lines of code are for testing purposes

    seed = 42
    bins = Bins(m=1000, seed=seed)

    # --- Standard simulate() tests ---
    ( _, t ) = time_it(bins.simulate, d=1, n=10000, beta=0.0)
    print("time:", t, repr(bins), bins.maximum_load(), bins.gap())
    bins.reset(seed=seed)

    ( _, t ) = time_it(bins.simulate, d=2, n=10000, beta=1.0)
    print("time:", t, repr(bins), bins.maximum_load(), bins.gap())
    bins.reset(seed=seed)

    ( _, t ) = time_it(bins.simulate, d=2, n=10000, beta=0.5)
    print("time:", t, repr(bins), bins.maximum_load(), bins.gap())
    bins.reset(seed=seed)

    ( _, t ) = time_it(bins.simulate, d=10, n=10000, beta=0.5)
    print("time:", t, repr(bins), bins.maximum_load(), bins.gap())
    bins.reset(seed=seed)

    ( _, t ) = time_it(bins.simulate, d=10, n=10000, beta=1.0)
    print("time:", t, repr(bins), bins.maximum_load(), bins.gap())
    bins.reset(seed=seed)

    ( _, t ) = time_it(bins.simulate, d=1, n=10000, beta=0.0, b_size=1000)
    print("time:", t, repr(bins), bins.maximum_load(), bins.gap())
    bins.reset(seed=seed)

    ( _, t ) = time_it(bins.simulate, d=2, n=10000, beta=0.5, b_size=70)
    print("time:", t, repr(bins), bins.maximum_load(), bins.gap())
    bins.reset(seed=seed)

    ( _, t ) = time_it(bins.simulate, d=2, n=100000, beta=0.5, b_size=70)
    print("time:", t, repr(bins), bins.maximum_load(), bins.gap())
    bins.reset(seed=seed)


    # --- Uncertainty tests ---
    ( _, t ) = time_it(bins.simulate_uncertainty, d=2, n=10000, beta=0, b_size=1)
    print("time:", t, repr(bins), bins.maximum_load(), bins.gap())
    bins.reset(seed=seed)

    ( _, t ) = time_it(bins.simulate_uncertainty, d=2, n=10000, beta=1, b_size=1)
    print("time:", t, repr(bins), bins.maximum_load(), bins.gap())
    bins.reset(seed=seed)

    ( _, t ) = time_it(bins.simulate_uncertainty, d=1000, n=10000, beta=0, b_size=1)
    print("time:", t, repr(bins), bins.maximum_load(), bins.gap())
    bins.reset(seed=seed)

    ( _, t ) = time_it(bins.simulate_uncertainty, d=1000, n=10000, beta=0.6, b_size=1)
    print("time:", t, repr(bins), bins.maximum_load(), bins.gap())
    bins.reset(seed=seed)

    ( _, t ) = time_it(bins.simulate_uncertainty, d=1000, n=10000, beta=1, b_size=1)
    print("time:", t, repr(bins), bins.maximum_load(), bins.gap())
    bins.reset(seed=seed)

    ( _, t ) = time_it(bins.simulate_uncertainty, d=6, n=10000, beta=0, b_size=1)
    print("time:", t, repr(bins), bins.maximum_load(), bins.gap())
    bins.reset(seed=seed)

    
    
    # print(bins)
    # print(bins.maximum_load(), bins.gap())
    # print(np.sum(bins.array))

