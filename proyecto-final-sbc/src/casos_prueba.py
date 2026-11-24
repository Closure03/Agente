"""Casos de prueba del sistema experto (datos + ejecutor). Python puro."""
from base_conocimiento import REGLAS
from motor_inferencia import razonar, validar_entrada

# VALIDACIÓN 2 · Casos de prueba diseñados a mano
CASOS = []

def caso(desc, sintomas, debe=(), no_debe=(), marca="", error=False, modelo=""):
    CASOS.append({"caso": len(CASOS) + 1, "desc": desc, "marca": marca, "modelo": modelo, "sintomas": set(sintomas),
                  "debe": set(debe), "no_debe": set(no_debe), "error": error})

# ---------- Eléctrico y encendido ----------
caso("Batería descargada", ["marcha_no_gira", "luces_debiles"],
     ["bateria_descargada", "recomendar_bateria_descargada"], ["bateria_vida_util_terminada", "conexion_bateria_deficiente"])
caso("Batería al final de su vida", ["marcha_no_gira", "luces_debiles", "bateria_se_descarga"],
     ["bateria_descargada", "bateria_vida_util_terminada", "recomendar_bateria_vida_util_terminada"])
caso("Bornes sulfatados (no es la batería)", ["marcha_no_gira", "bornes_sulfatados"],
     ["conexion_bateria_deficiente"], ["bateria_descargada"])
caso("Falla de carga con olor a quemado", ["bateria_se_descarga", "luces_debiles_en_marcha", "olor_quemado_electrico"],
     ["falla_sistema_carga", "regulador_rectificador_danado", "recomendar_regulador_rectificador_danado"])
caso("Cortocircuito (fusible + olor, sin falla de carga)", ["fusible_quemado_repetido", "olor_quemado_electrico"],
     ["cortocircuito_instalacion"], ["falla_sistema_carga", "regulador_rectificador_danado"])
caso("Bujía sucia", ["marcha_gira", "sin_chispa", "bujia_sucia"],
     ["falla_encendido", "bujia_danada", "recomendar_bujia_danada"])
caso("Falla con lluvia", ["marcha_gira", "sin_chispa", "falla_con_humedad"],
     ["humedad_en_encendido"], ["bujia_danada"])
caso("Sensor de encendido", ["marcha_gira", "sin_chispa", "testigo_check_engine"],
     ["sensor_encendido_defectuoso"], ["bujia_danada"])
# ---------- Combustible ----------
caso("Bomba de gasolina", ["marcha_gira", "no_llega_gasolina", "sin_ruido_bomba"],
     ["falla_alimentacion", "bomba_gasolina_danada"], ["carburador_inyectores_tapados"])
caso("Moto parada con gasolina vieja", ["marcha_gira", "no_llega_gasolina", "gasolina_vieja"],
     ["carburador_inyectores_tapados"], ["bomba_gasolina_danada"])
caso("Filtro de aire obstruido", ["tirones", "perdida_potencia", "filtro_aire_sucio"],
     ["mezcla_irregular", "filtro_aire_obstruido", "recomendar_filtro_aire_obstruido"], ["combustible_contaminado"])
caso("Combustible degradado", ["tirones", "perdida_potencia", "gasolina_vieja"],
     ["combustible_contaminado"], ["filtro_aire_obstruido"])
caso("Ralentí mal ajustado", ["ralenti_inestable", "se_apaga_en_ralenti"], ["ralenti_mal_ajustado"])
caso("Mezcla rica con sensor", ["humo_negro", "consumo_gasolina_alto", "testigo_check_engine"],
     ["mezcla_rica", "sensor_inyeccion_defectuoso"])
caso("Mezcla rica sin check engine", ["humo_negro", "consumo_gasolina_alto"],
     ["mezcla_rica"], ["sensor_inyeccion_defectuoso"])
