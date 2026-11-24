"""Catálogo de modelos de moto por marca (datos de referencia) + imagen de referencia. Python puro.

Cada modelo aporta HECHOS al motor (modelo_xxx, transmision_cadena, refrigeracion_liquida...) que las
reglas pueden usar como condiciones, y define qué síntomas tienen sentido para él.

IMPORTANTE: las fichas (cilindrada, tipo de transmisión, refrigeración) son datos de referencia generales
y no distinguen año ni versión. Verificar siempre con la ficha técnica del fabricante.
"""

TIPOS = {
    "naked": "Naked", "sport": "Deportiva", "adventure": "Adventure", "trail": "Trail / enduro",
    "scooter": "Scooter", "cruiser": "Cruiser", "touring": "Touring", "clasica": "Clásica",
}

TRANSMISION = {"cadena": "Cadena", "cardan": "Cardán (eje)", "correa": "Correa", "cvt": "Automática CVT (variador)"}
REFRIGERACION = {"liquida": "Líquida", "aire": "Aire / aceite"}
ALIMENTACION = {"inyeccion": "Inyección electrónica", "carburador": "Carburador"}

# Hechos de contexto que aporta un modelo, con su texto
ATRIBUTOS = {}
for _k, _v in TRANSMISION.items():
    ATRIBUTOS["transmision_" + _k] = "Transmisión: " + _v
for _k, _v in REFRIGERACION.items():
    ATRIBUTOS["refrigeracion_" + _k] = "Refrigeración: " + _v
for _k, _v in ALIMENTACION.items():
    ATRIBUTOS["alimentacion_" + _k] = "Alimentación: " + _v
for _k, _v in TIPOS.items():
    ATRIBUTOS["tipo_" + _k] = "Tipo de moto: " + _v

# Un síntoma solo aplica a un modelo si el atributo del modelo está permitido.
# Si el modelo no declara ese atributo (dato desconocido), el síntoma se considera aplicable.
APLICA = {
    "ruido_cadena": ("transmision", {"cadena"}),
    "cadena_floja": ("transmision", {"cadena"}),
    "cadena_oxidada": ("transmision", {"cadena"}),
    "vibracion_al_arrancar_scooter": ("transmision", {"cvt"}),
    "ruido_variador": ("transmision", {"cvt"}),
    "scooter_patina_al_acelerar": ("transmision", {"cvt"}),
    "correa_final_desgastada": ("transmision", {"correa"}),
    "ruido_transmision_cardan": ("transmision", {"cardan"}),
    "embrague_patina": ("transmision", {"cadena", "cardan", "correa"}),
    "palanca_embrague_dura": ("transmision", {"cadena", "cardan", "correa"}),
    "cambios_duros": ("transmision", {"cadena", "cardan", "correa"}),
    "salto_marchas": ("transmision", {"cadena", "cardan", "correa"}),
    "ruido_embrague_seco": ("transmision", {"cadena", "cardan", "correa"}),
    "ventilador_no_gira": ("refrigeracion", {"liquida"}),
    "nivel_refrigerante_bajo": ("refrigeracion", {"liquida"}),
    "testigo_check_engine": ("alimentacion", {"inyeccion"}),
    "sin_ruido_bomba": ("alimentacion", {"inyeccion"}),
}

# Diagnósticos que NO pueden derivarse si el modelo tiene cierto atributo
BLOQUEOS = {
    "refrigeracion_aire": {"fuga_refrigerante", "falla_ventilador", "fuga_interna_refrigerante",
                           "ventilacion_trafico_ktm", "termostato_ventilador_kawasaki"},
    "refrigeracion_liquida": {"calentamiento_motor_aire_trafico"},
    "transmision_cvt": {"kit_arrastre_desgastado", "cadena_sin_lubricar", "embrague_desgastado",
                        "circuito_embrague_defectuoso", "caja_cambios_desgastada", "embrague_seco_ducati",
                        "correa_transmision_desgastada", "cardan_con_fuga_o_desgaste"},
    "transmision_cadena": {"variador_cvt_desgastado", "variador_honda", "correa_cvt_desgastada",
                           "correa_transmision_desgastada", "cardan_con_fuga_o_desgaste", "fuga_transmision_final_bmw"},
    "transmision_correa": {"kit_arrastre_desgastado", "cadena_sin_lubricar", "variador_cvt_desgastado", "variador_honda",
                           "correa_cvt_desgastada", "cardan_con_fuga_o_desgaste", "fuga_transmision_final_bmw"},
    "transmision_cardan": {"kit_arrastre_desgastado", "cadena_sin_lubricar", "variador_cvt_desgastado", "variador_honda",
                           "correa_cvt_desgastada", "correa_transmision_desgastada"},
    "alimentacion_carburador": {"sensor_inyeccion_defectuoso", "sensor_encendido_defectuoso", "bomba_gasolina_danada",
                                "sensor_inyeccion_yamaha", "sensor_acelerador_aprilia", "sensor_acelerador_suzuki"},
}

