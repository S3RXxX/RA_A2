from multiprocessing import Pool
from bins import Bins
import pandas as pd

def worker(args):
    m, n, beta, d, b_batch, seed = args
    bins = Bins(m=m, seed=seed)
    bins.simulate(d=d, n=n, beta=beta, b_size=b_batch)
    return args, bins.gap()

seeds = [42, 67, 77, 69, 13, 28430, 44015, 42699, 57975, 32146]
T = len(seeds)

if __name__=="__main__":
    # n should go from low to n/m to n=m**2
    # 
    tasks = []

    ####################################
    ####### Batch experiment ###########
    ####################################
    # consider: b = m, b = 2m, . . . , b = 10m, . . . , b = 70m, . . . 
    # (and hence n = b, n = 2b, n = 3b, . . . ,n = m**2 = λ · b, with λ = m2/b).

    betas = [x/100 for x in range(0, 101, 25)]
    ds = [2]
    
    ms = [30]
    for m in ms:
        ns = [m//4,m//2] + [x for x in range(m, m*m + 1, max(m//2,1))]
        for n in ns:
            b_batches = [x for x in range(1, n + 1, m)]
            for beta in betas:
                for d in ds:
                    for b_batch in b_batches:
                        for seed in seeds:
                            tasks.append((m, n, beta, d, b_batch, seed))

    with Pool() as p:
        results = p.map(worker, tasks)

    args_list, gaps_list = zip(*results)
    # Convertir args en un DataFrame
    df_args = pd.DataFrame(args_list, columns=["m", "n", "beta", "d", "b_batch", "seed"])

    # Añadir los gaps
    df_args["gap"] = gaps_list

    df = df_args
    df.to_csv("exp3.csv")