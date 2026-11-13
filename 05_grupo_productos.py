import pandas as pd


grupo = pd.read_csv("productos_grupo.csv", header=None, names=["item_nbr"])

# Información de los productos
items = pd.read_csv("data/items.csv")

# Quedarnos solo con los productos del grupo
del_grupo = items[items["item_nbr"].isin(grupo["item_nbr"])]

print("Productos del grupo encontrados:", len(del_grupo))

print("\nProductos por familia (dentro del grupo):")
print(del_grupo["family"].value_counts())

print("\nPerecederos dentro del grupo (1 = sí, 0 = no):")
print(del_grupo["perishable"].value_counts())

# Para comparar, la misma distribución en todo el catálogo
print("\nProductos por familia (catálogo completo):")
print(items["family"].value_counts())