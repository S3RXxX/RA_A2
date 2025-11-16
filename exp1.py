from multiprocessing import Pool
from bins import Bins
import pandas as pd

def worker(args):
    m, n, beta, d, b_batch, seed = args
    bins = Bins(m=m, seed=seed)
    bins.simulate(d=d, n=n, beta=beta, b_size=b_batch)
    return args, bins.gap()

seeds = [42, 67, 77, 69, 13]
T = len(seeds)

if __name__=="__main__":
    ####################################
    ####### Standard experiment ########
    ####################################
    # compare d=1,2 and some betas
    betas = [x/100 for x in range(0, 101, 25)] # b == 0 -> d=1 b== 1 -> d=2
    ds = [2]
    b_batches = [1]
    ms = [2,5,10,30,50,100]
    tasks = []
    for m in ms:
        ns = [max(m//4, 1),max(m//2,1)] + [x for x in range(m, m*m + 1, max(m//2,1))]
        for n in ns:
            for beta in betas:
                for d in ds:
                    for b_batch in b_batches:
                        for seed in seeds:
                            tasks.append((m, n, beta, d, b_batch, seed))

    with Pool() as p:
        results = p.map(worker, tasks)

    args_list, gaps_list = zip(*results)
    df_args = pd.DataFrame(args_list, columns=["m", "n", "beta", "d", "b_batch", "seed"])

    df_args["gap"] = gaps_list

    df = df_args
    df.to_csv("exp1.csv")
        