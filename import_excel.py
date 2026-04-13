import sys
import openpyxl
import mysql.connector
from config import MYSQL_CONFIG

GROUPS = [
    ("DF", "Distrito Federal", "B"),
    ("SGI", "Suburbana Grupo I", "C"),
    ("SGI_KM", "Suburbana Grupo I KM", "D"),
    ("SGII", "Suburbana Grupo II", "E"),
    ("INP", "Interprovincial", "F"),
    ("UPA", "Urbana Provincial", "G"),
    ("UPA_KM", "Urbana Provincial KM", "H"),
    ("UMA_1", "Urbana Municipal 1", "I"),
    ("UMA_2", "Urbana Municipal 2", "J"),
]

PARAMETER_DEFS = [
    # 3- REND Y CONS
    ("combustible", "consumo_combustible", "Consumo de combustible (Lts/Km)", "Lts/Km", "3- REND Y CONS", 4, 1),
    ("lubricantes", "consumo_aceite", "Consumo de aceite (Lts/Km)", "Lts/Km", "3- REND Y CONS", 5, 1),
    ("lubricantes", "consumo_grasa", "Consumo de grasa (Kg/Km)", "Kg/Km", "3- REND Y CONS", 6, 1),
    ("lubricantes", "consumo_aceite_caja", "Consumo de aceite de caja (Lts/Km)", "Lts/Km", "3- REND Y CONS", 7, 1),
    ("neumaticos", "cantidad_cubiertas", "Cantidad de cubiertas", "un", "3- REND Y CONS", 8, 1),
    ("neumaticos", "vida_util_neumaticos", "Vida útil neumáticos (Km)", "Km", "3- REND Y CONS", 11, 1),
    ("neumaticos", "prolongacion_recapado", "Prolongación por recapado (Km)", "Km", "3- REND Y CONS", 12, 1),
    ("neumaticos", "vida_util_total_juego", "Vida útil total del juego de neumáticos (Km)", "Km", "3- REND Y CONS", 13, 1),
    ("neumaticos", "recapados_admisibles", "Recapados admisibles por cubierta", "un", "3- REND Y CONS", 14, 1),
    ("neumaticos", "conserv_neumaticos_pct", "Conservación neumáticos / costo neumáticos (%)", "%", "3- REND Y CONS", 15, 1),
    ("engrase_lavado", "engrases_cada_10000", "Engrases c/10.000 Km", "un", "3- REND Y CONS", 16, 1),
    ("engrase_lavado", "lav_carroceria_cada_10000", "Lavados carrocería c/10.000 Km", "un", "3- REND Y CONS", 17, 1),
    ("engrase_lavado", "lav_motor_cada_10000", "Lavados motor c/10.000 Km", "un", "3- REND Y CONS", 18, 1),
    ("engrase_lavado", "lav_chasis_cada_10000", "Lavados chasis c/10.000 Km", "un", "3- REND Y CONS", 19, 1),
    ("engrase_lavado", "filtros_gasoil_cada_10000", "Filtros de gasoil c/10.000 Km", "un", "3- REND Y CONS", 20, 1),
    ("engrase_lavado", "filtros_aceite_cada_10000", "Filtros de aceite c/10.000 Km", "un", "3- REND Y CONS", 21, 1),
    ("engrase_lavado", "filtros_aire_cada_10000", "Filtros de aire c/10.000 Km", "un", "3- REND Y CONS", 22, 1),
    ("engrase_lavado", "vida_util_service_km", "Vida útil del service (Km)", "Km", "3- REND Y CONS", 23, 1),
    ("empresa", "reparacion_chasis_pct", "Reparación chasis / precio vehículo renovación", "%", "3- REND Y CONS", 24, 1),
    ("empresa", "reparacion_carroceria_pct", "Reparación carrocería / precio carrocería nueva", "%", "3- REND Y CONS", 25, 1),
    ("empresa", "cantidad_controles_tecnicos_anual", "Cantidad anual de controles técnicos", "un", "3- REND Y CONS", 28, 1),

    # 4- PERSONAL
    ("personal", "conductores_x_veh", "Conductores por vehículo", "dot/veh", "4- PERSONAL", 4, 1),
    ("personal", "jefes_trafico_x_veh", "Jefes de tráfico por vehículo", "dot/veh", "4- PERSONAL", 6, 1),
    ("personal", "inspectores_x_veh", "Inspectores por vehículo", "dot/veh", "4- PERSONAL", 7, 1),
    ("personal", "otros_trafico_x_veh", "Otros tráfico por vehículo", "dot/veh", "4- PERSONAL", 8, 1),
    ("personal", "jefes_taller_x_veh", "Jefes de taller por vehículo", "dot/veh", "4- PERSONAL", 11, 1),
    ("personal", "oficiales_mecanicos_x_veh", "Oficiales mecánicos por vehículo", "dot/veh", "4- PERSONAL", 12, 1),
    ("personal", "gomeros_x_veh", "Gomeros por vehículo", "dot/veh", "4- PERSONAL", 13, 1),
    ("personal", "otros_mantenimiento_x_veh", "Otros mantenimiento por vehículo", "dot/veh", "4- PERSONAL", 14, 1),
    ("personal", "gerentes_x_veh", "Gerentes por vehículo", "dot/veh", "4- PERSONAL", 17, 1),
    ("personal", "jefes_admin_x_veh", "Jefes administración por vehículo", "dot/veh", "4- PERSONAL", 18, 1),
    ("personal", "administrativos_x_veh", "Administrativos por vehículo", "dot/veh", "4- PERSONAL", 19, 1),
    ("personal", "recaudadores_x_veh", "Recaudadores por vehículo", "dot/veh", "4- PERSONAL", 20, 1),
    ("personal", "otros_admin_x_veh", "Otros administración por vehículo", "dot/veh", "4- PERSONAL", 21, 1),

    # 5- PRECIOS SIN IVA
    ("combustible", "precio_gasoil_sin_iva", "Precio del gasoil sin IVA ($/Lt)", "$/Lt", "5-PRECIOS SIN IVA", 5, 1),
    ("lubricantes", "precio_aceite", "Precio del aceite ($/Lt)", "$/Lt", "5-PRECIOS SIN IVA", 6, 1),
    ("lubricantes", "precio_grasa", "Precio de la grasa ($/Kg)", "$/Kg", "5-PRECIOS SIN IVA", 7, 1),
    ("neumaticos", "precio_cubierta", "Precio de la cubierta ($)", "$", "5-PRECIOS SIN IVA", 8, 1),
    ("neumaticos", "precio_recapado", "Precio del recapado ($)", "$", "5-PRECIOS SIN IVA", 9, 1),
    ("engrase_lavado", "precio_engrase_general", "Precio engrase general ($)", "$", "5-PRECIOS SIN IVA", 10, 1),
    ("engrase_lavado", "precio_lavado_carroceria", "Precio lavado carrocería ($)", "$", "5-PRECIOS SIN IVA", 11, 1),
    ("engrase_lavado", "precio_lavado_motor", "Precio lavado motor ($)", "$", "5-PRECIOS SIN IVA", 12, 1),
    ("engrase_lavado", "precio_lavado_chasis", "Precio lavado chasis ($)", "$", "5-PRECIOS SIN IVA", 13, 1),
    ("engrase_lavado", "precio_filtro_gasoil", "Precio del filtro de gasoil ($)", "$", "5-PRECIOS SIN IVA", 14, 1),
    ("engrase_lavado", "precio_filtro_aceite", "Precio del filtro de aceite ($)", "$", "5-PRECIOS SIN IVA", 15, 1),
    ("engrase_lavado", "precio_filtro_aire", "Precio del filtro de aire ($)", "$", "5-PRECIOS SIN IVA", 16, 1),
    ("empresa", "precio_chasis", "Precio del chasis ($)", "$", "5-PRECIOS SIN IVA", 17, 1),
    ("empresa", "precio_carroceria", "Precio de la carrocería ($)", "$", "5-PRECIOS SIN IVA", 18, 1),
    ("empresa", "gastos_iniciales_material_rodante_pct", "Gastos iniciales material rodante (%)", "%", "5-PRECIOS SIN IVA", 19, 1),
    ("empresa", "valor_depreciable_chasis", "Valor depreciable del chasis ($)", "$", "5-PRECIOS SIN IVA", 21, 1),
    ("empresa", "valor_depreciable_carroceria", "Valor depreciable de la carrocería ($)", "$", "5-PRECIOS SIN IVA", 22, 1),
    ("empresa", "precio_control_tecnico", "Precio de cada control técnico ($)", "$", "5-PRECIOS SIN IVA", 23, 1),
    ("empresa", "premio_seguro_rc_anual", "Premio seguro responsabilidad civil ($/año)", "$", "5-PRECIOS SIN IVA", 27, 1),
    ("empresa", "costo_anual_franquicia", "Costo anual de franquicia por vehículo ($)", "$", "5-PRECIOS SIN IVA", 29, 1),
    ("empresa", "costo_anual_seguro_chasis", "Costo anual seguro del chasis ($)", "$", "5-PRECIOS SIN IVA", 34, 1),
    ("empresa", "costo_anual_seguro_carroceria", "Costo anual seguro carrocería ($)", "$", "5-PRECIOS SIN IVA", 35, 1),
    ("empresa", "valor_patente_anual", "Valor de la patente ($/año)", "$", "5-PRECIOS SIN IVA", 36, 1),
    ("empresa", "valor_tnft_anual", "Valor TNFT ($/vehículo-año)", "$", "5-PRECIOS SIN IVA", 37, 1),
    ("empresa", "aporte_actrans", "Aporte a ACTRANS ($)", "$", "5-PRECIOS SIN IVA", 38, 1),
    ("empresa", "tasa_interes_capital_invertido_pct", "Tasa de interés sobre el capital invertido (%)", "%", "5-PRECIOS SIN IVA", 39, 1),
    ("empresa", "costo_anual_camaras_seguridad", "Costo anual cámaras de seguridad por vehículo ($)", "$", "5-PRECIOS SIN IVA", 50, 1),
    ("cargos", "gerenciamiento_pct", "Remuneración del gerenciamiento", "%", "5-PRECIOS SIN IVA", 41, 1),
    ("cargos", "gerenciamiento_personal_pct", "Remuneración del gerenciamiento personal", "%", "5-PRECIOS SIN IVA", 42, 1),
    ("cargos", "alicuota_iibb_pct", "Alícuota impuesto a los ingresos brutos (%)", "%", "5-PRECIOS SIN IVA", 47, 1),
    ("cargos", "gasto_general_pct", "Costo gasto general / Km base 1983", "%", "5-PRECIOS SIN IVA", 58, 1),

    # 2- EMP. REP - toda la sección relevante editable
    ("empresa", "pasajeros_transportados", "Pasajeros transportados", "pas", "2- EMP. REP", 4, 1),
    ("empresa", "km_anual_empresa", "Kilometraje anual recorrido por la empresa", "Km", "2- EMP. REP", 5, 1),
    ("empresa", "parque_movil", "Parque móvil empresa tipo", "veh", "2- EMP. REP", 6, 1),
    ("empresa", "recaudacion_venta_boletos", "Recaudación por venta de boletos", "$", "2- EMP. REP", 7, 1),
    ("empresa", "km_productivo_anual_veh", "Recorrido productivo medio anual por vehículo", "Km", "2- EMP. REP", 8, 1),
    ("empresa", "km_improductivo_pct", "Kilometraje improductivo (%)", "%", "2- EMP. REP", 9, 1),
    ("empresa", "vida_util_vehiculo_km", "Vida útil del vehículo (Km)", "Km", "2- EMP. REP", 10, 1),
    ("empresa", "vida_util_vehiculo_anios", "Vida útil del vehículo (años)", "años", "2- EMP. REP", 11, 1),
    ("empresa", "velocidad_comercial", "Velocidad comercial (Km/h)", "Km/h", "2- EMP. REP", 12, 1),
    ("empresa", "recaudacion_media_km", "Recaudación media por Km", "$/Km", "2- EMP. REP", 13, 1),
    ("empresa", "ipk", "IPK", "pas/km", "2- EMP. REP", 14, 1),
    ("empresa", "antiguedad_media_parque", "Antigüedad media del parque", "años", "2- EMP. REP", 15, 1),
    ("empresa", "ingreso_medio_pasajero", "Ingreso medio por pasajero", "$", "2- EMP. REP", 16, 1),
]