# ---------- Motor y refrigeración ----------
caso("Aros desgastados", ["humo_azul", "consumo_aceite"], ["desgaste_aros", "recomendar_desgaste_aros"])
caso("Fuga por sello", ["fuga_aceite", "consumo_aceite"], ["sello_o_empaque_fuga"], ["desgaste_aros"])
caso("Empaque de culata (ALERTA)", ["humo_blanco", "aceite_lechoso", "nivel_refrigerante_bajo"],
     ["empaque_culata_danado", "alerta_culata"])
caso("Humo blanco sin aceite lechoso", ["humo_blanco", "nivel_refrigerante_bajo"], [], ["empaque_culata_danado", "alerta_culata"])
caso("Fuga de refrigerante", ["sobrecalentamiento", "nivel_refrigerante_bajo"], ["fuga_refrigerante"], ["falla_ventilador"])
caso("Ventilador parado", ["sobrecalentamiento", "ventilador_no_gira"], ["falla_ventilador"], ["fuga_refrigerante"])
caso("Aceite vencido y calentamiento", ["sobrecalentamiento", "aceite_vencido"],
     ["lubricacion_deficiente", "necesita_cambio_aceite"])
caso("Lubricación crítica (ALERTA)", ["ruido_golpeteo_motor", "luz_presion_aceite"],
     ["lubricacion_critica", "alerta_lubricacion"])
caso("Tensor de distribución", ["ruido_cadena_distribucion", "perdida_potencia"], ["tensor_distribucion_desgastado"])
# ---------- Transmisión ----------
caso("Kit de arrastre", ["ruido_cadena", "cadena_floja"], ["kit_arrastre_desgastado"], ["cadena_sin_lubricar"])
caso("Cadena seca", ["cadena_oxidada", "ruido_cadena"], ["cadena_sin_lubricar"], ["kit_arrastre_desgastado"])
caso("Cadena completa (floja, oxidada y ruidosa)", ["cadena_oxidada", "ruido_cadena", "cadena_floja"],
     ["kit_arrastre_desgastado", "cadena_sin_lubricar"])
caso("Embrague patina", ["embrague_patina", "perdida_potencia"], ["embrague_desgastado"])
caso("Embrague duro", ["palanca_embrague_dura", "cambios_duros"], ["circuito_embrague_defectuoso"], ["caja_cambios_desgastada"])
caso("Caja de cambios", ["salto_marchas", "cambios_duros"], ["caja_cambios_desgastada"])
caso("Scooter con variador gastado", ["vibracion_al_arrancar_scooter", "ruido_variador"],
     ["variador_cvt_desgastado"], ["variador_honda"])
# ---------- Frenos, suspensión y llantas ----------
caso("Pastillas", ["freno_chirrido", "recorrido_freno_largo"], ["pastillas_desgastadas"])
caso("Aire/humedad en frenos", ["freno_esponjoso", "liquido_freno_oscuro"], ["aire_humedad_frenos"], ["alerta_frenos"])
caso("Fuga en frenos (ALERTA)", ["freno_esponjoso", "nivel_liquido_bajo"],
     ["fuga_circuito_frenos", "alerta_frenos"])
caso("Disco rayado", ["vibracion_al_frenar", "disco_con_surcos"], ["disco_danado"])
caso("ABS genérico", ["abs_testigo_encendido"], ["falla_abs"], ["modulo_abs_bmw"])
caso("Retenes de horquilla", ["fuga_aceite_barra", "rebote_excesivo"], ["retenes_horquilla_danados"])
caso("Dirección floja", ["vibracion_manubrio", "direccion_floja"], ["rodamientos_direccion_flojos", "alerta_direccion"], ["balanceo_alineacion"])
caso("Balanceo", ["llanta_desgaste_irregular", "vibracion_manubrio"], ["balanceo_alineacion"], ["rodamientos_direccion_flojos"])
caso("Presión de llantas", ["llanta_baja_presion"], ["presion_llantas_incorrecta"])
# ---------- Combinados ----------
caso("Servicio mayor (aceite + filtro + bujía)",
     ["aceite_vencido", "tirones", "perdida_potencia", "filtro_aire_sucio", "marcha_gira", "sin_chispa", "bujia_sucia"],
     ["necesita_cambio_aceite", "filtro_aire_obstruido", "bujia_danada", "recomendar_servicio_mayor"])
