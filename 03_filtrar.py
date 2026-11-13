import pandas as pd
import os

# Tiendas elegidas para el proyecto
tiendas = [3, 44, 47, 45, 8]

# Crear la carpeta de salida si no existe
os.makedirs("processed", exist_ok=True)
ruta_salida = "processed/ventas_filtradas.csv"

primera_parte = True

# Leer train.csv por partes de 1,000,000 filas
for parte in pd.read_csv("data/train.csv", chunksize=1_000_000):
    # Quedarnos solo con las tiendas elegidas
    filtrada = parte[parte["store_nbr"].isin(tiendas)]

    # Guardar: la primera vez con encabezado, las demás sin él
    filtrada.to_csv(
        ruta_salida,
        mode="w" if primera_parte else "a",
        header=primera_parte,
        index=False,
    )
    primera_parte = False

print("Listo. Archivo guardado en", ruta_salida)