# ---------------------------------------------------------------- catálogo
MODELOS = {}


def _normalizar(texto):
    salida = ""
    for c in texto.lower():
        salida += c if c.isalnum() else "_"
    while "__" in salida:
        salida = salida.replace("__", "_")
    return salida.strip("_")


def modelo(marca, nombre, tipo, cc, motor, transmision, refrigeracion, alimentacion=None):
    mid = marca + "_" + _normalizar(nombre)
    MODELOS[mid] = {"id": mid, "marca": marca, "nombre": nombre, "tipo": tipo, "cc": cc, "motor": motor,
                    "transmision": transmision, "refrigeracion": refrigeracion, "alimentacion": alimentacion}


# KTM
modelo("ktm", "390 Duke", "naked", 373, "Monocilíndrico", "cadena", "liquida", "inyeccion")
modelo("ktm", "RC 390", "sport", 373, "Monocilíndrico", "cadena", "liquida", "inyeccion")
modelo("ktm", "390 Adventure", "adventure", 373, "Monocilíndrico", "cadena", "liquida", "inyeccion")
modelo("ktm", "790 Duke", "naked", 799, "Bicilíndrico paralelo", "cadena", "liquida", "inyeccion")
modelo("ktm", "1290 Super Duke R", "naked", 1301, "V2", "cadena", "liquida", "inyeccion")
# Aprilia
modelo("aprilia", "RS 660", "sport", 659, "Bicilíndrico paralelo", "cadena", "liquida", "inyeccion")
modelo("aprilia", "Tuono 660", "naked", 659, "Bicilíndrico paralelo", "cadena", "liquida", "inyeccion")
modelo("aprilia", "RSV4 1100", "sport", 1077, "V4", "cadena", "liquida", "inyeccion")
modelo("aprilia", "Tuono V4", "naked", 1077, "V4", "cadena", "liquida", "inyeccion")
modelo("aprilia", "Shiver 900", "naked", 896, "V2", "cadena", "liquida", "inyeccion")
# BMW Motorrad
modelo("bmw", "R 1250 GS", "adventure", 1254, "Bóxer", "cardan", "liquida", "inyeccion")
modelo("bmw", "F 850 GS", "adventure", 853, "Bicilíndrico paralelo", "cadena", "liquida", "inyeccion")
modelo("bmw", "G 310 R", "naked", 313, "Monocilíndrico", "cadena", "liquida", "inyeccion")
modelo("bmw", "G 310 GS", "adventure", 313, "Monocilíndrico", "cadena", "liquida", "inyeccion")
modelo("bmw", "S 1000 RR", "sport", 999, "4 cilindros en línea", "cadena", "liquida", "inyeccion")
# Ducati
modelo("ducati", "Monster", "naked", 937, "V2 (L-twin)", "cadena", "liquida", "inyeccion")
modelo("ducati", "Panigale V2", "sport", 955, "V2 (L-twin)", "cadena", "liquida", "inyeccion")
modelo("ducati", "Panigale V4", "sport", 1103, "V4", "cadena", "liquida", "inyeccion")
modelo("ducati", "Multistrada 950", "adventure", 937, "V2 (L-twin)", "cadena", "liquida", "inyeccion")
modelo("ducati", "Scrambler 800", "clasica", 803, "V2 (L-twin)", "cadena", "aire", "inyeccion")
# Triumph
modelo("triumph", "Bonneville T120", "clasica", 1200, "Bicilíndrico paralelo", "cadena", "liquida", "inyeccion")
modelo("triumph", "Street Triple 765", "naked", 765, "Tricilíndrico", "cadena", "liquida", "inyeccion")
modelo("triumph", "Speed Triple 1200 RS", "naked", 1160, "Tricilíndrico", "cadena", "liquida", "inyeccion")
modelo("triumph", "Tiger 900", "adventure", 888, "Tricilíndrico", "cadena", "liquida", "inyeccion")
modelo("triumph", "Trident 660", "naked", 660, "Tricilíndrico", "cadena", "liquida", "inyeccion")
# Yamaha
modelo("yamaha", "R15", "sport", 155, "Monocilíndrico", "cadena", "liquida", "inyeccion")
modelo("yamaha", "MT-03", "naked", 321, "Bicilíndrico paralelo", "cadena", "liquida", "inyeccion")
modelo("yamaha", "MT-07", "naked", 689, "Bicilíndrico paralelo", "cadena", "liquida", "inyeccion")
modelo("yamaha", "MT-09", "naked", 890, "Tricilíndrico", "cadena", "liquida", "inyeccion")
modelo("yamaha", "NMAX 155", "scooter", 155, "Monocilíndrico", "cvt", "liquida", "inyeccion")
modelo("yamaha", "FZ 25", "naked", 249, "Monocilíndrico", "cadena", "aire", "inyeccion")
# Honda
modelo("honda", "CB190R", "naked", 184, "Monocilíndrico", "cadena", "aire", "inyeccion")
modelo("honda", "XR150L", "trail", 149, "Monocilíndrico", "cadena", "aire")
modelo("honda", "CBR500R", "sport", 471, "Bicilíndrico paralelo", "cadena", "liquida", "inyeccion")
modelo("honda", "PCX", "scooter", 157, "Monocilíndrico", "cvt", "liquida", "inyeccion")
modelo("honda", "Africa Twin", "adventure", 1084, "Bicilíndrico paralelo", "cadena", "liquida", "inyeccion")
# Kawasaki
modelo("kawasaki", "Ninja 400", "sport", 399, "Bicilíndrico paralelo", "cadena", "liquida", "inyeccion")
modelo("kawasaki", "Z650", "naked", 649, "Bicilíndrico paralelo", "cadena", "liquida", "inyeccion")
modelo("kawasaki", "Z900", "naked", 948, "4 cilindros en línea", "cadena", "liquida", "inyeccion")
modelo("kawasaki", "Versys 650", "adventure", 649, "Bicilíndrico paralelo", "cadena", "liquida", "inyeccion")
modelo("kawasaki", "KLX 230", "trail", 233, "Monocilíndrico", "cadena", "aire", "inyeccion")
# Suzuki
modelo("suzuki", "GSX-R1000", "sport", 999, "4 cilindros en línea", "cadena", "liquida", "inyeccion")
modelo("suzuki", "V-Strom 650", "adventure", 645, "V2", "cadena", "liquida", "inyeccion")
modelo("suzuki", "Gixxer 155", "naked", 155, "Monocilíndrico", "cadena", "aire")
modelo("suzuki", "GN 125", "naked", 124, "Monocilíndrico", "cadena", "aire", "carburador")
# Harley-Davidson
modelo("harley", "Iron 883", "cruiser", 883, "V2", "correa", "aire")
modelo("harley", "Fat Boy", "cruiser", 1745, "V2", "correa", "aire", "inyeccion")
modelo("harley", "Street Glide", "touring", 1745, "V2", "correa", "aire", "inyeccion")
modelo("harley", "Pan America 1250", "adventure", 1252, "V2", "cadena", "liquida", "inyeccion")