caso("Moto en mal estado general (muchos sistemas)",
     ["marcha_gira", "sin_chispa", "bujia_sucia", "no_llega_gasolina", "gasolina_vieja", "tirones", "perdida_potencia",
      "filtro_aire_sucio", "humo_azul", "consumo_aceite", "ruido_cadena", "cadena_floja", "freno_chirrido",
      "recorrido_freno_largo", "aceite_vencido", "llanta_baja_presion", "vibracion_manubrio", "direccion_floja"],
     ["bujia_danada", "carburador_inyectores_tapados", "filtro_aire_obstruido", "desgaste_aros", "kit_arrastre_desgastado",
      "pastillas_desgastadas", "recomendar_servicio_mayor", "rodamientos_direccion_flojos", "presion_llantas_incorrecta"])
# ---------- Sin conclusión y bordes ----------
caso("Sin conclusión: síntoma aislado (luces débiles)", ["luces_debiles"], [], ["bateria_descargada"])
caso("Sin conclusión: freno chirría pero recorrido normal", ["freno_chirrido"], [], ["pastillas_desgastadas"])
caso("Borde: evidencia parcial de falla de encendido", ["marcha_gira", "sin_chispa"], ["falla_encendido"], ["bujia_danada", "recomendar_bujia_danada"])
caso("Error: sin síntomas", [], error=True)
caso("Error: síntomas contradictorios", ["marcha_gira", "marcha_no_gira"], error=True)
caso("Error: síntoma inexistente", ["motor_volador"], error=True)
caso("Error: marca como síntoma", ["marca_ktm", "tirones"], error=True)
caso("Error: marca inexistente", ["tirones"], marca="mercedes", error=True)
# ---------- Marcas ----------
caso("KTM · pierde carga", ["bateria_se_descarga", "luces_debiles_en_marcha"],
     ["falla_sistema_carga", "regulador_rectificador_ktm", "recomendar_regulador_rectificador_ktm"], ["regulador_rectificador_danado"], marca="ktm")
caso("Control: mismos síntomas sin marca (no sale diagnóstico de marca)", ["bateria_se_descarga", "luces_debiles_en_marcha"],
     ["falla_sistema_carga"], ["regulador_rectificador_ktm", "regulador_ducati"])
