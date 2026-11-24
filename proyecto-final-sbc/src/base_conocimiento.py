"""Base de conocimiento del taller de motos: marcas, predicados y reglas de producción.

Python puro (sin librerías). Los hechos son textos; una regla es un diccionario con
"si" (condiciones) y "entonces" (conclusión), igual que en el notebook de ejemplo.
"""

from catalogo_modelos import MODELOS, ATRIBUTOS


# Marcas del taller: clave -> (nombre, país, modelos de ejemplo)
MARCAS = {
    "ktm":       ("KTM", "Austria", "390 Duke, 790/890 Duke, 1290 Super Duke R, RC 390"),
    "aprilia":   ("Aprilia", "Italia", "RS 660, Tuono 660, RSV4, Shiver, Dorsoduro"),
    "bmw":       ("BMW Motorrad", "Alemania", "R 1250 GS, R 1200 GS, F 850 GS, G 310 R, S 1000 RR"),
    "ducati":    ("Ducati", "Italia", "Monster, Panigale V2/V4, Multistrada, Scrambler, Diavel"),
    "triumph":   ("Triumph", "Reino Unido", "Bonneville, Tiger 900, Street Triple, Speed Triple, Trident"),
    "yamaha":    ("Yamaha", "Japón", "R15, MT-03, MT-07, MT-09, NMAX, FZ"),
    "honda":     ("Honda", "Japón", "CB190R, XR150L, CBR500R, PCX, CB500F, Africa Twin"),
    "kawasaki":  ("Kawasaki", "Japón", "Ninja 400, Z650, Z900, Versys 650, KLX"),
    "suzuki":    ("Suzuki", "Japón", "GSX-R, V-Strom 650, Gixxer, GN125"),
    "harley":    ("Harley-Davidson", "EE. UU.", "Sportster, Softail, Street Glide, Fat Boy"),
}

# Predicados: nombre -> (clase, grupo, texto legible, acción sugerida, marca)
PREDICADOS = {}

def sintoma(nombre, grupo, texto):
    PREDICADOS[nombre] = ("sintoma", grupo, texto, None, None)

def contexto(nombre, texto, marca):
    PREDICADOS[nombre] = ("contexto", "Marca", texto, None, marca)

for clave in MARCAS:
    contexto("marca_" + clave, "Marca: " + MARCAS[clave][0], clave)

# --- Encendido y electricidad ---
g = "Encendido y electricidad"
sintoma("marcha_no_gira", g, "La marcha no hace girar el motor (solo clic o silencio)")
sintoma("luces_debiles", g, "Luces y pito débiles al intentar arrancar")
sintoma("bornes_sulfatados", g, "Bornes de la batería sulfatados o flojos")
sintoma("marcha_gira", g, "La marcha gira el motor pero no enciende")
sintoma("sin_chispa", g, "No hay chispa en la bujía")
sintoma("bujia_sucia", g, "Bujía negra, húmeda o con carbón")
sintoma("falla_con_humedad", g, "Falla o se apaga con lluvia o después de lavar")
sintoma("bateria_se_descarga", g, "La batería se descarga sola en pocos días")
sintoma("luces_debiles_en_marcha", g, "Luces débiles o parpadeantes con el motor andando")
sintoma("fusible_quemado_repetido", g, "Se quema el mismo fusible repetidas veces")
sintoma("olor_quemado_electrico", g, "Olor a quemado eléctrico o cables calientes")
sintoma("testigo_check_engine", g, "Testigo de falla del motor (check engine) encendido")

# --- Combustible y alimentación ---
g = "Combustible y alimentación"
sintoma("no_llega_gasolina", g, "No llega gasolina al carburador o inyector")
sintoma("sin_ruido_bomba", g, "No se oye la bomba de gasolina al dar contacto")
sintoma("gasolina_vieja", g, "La moto estuvo parada más de un mes con la misma gasolina")
sintoma("tirones", g, "La moto da tirones al acelerar")
sintoma("perdida_potencia", g, "Pérdida de potencia")
sintoma("filtro_aire_sucio", g, "Filtro de aire sucio u obstruido")
sintoma("ralenti_inestable", g, "Ralentí inestable (muy alto, bajo u oscilante)")
sintoma("se_apaga_en_ralenti", g, "Se apaga en ralentí o al soltar el acelerador")
sintoma("consumo_gasolina_alto", g, "Consumo de gasolina más alto de lo normal")
sintoma("olor_gasolina", g, "Olor fuerte a gasolina")
sintoma("humo_negro", g, "Humo negro por el escape")

