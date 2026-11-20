"""Interfaz web (Streamlit) del Sistema Experto del Taller de Motos.

Ejecutar desde la raíz del proyecto:   streamlit run src/app.py

Patrones usados:
  * Separación en capas: este archivo SOLO dibuja; la lógica vive en motor_inferencia.py.
  * st.session_state para recordar selecciones y el último resultado entre recargas del script.
  * Callbacks (on_click) para cargar casos y limpiar: es el único momento seguro para cambiar
    el valor de un widget que ya existe.
  * @st.cache_data para no recalcular el mismo diagnóstico.
  * Un multiselect por sistema de la moto (trae buscador) en lugar de decenas de checkboxes.
"""
import streamlit as st

from base_conocimiento import REGLAS, PREDICADOS, MARCAS, texto
from motor_inferencia import (diagnosticar, explicar_razonamiento, porque, que_falta,
                              validar_entrada, clasificar_resultado)
from casos_prueba import CASOS, ejecutar_casos
from validacion import cobertura_por_regla, explorar_escenarios

st.set_page_config(page_title="Taller Experto de Motos", page_icon="🏍️", layout="wide")

# ---------------------------------------------------------------- datos derivados de la base
GRUPOS = {}                                   # sistema de la moto -> lista de síntomas
for _nombre, _datos in PREDICADOS.items():
    if _datos[0] == "sintoma":
        GRUPOS.setdefault(_datos[1], []).append(_nombre)
CLAVES_GRUPO = {g: f"sint_{i}" for i, g in enumerate(GRUPOS)}
CASOS_UI = [c for c in CASOS if not c["error"]]          # los casos de error son solo de validación
NOMBRE_MARCA = {"": "Cualquiera / otra marca", **{k: v[0] for k, v in MARCAS.items()}}


# ---------------------------------------------------------------- caché
@st.cache_data(show_spinner=False)
def ejecutar(sintomas: tuple, marca: str):
    """Corre el motor. Los argumentos son hashables, así Streamlit puede cachear el resultado."""
    registro = []
    hechos, aplicadas = diagnosticar(set(sintomas), marca, registro)
    return sorted(hechos), aplicadas, registro


@st.cache_data(show_spinner=False)
def validacion_completa():
    return ejecutar_casos(), cobertura_por_regla(), explorar_escenarios()


# ---------------------------------------------------------------- estado y callbacks
def inicializar():
    st.session_state.setdefault("marca", "")
    st.session_state.setdefault("caso_idx", None)
    st.session_state.setdefault("resultado", None)
    for clave in CLAVES_GRUPO.values():
        st.session_state.setdefault(clave, [])


def seleccionados():
    return [s for clave in CLAVES_GRUPO.values() for s in st.session_state[clave]]


def cargar_caso():
    idx = st.session_state.get("caso_idx")
    if idx is None:
        return
    caso = CASOS_UI[idx]
    st.session_state["marca"] = caso["marca"]
    for grupo, items in GRUPOS.items():
        st.session_state[CLAVES_GRUPO[grupo]] = [s for s in items if s in caso["sintomas"]]
    st.session_state["ejecutar"] = True


def limpiar():
    st.session_state["marca"] = ""
    st.session_state["caso_idx"] = None
    st.session_state["resultado"] = None
    for clave in CLAVES_GRUPO.values():
        st.session_state[clave] = []


# ---------------------------------------------------------------- piezas de interfaz
def panel_marca(marca):
    if not marca:
        st.caption("Sin marca específica: solo se usan las reglas generales.")
        return
    nombre, pais, modelos = MARCAS[marca]
    problemas = [d[2] for d in PREDICADOS.values() if d[0] == "diagnostico" and d[4] == marca]
    st.info(f"**{nombre}** ({pais}) · ej.: {modelos}\n\n**Fallas frecuentes modeladas:**\n"
            + "\n".join(f"- {p}" for p in problemas)
            + "\n\n_Hipótesis de taller: confirmar con el manual y los llamados a revisión del fabricante._")