caso("KTM · se calienta en tráfico", ["sobrecalentamiento", "falla_en_trafico_lento"], ["ventilacion_trafico_ktm"], ["calor_cilindro_trasero_ducati"], marca="ktm")
caso("KTM · válvulas vencidas", ["servicio_valvulas_vencido", "perdida_potencia"], ["valvulas_fuera_de_rango_ktm"], ["correas_desmo_ducati"], marca="ktm")
caso("Aprilia · ride-by-wire", ["ralenti_inestable", "testigo_check_engine"], ["sensor_acelerador_aprilia"], [], marca="aprilia")
caso("Aprilia · estátor", ["bateria_se_descarga", "olor_quemado_electrico"], ["estator_aprilia"], ["falla_sistema_carga"], marca="aprilia")
caso("Aprilia · regulador", ["bateria_se_descarga", "luces_debiles_en_marcha"], ["regulador_rectificador_aprilia"], ["regulador_rectificador_ktm"], marca="aprilia")
caso("BMW · ABS", ["abs_testigo_encendido"], ["modulo_abs_bmw", "falla_abs"], [], marca="bmw")
caso("BMW · fuga de aceite", ["fuga_aceite"], ["fuga_transmision_final_bmw"], ["fugas_aceite_harley"], marca="bmw")
caso("BMW · balancines", ["ruido_golpeteo_motor", "perdida_potencia"], ["balancines_valvulas_bmw"], ["alerta_lubricacion"], marca="bmw")
caso("Ducati · servicio desmo", ["servicio_valvulas_vencido"], ["correas_desmo_ducati", "recomendar_correas_desmo_ducati"], ["valvulas_fuera_de_rango_ktm"], marca="ducati")
caso("Ducati · calor en tráfico", ["sobrecalentamiento", "falla_en_trafico_lento"], ["calor_cilindro_trasero_ducati"], ["ventilacion_trafico_ktm"], marca="ducati")
caso("Ducati · embrague seco", ["ruido_embrague_seco", "embrague_patina"], ["embrague_seco_ducati"], [], marca="ducati")
caso("Ducati · regulador", ["bateria_se_descarga", "luces_debiles_en_marcha"], ["regulador_ducati"], [], marca="ducati")
caso("Triumph · fuga de refrigerante", ["sobrecalentamiento", "nivel_refrigerante_bajo"], ["fuga_refrigerante", "fuga_refrigerante_triumph"], ["sello_bomba_agua_kawasaki"], marca="triumph")
caso("Triumph · cuerpos de aceleración", ["ralenti_inestable", "olor_gasolina"], ["cuerpos_aceleracion_triumph"], [], marca="triumph")
caso("Yamaha · tensor de distribución", ["ruido_cadena_distribucion"], ["tensor_distribucion_yamaha"], ["tensor_distribucion_desgastado", "tensor_distribucion_honda"], marca="yamaha")
caso("Yamaha · sensor de inyección", ["testigo_check_engine", "ralenti_inestable"], ["sensor_inyeccion_yamaha"], [], marca="yamaha")
caso("Honda · variador de scooter", ["vibracion_al_arrancar_scooter", "ruido_variador"], ["variador_cvt_desgastado", "variador_honda"], [], marca="honda")
caso("Honda · tensor", ["ruido_cadena_distribucion", "perdida_potencia"], ["tensor_distribucion_honda", "tensor_distribucion_desgastado"], ["tensor_distribucion_yamaha"], marca="honda")
caso("Kawasaki · bomba de agua", ["sobrecalentamiento", "nivel_refrigerante_bajo"], ["sello_bomba_agua_kawasaki"], ["fuga_refrigerante_triumph"], marca="kawasaki")
caso("Kawasaki · termostato en tráfico", ["sobrecalentamiento", "falla_en_trafico_lento"], ["termostato_ventilador_kawasaki"], [], marca="kawasaki")
caso("Suzuki · carburación", ["ralenti_inestable", "gasolina_vieja"], ["carburacion_suzuki"], [], marca="suzuki")
caso("Suzuki · sensor de acelerador", ["perdida_potencia", "testigo_check_engine"], ["sensor_acelerador_suzuki"], [], marca="suzuki")
caso("Harley · tensores de levas", ["ruido_cadena_distribucion"], ["tensores_levas_harley"], [], marca="harley")
caso("Harley · fuga de aceite", ["fuga_aceite"], ["fugas_aceite_harley"], ["fuga_transmision_final_bmw"], marca="harley")
caso("Cruce: síntomas Ducati en una Yamaha (no aplica)", ["servicio_valvulas_vencido"], [], ["correas_desmo_ducati"], marca="yamaha")
caso("KTM · escenario complejo (carga + calor + válvulas + frenos)",
     ["bateria_se_descarga", "luces_debiles_en_marcha", "olor_quemado_electrico", "sobrecalentamiento",
      "falla_en_trafico_lento", "nivel_refrigerante_bajo", "servicio_valvulas_vencido", "perdida_potencia",
      "freno_esponjoso", "nivel_liquido_bajo"],
     ["regulador_rectificador_ktm", "regulador_rectificador_danado", "ventilacion_trafico_ktm", "fuga_refrigerante",
      "valvulas_fuera_de_rango_ktm", "fuga_circuito_frenos", "alerta_frenos"], ["correas_desmo_ducati"], marca="ktm")

