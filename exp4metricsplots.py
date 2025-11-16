import matplotlib.pyplot as plt
import pandas as pd
import os

if __name__=="__main__":
    folders = ["exp1","exp2","exp3","exp4","exp5"]
    for folder in folders:
        folder_path = f"./{folder}/metrics"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    df = pd.read_csv("exp4.csv")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    group_cols = [c for c in df.columns if c not in ['seed', 'gap']]
    df_group = df.groupby(group_cols, as_index=False)['gap'].std()

    for m_value in sorted(df_group["m"].unique()):
        df_m = df_group[df_group["m"] == m_value]

        plt.figure()
        for beta_value in sorted(df_m["beta"].unique()):
            df_beta = df_m[df_m["beta"] == beta_value]

            plt.plot(
                df_beta["n"],
                df_beta["gap"],
                label=f"k = {beta_value+1}"
            )

        plt.axvline(
        x=m_value,
        linestyle="--",
        linewidth=1.5,
        label="light-load"
    )

        plt.xlabel("n")
        plt.ylabel("std gap")
        plt.title(f"m = {m_value}")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"./exp4/metrics/m{m_value}")
        plt.close()