def tarjeta(hecho, certeza, resultado):
    marca_hecho = PREDICADOS[hecho][4]
    with st.container(border=True):
        etiqueta = f"  `{MARCAS[marca_hecho][0]}`" if marca_hecho and PREDICADOS[hecho][0] == "diagnostico" else ""
        st.markdown(f"**{texto(hecho)}**{etiqueta}")
        st.progress(int(round(certeza * 100)), text=f"Certeza {certeza:.0%}")
        with st.expander("¿Por qué?"):
            st.code(porque(hecho, resultado["iniciales"], resultado["aplicadas"]), language=None)


def mostrar_resultado(res):
    if res["errores"]:
        st.error(" ".join(res["errores"]))
        return
    aplicadas = res["aplicadas"]
    if not aplicadas:
        st.warning("**Sin conclusión.** Con los datos ingresados no se puede derivar ningún diagnóstico.")
    grupos = clasificar_resultado(aplicadas)
    for h, c in grupos["alertas"]:
        st.error(f"⛔ {texto(h)}")
        with st.expander("¿Por qué esta alerta?"):
            st.code(porque(h, res["iniciales"], aplicadas), language=None)
    if grupos["diagnosticos"]:
        st.subheader(f"🩺 Diagnósticos ({len(grupos['diagnosticos'])})")
        for h, c in grupos["diagnosticos"]:
            tarjeta(h, c, res)
    if grupos["recomendaciones"]:
        st.subheader(f"✅ Recomendaciones ({len(grupos['recomendaciones'])})")
        for h, c in grupos["recomendaciones"]:
            tarjeta(h, c, res)
    faltantes = que_falta(REGLAS, set(res["hechos"]))
    if faltantes:
        st.info("**Para llegar más lejos, verifique:**\n" + "\n".join(
            f"- {texto(concl)} → falta: {', '.join(texto(a) for a in ausentes)}" for _, concl, ausentes in faltantes))
    st.subheader("🧠 Explicación del razonamiento")
    st.caption(f"Marca: {NOMBRE_MARCA[res['marca']]} · Síntomas: {len(res['sintomas'])} · "
               f"Reglas aplicadas: {len(aplicadas)} de {len(REGLAS)}")
    if aplicadas:
        st.code(explicar_razonamiento(aplicadas), language=None)
    with st.expander("Registro de inferencia (log)"):
        st.code("\n".join(res["registro"]), language=None)


def diagnosticar_ahora():
    sintomas, marca = seleccionados(), st.session_state["marca"]
    errores = validar_entrada(set(sintomas), marca)
    if errores:
        st.session_state["resultado"] = {"errores": errores}
        return
    with st.spinner("Analizando síntomas…"):
        hechos, aplicadas, registro = ejecutar(tuple(sorted(sintomas)), marca)
    iniciales = set(sintomas) | ({"marca_" + marca} if marca else set())
    st.session_state["resultado"] = {"errores": [], "hechos": hechos, "aplicadas": aplicadas, "registro": registro,
                                     "iniciales": iniciales, "sintomas": sintomas, "marca": marca}


# ---------------------------------------------------------------- página
inicializar()
st.title("🏍️ Taller Experto de Motos")
st.caption("Sistema basado en conocimiento · encadenamiento hacia adelante · diagnóstico multimarca")

with st.sidebar:
    st.header("Moto")
    st.selectbox("Marca", options=list(NOMBRE_MARCA), format_func=NOMBRE_MARCA.get, key="marca")
    disponibles = [i for i, c in enumerate(CASOS_UI) if c["marca"] in ("", st.session_state["marca"])]
    st.selectbox("Caso precargado", options=[None] + disponibles, key="caso_idx",
                 format_func=lambda i: "— elegir —" if i is None else f"#{CASOS_UI[i]['caso']} · {CASOS_UI[i]['desc']}")
    st.button("Cargar caso y diagnosticar", on_click=cargar_caso)
    st.button("🧹 Limpiar todo", on_click=limpiar)
    st.divider()
    st.caption(f"Base: {len(REGLAS)} reglas · {len(PREDICADOS)} predicados · {len(MARCAS)} marcas.")

tab_diag, tab_base, tab_valid, tab_info = st.tabs(["🔧 Diagnóstico", "📚 Base de conocimiento",
                                                   "✅ Validación", "ℹ️ Acerca de"])

