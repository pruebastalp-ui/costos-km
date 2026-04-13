# Costos MVP MySQL - Versión 2

Esta versión amplía la MVP original y agrega una carga más completa de parámetros, especialmente en el módulo **Empresa**.

## Cambios principales

- Se incorporan como editables los parámetros de la hoja **2- EMP. REP**:
  - Pasajeros transportados
  - Km anual empresa
  - Parque móvil
  - Recaudación por boletos
  - Km productivo anual por vehículo
  - Km improductivo
  - Vida útil del vehículo en km y años
  - Velocidad comercial
  - Recaudación media por km
  - IPK
  - Antigüedad media del parque
  - Ingreso medio por pasajero
- Se agregan parámetros faltantes de **3- REND Y CONS** y **5-PRECIOS SIN IVA** para mejorar el cálculo.
- Se corrige el esquema para usar `TIMESTAMP`, evitando el error de `invalid default value` en servidores MySQL/MariaDB más viejos.
- El motor recalcula con mayor detalle los rubros:
  - combustible
  - lubricantes
  - neumáticos
  - engrase y lavado
  - reparación y mantenimiento
  - depreciación del material rodante
  - seguro del vehículo
  - patentes y TNFT
  - salarios del personal
  - seguros del personal
  - licencia nacional habilitante
  - control técnico
  - ACTRANS
  - cámaras de seguridad
  - gastos generales
  - gerenciamiento
  - costo total por km
  - tarifa media

## Puesta en marcha

1. Crear la base con `schema.sql`
2. Configurar MySQL en `config.py`
3. Importar el Excel:
   ```bash
   python import_excel.py "GO - Costos Diciembre 2025.xlsx"
   ```
4. Ejecutar la app:
   ```bash
   python app.py
   ```

## Nota

Si ya corriste una versión anterior, para probar limpio conviene:

- vaciar la base `costos_mvp`, o
- borrar tablas y recrearlas con `schema.sql`,
- volver a ejecutar `import_excel.py`

Así se cargan también los nuevos parámetros del módulo **Empresa**.
