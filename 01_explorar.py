import pandas as pd

# Leer solo las primeras 1,000,000 filas para no saturar la memoria
df = pd.read_csv("data/train.csv", nrows=1_000_000)

print("Dimensiones (filas, columnas):", df.shape)
print("\nTipos de datos:")
print(df.dtypes)
print("\nPrimeras filas:")
print(df.head())
print("\nPeriodo de la muestra:", df["date"].min(), "a", df["date"].max())