# --- Motor, lubricación y refrigeración ---
g = "Motor, lubricación y refrigeración"
sintoma("humo_azul", g, "Humo azulado por el escape")
sintoma("humo_blanco", g, "Humo blanco persistente por el escape")
sintoma("consumo_aceite", g, "Consumo excesivo de aceite")
sintoma("aceite_lechoso", g, "Aceite de aspecto lechoso o espumoso")
sintoma("aceite_vencido", g, "Aceite con más de 5.000 km o 6 meses sin cambio")
sintoma("fuga_aceite", g, "Fuga o manchas de aceite en el motor")
sintoma("sobrecalentamiento", g, "El motor se sobrecalienta")
sintoma("nivel_refrigerante_bajo", g, "Nivel de refrigerante bajo")
sintoma("ventilador_no_gira", g, "El ventilador del radiador no gira")
sintoma("falla_en_trafico_lento", g, "El problema aparece en tráfico lento o con calor")
sintoma("ruido_golpeteo_motor", g, "Golpeteo metálico dentro del motor")
sintoma("ruido_cadena_distribucion", g, "Traqueteo en la parte alta del motor")
sintoma("luz_presion_aceite", g, "Testigo de presión de aceite encendido")
sintoma("servicio_valvulas_vencido", g, "Ajuste de válvulas o correas vencido según el manual")

# --- Transmisión y embrague ---
g = "Transmisión y embrague"
sintoma("ruido_cadena", g, "Ruido metálico en la cadena de transmisión")
sintoma("cadena_floja", g, "Cadena floja o con holgura excesiva")
sintoma("cadena_oxidada", g, "Cadena oxidada o seca")
sintoma("embrague_patina", g, "El embrague patina (sube revoluciones sin avanzar)")
sintoma("palanca_embrague_dura", g, "Palanca de embrague dura o sin recorrido")
sintoma("cambios_duros", g, "Los cambios entran duros")
sintoma("salto_marchas", g, "Se salen las marchas")
sintoma("ruido_embrague_seco", g, "Traqueteo metálico del embrague en ralentí")
sintoma("vibracion_al_arrancar_scooter", g, "Vibración al arrancar (scooter automático)")
sintoma("ruido_variador", g, "Ruido o zumbido en el variador (scooter)")

# --- Frenos ---
g = "Frenos"
sintoma("freno_chirrido", g, "Chirrido al frenar")
sintoma("recorrido_freno_largo", g, "La palanca o pedal de freno recorre demasiado")
sintoma("freno_esponjoso", g, "Freno esponjoso o blando")
sintoma("nivel_liquido_bajo", g, "Nivel de líquido de frenos bajo")
sintoma("liquido_freno_oscuro", g, "Líquido de frenos oscuro o con más de 2 años")
sintoma("vibracion_al_frenar", g, "Vibración o pulsación al frenar")
sintoma("disco_con_surcos", g, "Disco de freno con surcos o rayado")
sintoma("abs_testigo_encendido", g, "Testigo del ABS encendido")

# --- Suspensión, dirección y llantas ---
g = "Suspensión, dirección y llantas"
sintoma("fuga_aceite_barra", g, "Aceite en las barras de la horquilla")
sintoma("rebote_excesivo", g, "Suspensión con rebote excesivo")
sintoma("vibracion_manubrio", g, "Vibración en el manubrio")
sintoma("direccion_floja", g, "Dirección floja o con golpeteo al frenar")
sintoma("llanta_desgaste_irregular", g, "Llanta con desgaste irregular")
sintoma("llanta_baja_presion", g, "Llantas con presión baja")

# Pares de síntomas que no pueden darse a la vez (validación de entrada)
CONTRADICCIONES = [("marcha_gira", "marcha_no_gira")]


# Conclusiones intermedias y diagnósticos genéricos (aplican a cualquier marca)
def intermedio(nombre, texto):
    PREDICADOS[nombre] = ("intermedio", "Conclusión intermedia", texto, None, None)

def diagnostico(nombre, texto, accion, marca=None):
    grupo = "Diagnóstico" if marca is None else "Diagnóstico · " + MARCAS[marca][0]
    PREDICADOS[nombre] = ("diagnostico", grupo, texto, accion, marca)

intermedio("falla_sistema_carga", "Falla en el sistema de carga")
intermedio("falla_encendido", "Falla en el sistema de encendido")
intermedio("falla_alimentacion", "Falla en la alimentación de combustible")
intermedio("mezcla_irregular", "Mezcla aire-combustible irregular")
intermedio("mezcla_rica", "Mezcla demasiado rica")
intermedio("fuga_refrigerante", "Fuga o pérdida de refrigerante")