# ---------- Modelos: atributos del modelo, síntomas que no aplican y bloqueos ----------
caso("Modelo · KTM 390 Duke pierde carga", ["bateria_se_descarga", "luces_debiles_en_marcha"],
     ["regulador_rectificador_ktm"], ["regulador_ducati"], modelo="ktm_390_duke")
caso("Modelo · NMAX (scooter): variador", ["vibracion_al_arrancar_scooter", "ruido_variador"],
     ["variador_cvt_desgastado", "recomendar_variador_cvt_desgastado"], ["kit_arrastre_desgastado", "variador_honda"], modelo="yamaha_nmax_155")
caso("Modelo · NMAX con síntoma de cadena (no aplica)", ["ruido_cadena"], error=True, modelo="yamaha_nmax_155")
caso("Modelo · PCX: el scooter patina", ["scooter_patina_al_acelerar"], ["correa_cvt_desgastada"], [], modelo="honda_pcx")
caso("Modelo · PCX: variador (regla Honda)", ["vibracion_al_arrancar_scooter", "ruido_variador"],
     ["variador_honda", "variador_cvt_desgastado"], [], modelo="honda_pcx")
caso("Modelo · PCX con embrague manual (no aplica)", ["embrague_patina"], error=True, modelo="honda_pcx")
caso("Modelo · BMW R 1250 GS (cardán): ruido y fuga", ["ruido_transmision_cardan", "fuga_aceite"],
     ["cardan_con_fuga_o_desgaste", "fuga_transmision_final_bmw"], ["kit_arrastre_desgastado"], modelo="bmw_r_1250_gs")
caso("Modelo · BMW R 1250 GS con cadena (no aplica)", ["ruido_cadena"], error=True, modelo="bmw_r_1250_gs")
caso("Modelo · BMW F 850 GS (cadena): una fuga no es del cardán", ["fuga_aceite"],
     [], ["fuga_transmision_final_bmw", "cardan_con_fuga_o_desgaste"], modelo="bmw_f_850_gs")
caso("Modelo · BMW F 850 GS: kit de arrastre", ["ruido_cadena", "cadena_floja"], ["kit_arrastre_desgastado"], [], modelo="bmw_f_850_gs")
caso("Modelo · Harley Fat Boy (correa)", ["correa_final_desgastada"],
     ["correa_transmision_desgastada", "recomendar_correa_transmision_desgastada"], ["kit_arrastre_desgastado"], modelo="harley_fat_boy")
caso("Modelo · Harley Iron 883: tensores de levas", ["ruido_cadena_distribucion"], ["tensores_levas_harley"], [], modelo="harley_iron_883")
caso("Modelo · Scrambler 800 (aire) se calienta en tráfico", ["sobrecalentamiento", "falla_en_trafico_lento"],
     ["calentamiento_motor_aire_trafico", "calor_cilindro_trasero_ducati"], ["falla_ventilador"], modelo="ducati_scrambler_800")
caso("Modelo · Scrambler 800 sin radiador (refrigerante no aplica)", ["nivel_refrigerante_bajo"], error=True, modelo="ducati_scrambler_800")
caso("Modelo · Panigale V4 (líquida) se calienta en tráfico", ["sobrecalentamiento", "falla_en_trafico_lento"],
     ["calor_cilindro_trasero_ducati"], ["calentamiento_motor_aire_trafico"], modelo="ducati_panigale_v4")
caso("Modelo · KLX 230 (aire): termostato Kawasaki bloqueado", ["sobrecalentamiento", "falla_en_trafico_lento"],
     ["calentamiento_motor_aire_trafico"], ["termostato_ventilador_kawasaki"], modelo="kawasaki_klx_230")