RESULT_DEFS = [
    ("combustible", 4, "1. COMBUSTIBLE"),
    ("lubricantes", 5, "2. LUBRICANTES"),
    ("neumaticos", 6, "3. NEUMATICOS"),
    ("engrase_lavado", 7, "4. ENGRASE Y LAVADO"),
    ("reparacion_mantenimiento", 8, "5. REPARACION Y MANTENIMIENTO DEL MATERIAL RODANTE"),
    ("depreciacion_mr", 11, "6. DEPRECIACION DEL MATERIAL RODANTE"),
    ("seguro_vehiculo", 14, "7. SEGURO DEL VEHÍCULO"),
    ("patentes_tnft", 19, "8. PATENTES Y TNFT"),
    ("salarios_personal", 20, "9. SALARIOS DEL PERSONAL"),
    ("seguros_personal", 25, "10. SEGUROS DEL PERSONAL"),
    ("maq_herr_inmuebles", 26, "11. MÁQUINAS, HERRAMIENTAS E INMUEBLES"),
    ("impuestos_tasas_mun", 31, "12. IMPUESTOS Y TASAS MUNICIPALES"),
    ("capital_invertido", 32, "13. COSTO DEL CAPITAL INVERTIDO"),
    ("lnh", 37, "14. LICENCIA NACIONAL HABILITANTE"),
    ("control_tecnico", 38, "15. CONTROL TECNICO DEL MATERIAL RODANTE"),
    ("actrans", 39, "16. A.C.TRANS"),
    ("peajes", 40, "17. PEAJES"),
    ("vigilancia", 41, "18. SERVICIO DE VIGILANCIA"),
    ("camaras_seguridad", 42, "19. CAMARAS DE SEGURIDAD"),
    ("subtotal_sin_gg", 43, "SUBTOTAL SIN GASTOS GENERALES"),
    ("gastos_generales", 44, "20. GASTOS GENERALES"),
    ("costo_total_sin_imp", 45, "COSTO TOTAL SIN IMPUESTOS"),
    ("imp_nac_comp", 46, "21. IMPUESTOS NACIONALES Y COMPENSACIONES"),
    ("imp_cheque", 47, "Impuesto al cheque"),
    ("iibb", 48, "22. IMPUESTO A LOS INGRESOS BRUTOS"),
    ("gerenciamiento", 49, "23. Costo de gerenciamiento"),
    ("saldo_tecnico_iva", 50, "24. Saldo Técnico a Favor IVA"),
    ("costo_total_km_sin_iva", 51, "COSTO TOTAL POR KILOMETRO SIN IVA"),
    ("ipk", 52, "ÍNDICE PASAJERO KILÓMETRO (IPK)"),
    ("tarifa_media", 53, "Tarifa media sin compensación"),
]


