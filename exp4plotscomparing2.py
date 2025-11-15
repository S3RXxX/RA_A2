import matplotlib.pyplot as plt
import pandas as pd

if __name__=="__main__":
    df = pd.read_csv("exp4.csv")
    df2 = pd.read_csv("exp2.csv")

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df2 = df2.loc[:, ~df2.columns.str.contains('^Unnamed')]

    group_cols = [c for c in df.columns if c not in ['seed', 'gap']]
    df_group = df.groupby(group_cols, as_index=False)['gap'].mean()
    df2_group = df2.groupby(group_cols, as_index=False)['gap'].mean()

    m_value = 100
    d_value = 2

    df_d = df2_group[df2_group["d"] == d_value]
    df_db = df_d[df_d["beta"]==1]
    df_m = df_group[df_group["m"] == m_value]
    plt.figure()  # one separate plot

    for beta_value in sorted(df_m["beta"].unique()):
        df_beta = df_m[df_m["beta"] == beta_value]
        plt.plot(
            df_beta["n"],
            df_beta["gap"],
            label=f"Uncertainty k = {beta_value+1}",
            )
    plt.plot(
        df_db["n"],
        df_db["gap"],
        label=f"Standard with d=2 beta=1"
        )

    plt.axvline(
    x=m_value,
    linestyle="--",
    linewidth=1.5,
    label="light-load"
)

    plt.xlabel("n")
    plt.ylabel("gap")
    plt.title(f"m = {m_value}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"./exp4/m{m_value}_comparingexp2exp4")
    plt.show()