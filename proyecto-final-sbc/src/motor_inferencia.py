"""Motor de inferencia: encadenamiento hacia adelante, validación y explicación.

Python puro. No conoce nada de Streamlit: puede usarse desde un notebook, la consola o la web.
"""



from base_conocimiento import REGLAS, PREDICADOS, MARCAS, CONTRADICCIONES, texto



def mostrar_regla(regla):
    condiciones = " Y ".join(regla["si"])
    print(f'{regla["nombre"]}: SI {condiciones} '
          f'ENTONCES {regla["entonces"]}  (certeza {regla["certeza"]})')


def se_cumple(regla, hechos):
    """Una regla se cumple cuando TODAS sus condiciones están en los hechos."""
    for condicion in regla["si"]:
        if condicion not in hechos:
            return False
    return True


def una_pasada(base, sintomas):
    hechos = set(sintomas)  # copia
    for regla in base:
        if se_cumple(regla, hechos):
            hechos.add(regla["entonces"])
            print("Se disparó", regla["nombre"])
    return hechos


def hechos_de_entrada(sintomas, marca=""):
    """Convierte síntomas + marca elegida en el conjunto inicial de hechos."""
    hechos = set(sintomas)
    if marca:
        hechos.add("marca_" + marca)
    return hechos


def validar_entrada(sintomas, marca=""):
    """Devuelve una lista de mensajes de error (vacía si todo está bien)."""
    errores = []
    if len(sintomas) == 0:
        errores.append("Seleccione al menos un síntoma.")
    for s in sintomas:
        if s not in PREDICADOS or PREDICADOS[s][0] != "sintoma":
            errores.append(f"'{s}' no es un síntoma conocido.")
    if marca and marca not in MARCAS:
        errores.append(f"La marca '{marca}' no existe en el sistema.")
    for a, b in CONTRADICCIONES:
        if a in sintomas and b in sintomas:
            errores.append(f"Síntomas contradictorios: '{texto(a)}' y '{texto(b)}'.")
    return errores


def encadenamiento_adelante(base, hechos_iniciales, registro=None):
    """
    Aplica encadenamiento hacia adelante.
    Returns: (hechos_finales, reglas_aplicadas)
      - reglas_aplicadas: lista (en orden de disparo) de copias de las reglas,
        cada una con la clave extra 'certeza_final'.
    registro: lista opcional donde se guardan los mensajes del log.
    """
    if registro is None:
        registro = []
    hechos = set(hechos_iniciales)
    certeza = {h: 1.0 for h in hechos}      # síntomas y marca tienen certeza 1
    reglas_aplicadas = []
    pasada = 0
    hubo_cambios = True
    while hubo_cambios:
        pasada += 1
        if pasada > len(base) + 1:          # protección contra ciclos infinitos
            raise RuntimeError("Posible ciclo infinito en la base de conocimiento")
        registro.append(f"--- Pasada {pasada} ---")
        hubo_cambios = False
        for regla in base:
            if se_cumple(regla, hechos) and regla["entonces"] not in hechos:
                c = min(certeza[x] for x in regla["si"]) * regla["certeza"]
                certeza[regla["entonces"]] = c
                hechos.add(regla["entonces"])
                aplicada = dict(regla)
                aplicada["certeza_final"] = c
                reglas_aplicadas.append(aplicada)
                registro.append(f'Se disparó {regla["nombre"]}: '
                                f'{" Y ".join(regla["si"])} => {regla["entonces"]} (certeza {c:.2f})')
                hubo_cambios = True
    if not reglas_aplicadas:
        registro.append("No se pudo derivar ninguna conclusión con los hechos dados.")
    return hechos, reglas_aplicadas


def diagnosticar(sintomas, marca="", registro=None):
    """Valida la entrada y ejecuta el motor. Lanza ValueError si la entrada es inválida."""
    errores = validar_entrada(sintomas, marca)
    if errores:
        raise ValueError(" ".join(errores))
    return encadenamiento_adelante(REGLAS, hechos_de_entrada(sintomas, marca), registro)


def explicar_razonamiento(reglas_aplicadas):
    """Genera un texto legible con las reglas aplicadas en orden."""
    if not reglas_aplicadas:
        return "No se aplicó ninguna regla: con los datos dados no se puede concluir nada."
    lineas = []
    for i, r in enumerate(reglas_aplicadas, 1):
        lineas.append(f'Paso {i} · {r["nombre"]} ({r["descripcion"]}): '
                      f'SI {" Y ".join(texto(c) for c in r["si"])} '
                      f'ENTONCES {texto(r["entonces"])}  [certeza {r["certeza_final"]:.0%}]')
    return "\n".join(lineas)


