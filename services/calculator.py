GROUPS = ["DF", "SGI", "SGI_KM", "SGII", "INP", "UPA", "UPA_KM", "UMA_1", "UMA_2"]


STAFF_CODES = [
    "conductores_x_veh",
    "jefes_trafico_x_veh",
    "inspectores_x_veh",
    "otros_trafico_x_veh",
    "jefes_taller_x_veh",
    "oficiales_mecanicos_x_veh",
    "gomeros_x_veh",
    "otros_mantenimiento_x_veh",
    "gerentes_x_veh",
    "jefes_admin_x_veh",
    "administrativos_x_veh",
    "recaudadores_x_veh",
    "otros_admin_x_veh",
]


RESULT_CODES_USED = [
    "combustible",
    "lubricantes",
    "neumaticos",
    "engrase_lavado",
    "reparacion_mantenimiento",
    "depreciacion_mr",
    "seguro_vehiculo",
    "patentes_tnft",
    "salarios_personal",
    "seguros_personal",
    "maq_herr_inmuebles",
    "impuestos_tasas_mun",
    "capital_invertido",
    "lnh",
    "control_tecnico",
    "actrans",
    "peajes",
    "vigilancia",
    "camaras_seguridad",
    "iibb",
    "ipk",
    "subtotal_sin_gg",
    "gastos_generales",
    "costo_total_sin_imp",
    "gerenciamiento",
    "imp_nac_comp",
    "saldo_tecnico_iva",
    "costo_total_km_sin_iva",
    "tarifa_media",
]


def _safe_div(a, b):
    return a / b if b not in (0, None) else 0.0


def _pct(v):
    v = float(v)
    return v / 100.0 if v > 1 else v


def _get(data, code, group, default=0.0):
    try:
        return float(data.get(code, {}).get(group, default))
    except Exception:
        return float(default)


def _copy_results(baseline_results):
    return {
        code: {g: float(v) for g, v in values.items()}
        for code, values in baseline_results.items()
    }


def _ensure_result_groups(results, codes):
    """
    Garantiza que todos los rubros usados existan con todas las claves de grupos.
    """
    for code in codes:
        results.setdefault(code, {})
        for g in GROUPS:
            results[code].setdefault(g, 0.0)


