import matplotlib.pyplot as plt
import pandas as pd

if __name__=="__main__":
    df = pd.read_csv("exp5.csv")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    group_cols = [c for c in df.columns if c not in ['seed', 'gap']]
    df_group = df.groupby(group_cols, as_index=False)['gap'].mean()

    for m_value in sorted(df_group["m"].unique()):
        df_m = df_group[df_group["m"] == m_value]

        plt.figure()
        
        for beta_value in sorted(df_m["beta"].unique()):
            df_beta = df_m[df_m["beta"] == beta_value]

            for d_value in sorted(df_beta["d"].unique()):
                df_d = df_beta[df_beta["d"] == d_value]
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
            plt.title(f"m = {m_value} k = {beta_value+1}")
            plt.legend()
            plt.tight_layout()
            plt.savefig(f"./exp5/m{m_value}_beta{beta_value}")
            plt.show()