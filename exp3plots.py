import matplotlib.pyplot as plt
import pandas as pd
import os

if __name__=="__main__":
    df = pd.read_csv("exp3_m100.csv")

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    group_cols = [c for c in df.columns if c not in ['seed', 'gap']]
    df_group = df.groupby(group_cols, as_index=False)['gap'].mean()
    for beta_value in sorted(df_group["beta"].unique()):
        # folder_path = f"./exp3/beta_value{beta_value}"
        # if not os.path.exists(folder_path):
        #     os.makedirs(folder_path)
        df_beta = df_group[df_group["beta"] == beta_value]
        batch_values = sorted(df_beta["b_batch"].unique())

        # Dividimos los batch en grupos de 10
        for i in range(0, len(batch_values), 10):
            batch_subset = batch_values[i:i+10]

            plt.figure()
            for batch in batch_subset:
                df_batch = df_beta[df_beta["b_batch"] == batch]
                plt.plot(
                    df_batch["n"],
                    df_batch["gap"],
                    label=f"batch_value = {batch}"
                )

            plt.axvline(
                x=100,
                linestyle="--",
                linewidth=1.5,
                label="light-load"
            )

            plt.xlabel("n")
            plt.ylabel("gap")
            plt.title(f"m = {100} for beta = {beta_value}, batches {i+1}-{i+len(batch_subset)}")
            plt.legend()
            plt.tight_layout()

            # Guardamos el gráfico con índice del grupo de batches
            plt.savefig(f"./exp3/m100_beta{beta_value}_batches{i}-{i+len(batch_subset)}.png")
            plt.show()

        # for batch in sorted(df_beta["b_batch"].unique()):
        #     df_batch = df_beta[df_beta["b_batch"] == batch]

        #     plt.plot(
        #         df_batch["n"],
        #         df_batch["gap"],
        #         label=f"batch_value = {batch}"
        #     )

        # plt.axvline(
        # x=100,
        # linestyle="--",
        # linewidth=1.5,
        # label="light-load"
        # )

        # plt.xlabel("n")
        # plt.ylabel("gap")
        # plt.title(f"m = {100} for beta = {beta_value}")
        # plt.legend()
        # plt.tight_layout()
        # plt.savefig(f"./exp3/m{100}_{beta_value}.png")
        # plt.show()