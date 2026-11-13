import pandas as pd

# Cargar solo lo necesario, con tipos que ocupan poca memoria
df = pd.read_csv(
    "processed/ventas_filtradas.csv",
    usecols=["date", "store_nbr", "item_nbr"],
    dtype={"store_nbr": "int16", "item_nbr": "int32"},
    parse_dates=["date"],
)

# Solo el año 2016
df = df[df["date"].dt.year == 2016].copy()
df["mes"] = df["date"].dt.month

for tienda in [3, 44]:
    sub = df[df["store_nbr"] == tienda]

    # Cuántos meses se vendió cada producto
    meses_por_producto = sub.groupby("item_nbr")["mes"].nunique()

    print(f"\nTienda {tienda}: productos según cantidad de meses con ventas")
    print(meses_por_producto.value_counts().sort_index())

    # Combinación de meses más común entre los productos
    combinaciones = sub.groupby("item_nbr")["mes"].apply(
        lambda m: ",".join(str(x) for x in sorted(m.unique()))
    )
    print(f"\nTienda {tienda}: combinaciones de meses más comunes")
    print(combinaciones.value_counts().head(3))