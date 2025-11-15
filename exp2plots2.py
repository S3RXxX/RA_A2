import matplotlib.pyplot as plt
import pandas as pd
import os
import math

if __name__=="__main__":
    df = pd.read_csv("exp2.csv")

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    group_cols = [c for c in df.columns if c not in ['seed', 'gap']]
    df_group = df.groupby(group_cols, as_index=False)['gap'].mean()
    for beta_value in sorted(df_group["beta"].unique()):
        df_beta = df_group[df_group["beta"] == beta_value]

        for m_value in sorted(df_beta["m"].unique()):
            df_m = df_beta[df_beta["m"] == m_value]
            plt.figure()
            
            for d_value in sorted(df_m["d"].unique()):
                df_d = df_m[df_m["d"] == d_value]

                plt.plot(
                    df_d["n"],
                    df_d["gap"],
                    label=f"d = {d_value}"
                )

            plt.axvline(
            x=m_value,
            linestyle="--",
            linewidth=1.5,
            label="light-load"
        )

            plt.xlabel("n")
            plt.ylabel("gap")
            plt.title(f"m = {m_value} for beta = {beta_value}")
            plt.legend()
            plt.tight_layout()
            plt.savefig(f"./exp2/d_value{d_value}/m{m_value}_beta{beta_value}.png")
            plt.show()