# --- Eléctrico ---
diagnostico("bateria_descargada", "Batería descargada", "Cargar la batería; si no retiene carga, cambiarla")
diagnostico("conexion_bateria_deficiente", "Conexión de batería deficiente", "Limpiar y apretar bornes y aplicar protector")
diagnostico("bateria_vida_util_terminada", "Batería al final de su vida útil", "Cambiar la batería y verificar el sistema de carga")
diagnostico("cortocircuito_instalacion", "Cortocircuito en la instalación eléctrica", "Revisar mazo de cables, conectores y accesorios añadidos; nunca subir el amperaje del fusible")
diagnostico("regulador_rectificador_danado", "Regulador-rectificador quemado", "Medir voltaje de carga a 3.000 rpm y cambiar el regulador-rectificador")
diagnostico("bujia_danada", "Bujía dañada o contaminada", "Cambiar la bujía y revisar su calibración")
diagnostico("humedad_en_encendido", "Humedad en capuchón o bobina", "Secar y limpiar capuchón y conectores; cambiar el capuchón si está agrietado")
diagnostico("sensor_encendido_defectuoso", "Sensor del sistema de encendido defectuoso", "Escanear códigos de falla; revisar sensor de cigüeñal y bobina")
# --- Combustible ---
diagnostico("carburador_inyectores_tapados", "Carburador o inyectores tapados por gasolina vieja", "Drenar el combustible y limpiar carburador o inyectores")
diagnostico("bomba_gasolina_danada", "Bomba de gasolina dañada", "Medir presión y cambiar la bomba o su relé")
diagnostico("filtro_aire_obstruido", "Filtro de aire obstruido", "Limpiar o cambiar el filtro de aire")
diagnostico("combustible_contaminado", "Combustible contaminado o degradado", "Drenar el tanque y reponer gasolina fresca")
diagnostico("ralenti_mal_ajustado", "Ralentí mal ajustado o cuerpo de aceleración sucio", "Limpiar el cuerpo de aceleración y reajustar el ralentí")
diagnostico("sensor_inyeccion_defectuoso", "Sensor de inyección u oxígeno defectuoso", "Escanear códigos; revisar sensor de oxígeno e inyectores")
# --- Motor y refrigeración ---
diagnostico("desgaste_aros", "Desgaste de aros o retenes de válvula", "Medir compresión y llevar el motor a revisión")
diagnostico("empaque_culata_danado", "Empaque de culata dañado", "No usar la moto; desarmar y revisar culata y empaque")
diagnostico("falla_ventilador", "Ventilador de refrigeración sin funcionar", "Revisar fusible, relé y motor del ventilador")
diagnostico("lubricacion_deficiente", "Lubricación deficiente por aceite vencido", "Cambiar aceite y filtro de inmediato")
diagnostico("necesita_cambio_aceite", "Cambio de aceite pendiente", "Cambiar aceite y filtro según el manual")
diagnostico("lubricacion_critica", "Lubricación crítica con riesgo de falla del motor", "Apagar el motor; revisar nivel y presión de aceite antes de volver a encender")
diagnostico("tensor_distribucion_desgastado", "Tensor de cadena de distribución desgastado", "Cambiar el tensor y revisar la cadena de distribución")
diagnostico("sello_o_empaque_fuga", "Fuga por sello o empaque del motor", "Localizar la fuga y cambiar el sello o empaque")
# --- Transmisión ---
diagnostico("kit_arrastre_desgastado", "Kit de arrastre desgastado", "Cambiar cadena, piñón y corona en conjunto")
diagnostico("cadena_sin_lubricar", "Cadena sin lubricar", "Limpiar, lubricar y tensionar; cambiarla si está rígida")
diagnostico("embrague_desgastado", "Discos de embrague desgastados", "Medir discos y resortes; cambiar el kit de embrague")
diagnostico("circuito_embrague_defectuoso", "Cable o circuito de embrague defectuoso", "Lubricar o cambiar el cable; purgar si es hidráulico")
diagnostico("caja_cambios_desgastada", "Desgaste en la caja de cambios", "Revisar horquillas y piñones; llevar a revisión de caja")
diagnostico("variador_cvt_desgastado", "Variador CVT desgastado (scooter)", "Cambiar rodillos y correa del variador")
# --- Frenos ---
diagnostico("pastillas_desgastadas", "Pastillas de freno desgastadas", "Cambiar pastillas y revisar discos")
diagnostico("aire_humedad_frenos", "Aire o humedad en el circuito de frenos", "Purgar y cambiar el líquido de frenos")
diagnostico("fuga_circuito_frenos", "Fuga en el circuito de frenos", "Inspeccionar mangueras, bomba y pinzas; reparar antes de circular")
diagnostico("disco_danado", "Disco de freno rayado o alabeado", "Medir espesor; rectificar o cambiar disco y pastillas")
diagnostico("falla_abs", "Falla en el sistema ABS", "Escanear el ABS; revisar sensores de rueda y cableado")
# --- Suspensión y llantas ---
diagnostico("retenes_horquilla_danados", "Retenes de horquilla dañados", "Cambiar retenes y aceite de suspensión")
diagnostico("rodamientos_direccion_flojos", "Rodamientos de dirección flojos", "Ajustar o cambiar los rodamientos de dirección")
diagnostico("balanceo_alineacion", "Balanceo o alineación deficiente", "Balancear las ruedas y alinear")
diagnostico("presion_llantas_incorrecta", "Presión de llantas incorrecta", "Ajustar a la presión del fabricante y revisar el desgaste")


