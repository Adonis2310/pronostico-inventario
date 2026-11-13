import pandas as pd

# Leer la misma muestra de 1,000,000 filas
df = pd.read_csv("data/train.csv", nrows=1_000_000)

# 1. Convertir la columna date de texto a fecha
df["date"] = pd.to_datetime(df["date"])

# 2. Cantidad de tiendas y productos distintos
print("Tiendas distintas:", df["store_nbr"].nunique())
print("Productos distintos:", df["item_nbr"].nunique())

# 3. Valores nulos por columna
print("\nValores nulos por columna:")
print(df.isna().sum())

# 4. Filas por tienda
print("\nFilas por tienda:")
print(df["store_nbr"].value_counts())