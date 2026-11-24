# Casos de prueba

107 de 107 casos aprobados. Se ejecutan con `python tests/test_sbc.py`.
Cada caso exige que aparezcan las conclusiones esperadas y que no aparezcan las prohibidas. Los casos de modelo comprueban
que los síntomas que no aplican se rechazan y que los diagnósticos incompatibles quedan descartados.

| Caso | Descripción | Hechos iniciales | Conclusiones esperadas | Reglas disparadas | Estado |
|---|---|---|---|---|---|
| 1 | Batería descargada | luces_debiles, marcha_no_gira | bateria_descargada, recomendar_bateria_descargada | R1, R87 | ✓ |
| 2 | Batería al final de su vida | bateria_se_descarga, luces_debiles, marcha_no_gira | bateria_descargada, bateria_vida_util_terminada, recomendar_bateria_vida_util_terminada | R1, R3, R87, R89 | ✓ |
| 3 | Bornes sulfatados (no es la batería) | bornes_sulfatados, marcha_no_gira | conexion_bateria_deficiente | R2, R88 | ✓ |
| 4 | Falla de carga con olor a quemado | bateria_se_descarga, luces_debiles_en_marcha, olor_quemado_electrico | falla_sistema_carga, recomendar_regulador_rectificador_danado, regulador_rectificador_danado | R4, R5, R91 | ✓ |
| 5 | Cortocircuito (fusible + olor, sin falla de carga) | fusible_quemado_repetido, olor_quemado_electrico | cortocircuito_instalacion | R6, R90 | ✓ |
| 6 | Bujía sucia | bujia_sucia, marcha_gira, sin_chispa | bujia_danada, falla_encendido, recomendar_bujia_danada | R7, R8, R92 | ✓ |
| 7 | Falla con lluvia | falla_con_humedad, marcha_gira, sin_chispa | humedad_en_encendido | R7, R9, R93 | ✓ |
| 8 | Sensor de encendido | marcha_gira, sin_chispa, testigo_check_engine | sensor_encendido_defectuoso | R7, R10, R94 | ✓ |
| 9 | Bomba de gasolina | marcha_gira, no_llega_gasolina, sin_ruido_bomba | bomba_gasolina_danada, falla_alimentacion | R11, R13, R96 | ✓ |
| 10 | Moto parada con gasolina vieja | gasolina_vieja, marcha_gira, no_llega_gasolina | carburador_inyectores_tapados | R11, R12, R95 | ✓ |
| 11 | Filtro de aire obstruido | filtro_aire_sucio, perdida_potencia, tirones | filtro_aire_obstruido, mezcla_irregular, recomendar_filtro_aire_obstruido | R14, R15, R97 | ✓ |
| 12 | Combustible degradado | gasolina_vieja, perdida_potencia, tirones | combustible_contaminado | R14, R16, R98 | ✓ |
| 13 | Ralentí mal ajustado | ralenti_inestable, se_apaga_en_ralenti | ralenti_mal_ajustado | R17, R99 | ✓ |
| 14 | Mezcla rica con sensor | consumo_gasolina_alto, humo_negro, testigo_check_engine | mezcla_rica, sensor_inyeccion_defectuoso | R18, R19, R100 | ✓ |
| 15 | Mezcla rica sin check engine | consumo_gasolina_alto, humo_negro | mezcla_rica | R18 | ✓ |
| 16 | Aros desgastados | consumo_aceite, humo_azul | desgaste_aros, recomendar_desgaste_aros | R20, R101 | ✓ |
| 17 | Fuga por sello | consumo_aceite, fuga_aceite | sello_o_empaque_fuga | R28, R108 | ✓ |
| 18 | Empaque de culata (ALERTA) | aceite_lechoso, humo_blanco, nivel_refrigerante_bajo | alerta_culata, empaque_culata_danado | R21, R45, R102 | ✓ |
| 19 | Humo blanco sin aceite lechoso | humo_blanco, nivel_refrigerante_bajo | sin conclusión | ninguna | ✓ |
| 20 | Fuga de refrigerante | nivel_refrigerante_bajo, sobrecalentamiento | fuga_refrigerante | R22 | ✓ |
| 21 | Ventilador parado | sobrecalentamiento, ventilador_no_gira | falla_ventilador | R23, R103 | ✓ |
| 22 | Aceite vencido y calentamiento | aceite_vencido, sobrecalentamiento | lubricacion_deficiente, necesita_cambio_aceite | R24, R25, R104, R105 | ✓ |
| 23 | Lubricación crítica (ALERTA) | luz_presion_aceite, ruido_golpeteo_motor | alerta_lubricacion, lubricacion_critica | R26, R44, R106 | ✓ |
| 24 | Tensor de distribución | perdida_potencia, ruido_cadena_distribucion | tensor_distribucion_desgastado | R27, R107 | ✓ |
| 25 | Kit de arrastre | cadena_floja, ruido_cadena | kit_arrastre_desgastado | R29, R109 | ✓ |
| 26 | Cadena seca | cadena_oxidada, ruido_cadena | cadena_sin_lubricar | R30, R110 | ✓ |
| 27 | Cadena completa (floja, oxidada y ruidosa) | cadena_floja, cadena_oxidada, ruido_cadena | cadena_sin_lubricar, kit_arrastre_desgastado | R29, R30, R109, R110 | ✓ |
| 28 | Embrague patina | embrague_patina, perdida_potencia | embrague_desgastado | R31, R111 | ✓ |
| 29 | Embrague duro | cambios_duros, palanca_embrague_dura | circuito_embrague_defectuoso | R32, R112 | ✓ |
| 30 | Caja de cambios | cambios_duros, salto_marchas | caja_cambios_desgastada | R33, R113 | ✓ |
| 31 | Scooter con variador gastado | ruido_variador, vibracion_al_arrancar_scooter | variador_cvt_desgastado | R34, R114 | ✓ |
| 32 | Pastillas | freno_chirrido, recorrido_freno_largo | pastillas_desgastadas | R35, R115 | ✓ |
| 33 | Aire/humedad en frenos | freno_esponjoso, liquido_freno_oscuro | aire_humedad_frenos | R36, R116 | ✓ |
| 34 | Fuga en frenos (ALERTA) | freno_esponjoso, nivel_liquido_bajo | alerta_frenos, fuga_circuito_frenos | R37, R46, R117 | ✓ |
| 35 | Disco rayado | disco_con_surcos, vibracion_al_frenar | disco_danado | R38, R118 | ✓ |
| 36 | ABS genérico | abs_testigo_encendido | falla_abs | R39, R119 | ✓ |
| 37 | Retenes de horquilla | fuga_aceite_barra, rebote_excesivo | retenes_horquilla_danados | R40, R120 | ✓ |
| 38 | Dirección floja | direccion_floja, vibracion_manubrio | alerta_direccion, rodamientos_direccion_flojos | R41, R47, R121 | ✓ |
| 39 | Balanceo | llanta_desgaste_irregular, vibracion_manubrio | balanceo_alineacion | R42, R122 | ✓ |
| 40 | Presión de llantas | llanta_baja_presion | presion_llantas_incorrecta | R43, R123 | ✓ |
| 41 | Servicio mayor (aceite + filtro + bujía) | aceite_vencido, bujia_sucia, filtro_aire_sucio, marcha_gira, perdida_potencia, sin_chispa, tirones | bujia_danada, filtro_aire_obstruido, necesita_cambio_aceite, recomendar_servicio_mayor | R7, R8, R14, R15, R25, R79, R92, R97, R105 | ✓ |
| 42 | Moto en mal estado general (muchos sistemas) | aceite_vencido, bujia_sucia, cadena_floja, consumo_aceite, direccion_floja, filtro_aire_sucio, freno_chirrido, gasolina_vieja, humo_azul, llanta_baja_presion, marcha_gira, no_llega_gasolina, perdida_potencia, recorrido_freno_largo, ruido_cadena, sin_chispa, tirones, vibracion_manubrio | bujia_danada, carburador_inyectores_tapados, desgaste_aros, filtro_aire_obstruido, kit_arrastre_desgastado, pastillas_desgastadas, presion_llantas_incorrecta, recomendar_servicio_mayor, rodamientos_direccion_flojos | R7, R8, R11, R12, R14, R15, R16, R20, R25, R29, R35, R41, R43, R47, R79, R92, R95, R97, R98, R101, R105, R109, R115, R121, R123 | ✓ |
| 43 | Sin conclusión: síntoma aislado (luces débiles) | luces_debiles | sin conclusión | ninguna | ✓ |
| 44 | Sin conclusión: freno chirría pero recorrido normal | freno_chirrido | sin conclusión | ninguna | ✓ |
| 45 | Borde: evidencia parcial de falla de encendido | marcha_gira, sin_chispa | falla_encendido | R7 | ✓ |
| 46 | Error: sin síntomas | (ninguno) | error de validación | error de validación | ✓ |
| 47 | Error: síntomas contradictorios | marcha_gira, marcha_no_gira | error de validación | error de validación | ✓ |
| 48 | Error: síntoma inexistente | motor_volador | error de validación | error de validación | ✓ |
| 49 | Error: marca como síntoma | marca_ktm, tirones | error de validación | error de validación | ✓ |
| 50 | Error: marca inexistente | **marca:** mercedes · tirones | error de validación | error de validación | ✓ |
| 51 | KTM · pierde carga | **marca:** ktm · bateria_se_descarga, luces_debiles_en_marcha | falla_sistema_carga, recomendar_regulador_rectificador_ktm, regulador_rectificador_ktm | R4, R48, R124 | ✓ |
| 52 | Control: mismos síntomas sin marca (no sale diagnóstico de marca) | bateria_se_descarga, luces_debiles_en_marcha | falla_sistema_carga | R4 | ✓ |
| 53 | KTM · se calienta en tráfico | **marca:** ktm · falla_en_trafico_lento, sobrecalentamiento | ventilacion_trafico_ktm | R49, R125 | ✓ |
| 54 | KTM · válvulas vencidas | **marca:** ktm · perdida_potencia, servicio_valvulas_vencido | valvulas_fuera_de_rango_ktm | R50, R126 | ✓ |
| 55 | Aprilia · ride-by-wire | **marca:** aprilia · ralenti_inestable, testigo_check_engine | sensor_acelerador_aprilia | R52, R128 | ✓ |
| 56 | Aprilia · estátor | **marca:** aprilia · bateria_se_descarga, olor_quemado_electrico | estator_aprilia | R53, R129 | ✓ |
| 57 | Aprilia · regulador | **marca:** aprilia · bateria_se_descarga, luces_debiles_en_marcha | regulador_rectificador_aprilia | R4, R51, R127 | ✓ |
| 58 | BMW · ABS | **marca:** bmw · abs_testigo_encendido | falla_abs, modulo_abs_bmw | R39, R54, R119, R130 | ✓ |
| 59 | BMW · fuga de aceite | **marca:** bmw · fuga_aceite | fuga_transmision_final_bmw | R55, R131 | ✓ |
| 60 | BMW · balancines | **marca:** bmw · perdida_potencia, ruido_golpeteo_motor | balancines_valvulas_bmw | R56, R132 | ✓ |
| 61 | Ducati · servicio desmo | **marca:** ducati · servicio_valvulas_vencido | correas_desmo_ducati, recomendar_correas_desmo_ducati | R57, R133 | ✓ |
| 62 | Ducati · calor en tráfico | **marca:** ducati · falla_en_trafico_lento, sobrecalentamiento | calor_cilindro_trasero_ducati | R58, R134 | ✓ |
| 63 | Ducati · embrague seco | **marca:** ducati · embrague_patina, ruido_embrague_seco | embrague_seco_ducati | R59, R135 | ✓ |
| 64 | Ducati · regulador | **marca:** ducati · bateria_se_descarga, luces_debiles_en_marcha | regulador_ducati | R4, R60, R136 | ✓ |
| 65 | Triumph · fuga de refrigerante | **marca:** triumph · nivel_refrigerante_bajo, sobrecalentamiento | fuga_refrigerante, fuga_refrigerante_triumph | R22, R62, R138 | ✓ |
| 66 | Triumph · cuerpos de aceleración | **marca:** triumph · olor_gasolina, ralenti_inestable | cuerpos_aceleracion_triumph | R63, R139 | ✓ |
| 67 | Yamaha · tensor de distribución | **marca:** yamaha · ruido_cadena_distribucion | tensor_distribucion_yamaha | R65, R141 | ✓ |
| 68 | Yamaha · sensor de inyección | **marca:** yamaha · ralenti_inestable, testigo_check_engine | sensor_inyeccion_yamaha | R66, R142 | ✓ |
| 69 | Honda · variador de scooter | **marca:** honda · ruido_variador, vibracion_al_arrancar_scooter | variador_cvt_desgastado, variador_honda | R34, R69, R114, R145 | ✓ |
| 70 | Honda · tensor | **marca:** honda · perdida_potencia, ruido_cadena_distribucion | tensor_distribucion_desgastado, tensor_distribucion_honda | R27, R68, R107, R144 | ✓ |
| 71 | Kawasaki · bomba de agua | **marca:** kawasaki · nivel_refrigerante_bajo, sobrecalentamiento | sello_bomba_agua_kawasaki | R22, R71, R147 | ✓ |
| 72 | Kawasaki · termostato en tráfico | **marca:** kawasaki · falla_en_trafico_lento, sobrecalentamiento | termostato_ventilador_kawasaki | R72, R148 | ✓ |
| 73 | Suzuki · carburación | **marca:** suzuki · gasolina_vieja, ralenti_inestable | carburacion_suzuki | R74, R150 | ✓ |
| 74 | Suzuki · sensor de acelerador | **marca:** suzuki · perdida_potencia, testigo_check_engine | sensor_acelerador_suzuki | R75, R151 | ✓ |
| 75 | Harley · tensores de levas | **marca:** harley · ruido_cadena_distribucion | tensores_levas_harley | R77, R153 | ✓ |
| 76 | Harley · fuga de aceite | **marca:** harley · fuga_aceite | fugas_aceite_harley | R78, R154 | ✓ |
| 77 | Cruce: síntomas Ducati en una Yamaha (no aplica) | **marca:** yamaha · servicio_valvulas_vencido | sin conclusión | ninguna | ✓ |
| 78 | KTM · escenario complejo (carga + calor + válvulas + frenos) | **marca:** ktm · bateria_se_descarga, falla_en_trafico_lento, freno_esponjoso, luces_debiles_en_marcha, nivel_liquido_bajo, nivel_refrigerante_bajo, olor_quemado_electrico, perdida_potencia, servicio_valvulas_vencido, sobrecalentamiento | alerta_frenos, fuga_circuito_frenos, fuga_refrigerante, regulador_rectificador_danado, regulador_rectificador_ktm, valvulas_fuera_de_rango_ktm, ventilacion_trafico_ktm | R4, R5, R22, R37, R46, R48, R49, R50, R91, R117, R124, R125, R126 | ✓ |
| 79 | Modelo · KTM 390 Duke pierde carga | **modelo:** ktm_390_duke · bateria_se_descarga, luces_debiles_en_marcha | regulador_rectificador_ktm | R4, R48, R124 | ✓ |
| 80 | Modelo · NMAX (scooter): variador | **modelo:** yamaha_nmax_155 · ruido_variador, vibracion_al_arrancar_scooter | recomendar_variador_cvt_desgastado, variador_cvt_desgastado | R34, R114 | ✓ |
| 81 | Modelo · NMAX con síntoma de cadena (no aplica) | **modelo:** yamaha_nmax_155 · ruido_cadena | error de validación | error de validación | ✓ |
| 82 | Modelo · PCX: el scooter patina | **modelo:** honda_pcx · scooter_patina_al_acelerar | correa_cvt_desgastada | R80, R155 | ✓ |
| 83 | Modelo · PCX: variador (regla Honda) | **modelo:** honda_pcx · ruido_variador, vibracion_al_arrancar_scooter | variador_cvt_desgastado, variador_honda | R34, R69, R114, R145 | ✓ |
| 84 | Modelo · PCX con embrague manual (no aplica) | **modelo:** honda_pcx · embrague_patina | error de validación | error de validación | ✓ |
| 85 | Modelo · BMW R 1250 GS (cardán): ruido y fuga | **modelo:** bmw_r_1250_gs · fuga_aceite, ruido_transmision_cardan | cardan_con_fuga_o_desgaste, fuga_transmision_final_bmw | R55, R82, R131, R157 | ✓ |
| 86 | Modelo · BMW R 1250 GS con cadena (no aplica) | **modelo:** bmw_r_1250_gs · ruido_cadena | error de validación | error de validación | ✓ |
| 87 | Modelo · BMW F 850 GS (cadena): una fuga no es del cardán | **modelo:** bmw_f_850_gs · fuga_aceite | sin conclusión | ninguna | ✓ |
| 88 | Modelo · BMW F 850 GS: kit de arrastre | **modelo:** bmw_f_850_gs · cadena_floja, ruido_cadena | kit_arrastre_desgastado | R29, R109 | ✓ |
| 89 | Modelo · Harley Fat Boy (correa) | **modelo:** harley_fat_boy · correa_final_desgastada | correa_transmision_desgastada, recomendar_correa_transmision_desgastada | R81, R156 | ✓ |
| 90 | Modelo · Harley Iron 883: tensores de levas | **modelo:** harley_iron_883 · ruido_cadena_distribucion | tensores_levas_harley | R77, R153 | ✓ |
| 91 | Modelo · Scrambler 800 (aire) se calienta en tráfico | **modelo:** ducati_scrambler_800 · falla_en_trafico_lento, sobrecalentamiento | calentamiento_motor_aire_trafico, calor_cilindro_trasero_ducati | R58, R83, R134, R158 | ✓ |
| 92 | Modelo · Scrambler 800 sin radiador (refrigerante no aplica) | **modelo:** ducati_scrambler_800 · nivel_refrigerante_bajo | error de validación | error de validación | ✓ |
| 93 | Modelo · Panigale V4 (líquida) se calienta en tráfico | **modelo:** ducati_panigale_v4 · falla_en_trafico_lento, sobrecalentamiento | calor_cilindro_trasero_ducati | R58, R134 | ✓ |
| 94 | Modelo · KLX 230 (aire): termostato Kawasaki bloqueado | **modelo:** kawasaki_klx_230 · falla_en_trafico_lento, sobrecalentamiento | calentamiento_motor_aire_trafico | R83, R158 | ✓ |
| 95 | Modelo · KLX 230 con ventilador (no aplica) | **modelo:** kawasaki_klx_230 · ventilador_no_gira | error de validación | error de validación | ✓ |
| 96 | Modelo · Z650 (líquida): termostato Kawasaki | **modelo:** kawasaki_z650 · falla_en_trafico_lento, sobrecalentamiento | termostato_ventilador_kawasaki | R72, R148 | ✓ |
| 97 | Modelo · Tiger 900: fuga de refrigerante | **modelo:** triumph_tiger_900 · nivel_refrigerante_bajo, sobrecalentamiento | fuga_refrigerante, fuga_refrigerante_triumph | R22, R62, R138 | ✓ |
| 98 | Modelo · F 850 GS: aceite lechoso + refrigerante bajo | **modelo:** bmw_f_850_gs · aceite_lechoso, nivel_refrigerante_bajo | fuga_interna_refrigerante | R85, R160 | ✓ |
| 99 | Modelo · GN 125 (carburador) con gasolina vieja | **modelo:** suzuki_gn_125 · gasolina_vieja, ralenti_inestable | carburacion_suzuki, carburador_sucio_carburado | R74, R84, R150, R159 | ✓ |
| 100 | Modelo · GN 125 con check engine (carburador, no aplica) | **modelo:** suzuki_gn_125 · testigo_check_engine | error de validación | error de validación | ✓ |
| 101 | Modelo · Yamaha R15: tensor de distribución | **modelo:** yamaha_r15 · ruido_cadena_distribucion | tensor_distribucion_r15, tensor_distribucion_yamaha | R65, R86, R141, R161 | ✓ |
| 102 | Modelo · Yamaha MT-07: tensor (no es la regla de la R15) | **modelo:** yamaha_mt_07 · ruido_cadena_distribucion | tensor_distribucion_yamaha | R65, R141 | ✓ |
| 103 | Modelo · Aprilia RSV4: ride-by-wire | **modelo:** aprilia_rsv4_1100 · ralenti_inestable, testigo_check_engine | sensor_acelerador_aprilia | R52, R128 | ✓ |
| 104 | Modelo · Honda CB190R: embrague | **modelo:** honda_cb190r · embrague_patina, perdida_potencia | embrague_desgastado | R31, R111 | ✓ |
| 105 | Error: modelo de otra marca | **modelo:** ktm_390_duke · **marca:** ducati · tirones | error de validación | error de validación | ✓ |
| 106 | Error: modelo inexistente | **modelo:** ktm_inexistente · tirones | error de validación | error de validación | ✓ |
| 107 | Modelo · KTM 790 Duke, escenario complejo | **modelo:** ktm_790_duke · bateria_se_descarga, cadena_floja, falla_en_trafico_lento, freno_esponjoso, luces_debiles_en_marcha, nivel_liquido_bajo, nivel_refrigerante_bajo, olor_quemado_electrico, perdida_potencia, ruido_cadena, servicio_valvulas_vencido, sobrecalentamiento | alerta_frenos, fuga_circuito_frenos, fuga_refrigerante, kit_arrastre_desgastado, regulador_rectificador_ktm, valvulas_fuera_de_rango_ktm, ventilacion_trafico_ktm | R4, R5, R22, R29, R37, R46, R48, R49, R50, R91, R109, R117, R124, R125, R126 | ✓ |