# Diagnósticos propios de cada marca (fallas frecuentes reportadas en la práctica de taller).
# OJO: son hipótesis de trabajo; hay que contrastarlas con el manual de servicio y los llamados a revisión (recall) del fabricante.
# --- KTM ---
diagnostico("regulador_rectificador_ktm", "Regulador-rectificador (falla frecuente en KTM)", "Medir voltaje de carga y cambiar el regulador-rectificador; revisar conectores", "ktm")
diagnostico("ventilacion_trafico_ktm", "Refrigeración insuficiente en tráfico (KTM)", "Revisar ventilador, relé, termostato y refrigerante; evitar ralentí prolongado", "ktm")
diagnostico("valvulas_fuera_de_rango_ktm", "Holgura de válvulas fuera de rango (KTM)", "Medir y ajustar la holgura de válvulas según el intervalo del manual KTM", "ktm")
# --- Aprilia ---
diagnostico("regulador_rectificador_aprilia", "Regulador-rectificador (falla frecuente en Aprilia)", "Medir voltaje de carga; cambiar el regulador y revisar el estátor", "aprilia")
diagnostico("sensor_acelerador_aprilia", "Sensor de acelerador o calibración ride-by-wire (Aprilia)", "Escanear con diagnosis Aprilia, verificar el sensor de acelerador y recalibrar", "aprilia")
diagnostico("estator_aprilia", "Estátor o generador quemado (Aprilia)", "Medir resistencia del estátor y cambiarlo junto con el regulador", "aprilia")
# --- BMW ---
diagnostico("modulo_abs_bmw", "Falla del ABS o servofreno (BMW)", "Escanear con equipo de diagnóstico BMW; revisar sensores y módulo ABS", "bmw")
diagnostico("fuga_transmision_final_bmw", "Fuga en cardán o transmisión final (BMW)", "Revisar nivel y sellos del cardán o transmisión final y cambiar los sellos", "bmw")
diagnostico("balancines_valvulas_bmw", "Desgaste de balancines o tren de válvulas (BMW bóxer)", "Inspeccionar el tren de válvulas y consultar llamados a revisión del modelo", "bmw")
# --- Ducati ---
diagnostico("correas_desmo_ducati", "Servicio de correas y válvulas desmodrómicas vencido (Ducati)", "Cambiar correas de distribución y ajustar válvulas según el manual Ducati", "ducati")
diagnostico("calor_cilindro_trasero_ducati", "Calentamiento del cilindro trasero en tráfico (Ducati)", "Verificar ventilador, refrigerante y mapa; evitar ralentí prolongado", "ducati")
diagnostico("embrague_seco_ducati", "Desgaste del embrague en seco (Ducati)", "Medir discos y campana; cambiar el kit si está fuera de tolerancia", "ducati")
diagnostico("regulador_ducati", "Regulador-rectificador (falla frecuente en Ducati)", "Medir voltaje de carga y cambiar el regulador; revisar conectores", "ducati")
# --- Triumph ---
diagnostico("regulador_estator_triumph", "Regulador o estátor (Triumph)", "Medir voltaje de carga y resistencia del estátor", "triumph")
diagnostico("fuga_refrigerante_triumph", "Manguera o bomba de agua con fuga (Triumph)", "Presurizar el sistema y cambiar la manguera o el sello de la bomba", "triumph")
diagnostico("cuerpos_aceleracion_triumph", "Cuerpos de aceleración desincronizados (Triumph)", "Sincronizar cuerpos de aceleración y limpiar el sistema", "triumph")
# --- Yamaha ---
diagnostico("regulador_yamaha", "Regulador-rectificador (Yamaha)", "Medir voltaje de carga y cambiar el regulador", "yamaha")
diagnostico("tensor_distribucion_yamaha", "Tensor de la cadena de distribución (Yamaha)", "Cambiar el tensor y revisar la cadena de distribución", "yamaha")
diagnostico("sensor_inyeccion_yamaha", "Sensor de inyección (Yamaha)", "Escanear con diagnosis Yamaha y revisar sensores de temperatura y acelerador", "yamaha")
# --- Honda ---
diagnostico("regulador_honda", "Regulador-rectificador (falla frecuente en Honda)", "Medir voltaje de carga y cambiar el regulador; revisar conectores", "honda")
diagnostico("tensor_distribucion_honda", "Tensor automático de la cadena de distribución (Honda)", "Cambiar el tensor y revisar la cadena", "honda")
diagnostico("variador_honda", "Rodillos y correa del variador (scooter Honda)", "Cambiar rodillos y correa del variador", "honda")
# --- Kawasaki ---
diagnostico("estator_regulador_kawasaki", "Estátor o regulador (Kawasaki)", "Medir resistencia del estátor y voltaje de carga; cambiar el componente fallido", "kawasaki")
diagnostico("sello_bomba_agua_kawasaki", "Sello de la bomba de agua (Kawasaki)", "Cambiar el sello mecánico de la bomba de agua", "kawasaki")
diagnostico("termostato_ventilador_kawasaki", "Termostato o ventilador (Kawasaki)", "Probar termostato y ventilador; cambiar el que falle", "kawasaki")
# --- Suzuki ---
diagnostico("regulador_suzuki", "Regulador-rectificador (falla frecuente en Suzuki)", "Medir voltaje de carga y cambiar el regulador; revisar conectores", "suzuki")
diagnostico("carburacion_suzuki", "Carburación o inyectores sucios (Suzuki)", "Limpiar carburador o inyectores y reajustar el ralentí", "suzuki")
diagnostico("sensor_acelerador_suzuki", "Sensor de acelerador o sincronización (Suzuki)", "Escanear, revisar sensor de acelerador y sincronizar", "suzuki")
# --- Harley-Davidson ---
diagnostico("estator_regulador_harley", "Estátor o regulador (Harley-Davidson)", "Medir voltaje de carga y resistencia del estátor", "harley")
diagnostico("tensores_levas_harley", "Tensores de la cadena de levas (Harley-Davidson)", "Revisar y cambiar tensores de la cadena de levas", "harley")
diagnostico("fugas_aceite_harley", "Fuga de aceite típica (Harley-Davidson)", "Revisar empaques, tubos de varillas y bases; cambiar el sello que gotea", "harley")


