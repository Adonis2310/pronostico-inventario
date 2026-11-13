import pandas as pd
from sqlalchemy import create_engine

# Conexión a la base inventario con autenticación de Windows
engine = create_engine(
    "mssql+pyodbc://@PC_ADONIS\\SQLEXPRESS/inventario"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&trusted_connection=yes&TrustServerCertificate=yes",
    fast_executemany=True,
)

# Primera prueba: solo la tienda 3. Después puedes agregar más tiendas.
tiendas_a_cargar = [3]

total = 0
lector = pd.read_csv(
    "processed/ventas_filtradas.csv",
    usecols=["id", "date", "store_nbr", "item_nbr", "unit_sales"],
    parse_dates=["date"],
    chunksize=500_000,
)

for parte in lector:
    parte = parte.rename(columns={"date": "fecha"})
    parte = parte[parte["store_nbr"].isin(tiendas_a_cargar)]
    parte.to_sql("ventas", engine, if_exists="append", index=False)
    total += len(parte)

print("Filas cargadas:", total)