# ---------------------------------------------------------------- funciones
def modelos_de_marca(marca):
    """Ids de los modelos de una marca, en orden de catálogo."""
    return [mid for mid, m in MODELOS.items() if m["marca"] == marca]


def nombre_completo(mid, marcas):
    return marcas[MODELOS[mid]["marca"]][0] + " " + MODELOS[mid]["nombre"]


def hechos_del_modelo(mid):
    """Hechos de contexto que un modelo aporta al motor."""
    m = MODELOS[mid]
    h = {"modelo_" + mid, "tipo_" + m["tipo"], "transmision_" + m["transmision"],
         "refrigeracion_" + m["refrigeracion"]}
    if m["alimentacion"]:
        h.add("alimentacion_" + m["alimentacion"])
    return h


def sintoma_aplica(sintoma, mid):
    """True si el síntoma tiene sentido para el modelo (sin modelo, todos aplican)."""
    if not mid or mid not in MODELOS or sintoma not in APLICA:
        return True
    dimension, permitidos = APLICA[sintoma]
    valor = MODELOS[mid][dimension]
    return valor is None or valor in permitidos


def bloqueos_del_modelo(mid):
    """Conjunto de conclusiones que no pueden derivarse para este modelo."""
    bloqueados = set()
    if mid and mid in MODELOS:
        for hecho in hechos_del_modelo(mid):
            bloqueados |= BLOQUEOS.get(hecho, set())
    return bloqueados