# Alerta de seguridad y recomendación combinada
PREDICADOS["alerta_lubricacion"] = ("alerta", "Alerta", "ALERTA: no encender el motor, lubricación crítica", None, None)
PREDICADOS["alerta_culata"] = ("alerta", "Alerta", "ALERTA: no circular, posible mezcla de aceite y refrigerante por empaque de culata", None, None)
PREDICADOS["alerta_frenos"] = ("alerta", "Alerta", "ALERTA: no circular, pérdida de líquido en el circuito de frenos", None, None)
PREDICADOS["alerta_direccion"] = ("alerta", "Alerta", "ALERTA: no circular a alta velocidad, dirección floja", None, None)
PREDICADOS["recomendar_servicio_mayor"] = ("recomendacion", "Recomendación",
    "Programar servicio mayor (aceite, filtro de aire y bujía)", None, None)

def texto(hecho):
    """Texto legible de un hecho (si no está en PREDICADOS devuelve el mismo nombre)."""
    return PREDICADOS[hecho][2] if hecho in PREDICADOS else hecho


# Base de conocimiento: cada regla es un diccionario como en el notebook de ejemplo.
# El nombre (R1, R2, ...) se asigna automáticamente según el orden.
base_conocimiento = []

def regla(descripcion, si, entonces, certeza):
    base_conocimiento.append({"nombre": "R" + str(len(base_conocimiento) + 1),
                              "descripcion": descripcion, "si": si,
                              "entonces": entonces, "certeza": certeza})

# ---------- Encendido y electricidad ----------
regla("Sin giro de marcha y luces débiles: batería", ["marcha_no_gira", "luces_debiles"], "bateria_descargada", 0.95)
regla("Sin giro de marcha y bornes sulfatados: mala conexión", ["marcha_no_gira", "bornes_sulfatados"], "conexion_bateria_deficiente", 0.90)
regla("Batería descargada que se vuelve a descargar: fin de vida útil", ["bateria_descargada", "bateria_se_descarga"], "bateria_vida_util_terminada", 0.85)
regla("Batería que se descarga y luces débiles en marcha: falla de carga", ["bateria_se_descarga", "luces_debiles_en_marcha"], "falla_sistema_carga", 0.85)
regla("Falla de carga con olor a quemado: regulador", ["falla_sistema_carga", "olor_quemado_electrico"], "regulador_rectificador_danado", 0.85)
regla("Fusible repetido con olor a quemado: cortocircuito", ["fusible_quemado_repetido", "olor_quemado_electrico"], "cortocircuito_instalacion", 0.90)
regla("Gira pero no hay chispa: falla de encendido", ["marcha_gira", "sin_chispa"], "falla_encendido", 0.90)
regla("Falla de encendido con bujía sucia: bujía dañada", ["falla_encendido", "bujia_sucia"], "bujia_danada", 0.90)
regla("Falla de encendido con humedad: capuchón o bobina", ["falla_encendido", "falla_con_humedad"], "humedad_en_encendido", 0.85)
regla("Falla de encendido con check engine: sensor", ["falla_encendido", "testigo_check_engine"], "sensor_encendido_defectuoso", 0.80)

# ---------- Combustible y alimentación ----------
regla("Gira pero no llega gasolina: falla de alimentación", ["marcha_gira", "no_llega_gasolina"], "falla_alimentacion", 0.90)
regla("Falla de alimentación con gasolina vieja: carburador o inyectores", ["falla_alimentacion", "gasolina_vieja"], "carburador_inyectores_tapados", 0.85)
regla("Falla de alimentación sin ruido de bomba: bomba", ["falla_alimentacion", "sin_ruido_bomba"], "bomba_gasolina_danada", 0.90)
regla("Tirones con falta de potencia: mezcla irregular", ["tirones", "perdida_potencia"], "mezcla_irregular", 0.85)
regla("Mezcla irregular con filtro sucio: filtro de aire", ["mezcla_irregular", "filtro_aire_sucio"], "filtro_aire_obstruido", 0.90)
regla("Mezcla irregular con gasolina vieja: combustible degradado", ["mezcla_irregular", "gasolina_vieja"], "combustible_contaminado", 0.80)
regla("Ralentí inestable y se apaga: ralentí mal ajustado", ["ralenti_inestable", "se_apaga_en_ralenti"], "ralenti_mal_ajustado", 0.85)
regla("Humo negro y consumo alto: mezcla rica", ["humo_negro", "consumo_gasolina_alto"], "mezcla_rica", 0.85)
regla("Mezcla rica con check engine: sensor de inyección", ["mezcla_rica", "testigo_check_engine"], "sensor_inyeccion_defectuoso", 0.80)

