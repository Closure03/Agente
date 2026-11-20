"""Validaciones automáticas de la base de conocimiento y del motor. Python puro."""
from base_conocimiento import REGLAS, PREDICADOS, MARCAS
from motor_inferencia import diagnosticar, encadenamiento_adelante, hechos_de_entrada


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
        marca = ""
        for d in list(datos):
            if d.startswith("marca_"):
                marca = d[6:]
                datos.discard(d)
        if not datos:
            continue
        _, aplicadas = diagnosticar(datos, marca)
        if r["nombre"] not in {a["nombre"] for a in aplicadas}:
            sin_cubrir.append(r["nombre"])
    return sin_cubrir


def explorar_escenarios():
    """
    Prueba TODOS los escenarios de 1, 2 y 3 síntomas (y 1-2 síntomas con cada marca).
    P1 termina sin ciclos · P2 monotonía · P3/P4 marcas no se mezclan · P5 idempotencia.
    """
    sintomas = sorted(k for k, v in PREDICADOS.items() if v[0] == "sintoma")
    marcas = sorted(MARCAS)
    diag_marca = {m: {k for k, v in PREDICADOS.items() if v[0] == "diagnostico" and v[4] == m} for m in marcas}
    todos = set().union(*diag_marca.values())
    violaciones, total, sin_conclusion = [], 0, 0

    def razonar(s, marca=""):
        return encadenamiento_adelante(REGLAS, hechos_de_entrada(s, marca))

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
    return {"total": total, "sin_conclusion": sin_conclusion, "violaciones": violaciones,
            "sintomas": n, "marcas": len(marcas)}
