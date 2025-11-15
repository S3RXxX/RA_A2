import pandas as pd

csvs = ["exp1.csv","exp2.csv","exp3.csv","exp4.csv","exp5.csv"]
# Cargar CSV
for csv_ in csvs:
    df = pd.read_csv(csv_)

    # Eliminar columnas de índice extra
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Columnas que NO se usan para agrupar
    ignore = ['n', 'seed', 'gap']

    # Columnas para agrupar: todas excepto las de ignore
    group_cols = [c for c in df.columns if c not in ignore]

    # Calcular media, std y var del GAP
    df_stats = df.groupby(group_cols).agg(
        gap_mean=('gap', 'mean'),
        gap_std=('gap', 'std'),
        gap_var=('gap', 'var')
    ).reset_index()

    print(df_stats)
    df_stats.to_csv(csv_[:-4]+"_stats.csv", index=False)