caso("Modelo · KLX 230 con ventilador (no aplica)", ["ventilador_no_gira"], error=True, modelo="kawasaki_klx_230")
caso("Modelo · Z650 (líquida): termostato Kawasaki", ["sobrecalentamiento", "falla_en_trafico_lento"],
     ["termostato_ventilador_kawasaki"], ["calentamiento_motor_aire_trafico"], modelo="kawasaki_z650")
caso("Modelo · Tiger 900: fuga de refrigerante", ["sobrecalentamiento", "nivel_refrigerante_bajo"],
     ["fuga_refrigerante", "fuga_refrigerante_triumph"], [], modelo="triumph_tiger_900")
caso("Modelo · F 850 GS: aceite lechoso + refrigerante bajo", ["aceite_lechoso", "nivel_refrigerante_bajo"],
     ["fuga_interna_refrigerante"], ["empaque_culata_danado"], modelo="bmw_f_850_gs")
caso("Modelo · GN 125 (carburador) con gasolina vieja", ["ralenti_inestable", "gasolina_vieja"],
     ["carburador_sucio_carburado", "carburacion_suzuki"], [], modelo="suzuki_gn_125")
caso("Modelo · GN 125 con check engine (carburador, no aplica)", ["testigo_check_engine"], error=True, modelo="suzuki_gn_125")
caso("Modelo · Yamaha R15: tensor de distribución", ["ruido_cadena_distribucion"],
     ["tensor_distribucion_r15", "tensor_distribucion_yamaha"], [], modelo="yamaha_r15")
caso("Modelo · Yamaha MT-07: tensor (no es la regla de la R15)", ["ruido_cadena_distribucion"],
     ["tensor_distribucion_yamaha"], ["tensor_distribucion_r15"], modelo="yamaha_mt_07")
caso("Modelo · Aprilia RSV4: ride-by-wire", ["ralenti_inestable", "testigo_check_engine"],
     ["sensor_acelerador_aprilia"], [], modelo="aprilia_rsv4_1100")
caso("Modelo · Honda CB190R: embrague", ["embrague_patina", "perdida_potencia"], ["embrague_desgastado"], [], modelo="honda_cb190r")
caso("Error: modelo de otra marca", ["tirones"], marca="ducati", error=True, modelo="ktm_390_duke")
caso("Error: modelo inexistente", ["tirones"], error=True, modelo="ktm_inexistente")
caso("Modelo · KTM 790 Duke, escenario complejo",
     ["bateria_se_descarga", "luces_debiles_en_marcha", "olor_quemado_electrico", "sobrecalentamiento",
      "falla_en_trafico_lento", "nivel_refrigerante_bajo", "servicio_valvulas_vencido", "perdida_potencia",
      "freno_esponjoso", "nivel_liquido_bajo", "ruido_cadena", "cadena_floja"],
     ["regulador_rectificador_ktm", "ventilacion_trafico_ktm", "fuga_refrigerante", "valvulas_fuera_de_rango_ktm",
      "fuga_circuito_frenos", "alerta_frenos", "kit_arrastre_desgastado"], ["correa_cvt_desgastada"], modelo="ktm_790_duke")



def ejecutar_casos():
    """Ejecuta todos los casos y devuelve una lista de resultados comparados con lo esperado."""
    resultados = []
    for c in CASOS:
        errores = validar_entrada(c["sintomas"], c["marca"], c["modelo"])
        if c["error"]:
            ok = len(errores) > 0
            reglas, faltan, sobran = [], set(), set()
        else:
            hechos, aplicadas = razonar(c["sintomas"], c["marca"], c["modelo"])
            faltan = c["debe"] - hechos
            sobran = c["no_debe"] & hechos
            ok = (not errores) and not faltan and not sobran
            reglas = [a["nombre"] for a in aplicadas]
        resultados.append({"caso": c["caso"], "desc": c["desc"], "marca": c["marca"], "modelo": c["modelo"],
                           "reglas": reglas, "faltan": sorted(faltan), "sobran": sorted(sobran),
                           "error_esperado": c["error"], "ok": ok})
    return resultados
