import matplotlib.pyplot as plt
import pandas as pd
import os
import math

if __name__=="__main__":
    df = pd.read_csv("exp2.csv")

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    group_cols = [c for c in df.columns if c not in ['seed', 'gap']]
    df_group = df.groupby(group_cols, as_index=False)['gap'].mean()
    for d_value in sorted(df_group["d"].unique()):
        folder_path = f"./exp2/d_value{d_value}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        df_d = df_group[df_group["d"] == d_value]
        for m_value in sorted(df_d["m"].unique()):
            df_m = df_d[df_d["m"] == m_value]
            plt.figure()
            
            for beta_value in sorted(df_m["beta"].unique()):
                df_beta = df_m[df_m["beta"] == beta_value]

                plt.plot(
                    df_beta["n"],
                    df_beta["gap"],
                    label=f"beta = {beta_value}"
                )

            plt.axvline(
            x=m_value,
            linestyle="--",
            linewidth=1.5,
            label="light-load"
        )

            plt.xlabel("n")
            plt.ylabel("gap")
            plt.title(f"m = {m_value} for d = {d_value}")
            plt.legend()
            plt.tight_layout()
            plt.savefig(f"./exp2/d_value{d_value}/m{m_value}_{d_value}")
            plt.show()