def resumen_modelo(mid):
    m = MODELOS[mid]
    partes = [f'{m["cc"]} cc', m["motor"], "transmisión " + TRANSMISION[m["transmision"]].lower(),
              "refrigeración " + REFRIGERACION[m["refrigeracion"]].lower()]
    if m["alimentacion"]:
        partes.append(ALIMENTACION[m["alimentacion"]].lower())
    return " · ".join(partes)


# ---------------------------------------------------------------- imagen de referencia
# Fotos reales (opcional, recomendado): guardar el archivo en assets/modelos/<id>.jpg (o .png/.webp), o
# registrar aquí una URL con su crédito. Si no hay foto ni URL, se usa la ilustración SVG de abajo.
IMAGENES_URL = {}        # id -> URL de la imagen
FUENTES_IMAGEN = {}      # id -> crédito / fuente (se muestra como pie de foto)

COLORES = {"ktm": "#ff6600", "aprilia": "#b3001b", "bmw": "#1c69d4", "ducati": "#9d0b0e", "triumph": "#2f2f2f",
           "yamaha": "#1d2b6b", "honda": "#d71920", "kawasaki": "#3a9d23", "suzuki": "#005baa", "harley": "#e8590c"}


def _silueta(tipo, y, r):
    """Primitivas SVG (sin ruedas) de una silueta aproximada según el tipo de moto."""
    b = 'fill="#ffffff" stroke="#ffffff" stroke-linejoin="round"'
    linea = 'fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round"'
    if tipo == "scooter":
        return (f'<path d="M62 {y-30} Q62 {y-62} 104 {y-58} L150 {y-34} L214 {y-34} L228 {y-66} L248 {y-66} '
                f'L262 {y} L236 {y} Q226 {y-22} 212 {y-26} L122 {y-26} Q112 {y} 92 {y} Z" {b} stroke-width="2"/>'
                f'<rect x="98" y="{y-74}" width="74" height="14" rx="7" fill="#ffffff"/>'
                f'<path d="M232 {y-66} L242 {y-98} L226 {y-102}" {linea}/>')
    if tipo in ("cruiser", "touring"):
        extra = (f'<rect x="76" y="{y-62}" width="62" height="26" rx="8" fill="#ffffff" opacity="0.85"/>'
                 f'<path d="M236 {y-66} L246 {y-108} L262 {y-108}" {linea}/>') if tipo == "touring" else ""
        return (f'<path d="M92 {y} L170 {y-8} L196 {y-52}" {linea}/>'
                f'<path d="M196 {y-52} L252 {y-62}" {linea}/>'
                f'<path d="M170 {y-54} Q190 {y-90} 236 {y-70} L226 {y-48} L176 {y-44} Z" {b} stroke-width="2"/>'
                f'<path d="M96 {y-46} Q130 {y-62} 168 {y-52} L166 {y-42} L100 {y-34} Z" {b} stroke-width="2"/>'
                f'<path d="M244 {y-64} L278 {y}" {linea}/>'
                f'<path d="M244 {y-64} L228 {y-86} L204 {y-84}" {linea}/>'
                f'<rect x="168" y="{y-40}" width="48" height="30" rx="6" fill="#ffffff" opacity="0.7"/>' + extra)
    if tipo == "sport":
        return (f'<path d="M92 {y} L158 {y-10}" {linea}/>'
                f'<path d="M104 {y-40} Q112 {y-58} 160 {y-56} L162 {y-44} Z" {b} stroke-width="2"/>'
                f'<path d="M168 {y-52} Q196 {y-72} 238 {y-60} L228 {y-46} L170 {y-44} Z" {b} stroke-width="2"/>'
                f'<path d="M206 {y-50} Q248 {y-62} 266 {y-26} L270 {y} L222 {y-8} Z" {b} stroke-width="2"/>'
                f'<path d="M236 {y-60} L226 {y-84}" {linea}/>'
                f'<rect x="164" y="{y-38}" width="44" height="28" rx="6" fill="#ffffff" opacity="0.7"/>')
    alto = 14 if tipo in ("adventure", "trail") else 0
    extra = (f'<path d="M238 {y-58-alto} L230 {y-96-alto} L246 {y-96-alto}" {linea}/>') if tipo in ("adventure", "trail") else ""
    return (f'<path d="M92 {y} L160 {y-12}" {linea}/>'
            f'<path d="M160 {y-12} L150 {y-48-alto} L214 {y-48-alto} L238 {y-58-alto}" {linea}/>'
            f'<path d="M168 {y-46-alto} Q190 {y-68-alto} 236 {y-56-alto} L226 {y-42-alto} L172 {y-40-alto} Z" {b} stroke-width="2"/>'
            f'<path d="M106 {y-38-alto} Q130 {y-54-alto} 164 {y-48-alto} L164 {y-38-alto} L110 {y-30-alto} Z" {b} stroke-width="2"/>'
            f'<path d="M238 {y-58-alto} L268 {y}" {linea}/>'
            f'<path d="M238 {y-58-alto} L226 {y-72-alto} L208 {y-72-alto}" {linea}/>'
            f'<rect x="166" y="{y-38}" width="46" height="28" rx="6" fill="#ffffff" opacity="0.7"/>' + extra)


