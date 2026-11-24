"""Validaciones automáticas de la base de conocimiento, el catálogo y el motor. Python puro."""
from base_conocimiento import REGLAS, PREDICADOS, MARCAS
from catalogo_modelos import MODELOS, APLICA, sintoma_aplica, bloqueos_del_modelo, validar_catalogo
from motor_inferencia import razonar, validar_entrada, encadenamiento_adelante, hechos_de_entrada


def validar_catalogo_completo():
    """Catálogo + coherencia con la base (los síntomas de APLICA existen)."""
    problemas = validar_catalogo(MARCAS)
    for s in APLICA:
        if s not in PREDICADOS or PREDICADOS[s][0] != "sintoma":
            problemas.append(f"APLICA menciona un síntoma inexistente: {s}")
    return problemas


def cobertura_por_regla():
    """Para cada regla arma el escenario mínimo que debería dispararla. Devuelve las que NO se dispararon."""
    def minimas(hecho, acumulado):
        if hecho in acumulado:
            return
        if PREDICADOS[hecho][0] in ("sintoma", "contexto"):
            acumulado.add(hecho)
            return
        for r in REGLAS:
            if r["entonces"] == hecho:
                for cond in r["si"]:
                    minimas(cond, acumulado)
                return

    sin_cubrir = []
    for r in REGLAS:
        datos = set()
        for cond in r["si"]:
            minimas(cond, datos)
        _, aplicadas = encadenamiento_adelante(REGLAS, datos)
        if r["nombre"] not in {a["nombre"] for a in aplicadas}:
            sin_cubrir.append(r["nombre"])
    return sin_cubrir


def explorar_escenarios():
    """
    Explora sistemáticamente:
      A) todos los escenarios de 1, 2 y 3 síntomas sin marca; y de 1-2 síntomas con cada marca
      B) para cada MODELO del catálogo: todos los escenarios de 1 y 2 síntomas aplicables
    Propiedades: P1 termina sin ciclos · P2 monotonía · P3/P4 las marcas no se mezclan · P5 idempotencia
                 P6 la validación rechaza exactamente los síntomas que no aplican al modelo
                 P8 los bloqueos del modelo solo quitan conclusiones · P9 nada bloqueado aparece
    """
    sintomas = sorted(k for k, v in PREDICADOS.items() if v[0] == "sintoma")
    marcas = sorted(MARCAS)
    diag_marca = {m: {k for k, v in PREDICADOS.items() if v[0] == "diagnostico" and v[4] == m} for m in marcas}
    todos = set().union(*diag_marca.values())
    violaciones, total, sin_conclusion = [], 0, 0

    def revisar(hechos, marca, etiqueta):
        ajenos = todos & hechos
        if marca:
            ajenos -= diag_marca[marca]
        if ajenos:
            violaciones.append(("P3/P4", etiqueta, sorted(ajenos)))

    n = len(sintomas)
    unos, pares = {}, {}
    for marca in [""] + marcas:
        for i in range(n):
            try:
                h, ap = razonar({sintomas[i]}, marca)
            except RuntimeError as e:
                violaciones.append(("P1", (sintomas[i], marca), str(e)))
                continue
            total += 1
            sin_conclusion += 0 if ap else 1
            unos[(marca, i)] = h
            revisar(h, marca, (sintomas[i], marca))
    for marca in [""] + marcas:
        for i in range(n):
            for j in range(i + 1, n):
                h, ap = razonar({sintomas[i], sintomas[j]}, marca)
                total += 1
                sin_conclusion += 0 if ap else 1
                if not (unos[(marca, i)] <= h and unos[(marca, j)] <= h):
                    violaciones.append(("P2", (sintomas[i], sintomas[j], marca), "se perdió una conclusión"))
                revisar(h, marca, (sintomas[i], sintomas[j], marca))
                if marca == "":
                    pares[(i, j)] = h
                    _, ap2 = encadenamiento_adelante(REGLAS, h)
                    if ap2:
                        violaciones.append(("P5", (sintomas[i], sintomas[j]), [a["nombre"] for a in ap2]))
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                h, ap = razonar({sintomas[i], sintomas[j], sintomas[k]})
                total += 1
                sin_conclusion += 0 if ap else 1
                if not (pares[(i, j)] <= h and pares[(i, k)] <= h and pares[(j, k)] <= h):
                    violaciones.append(("P2", (sintomas[i], sintomas[j], sintomas[k]), "se perdió una conclusión"))
                revisar(h, "", (sintomas[i], sintomas[j], sintomas[k]))

    escenarios_modelo = 0
    for mid in sorted(MODELOS):
        marca = MODELOS[mid]["marca"]
        bloq = bloqueos_del_modelo(mid)
        aplicables = [s for s in sintomas if sintoma_aplica(s, mid)]
        for s in sintomas:                                                     # P6
            rechaza = bool(validar_entrada({s}, "", mid))
            if rechaza == (s in aplicables):
                violaciones.append(("P6", (mid, s), "la validación no coincide con sintoma_aplica"))
        unos_m = {}
        for s in aplicables:
            h, ap = razonar({s}, "", mid)
            total += 1
            escenarios_modelo += 1
            sin_conclusion += 0 if ap else 1
            unos_m[s] = h
            revisar(h, marca, (mid, s))
            if bloq & h:
                violaciones.append(("P9", (mid, s), sorted(bloq & h)))
            sin_bloqueo, _ = encadenamiento_adelante(REGLAS, hechos_de_entrada({s}, "", mid))
            if not h <= sin_bloqueo:
                violaciones.append(("P8", (mid, s), "el bloqueo añadió conclusiones"))
        for a in range(len(aplicables)):
            for b in range(a + 1, len(aplicables)):
                s1, s2 = aplicables[a], aplicables[b]
                h, ap = razonar({s1, s2}, "", mid)
                total += 1
                escenarios_modelo += 1
                sin_conclusion += 0 if ap else 1
                if not (unos_m[s1] <= h and unos_m[s2] <= h):
                    violaciones.append(("P2", (mid, s1, s2), "se perdió una conclusión"))
                revisar(h, marca, (mid, s1, s2))
                if bloq & h:
                    violaciones.append(("P9", (mid, s1, s2), sorted(bloq & h)))
    return {"total": total, "sin_conclusion": sin_conclusion, "violaciones": violaciones,
            "sintomas": n, "marcas": len(marcas), "modelos": len(MODELOS), "escenarios_modelo": escenarios_modelo}
