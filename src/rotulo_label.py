import pandas as pd
from scipy.stats import zscore

df = pd.read_csv("tabela.csv")

# Exemplo de regra: erro se qualquer um desses sinais estiver muito fora da curva
signals = ["rx_errors", "tx_errors", "drops", "collisions", "latency_ms", "queue_occupancy"]
for c in signals:
    if c in df.columns:
        df[f"{c}_z"] = zscore(df[c].fillna(df[c].median()))

# label = 1 se algum |z| > 3, senão 0
z_cols = [c for c in df.columns if c.endswith("_z")]
df["label"] = (df[z_cols].abs().max(axis=1) > 3).astype(int)

# Salva e usa no script
df.drop(columns=z_cols).to_csv("tabela_rotulada.csv", index=False)