def as_float(value):
    if value is None or value == "":
        return 0.0
    try:
        return float(value)
    except Exception:
        return 0.0


def main(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cur = conn.cursor()

    for idx, (code, name, _col) in enumerate(GROUPS, start=1):
        cur.execute(
            "INSERT INTO grupos_tarifarios (codigo, nombre, orden) VALUES (%s,%s,%s) "
            "ON DUPLICATE KEY UPDATE nombre=VALUES(nombre), orden=VALUES(orden)",
            (code, name, idx),
        )

    for modulo, code, label, unit, sheet, row, editable in PARAMETER_DEFS:
        cur.execute(
            "INSERT INTO definiciones_parametros (codigo, modulo, hoja_origen, fila_origen, descripcion, unidad, editable) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s) "
            "ON DUPLICATE KEY UPDATE modulo=VALUES(modulo), hoja_origen=VALUES(hoja_origen), "
            "fila_origen=VALUES(fila_origen), descripcion=VALUES(descripcion), unidad=VALUES(unidad), editable=VALUES(editable)",
            (code, modulo, sheet, row, label, unit, editable),
        )

    for modulo, code, label, unit, sheet_name, row, editable in PARAMETER_DEFS:
        ws = wb[sheet_name]
        cur.execute("SELECT id FROM definiciones_parametros WHERE codigo=%s", (code,))
        parametro_id = cur.fetchone()[0]
        for group_code, _group_name, col in GROUPS:
            val = as_float(ws[f"{col}{row}"].value)
            cur.execute("SELECT id FROM grupos_tarifarios WHERE codigo=%s", (group_code,))
            group_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO valores_base (parametro_id, grupo_id, valor) VALUES (%s,%s,%s) "
                "ON DUPLICATE KEY UPDATE valor=VALUES(valor)",
                (parametro_id, group_id, val),
            )

    for code, order, label in RESULT_DEFS:
        cur.execute(
            "INSERT INTO definiciones_resultados (codigo, orden, descripcion) VALUES (%s,%s,%s) "
            "ON DUPLICATE KEY UPDATE orden=VALUES(orden), descripcion=VALUES(descripcion)",
            (code, order, label),
        )

    ws_result = wb["1-COSTO X KM"]
    for code, order, label in RESULT_DEFS:
        cur.execute("SELECT id FROM definiciones_resultados WHERE codigo=%s", (code,))
        result_id = cur.fetchone()[0]
        for group_code, _group_name, col in GROUPS:
            val = as_float(ws_result[f"{col}{order}"].value)
            cur.execute("SELECT id FROM grupos_tarifarios WHERE codigo=%s", (group_code,))
            group_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO resultados_base (resultado_id, grupo_id, valor) VALUES (%s,%s,%s) "
                "ON DUPLICATE KEY UPDATE valor=VALUES(valor)",
                (result_id, group_id, val),
            )

    cur.execute(
        "INSERT IGNORE INTO escenarios (nombre, descripcion) VALUES (%s, %s)",
        ("Base", "Escenario base importado desde Excel"),
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Importación completada.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Uso: python import_excel.py "GO - Costos Diciembre 2025.xlsx"')
    main(sys.argv[1])
