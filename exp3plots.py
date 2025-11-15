import matplotlib.pyplot as plt
import pandas as pd
import os

if __name__=="__main__":
    df = pd.read_csv("exp3.csv")

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    group_cols = [c for c in df.columns if c not in ['seed', 'gap']]
    df_group = df.groupby(group_cols, as_index=False)['gap'].mean()
    for batch_value in sorted(df_group["b_batch"].unique()):
        df_batch = df_group[df_group["b_batch"] == batch_value]
        plt.figure()
        for beta_value in sorted(df_batch["beta"].unique()):
            df_beta = df_batch[df_batch["beta"] == beta_value]
            plt.plot(
                df_beta["n"],
                df_beta["gap"],
                label=f"beta = {beta_value}"
            )

        plt.axvline(
            x=100,
            linestyle="--",
            linewidth=1.5,
            label="light-load"
        )

        plt.xlabel("n")
        plt.ylabel("gap")
        plt.title(f"m = {100} for batch_size = {batch_value}")
        plt.legend()
        plt.tight_layout()

        # Guardamos el gráfico con índice del grupo de batches
        plt.savefig(f"./exp3/m100_batchSize{batch_value}.png")
        plt.close()