# ---------- Motor, lubricación y refrigeración ----------
regla("Humo azul y consumo de aceite: aros o retenes", ["humo_azul", "consumo_aceite"], "desgaste_aros", 0.85)
regla("Humo blanco, aceite lechoso y refrigerante bajo: empaque de culata", ["humo_blanco", "aceite_lechoso", "nivel_refrigerante_bajo"], "empaque_culata_danado", 0.90)
regla("Sobrecalentamiento y refrigerante bajo: fuga de refrigerante", ["sobrecalentamiento", "nivel_refrigerante_bajo"], "fuga_refrigerante", 0.85)
regla("Sobrecalentamiento con ventilador parado: ventilador", ["sobrecalentamiento", "ventilador_no_gira"], "falla_ventilador", 0.90)
regla("Sobrecalentamiento con aceite vencido: lubricación deficiente", ["sobrecalentamiento", "aceite_vencido"], "lubricacion_deficiente", 0.80)
regla("Aceite vencido: cambio pendiente", ["aceite_vencido"], "necesita_cambio_aceite", 0.95)
regla("Golpeteo y testigo de presión de aceite: lubricación crítica", ["ruido_golpeteo_motor", "luz_presion_aceite"], "lubricacion_critica", 0.90)
regla("Traqueteo alto y pérdida de potencia: tensor de distribución", ["ruido_cadena_distribucion", "perdida_potencia"], "tensor_distribucion_desgastado", 0.85)
regla("Fuga de aceite y consumo: sello o empaque", ["fuga_aceite", "consumo_aceite"], "sello_o_empaque_fuga", 0.85)

# ---------- Transmisión y embrague ----------
regla("Ruido y holgura en la cadena: kit de arrastre", ["ruido_cadena", "cadena_floja"], "kit_arrastre_desgastado", 0.95)
regla("Cadena oxidada y ruidosa: sin lubricar", ["cadena_oxidada", "ruido_cadena"], "cadena_sin_lubricar", 0.85)
regla("Embrague que patina con pérdida de potencia: discos", ["embrague_patina", "perdida_potencia"], "embrague_desgastado", 0.90)
regla("Palanca dura y cambios duros: cable o circuito de embrague", ["palanca_embrague_dura", "cambios_duros"], "circuito_embrague_defectuoso", 0.85)
regla("Se salen las marchas y cambios duros: caja", ["salto_marchas", "cambios_duros"], "caja_cambios_desgastada", 0.85)
regla("Vibración al arrancar y ruido de variador: CVT", ["vibracion_al_arrancar_scooter", "ruido_variador"], "variador_cvt_desgastado", 0.90)

# ---------- Frenos ----------
regla("Chirrido y recorrido largo: pastillas", ["freno_chirrido", "recorrido_freno_largo"], "pastillas_desgastadas", 0.95)
regla("Freno esponjoso y líquido oscuro: aire o humedad", ["freno_esponjoso", "liquido_freno_oscuro"], "aire_humedad_frenos", 0.90)
regla("Freno esponjoso y nivel bajo: fuga en el circuito", ["freno_esponjoso", "nivel_liquido_bajo"], "fuga_circuito_frenos", 0.90)
regla("Vibración al frenar y disco con surcos: disco", ["vibracion_al_frenar", "disco_con_surcos"], "disco_danado", 0.90)
regla("Testigo del ABS encendido: falla de ABS", ["abs_testigo_encendido"], "falla_abs", 0.80)

# ---------- Suspensión, dirección y llantas ----------
regla("Aceite en barras y rebote excesivo: retenes", ["fuga_aceite_barra", "rebote_excesivo"], "retenes_horquilla_danados", 0.90)
regla("Vibración y dirección floja: rodamientos", ["vibracion_manubrio", "direccion_floja"], "rodamientos_direccion_flojos", 0.85)
regla("Desgaste irregular y vibración: balanceo o alineación", ["llanta_desgaste_irregular", "vibracion_manubrio"], "balanceo_alineacion", 0.85)
regla("Llantas con presión baja: presión incorrecta", ["llanta_baja_presion"], "presion_llantas_incorrecta", 0.80)

# ---------- Alertas de seguridad y recomendación combinada ----------
regla("Lubricación crítica: no encender el motor", ["lubricacion_critica"], "alerta_lubricacion", 0.95)
regla("Empaque de culata dañado: no circular", ["empaque_culata_danado"], "alerta_culata", 0.95)
regla("Fuga en frenos: no circular", ["fuga_circuito_frenos"], "alerta_frenos", 0.95)
regla("Rodamientos de dirección flojos: no circular rápido", ["rodamientos_direccion_flojos"], "alerta_direccion", 0.85)

