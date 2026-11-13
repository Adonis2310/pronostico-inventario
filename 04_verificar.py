import pandas as pd

# Cargar solo las columnas necesarias, con tipos que ocupan menos memoria
df = pd.read_csv(
    "processed/ventas_filtradas.csv",
    usecols=["date", "store_nbr", "item_nbr", "unit_sales"],
    dtype={"store_nbr": "int16", "item_nbr": "int32", "unit_sales": "float32"},
    parse_dates=["date"],
)

print("Filas:", len(df))
print("Tiendas:", sorted(df["store_nbr"].unique()))
print("Fecha mínima:", df["date"].min())
print("Fecha máxima:", df["date"].max())