with tab_diag:
    izq, der = st.columns([1, 1.3], gap="large")
    with izq:
        st.subheader("1. Síntomas")
        panel_marca(st.session_state["marca"])
        for grupo, items in GRUPOS.items():
            st.multiselect(grupo, options=items, format_func=lambda s: PREDICADOS[s][2],
                           key=CLAVES_GRUPO[grupo], placeholder="Escriba para buscar y elija…")
        st.caption(f"Síntomas seleccionados: {len(seleccionados())}")
        pulsado = st.button("🔧 Diagnosticar", type="primary")
    if pulsado or st.session_state.pop("ejecutar", False):
        diagnosticar_ahora()
    with der:
        st.subheader("2. Resultados")
        if st.session_state["resultado"] is None:
            st.info("Elija la marca (opcional), marque los síntomas y pulse **Diagnosticar**.")
        else:
            mostrar_resultado(st.session_state["resultado"])

with tab_base:
    st.subheader("Reglas de producción")
    c1, c2, c3 = st.columns(3)
    clase = c1.selectbox("Concluye un(a)", ["Todas", "intermedio", "diagnostico", "alerta", "recomendacion"])
    marca_f = c2.selectbox("Marca", ["Todas", "Solo generales"] + [MARCAS[k][0] for k in MARCAS])
    buscar = c3.text_input("Buscar texto")
    filas = []
    for r in REGLAS:
        dc = PREDICADOS[r["entonces"]]
        if clase != "Todas" and dc[0] != clase:
            continue
        es_marca = any(c.startswith("marca_") for c in r["si"]) or dc[4]
        if marca_f == "Solo generales" and es_marca:
            continue
        if marca_f not in ("Todas", "Solo generales") and not (dc[4] and MARCAS[dc[4]][0] == marca_f):
            continue
        fila = {"Regla": r["nombre"], "SI": " Y ".join(texto(c) for c in r["si"]),
                "ENTONCES": texto(r["entonces"]), "Certeza": r["certeza"]}
        if buscar and buscar.lower() not in (fila["SI"] + fila["ENTONCES"]).lower():
            continue
        filas.append(fila)
    st.caption(f"{len(filas)} de {len(REGLAS)} reglas")
    st.dataframe(filas, hide_index=True)

with tab_valid:
    st.subheader("Validación del sistema")
    st.write("Ejecuta los casos de prueba, una prueba por regla y la exploración sistemática de escenarios.")
    if st.button("▶️ Ejecutar validación completa"):
        with st.spinner("Validando (puede tardar unos segundos)…"):
            casos_res, sin_cubrir, explor = validacion_completa()
        ok = sum(1 for r in casos_res if r["ok"])
        m1, m2, m3 = st.columns(3)
        m1.metric("Casos aprobados", f"{ok} / {len(casos_res)}")
        m2.metric("Reglas sin cubrir", len(sin_cubrir))
        m3.metric("Escenarios explorados", f"{explor['total']:,}", delta=f"{len(explor['violaciones'])} violaciones",
                  delta_color="inverse")
        st.dataframe([{"#": r["caso"], "Descripción": r["desc"], "Marca": r["marca"] or "-",
                       "Reglas disparadas": ", ".join(r["reglas"]) or ("(error esperado)" if r["error_esperado"] else "ninguna"),
                       "Estado": "✓" if r["ok"] else "✗"} for r in casos_res],
                     hide_index=True)

with tab_info:
    st.markdown("""
**Cómo funciona.** El motor parte de los síntomas (y la marca como un hecho más) y dispara reglas
`SI … ENTONCES …` hasta que no se pueden derivar hechos nuevos (*encadenamiento hacia adelante*).
Cada conclusión conserva la regla que la produjo, de modo que el botón **¿Por qué?** reconstruye la cadena completa.

**Certeza.** `mínimo(certezas de las condiciones) × certeza de la regla`. Síntomas y marca valen 1.0.

**Alcance y límites.** Las fallas por marca son hipótesis de taller, no datos oficiales: deben contrastarse con el
manual de servicio y los llamados a revisión (recall). No se modelan año, kilometraje ni negaciones.
""")