# ---------- Reglas por marca (la marca es un hecho más: marca_xxx) ----------
# KTM
regla("KTM con falla de carga: regulador-rectificador", ["marca_ktm", "falla_sistema_carga"], "regulador_rectificador_ktm", 0.90)
regla("KTM que se sobrecalienta en tráfico", ["marca_ktm", "sobrecalentamiento", "falla_en_trafico_lento"], "ventilacion_trafico_ktm", 0.80)
regla("KTM con servicio de válvulas vencido y pérdida de potencia", ["marca_ktm", "servicio_valvulas_vencido", "perdida_potencia"], "valvulas_fuera_de_rango_ktm", 0.80)
# Aprilia
regla("Aprilia con falla de carga: regulador-rectificador", ["marca_aprilia", "falla_sistema_carga"], "regulador_rectificador_aprilia", 0.90)
regla("Aprilia con ralentí inestable y check engine: sensor de acelerador", ["marca_aprilia", "ralenti_inestable", "testigo_check_engine"], "sensor_acelerador_aprilia", 0.80)
regla("Aprilia con batería que se descarga y olor a quemado: estátor", ["marca_aprilia", "bateria_se_descarga", "olor_quemado_electrico"], "estator_aprilia", 0.85)
# BMW
regla("BMW con testigo ABS: módulo ABS o servofreno", ["marca_bmw", "abs_testigo_encendido"], "modulo_abs_bmw", 0.85)
regla("BMW con fuga de aceite: cardán o transmisión final", ["marca_bmw", "fuga_aceite"], "fuga_transmision_final_bmw", 0.75)
regla("BMW con golpeteo y pérdida de potencia: balancines", ["marca_bmw", "ruido_golpeteo_motor", "perdida_potencia"], "balancines_valvulas_bmw", 0.75)
# Ducati
regla("Ducati con servicio desmodrómico vencido", ["marca_ducati", "servicio_valvulas_vencido"], "correas_desmo_ducati", 0.95)
regla("Ducati que se calienta en tráfico: cilindro trasero", ["marca_ducati", "sobrecalentamiento", "falla_en_trafico_lento"], "calor_cilindro_trasero_ducati", 0.80)
regla("Ducati con traqueteo y patinaje de embrague: embrague seco", ["marca_ducati", "ruido_embrague_seco", "embrague_patina"], "embrague_seco_ducati", 0.85)
regla("Ducati con falla de carga: regulador", ["marca_ducati", "falla_sistema_carga"], "regulador_ducati", 0.85)
# Triumph
regla("Triumph con falla de carga: regulador o estátor", ["marca_triumph", "falla_sistema_carga"], "regulador_estator_triumph", 0.85)
regla("Triumph con fuga de refrigerante: manguera o bomba", ["marca_triumph", "fuga_refrigerante"], "fuga_refrigerante_triumph", 0.80)
regla("Triumph con ralentí inestable y olor a gasolina: cuerpos de aceleración", ["marca_triumph", "ralenti_inestable", "olor_gasolina"], "cuerpos_aceleracion_triumph", 0.80)
# Yamaha
regla("Yamaha con falla de carga: regulador", ["marca_yamaha", "falla_sistema_carga"], "regulador_yamaha", 0.85)
regla("Yamaha con traqueteo alto: tensor de distribución", ["marca_yamaha", "ruido_cadena_distribucion"], "tensor_distribucion_yamaha", 0.85)
regla("Yamaha con check engine y ralentí inestable: sensor", ["marca_yamaha", "testigo_check_engine", "ralenti_inestable"], "sensor_inyeccion_yamaha", 0.80)
# Honda
regla("Honda con falla de carga: regulador-rectificador", ["marca_honda", "falla_sistema_carga"], "regulador_honda", 0.90)
regla("Honda con traqueteo alto: tensor automático", ["marca_honda", "ruido_cadena_distribucion"], "tensor_distribucion_honda", 0.85)
regla("Honda scooter con vibración y ruido de variador", ["marca_honda", "vibracion_al_arrancar_scooter", "ruido_variador"], "variador_honda", 0.90)
# Kawasaki
regla("Kawasaki con falla de carga: estátor o regulador", ["marca_kawasaki", "falla_sistema_carga"], "estator_regulador_kawasaki", 0.90)
regla("Kawasaki con fuga de refrigerante: bomba de agua", ["marca_kawasaki", "fuga_refrigerante"], "sello_bomba_agua_kawasaki", 0.80)
regla("Kawasaki que se calienta en tráfico: termostato o ventilador", ["marca_kawasaki", "sobrecalentamiento", "falla_en_trafico_lento"], "termostato_ventilador_kawasaki", 0.75)
# Suzuki
regla("Suzuki con falla de carga: regulador-rectificador", ["marca_suzuki", "falla_sistema_carga"], "regulador_suzuki", 0.90)
regla("Suzuki con ralentí inestable y gasolina vieja: carburación", ["marca_suzuki", "ralenti_inestable", "gasolina_vieja"], "carburacion_suzuki", 0.80)
regla("Suzuki con pérdida de potencia y check engine: sensor de acelerador", ["marca_suzuki", "perdida_potencia", "testigo_check_engine"], "sensor_acelerador_suzuki", 0.75)
# Harley-Davidson
regla("Harley con falla de carga: estátor o regulador", ["marca_harley", "falla_sistema_carga"], "estator_regulador_harley", 0.90)
regla("Harley con traqueteo alto: tensores de levas", ["marca_harley", "ruido_cadena_distribucion"], "tensores_levas_harley", 0.85)
regla("Harley con fuga de aceite: fuga típica", ["marca_harley", "fuga_aceite"], "fugas_aceite_harley", 0.75)

