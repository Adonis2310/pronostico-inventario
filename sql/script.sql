create database inventario
go

USE inventario;

CREATE TABLE ventas (
    id BIGINT PRIMARY KEY,
    fecha DATE NOT NULL,
    store_nbr SMALLINT NOT NULL,
    item_nbr INT NOT NULL,
    unit_sales FLOAT NOT NULL
);

SELECT COUNT(*) AS filas,
       MIN(fecha) AS desde,
       MAX(fecha) AS hasta
FROM ventas;

SELECT YEAR(fecha) AS anio,
       MONTH(fecha) AS mes,
       SUM(unit_sales) AS ventas_totales
FROM ventas
WHERE store_nbr = 3
GROUP BY YEAR(fecha), MONTH(fecha)
ORDER BY anio, mes;

SELECT YEAR(fecha) AS anio,
       MONTH(fecha) AS mes,
       COUNT(DISTINCT fecha) AS dias_con_ventas,
       ROUND(SUM(unit_sales), 2) AS ventas_totales
FROM ventas
WHERE store_nbr = 3
  AND YEAR(fecha) = 2014
GROUP BY YEAR(fecha), MONTH(fecha)
ORDER BY anio, mes;


SELECT YEAR(fecha) AS anio,
       MONTH(fecha) AS mes,
       COUNT(DISTINCT item_nbr) AS productos_distintos,
       COUNT(*) AS filas,
       ROUND(AVG(unit_sales), 2) AS promedio_por_fila
FROM ventas
WHERE store_nbr = 3
  AND YEAR(fecha) = 2014
GROUP BY YEAR(fecha), MONTH(fecha)
ORDER BY anio, mes;


WITH meses_por_producto AS (
    SELECT item_nbr,
           COUNT(DISTINCT MONTH(fecha)) AS meses_con_ventas
    FROM ventas
    WHERE store_nbr = 3
      AND YEAR(fecha) = 2014
    GROUP BY item_nbr
)
SELECT meses_con_ventas,
       COUNT(*) AS productos
FROM meses_por_producto
GROUP BY meses_con_ventas
ORDER BY meses_con_ventas;

WITH meses AS (
    SELECT DISTINCT item_nbr, MONTH(fecha) AS mes
    FROM ventas
    WHERE store_nbr = 3
      AND YEAR(fecha) = 2014
),
lista_por_producto AS (
    SELECT item_nbr,
           STRING_AGG(CAST(mes AS VARCHAR(2)), ',') WITHIN GROUP (ORDER BY mes) AS meses_con_ventas
    FROM meses
    GROUP BY item_nbr
)
SELECT meses_con_ventas,
       COUNT(*) AS productos
FROM lista_por_producto
GROUP BY meses_con_ventas
ORDER BY productos DESC;

WITH meses AS (
    SELECT DISTINCT item_nbr, MONTH(fecha) AS mes
    FROM ventas
    WHERE store_nbr = 3
      AND YEAR(fecha) = 2014
),
lista AS (
    SELECT item_nbr,
           STRING_AGG(CAST(mes AS VARCHAR(2)), ',') WITHIN GROUP (ORDER BY mes) AS meses_con_ventas
    FROM meses
    GROUP BY item_nbr
)
SELECT item_nbr
FROM lista
WHERE meses_con_ventas = '1,3,7,9,10,11,12'
ORDER BY item_nbr;