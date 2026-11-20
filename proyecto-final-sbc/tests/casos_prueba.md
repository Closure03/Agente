# Casos de prueba

78 de 78 casos aprobados. Se generan y ejecutan con `python tests/test_sbc.py`.
Cada caso exige que aparezcan las conclusiones esperadas y que no aparezcan las prohibidas.

| Caso | Descripción | Hechos iniciales | Conclusiones esperadas | Reglas disparadas | Estado |
|---|---|---|---|---|---|
| 1 | Batería descargada | luces_debiles, marcha_no_gira | bateria_descargada, recomendar_bateria_descargada | R1, R80 | ✓ |
| 2 | Batería al final de su vida | bateria_se_descarga, luces_debiles, marcha_no_gira | bateria_descargada, bateria_vida_util_terminada, recomendar_bateria_vida_util_terminada | R1, R3, R80, R82 | ✓ |
| 3 | Bornes sulfatados (no es la batería) | bornes_sulfatados, marcha_no_gira | conexion_bateria_deficiente | R2, R81 | ✓ |
| 4 | Falla de carga con olor a quemado | bateria_se_descarga, luces_debiles_en_marcha, olor_quemado_electrico | falla_sistema_carga, recomendar_regulador_rectificador_danado, regulador_rectificador_danado | R4, R5, R84 | ✓ |
| 5 | Cortocircuito (fusible + olor, sin falla de carga) | fusible_quemado_repetido, olor_quemado_electrico | cortocircuito_instalacion | R6, R83 | ✓ |
| 6 | Bujía sucia | bujia_sucia, marcha_gira, sin_chispa | bujia_danada, falla_encendido, recomendar_bujia_danada | R7, R8, R85 | ✓ |
| 7 | Falla con lluvia | falla_con_humedad, marcha_gira, sin_chispa | humedad_en_encendido | R7, R9, R86 | ✓ |
| 8 | Sensor de encendido | marcha_gira, sin_chispa, testigo_check_engine | sensor_encendido_defectuoso | R7, R10, R87 | ✓ |
| 9 | Bomba de gasolina | marcha_gira, no_llega_gasolina, sin_ruido_bomba | bomba_gasolina_danada, falla_alimentacion | R11, R13, R89 | ✓ |
| 10 | Moto parada con gasolina vieja | gasolina_vieja, marcha_gira, no_llega_gasolina | carburador_inyectores_tapados | R11, R12, R88 | ✓ |
| 11 | Filtro de aire obstruido | filtro_aire_sucio, perdida_potencia, tirones | filtro_aire_obstruido, mezcla_irregular, recomendar_filtro_aire_obstruido | R14, R15, R90 | ✓ |
| 12 | Combustible degradado | gasolina_vieja, perdida_potencia, tirones | combustible_contaminado | R14, R16, R91 | ✓ |
| 13 | Ralentí mal ajustado | ralenti_inestable, se_apaga_en_ralenti | ralenti_mal_ajustado | R17, R92 | ✓ |
| 14 | Mezcla rica con sensor | consumo_gasolina_alto, humo_negro, testigo_check_engine | mezcla_rica, sensor_inyeccion_defectuoso | R18, R19, R93 | ✓ |
| 15 | Mezcla rica sin check engine | consumo_gasolina_alto, humo_negro | mezcla_rica | R18 | ✓ |
| 16 | Aros desgastados | consumo_aceite, humo_azul | desgaste_aros, recomendar_desgaste_aros | R20, R94 | ✓ |
| 17 | Fuga por sello | consumo_aceite, fuga_aceite | sello_o_empaque_fuga | R28, R101 | ✓ |
| 18 | Empaque de culata (ALERTA) | aceite_lechoso, humo_blanco, nivel_refrigerante_bajo | alerta_culata, empaque_culata_danado | R21, R45, R95 | ✓ |
| 19 | Humo blanco sin aceite lechoso | humo_blanco, nivel_refrigerante_bajo | sin conclusión | ninguna | ✓ |
| 20 | Fuga de refrigerante | nivel_refrigerante_bajo, sobrecalentamiento | fuga_refrigerante | R22 | ✓ |
| 21 | Ventilador parado | sobrecalentamiento, ventilador_no_gira | falla_ventilador | R23, R96 | ✓ |
| 22 | Aceite vencido y calentamiento | aceite_vencido, sobrecalentamiento | lubricacion_deficiente, necesita_cambio_aceite | R24, R25, R97, R98 | ✓ |
| 23 | Lubricación crítica (ALERTA) | luz_presion_aceite, ruido_golpeteo_motor | alerta_lubricacion, lubricacion_critica | R26, R44, R99 | ✓ |
| 24 | Tensor de distribución | perdida_potencia, ruido_cadena_distribucion | tensor_distribucion_desgastado | R27, R100 | ✓ |
| 25 | Kit de arrastre | cadena_floja, ruido_cadena | kit_arrastre_desgastado | R29, R102 | ✓ |
| 26 | Cadena seca | cadena_oxidada, ruido_cadena | cadena_sin_lubricar | R30, R103 | ✓ |
| 27 | Cadena completa (floja, oxidada y ruidosa) | cadena_floja, cadena_oxidada, ruido_cadena | cadena_sin_lubricar, kit_arrastre_desgastado | R29, R30, R102, R103 | ✓ |
| 28 | Embrague patina | embrague_patina, perdida_potencia | embrague_desgastado | R31, R104 | ✓ |
| 29 | Embrague duro | cambios_duros, palanca_embrague_dura | circuito_embrague_defectuoso | R32, R105 | ✓ |
| 30 | Caja de cambios | cambios_duros, salto_marchas | caja_cambios_desgastada | R33, R106 | ✓ |
| 31 | Scooter con variador gastado | ruido_variador, vibracion_al_arrancar_scooter | variador_cvt_desgastado | R34, R107 | ✓ |
| 32 | Pastillas | freno_chirrido, recorrido_freno_largo | pastillas_desgastadas | R35, R108 | ✓ |
| 33 | Aire/humedad en frenos | freno_esponjoso, liquido_freno_oscuro | aire_humedad_frenos | R36, R109 | ✓ |
| 34 | Fuga en frenos (ALERTA) | freno_esponjoso, nivel_liquido_bajo | alerta_frenos, fuga_circuito_frenos | R37, R46, R110 | ✓ |
| 35 | Disco rayado | disco_con_surcos, vibracion_al_frenar | disco_danado | R38, R111 | ✓ |
| 36 | ABS genérico | abs_testigo_encendido | falla_abs | R39, R112 | ✓ |
| 37 | Retenes de horquilla | fuga_aceite_barra, rebote_excesivo | retenes_horquilla_danados | R40, R113 | ✓ |
| 38 | Dirección floja | direccion_floja, vibracion_manubrio | alerta_direccion, rodamientos_direccion_flojos | R41, R47, R114 | ✓ |
| 39 | Balanceo | llanta_desgaste_irregular, vibracion_manubrio | balanceo_alineacion | R42, R115 | ✓ |
| 40 | Presión de llantas | llanta_baja_presion | presion_llantas_incorrecta | R43, R116 | ✓ |
| 41 | Servicio mayor (aceite + filtro + bujía) | aceite_vencido, bujia_sucia, filtro_aire_sucio, marcha_gira, perdida_potencia, sin_chispa, tirones | bujia_danada, filtro_aire_obstruido, necesita_cambio_aceite, recomendar_servicio_mayor | R7, R8, R14, R15, R25, R79, R85, R90, R98 | ✓ |
| 42 | Moto en mal estado general (muchos sistemas) | aceite_vencido, bujia_sucia, cadena_floja, consumo_aceite, direccion_floja, filtro_aire_sucio, freno_chirrido, gasolina_vieja, humo_azul, llanta_baja_presion, marcha_gira, no_llega_gasolina, perdida_potencia, recorrido_freno_largo, ruido_cadena, sin_chispa, tirones, vibracion_manubrio | bujia_danada, carburador_inyectores_tapados, desgaste_aros, filtro_aire_obstruido, kit_arrastre_desgastado, pastillas_desgastadas, presion_llantas_incorrecta, recomendar_servicio_mayor, rodamientos_direccion_flojos | R7, R8, R11, R12, R14, R15, R16, R20, R25, R29, R35, R41, R43, R47, R79, R85, R88, R90, R91, R94, R98, R102, R108, R114, R116 | ✓ |
| 43 | Sin conclusión: síntoma aislado (luces débiles) | luces_debiles | sin conclusión | ninguna | ✓ |
| 44 | Sin conclusión: freno chirría pero recorrido normal | freno_chirrido | sin conclusión | ninguna | ✓ |
| 45 | Borde: evidencia parcial de falla de encendido | marcha_gira, sin_chispa | falla_encendido | R7 | ✓ |
| 46 | Error: sin síntomas | (ninguno) | error de validación | error de validación | ✓ |
| 47 | Error: síntomas contradictorios | marcha_gira, marcha_no_gira | error de validación | error de validación | ✓ |
| 48 | Error: síntoma inexistente | motor_volador | error de validación | error de validación | ✓ |
| 49 | Error: marca como síntoma | marca_ktm, tirones | error de validación | error de validación | ✓ |
| 50 | Error: marca inexistente | **marca:** mercedes · tirones | error de validación | error de validación | ✓ |
| 51 | KTM · pierde carga | **marca:** ktm · bateria_se_descarga, luces_debiles_en_marcha | falla_sistema_carga, recomendar_regulador_rectificador_ktm, regulador_rectificador_ktm | R4, R48, R117 | ✓ |
| 52 | Control: mismos síntomas sin marca (no sale diagnóstico de marca) | bateria_se_descarga, luces_debiles_en_marcha | falla_sistema_carga | R4 | ✓ |
| 53 | KTM · se calienta en tráfico | **marca:** ktm · falla_en_trafico_lento, sobrecalentamiento | ventilacion_trafico_ktm | R49, R118 | ✓ |
| 54 | KTM · válvulas vencidas | **marca:** ktm · perdida_potencia, servicio_valvulas_vencido | valvulas_fuera_de_rango_ktm | R50, R119 | ✓ |
| 55 | Aprilia · ride-by-wire | **marca:** aprilia · ralenti_inestable, testigo_check_engine | sensor_acelerador_aprilia | R52, R121 | ✓ |
| 56 | Aprilia · estátor | **marca:** aprilia · bateria_se_descarga, olor_quemado_electrico | estator_aprilia | R53, R122 | ✓ |
| 57 | Aprilia · regulador | **marca:** aprilia · bateria_se_descarga, luces_debiles_en_marcha | regulador_rectificador_aprilia | R4, R51, R120 | ✓ |
| 58 | BMW · ABS | **marca:** bmw · abs_testigo_encendido | falla_abs, modulo_abs_bmw | R39, R54, R112, R123 | ✓ |
| 59 | BMW · fuga de aceite | **marca:** bmw · fuga_aceite | fuga_transmision_final_bmw | R55, R124 | ✓ |
| 60 | BMW · balancines | **marca:** bmw · perdida_potencia, ruido_golpeteo_motor | balancines_valvulas_bmw | R56, R125 | ✓ |
| 61 | Ducati · servicio desmo | **marca:** ducati · servicio_valvulas_vencido | correas_desmo_ducati, recomendar_correas_desmo_ducati | R57, R126 | ✓ |
| 62 | Ducati · calor en tráfico | **marca:** ducati · falla_en_trafico_lento, sobrecalentamiento | calor_cilindro_trasero_ducati | R58, R127 | ✓ |
| 63 | Ducati · embrague seco | **marca:** ducati · embrague_patina, ruido_embrague_seco | embrague_seco_ducati | R59, R128 | ✓ |
| 64 | Ducati · regulador | **marca:** ducati · bateria_se_descarga, luces_debiles_en_marcha | regulador_ducati | R4, R60, R129 | ✓ |
| 65 | Triumph · fuga de refrigerante | **marca:** triumph · nivel_refrigerante_bajo, sobrecalentamiento | fuga_refrigerante, fuga_refrigerante_triumph | R22, R62, R131 | ✓ |
| 66 | Triumph · cuerpos de aceleración | **marca:** triumph · olor_gasolina, ralenti_inestable | cuerpos_aceleracion_triumph | R63, R132 | ✓ |
| 67 | Yamaha · tensor de distribución | **marca:** yamaha · ruido_cadena_distribucion | tensor_distribucion_yamaha | R65, R134 | ✓ |
| 68 | Yamaha · sensor de inyección | **marca:** yamaha · ralenti_inestable, testigo_check_engine | sensor_inyeccion_yamaha | R66, R135 | ✓ |
| 69 | Honda · variador de scooter | **marca:** honda · ruido_variador, vibracion_al_arrancar_scooter | variador_cvt_desgastado, variador_honda | R34, R69, R107, R138 | ✓ |
| 70 | Honda · tensor | **marca:** honda · perdida_potencia, ruido_cadena_distribucion | tensor_distribucion_desgastado, tensor_distribucion_honda | R27, R68, R100, R137 | ✓ |
| 71 | Kawasaki · bomba de agua | **marca:** kawasaki · nivel_refrigerante_bajo, sobrecalentamiento | sello_bomba_agua_kawasaki | R22, R71, R140 | ✓ |
| 72 | Kawasaki · termostato en tráfico | **marca:** kawasaki · falla_en_trafico_lento, sobrecalentamiento | termostato_ventilador_kawasaki | R72, R141 | ✓ |
| 73 | Suzuki · carburación | **marca:** suzuki · gasolina_vieja, ralenti_inestable | carburacion_suzuki | R74, R143 | ✓ |
| 74 | Suzuki · sensor de acelerador | **marca:** suzuki · perdida_potencia, testigo_check_engine | sensor_acelerador_suzuki | R75, R144 | ✓ |
| 75 | Harley · tensores de levas | **marca:** harley · ruido_cadena_distribucion | tensores_levas_harley | R77, R146 | ✓ |
| 76 | Harley · fuga de aceite | **marca:** harley · fuga_aceite | fugas_aceite_harley | R78, R147 | ✓ |
| 77 | Cruce: síntomas Ducati en una Yamaha (no aplica) | **marca:** yamaha · servicio_valvulas_vencido | sin conclusión | ninguna | ✓ |
| 78 | KTM · escenario complejo (carga + calor + válvulas + frenos) | **marca:** ktm · bateria_se_descarga, falla_en_trafico_lento, freno_esponjoso, luces_debiles_en_marcha, nivel_liquido_bajo, nivel_refrigerante_bajo, olor_quemado_electrico, perdida_potencia, servicio_valvulas_vencido, sobrecalentamiento | alerta_frenos, fuga_circuito_frenos, fuga_refrigerante, regulador_rectificador_danado, regulador_rectificador_ktm, valvulas_fuera_de_rango_ktm, ventilacion_trafico_ktm | R4, R5, R22, R37, R46, R48, R49, R50, R84, R110, R117, R118, R119 | ✓ |