# ---------- Recomendación combinada ----------
regla("Aceite, filtro de aire y bujía en mal estado: servicio mayor",
      ["necesita_cambio_aceite", "filtro_aire_obstruido", "bujia_danada"], "recomendar_servicio_mayor", 0.85)


# ======================================================================================
# AMPLIACIÓN · MODELOS: síntomas, diagnósticos, hechos de contexto y reglas que dependen del modelo
# ======================================================================================
g = "Transmisión y embrague"
sintoma("scooter_patina_al_acelerar", g, "El scooter acelera el motor pero avanza poco")
sintoma("correa_final_desgastada", g, "Correa de transmisión con grietas, desgaste o ruido")
sintoma("ruido_transmision_cardan", g, "Zumbido o golpe seco en la transmisión final (cardán)")

diagnostico("correa_cvt_desgastada", "Correa del CVT desgastada (scooter)", "Medir y cambiar la correa, revisar rodillos y el embrague centrífugo")
diagnostico("correa_transmision_desgastada", "Correa de transmisión final desgastada", "Medir tensión y alineación; cambiar la correa si hay grietas o dientes dañados")
diagnostico("cardan_con_fuga_o_desgaste", "Transmisión por cardán con fuga o desgaste", "Revisar nivel de aceite y retenes del cardán; inspeccionar juntas")
diagnostico("calentamiento_motor_aire_trafico", "Motor refrigerado por aire que se calienta en tráfico", "Revisar nivel y viscosidad del aceite, aletas limpias y evitar ralentí prolongado")
diagnostico("carburador_sucio_carburado", "Carburador sucio en moto carburada", "Desarmar y limpiar el carburador (surtidores y cuba) y reajustar el ralentí")
diagnostico("fuga_interna_refrigerante", "Posible mezcla interna de aceite y refrigerante", "Prueba de presión del sistema y de compresión; revisar empaque de culata y sello de la bomba de agua")
diagnostico("tensor_distribucion_r15", "Tensor de distribución típico de la R15 (Yamaha)", "Cambiar el tensor de la cadena de distribución y verificar el ajuste", "yamaha")

# Hechos de contexto: cada modelo y cada atributo (transmisión, refrigeración, alimentación, tipo)
for _mid, _m in MODELOS.items():
    PREDICADOS["modelo_" + _mid] = ("contexto", "Modelo", MARCAS[_m["marca"]][0] + " " + _m["nombre"], None, _m["marca"])
for _hecho, _txt in ATRIBUTOS.items():
    PREDICADOS[_hecho] = ("contexto", "Atributo del modelo", _txt, None, None)

# ---------- Reglas que dependen del modelo (sus atributos o el modelo mismo) ----------
regla("Scooter que acelera sin avanzar: correa CVT", ["scooter_patina_al_acelerar"], "correa_cvt_desgastada", 0.80)
regla("Correa final con desgaste: correa de transmisión", ["correa_final_desgastada"], "correa_transmision_desgastada", 0.90)
regla("Cardán con ruido y fuga de aceite", ["ruido_transmision_cardan", "fuga_aceite"], "cardan_con_fuga_o_desgaste", 0.85)
regla("Motor refrigerado por aire que se calienta en tráfico",
      ["refrigeracion_aire", "sobrecalentamiento", "falla_en_trafico_lento"], "calentamiento_motor_aire_trafico", 0.80)
regla("Moto con carburador, ralentí inestable y gasolina vieja",
      ["alimentacion_carburador", "ralenti_inestable", "gasolina_vieja"], "carburador_sucio_carburado", 0.85)
regla("Motor con refrigeración líquida: aceite lechoso y refrigerante bajo",
      ["refrigeracion_liquida", "aceite_lechoso", "nivel_refrigerante_bajo"], "fuga_interna_refrigerante", 0.85)
regla("Yamaha R15 con traqueteo en la parte alta", ["modelo_yamaha_r15", "ruido_cadena_distribucion"], "tensor_distribucion_r15", 0.90)

# ---------- Recomendaciones automáticas: una por cada diagnóstico ----------
for nombre_pred, datos in list(PREDICADOS.items()):
    if datos[0] == "diagnostico":
        rec = "recomendar_" + nombre_pred
        PREDICADOS[rec] = ("recomendacion", "Recomendación", datos[3], None, datos[4])
        regla("Acción para: " + datos[2], [nombre_pred], rec, 0.95)

# Nombre usado en la actividad (from base_conocimiento import REGLAS, PREDICADOS)
REGLAS = base_conocimiento