def calculate_results(base_params, scenario_params, baseline_results):
    """
    Regla general aplicada:
    cada rubro se calcula exclusivamente con los parámetros del grupo actual 'g'.
    No se copian resultados entre grupos ni se leen columnas contiguas.
    """
    params = {}
    all_codes = set(base_params) | set(scenario_params)

    for code in all_codes:
        params[code] = {}
        for g in GROUPS:
            params[code][g] = _get(
                scenario_params,
                code,
                g,
                _get(base_params, code, g, 0.0)
            )

    results = _copy_results(baseline_results)
    _ensure_result_groups(results, RESULT_CODES_USED)

    base_salary_annual_per_staff = {}
    base_lnh_annual_per_conductor = {}
    seguros_personal_ratio = {}
    km_prod_base = {}
    km_empresa_base = {}
    staff_base = {}
    conductores_base = {}

    for g in GROUPS:
        km_prod_base[g] = _get(base_params, "km_productivo_anual_veh", g, 0.0)
        km_empresa_base[g] = _get(base_params, "km_anual_empresa", g, 0.0)
        staff_base[g] = sum(_get(base_params, code, g, 0.0) for code in STAFF_CODES)
        conductores_base[g] = _get(base_params, "conductores_x_veh", g, 0.0)

        base_salary_annual_per_staff[g] = _safe_div(
            _get(baseline_results, "salarios_personal", g, 0.0) * km_prod_base[g],
            staff_base[g],
        )

        base_lnh_annual_per_conductor[g] = _safe_div(
            _get(baseline_results, "lnh", g, 0.0) * km_empresa_base[g],
            conductores_base[g],
        )

        seguros_personal_ratio[g] = _safe_div(
            _get(baseline_results, "seguros_personal", g, 0.0),
            _get(baseline_results, "salarios_personal", g, 0.0),
        )

    for g in GROUPS:
        km_prod = _get(params, "km_productivo_anual_veh", g, 0.0)
        km_empresa = _get(params, "km_anual_empresa", g, 0.0)
        parque = _get(params, "parque_movil", g, 0.0)
        km_improd = _pct(_get(params, "km_improductivo_pct", g, 0.0))
        vida_veh_km = _get(params, "vida_util_vehiculo_km", g, 0.0)
        vida_veh_anios = _get(params, "vida_util_vehiculo_anios", g, 0.0)

        # 1. Combustible
        results["combustible"][g] = (
            _get(params, "consumo_combustible", g, 0.0)
            * _get(params, "precio_gasoil_sin_iva", g, 0.0)
        )

        # 2. Lubricantes
        results["lubricantes"][g] = (
            (
                _get(params, "consumo_aceite", g, 0.0) * _get(params, "precio_aceite", g, 0.0)
                + (
                    _get(params, "consumo_grasa", g, 0.0)
                    + _get(params, "consumo_aceite_caja", g, 0.0)
                ) * _get(params, "precio_grasa", g, 0.0)
            )
            * (1 + km_improd)
        )

        # 3. Neumáticos
        vida_total_juego = _get(params, "vida_util_total_juego", g, 0.0)
        if not vida_total_juego:
            vida_total_juego = (
                _get(params, "vida_util_neumaticos", g, 0.0)
                + _get(params, "recapados_admisibles", g, 0.0)
                * _get(params, "prolongacion_recapado", g, 0.0)
            )

        results["neumaticos"][g] = _safe_div(
            (
                _get(params, "cantidad_cubiertas", g, 0.0)
                * _get(params, "precio_cubierta", g, 0.0)
                + _get(params, "recapados_admisibles", g, 0.0)
                * _get(params, "precio_recapado", g, 0.0)
                * _get(params, "cantidad_cubiertas", g, 0.0)
            )
            * (1 + km_improd),
            vida_total_juego,
        )

        # 4. Engrase y lavado
        results["engrase_lavado"][g] = _safe_div(
            _get(params, "engrases_cada_10000", g, 0.0) * _get(params, "precio_engrase_general", g, 0.0)
            + _get(params, "lav_carroceria_cada_10000", g, 0.0) * _get(params, "precio_lavado_carroceria", g, 0.0)
            + _get(params, "lav_motor_cada_10000", g, 0.0) * _get(params, "precio_lavado_motor", g, 0.0)
            + _get(params, "lav_chasis_cada_10000", g, 0.0) * _get(params, "precio_lavado_chasis", g, 0.0)
            + _get(params, "filtros_gasoil_cada_10000", g, 0.0) * _get(params, "precio_filtro_gasoil", g, 0.0)
            + _get(params, "filtros_aceite_cada_10000", g, 0.0) * _get(params, "precio_filtro_aceite", g, 0.0)
            + _get(params, "filtros_aire_cada_10000", g, 0.0) * _get(params, "precio_filtro_aire", g, 0.0),
            _get(params, "vida_util_service_km", g, 0.0),
        )

        # 5. Reparación y mantenimiento material rodante
        rep_chasis = _safe_div(
            _get(params, "reparacion_chasis_pct", g, 0.0)
            * (
                _get(params, "precio_chasis", g, 0.0)
                - 6 * _get(params, "precio_cubierta", g, 0.0)
            )
            * vida_veh_anios,
            vida_veh_km,
        )

        rep_carroceria = _safe_div(
            _get(params, "reparacion_carroceria_pct", g, 0.0)
            * _get(params, "precio_carroceria", g, 0.0)
            * vida_veh_anios,
            vida_veh_km,
        )

        results["reparacion_mantenimiento"][g] = rep_chasis + rep_carroceria

        # 6. Depreciación del material rodante
        results["depreciacion_mr"][g] = _safe_div(
            _get(params, "valor_depreciable_chasis", g, 0.0)
            * (1 + _pct(_get(params, "gastos_iniciales_material_rodante_pct", g, 0.0)))
            + _get(params, "valor_depreciable_carroceria", g, 0.0),
            vida_veh_km,
        )

        # 7. Seguro del vehículo
        results["seguro_vehiculo"][g] = _safe_div(
            _get(params, "premio_seguro_rc_anual", g, 0.0)
            + _get(params, "costo_anual_franquicia", g, 0.0)
            + _get(params, "costo_anual_seguro_chasis", g, 0.0)
            + _get(params, "costo_anual_seguro_carroceria", g, 0.0),
            km_prod,
        )

        # 8. Patentes y TNFT
        results["patentes_tnft"][g] = _safe_div(
            _get(params, "valor_patente_anual", g, 0.0)
            + _get(params, "valor_tnft_anual", g, 0.0),
            km_prod,
        )

        # 9. Salarios del personal // version anterior 
        #staff_scenario = sum(_get(params, code, g, 0.0) for code in STAFF_CODES)
        #parque = _get(params, "parque_movil", g, 0.0)

        #results["salarios_personal"][g] = _safe_div(
        #    staff_scenario * base_salary_annual_per_staff[g] * parque,
        #    km_empresa,
        #)
        # 9. Salarios del personal
        staff_scenario = sum(_get(params, code, g, 0.0) for code in STAFF_CODES)
        parque = _get(params, "parque_movil", g, 0.0)
        km_empresa = _get(params, "km_anual_empresa", g, 0.0)

        results["salarios_personal"][g] = _safe_div(
            staff_scenario * base_salary_annual_per_staff[g] * parque,
            km_empresa,
        )

        # 10. Seguros del personal
        #results["seguros_personal"][g] = (
        #    results["salarios_personal"][g] * seguros_personal_ratio[g]
        #)

        # 10. Seguros del personal
        results["seguros_personal"][g] = results["salarios_personal"][g] * seguros_personal_ratio[g]

        # 11. Máquinas, herramientas e inmuebles
        if km_empresa and km_empresa_base[g]:
            results["maq_herr_inmuebles"][g] = (
                _get(baseline_results, "maq_herr_inmuebles", g, 0.0)
                * (km_empresa_base[g] / km_empresa)
            )
        else:
            results["maq_herr_inmuebles"][g] = 0.0

        # 12. Impuestos y tasas municipales
        if km_empresa and km_empresa_base[g]:
            results["impuestos_tasas_mun"][g] = (
                _get(baseline_results, "impuestos_tasas_mun", g, 0.0)
                * (km_empresa_base[g] / km_empresa)
            )
        else:
            results["impuestos_tasas_mun"][g] = 0.0

        # 13. Costo del capital invertido
        parque_base = _get(base_params, "parque_movil", g, 0.0)
        if km_empresa and km_empresa_base[g]:
            parque_factor = _safe_div(parque, parque_base) if parque_base else 1.0
            results["capital_invertido"][g] = (
                _get(baseline_results, "capital_invertido", g, 0.0)
                * parque_factor
                * (km_empresa_base[g] / km_empresa)
            )
        else:
            results["capital_invertido"][g] = 0.0

        # 14. Licencia nacional habilitante
        conductores = _get(params, "conductores_x_veh", g, 0.0)
        results["lnh"][g] = _safe_div(
            conductores * base_lnh_annual_per_conductor[g],
            km_empresa,
        )

        # 15. Control técnico
        results["control_tecnico"][g] = _safe_div(
            _get(params, "cantidad_controles_tecnicos_anual", g, 0.0)
            * _get(params, "precio_control_tecnico", g, 0.0),
            km_prod,
        )

        # 16. ACTRANS
        results["actrans"][g] = _safe_div(
            parque * _get(params, "aporte_actrans", g, 0.0),
            _safe_div(km_empresa, 12.0),
        )

        # 17. Peajes
        # Se mantiene el valor base del mismo grupo salvo futura fórmula específica.
        results["peajes"][g] = _get(baseline_results, "peajes", g, 0.0)

        # 18. Servicio de vigilancia
        if km_empresa and km_empresa_base[g]:
            results["vigilancia"][g] = (
                _get(baseline_results, "vigilancia", g, 0.0)
                * (km_empresa_base[g] / km_empresa)
            )
        else:
            results["vigilancia"][g] = 0.0

        # 19. Cámaras de seguridad
        results["camaras_seguridad"][g] = _safe_div(
            _get(params, "costo_anual_camaras_seguridad", g, 0.0),
            km_prod,
        )

        # 20. Impuestos nacionales compensables
        # Se mantiene base del mismo grupo hasta modelado específico.
        results["imp_nac_comp"][g] = _get(baseline_results, "imp_nac_comp", g, 0.0)

        # 21. Saldo técnico IVA
        # Se mantiene base del mismo grupo hasta modelado específico.
        results["saldo_tecnico_iva"][g] = _get(
            baseline_results,
            "saldo_tecnico_iva",
            g,
            0.0,
        )

        # 22. Ingresos Brutos (TEMPORAL - congelado a base)
        results["iibb"][g] = _get(baseline_results, "iibb", g, 0.0)

        # IPK
        results["ipk"][g] = _get(params, "ipk", g, _get(baseline_results, "ipk", g, 0.0))

        subtotal_components = [
        "combustible",
        "lubricantes",
        "neumaticos",
        "engrase_lavado",
        "reparacion_mantenimiento",
        "depreciacion_mr",
        "seguro_vehiculo",
        "patentes_tnft",
        "salarios_personal",
        "seguros_personal",
        "maq_herr_inmuebles",
        "impuestos_tasas_mun",
        "capital_invertido",
        "lnh",
        "control_tecnico",
        "actrans",
        "peajes",
        "vigilancia",
        "camaras_seguridad",
    ]

    for g in GROUPS:
        subtotal = sum(_get(results, c, g, 0.0) for c in subtotal_components)

        # 20. Gastos generales
        gg_pct = _pct(_get(params, "gasto_general_pct", g, 0.0))
        gastos_generales = _safe_div(gg_pct * subtotal, 1.0 - gg_pct) if gg_pct < 1 else 0.0

        total_sin_imp = subtotal + gastos_generales

        # 22. Ingresos Brutos (TEMPORAL - congelado a base)
        results["iibb"][g] = _get(baseline_results, "iibb", g, 0.0)

        # 23. Gerenciamiento (TEMPORAL - congelado a base)
        gerenciamiento = _get(baseline_results, "gerenciamiento", g, 0.0)
        results["gerenciamiento"][g] = gerenciamiento

        # Guardamos subtotales
        results["subtotal_sin_gg"][g] = subtotal
        results["gastos_generales"][g] = gastos_generales
        results["costo_total_sin_imp"][g] = total_sin_imp

        # Costo total
        costo_total = (
            total_sin_imp
            + _get(results, "imp_nac_comp", g, 0.0)
            + _get(results, "iibb", g, 0.0)
            + gerenciamiento
            + _get(results, "saldo_tecnico_iva", g, 0.0)
        )

        results["costo_total_km_sin_iva"][g] = costo_total

        # Tarifa media
        results["tarifa_media"][g] = _safe_div(
            costo_total,
            _get(results, "ipk", g, 0.0),
        )

    return results