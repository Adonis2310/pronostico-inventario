import os
import numpy as np
import pandas as pd

os.makedirs("dashboard", exist_ok=True)

# Carga con tipos que ocupan poca memoria
df = pd.read_csv(
    "processed/ventas_filtradas.csv",
    usecols=["date", "store_nbr", "item_nbr", "unit_sales"],
    dtype={"store_nbr": "int16", "item_nbr": "int32", "unit_sales": "float32"},
    parse_dates=["date"],
)
df["anio"] = df["date"].dt.year.astype("int16")
df["mes"] = df["date"].dt.month.astype("int8")

items = pd.read_csv("data/items.csv")

# 1. Ventas mensuales por tienda
ventas_mensuales = (
    df.groupby(["store_nbr", "anio", "mes"])
    .agg(ventas=("unit_sales", "sum"),
         productos=("item_nbr", "nunique"),
         dias=("date", "nunique"))
    .reset_index()
)
ventas_mensuales["ventas"] = ventas_mensuales["ventas"].round(2)
ventas_mensuales.to_csv("dashboard/ventas_mensuales.csv", index=False)

# 2. Ventas por tienda, producto y mes
ventas_producto_mes = (
    df.groupby(["store_nbr", "item_nbr", "anio", "mes"])
    .agg(ventas=("unit_sales", "sum"))
    .reset_index()
)
ventas_producto_mes["ventas"] = ventas_producto_mes["ventas"].round(2)

# 3. Clasificación por tienda y producto
fechas = df.groupby(["store_nbr", "item_nbr"])["date"].agg(["min", "max"]).reset_index()
meses_activos = (
    ventas_producto_mes.groupby(["store_nbr", "item_nbr"])
    .size().rename("meses_activos").reset_index()
)
productos = fechas.merge(meses_activos, on=["store_nbr", "item_nbr"])
productos["meses_en_periodo"] = (
    (productos["max"].dt.year - productos["min"].dt.year) * 12
    + (productos["max"].dt.month - productos["min"].dt.month) + 1
)
productos["cobertura"] = (productos["meses_activos"] / productos["meses_en_periodo"]).round(3)

# Meses con ventas por año, expresados como proporción del año
anios = [2013, 2014, 2015, 2016]
meses_por_anio = (
    ventas_producto_mes.groupby(["store_nbr", "item_nbr", "anio"])
    .size().unstack(fill_value=0)[anios] / 12
)

# Solo cuentan los años completos posteriores al año de primera venta
prod_idx = productos.set_index(["store_nbr", "item_nbr"])
primer_anio = prod_idx["min"].dt.year.reindex(meses_por_anio.index)
mascara = np.array(anios)[None, :] > primer_anio.to_numpy()[:, None]
cobertura_min = meses_por_anio.where(mascara).min(axis=1, skipna=True)
cobertura_min = cobertura_min.rename("cobertura_anual_minima").reset_index()

productos = productos.merge(cobertura_min, on=["store_nbr", "item_nbr"], how="left")

productos["tipo"] = np.select(
    [productos["max"] < "2017-06-01",
     productos["cobertura_anual_minima"].isna(),
     productos["cobertura_anual_minima"] >= 0.6],
    ["Descontinuado", "Nuevo", "Estable"],
    default="Intermitente",
)

productos = productos.merge(items[["item_nbr", "family", "perishable"]], on="item_nbr", how="left")
productos = productos.rename(columns={
    "min": "primera_venta", "max": "ultima_venta",
    "family": "familia", "perishable": "perecedero",
})
productos.to_csv("dashboard/productos.csv", index=False)

# 4. Agregar familia y tipo a las ventas por tienda y producto
ventas_producto_mes = ventas_producto_mes.merge(
    productos[["store_nbr", "item_nbr", "familia", "perecedero", "tipo"]],
    on=["store_nbr", "item_nbr"], how="left",
)
ventas_producto_mes.to_csv("dashboard/ventas_producto_mes.csv", index=False)

print("Tipos de producto (total):")
print(productos["tipo"].value_counts())
print("\nTipos de producto por tienda:")
print(pd.crosstab(productos["store_nbr"], productos["tipo"]))
print("\nArchivos listos en la carpeta dashboard/")