def porque(conclusion, hechos_iniciales, reglas_aplicadas, nivel=0):
    """Explica por qué se llegó a una conclusión (cadena de razonamiento recursiva)."""
    origen = {r["entonces"]: r for r in reglas_aplicadas}
    sangria = "    " * nivel
    if conclusion in origen:
        regla = origen[conclusion]
        salida = f'{sangria}{conclusion} .- {regla["nombre"]} ({regla["descripcion"]})\n'
        for c in regla["si"]:
            salida += porque(c, hechos_iniciales, reglas_aplicadas, nivel + 1)
        return salida
    if conclusion in hechos_iniciales:
        tipo = PREDICADOS[conclusion][0] if conclusion in PREDICADOS else ""
        etiqueta = "marca seleccionada" if tipo == "contexto" else "síntoma ingresado"
        return f"{sangria}{conclusion} .- {etiqueta}\n"
    return f"{sangria}{conclusion} .- no se pudo derivar\n"


def que_falta(base, hechos, limite=6):
    """
    Para cada regla no disparada con evidencia parcial indica qué condiciones faltan.
    Se ignoran las reglas de marcas distintas a la elegida y las evidencias que son solo la marca.
    """
    faltantes = []
    for regla in base:
        if regla["entonces"] in hechos:
            continue
        presentes = [c for c in regla["si"] if c in hechos and not c.startswith("marca_")]
        ausentes = [c for c in regla["si"] if c not in hechos]
        if not presentes or not ausentes:
            continue
        if any(c.startswith("marca_") for c in ausentes):
            continue
        faltantes.append((regla["nombre"], regla["entonces"], ausentes))
    faltantes.sort(key=lambda f: len(f[2]))
    return faltantes[:limite]


def validar_base(base):
    problemas = []
    nombres = [r["nombre"] for r in base]
    if len(nombres) != len(set(nombres)):
        problemas.append("Hay nombres de regla repetidos")
    conclusiones = {}
    for r in base:
        if len(set(r["si"])) != len(r["si"]):
            problemas.append(f'{r["nombre"]}: condiciones repetidas')
        for c in r["si"]:
            if c not in PREDICADOS:
                problemas.append(f'{r["nombre"]}: condición desconocida {c}')
        if r["entonces"] not in PREDICADOS:
            problemas.append(f'{r["nombre"]}: conclusión desconocida {r["entonces"]}')
        elif PREDICADOS[r["entonces"]][0] in ("sintoma", "contexto"):
            problemas.append(f'{r["nombre"]}: concluye un dato de entrada')
        if r["entonces"] in conclusiones:
            problemas.append(f'{r["nombre"]}: la conclusión {r["entonces"]} ya la produce {conclusiones[r["entonces"]]}')
        conclusiones[r["entonces"]] = r["nombre"]
        if not (0 < r["certeza"] <= 1):
            problemas.append(f'{r["nombre"]}: certeza fuera de rango')
    # todo hecho derivado debe tener una regla que lo produzca
    for nombre, datos in PREDICADOS.items():
        if datos[0] in ("intermedio", "diagnostico", "recomendacion", "alerta") and nombre not in conclusiones:
            problemas.append(f"El predicado {nombre} nunca se puede derivar")
    # ningún diagnóstico sin recomendación
    for nombre, datos in PREDICADOS.items():
        if datos[0] == "diagnostico" and ("recomendar_" + nombre) not in conclusiones:
            problemas.append(f"El diagnóstico {nombre} no tiene recomendación")
    # detección de ciclos con DFS sobre el grafo conclusión -> condiciones
    dependencias = {r["entonces"]: r["si"] for r in base}
    estado = {}
    def visita(n):
        if estado.get(n) == 1:
            return True               # ciclo
        if estado.get(n) == 2:
            return False
        estado[n] = 1
        for hijo in dependencias.get(n, []):
            if visita(hijo):
                return True
        estado[n] = 2
        return False
    for n in dependencias:
        if visita(n):
            problemas.append(f"Ciclo de dependencias que pasa por {n}")
            break
    return problemas


def clasificar_resultado(reglas_aplicadas):
    """Separa lo derivado en alertas, diagnósticos y recomendaciones (de mayor a menor certeza)."""
    grupos = {"alertas": [], "diagnosticos": [], "recomendaciones": []}
    destino = {"alerta": "alertas", "diagnostico": "diagnosticos", "recomendacion": "recomendaciones"}
    for r in reglas_aplicadas:
        clase = PREDICADOS[r["entonces"]][0]
        if clase in destino:
            grupos[destino[clase]].append((r["entonces"], r["certeza_final"]))
    for lista in grupos.values():
        lista.sort(key=lambda par: -par[1])
    return grupos