def imagen_svg(mid):
    """Ilustración SVG de referencia del modelo (no es una foto real)."""
    m = MODELOS[mid]
    color = COLORES.get(m["marca"], "#444444")
    r = {"scooter": 28, "cruiser": 38, "touring": 38, "adventure": 40, "trail": 40}.get(m["tipo"], 36)
    y = 188 - r
    ruedas = ""
    for x in (92, 268):
        ruedas += (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#111" stroke="#ffffff" stroke-width="6"/>'
                   f'<circle cx="{x}" cy="{y}" r="{max(r-16, 8)}" fill="none" stroke="#9ca3af" stroke-width="2"/>'
                   f'<circle cx="{x}" cy="{y}" r="5" fill="#ffffff"/>')
    nombre = m["nombre"].replace("&", "y").replace("<", "").replace(">", "")
    marca = m["marca"].upper()
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 240" width="360" height="240">'
            f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{color}"/>'
            '<stop offset="1" stop-color="#111827"/></linearGradient></defs>'
            '<rect width="360" height="240" rx="14" fill="url(#g)"/>'
            f'<text x="16" y="30" font-family="Arial,sans-serif" font-size="16" font-weight="700" fill="#ffffff" opacity="0.9">{marca}</text>'
            '<line x1="10" y1="188" x2="350" y2="188" stroke="#ffffff" stroke-opacity="0.35" stroke-width="2"/>'
            + _silueta(m["tipo"], y, r) + ruedas +
            f'<text x="16" y="218" font-family="Arial,sans-serif" font-size="20" font-weight="700" fill="#ffffff">{nombre}</text>'
            f'<text x="344" y="232" text-anchor="end" font-family="Arial,sans-serif" font-size="9" fill="#ffffff" opacity="0.7">'
            'ilustración de referencia</text></svg>')


def validar_catalogo(marcas):
    """Devuelve una lista de problemas del catálogo (vacía si todo está bien)."""
    problemas = []
    for mid, m in MODELOS.items():
        if m["marca"] not in marcas:
            problemas.append(f"{mid}: marca desconocida")
        if m["tipo"] not in TIPOS:
            problemas.append(f"{mid}: tipo desconocido")
        if m["transmision"] not in TRANSMISION:
            problemas.append(f"{mid}: transmisión desconocida")
        if m["refrigeracion"] not in REFRIGERACION:
            problemas.append(f"{mid}: refrigeración desconocida")
        if m["alimentacion"] is not None and m["alimentacion"] not in ALIMENTACION:
            problemas.append(f"{mid}: alimentación desconocida")
        if not imagen_svg(mid).startswith("<svg"):
            problemas.append(f"{mid}: imagen inválida")
    for marca in marcas:
        if len(modelos_de_marca(marca)) < 3:
            problemas.append(f"{marca}: menos de 3 modelos en el catálogo")
    return problemas
