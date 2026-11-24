"""Interfaz web (Streamlit) del Sistema Experto del Taller de Motos.

Ejecutar desde la raíz del proyecto:   streamlit run src/app.py

Patrones usados:
  * Capas: este archivo SOLO dibuja; la lógica vive en motor_inferencia.py y catalogo_modelos.py.
  * st.session_state para recordar marca, modelo, síntomas y último resultado entre recargas.
  * Callbacks (on_click / on_change): único momento seguro para cambiar el valor de un widget existente.
  * @st.cache_data para no recalcular el mismo diagnóstico.
  * Un multiselect por sistema de la moto (trae buscador); sus opciones se filtran por el modelo elegido.
  * Imagen del modelo con prioridad: foto local (assets/modelos) > URL registrada > ilustración SVG.
"""
import os

import streamlit as st

from base_conocimiento import REGLAS, PREDICADOS, MARCAS, texto
from catalogo_modelos import (MODELOS, TIPOS, IMAGENES_URL, FUENTES_IMAGEN, modelos_de_marca, sintoma_aplica,
                              bloqueos_del_modelo, imagen_svg, resumen_modelo, nombre_completo)
from motor_inferencia import (diagnosticar, explicar_razonamiento, porque, que_falta,
                              validar_entrada, clasificar_resultado)
from casos_prueba import CASOS, ejecutar_casos
from validacion import cobertura_por_regla, explorar_escenarios, validar_catalogo_completo

st.set_page_config(page_title="Taller Experto de Motos", page_icon="🏍️", layout="wide")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_FOTOS = os.path.join(RAIZ, "assets", "modelos")

# ---------------------------------------------------------------- datos derivados de la base
GRUPOS = {}                                   # sistema de la moto -> lista de síntomas
for _nombre, _datos in PREDICADOS.items():
    if _datos[0] == "sintoma":
        GRUPOS.setdefault(_datos[1], []).append(_nombre)
CLAVES_GRUPO = {g: f"sint_{i}" for i, g in enumerate(GRUPOS)}
CASOS_UI = [c for c in CASOS if not c["error"]]          # los casos de error son solo de validación
NOMBRE_MARCA = {"": "Cualquiera / otra marca", **{k: v[0] for k, v in MARCAS.items()}}


def nombre_modelo(mid):
    return "— sin modelo —" if not mid else MODELOS[mid]["nombre"]


# ---------------------------------------------------------------- imágenes
def ruta_foto(mid):
    for ext in ("jpg", "jpeg", "png", "webp"):
        ruta = os.path.join(DIR_FOTOS, f"{mid}.{ext}")
        if os.path.exists(ruta):
            return ruta
    return None


def mostrar_imagen(mid):
    """Foto local si existe; si no, URL registrada; si no, ilustración SVG de referencia."""
    ruta = ruta_foto(mid)
    if ruta:
        st.image(ruta)
    elif mid in IMAGENES_URL:
        st.image(IMAGENES_URL[mid], caption=FUENTES_IMAGEN.get(mid))
    else:
        st.image(imagen_svg(mid))


# ---------------------------------------------------------------- caché
@st.cache_data(show_spinner=False)
def ejecutar(sintomas: tuple, marca: str, modelo: str):
    """Corre el motor. Los argumentos son hashables, así Streamlit puede cachear el resultado."""
    registro = []
    hechos, aplicadas = diagnosticar(set(sintomas), marca, modelo, registro)
    return sorted(hechos), aplicadas, registro


@st.cache_data(show_spinner=False)
def validacion_completa():
    return ejecutar_casos(), cobertura_por_regla(), explorar_escenarios(), validar_catalogo_completo()


# ---------------------------------------------------------------- estado y callbacks
def inicializar():
    st.session_state.setdefault("marca", "")
    st.session_state.setdefault("modelo", "")
    st.session_state.setdefault("caso_idx", None)
    st.session_state.setdefault("resultado", None)
    for clave in CLAVES_GRUPO.values():
        st.session_state.setdefault(clave, [])


def seleccionados():
    return [s for clave in CLAVES_GRUPO.values() for s in st.session_state.get(clave, [])]


def podar_sintomas():
    """Quita los síntomas que no aplican al modelo elegido (evita opciones inválidas en los multiselect)."""
    modelo = st.session_state.get("modelo", "")
    for clave in CLAVES_GRUPO.values():
        st.session_state[clave] = [s for s in st.session_state.get(clave, []) if sintoma_aplica(s, modelo)]


def al_cambiar_marca():
    st.session_state["modelo"] = ""
    st.session_state["resultado"] = None
    podar_sintomas()


def al_cambiar_modelo():
    st.session_state["resultado"] = None
    podar_sintomas()


def elegir_modelo(mid):
    st.session_state["modelo"] = mid
    st.session_state["resultado"] = None
    podar_sintomas()


def cargar_caso():
    idx = st.session_state.get("caso_idx")
    if idx is None:
        return
    caso = CASOS_UI[idx]
    st.session_state["marca"] = MODELOS[caso["modelo"]]["marca"] if caso["modelo"] else caso["marca"]
    st.session_state["modelo"] = caso["modelo"]
    for grupo, items in GRUPOS.items():
        st.session_state[CLAVES_GRUPO[grupo]] = [s for s in items if s in caso["sintomas"]]
    st.session_state["ejecutar"] = True


def limpiar():
    st.session_state["marca"] = ""
    st.session_state["modelo"] = ""
    st.session_state["caso_idx"] = None
    st.session_state["resultado"] = None
    for clave in CLAVES_GRUPO.values():
        st.session_state[clave] = []


# ---------------------------------------------------------------- piezas de interfaz
def panel_marca(marca):
    if not marca:
        st.caption("Sin marca específica: solo se usan las reglas generales. Elija una marca para ver su catálogo de modelos.")
        return
    nombre, pais, modelos = MARCAS[marca]
    problemas = [d[2] for d in PREDICADOS.values() if d[0] == "diagnostico" and d[4] == marca]
    with st.expander(f"Fallas frecuentes modeladas de {nombre}"):
        st.markdown("\n".join(f"- {p}" for p in problemas))
        st.caption("Hipótesis de taller: confirmar con el manual de servicio y los llamados a revisión del fabricante.")


def catalogo(marca):
    """Cuadrícula de modelos de la marca, con imagen y botón para elegir."""
    ids = modelos_de_marca(marca)
    elegido = st.session_state["modelo"]
    with st.expander(f"📖 Catálogo de modelos {MARCAS[marca][0]} ({len(ids)})", expanded=not elegido):
        columnas = st.columns(3)
        for n, mid in enumerate(ids):
            with columnas[n % 3]:
                with st.container(border=True):
                    mostrar_imagen(mid)
                    st.markdown(f"**{MODELOS[mid]['nombre']}**")
                    st.caption(f"{TIPOS[MODELOS[mid]['tipo']]} · {resumen_modelo(mid)}")
                    st.button("✅ Seleccionado" if mid == elegido else "Elegir este modelo", key=f"elegir_{mid}",
                              on_click=elegir_modelo, args=(mid,), disabled=(mid == elegido))


def ficha_modelo(mid):
    m = MODELOS[mid]
    with st.container(border=True):
        c1, c2 = st.columns([1, 2])
        with c1:
            mostrar_imagen(mid)
        with c2:
            st.markdown(f"### {nombre_completo(mid, MARCAS)}")
            st.caption(f"{TIPOS[m['tipo']]} · {resumen_modelo(mid)}")
            ocultos = [s for s, d in PREDICADOS.items() if d[0] == "sintoma" and not sintoma_aplica(s, mid)]
            if ocultos:
                st.caption(f"Se ocultaron {len(ocultos)} síntomas que no aplican a este modelo "
                           f"(por ejemplo: {texto(ocultos[0]).lower()}).")
            bloq = bloqueos_del_modelo(mid)
            if bloq:
                st.caption(f"{len(bloq)} diagnósticos quedan descartados por su ficha técnica.")
            st.caption("Ficha de referencia general (sin año ni versión): verificar con el fabricante.")


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
    faltantes = que_falta(REGLAS, set(res["hechos"]), bloqueados=bloqueos_del_modelo(res["modelo"]))
    if faltantes:
        st.info("**Para llegar más lejos, verifique:**\n" + "\n".join(
            f"- {texto(concl)} → falta: {', '.join(texto(a) for a in ausentes)}" for _, concl, ausentes in faltantes))
    st.subheader("🧠 Explicación del razonamiento")
    moto = nombre_completo(res["modelo"], MARCAS) if res["modelo"] else NOMBRE_MARCA[res["marca"]]
    st.caption(f"Moto: {moto} · Síntomas: {len(res['sintomas'])} · Reglas aplicadas: {len(aplicadas)} de {len(REGLAS)}")
    if aplicadas:
        st.code(explicar_razonamiento(aplicadas), language=None)
    with st.expander("Registro de inferencia (log)"):
        st.code("\n".join(res["registro"]), language=None)


def diagnosticar_ahora():
    sintomas, marca, modelo = seleccionados(), st.session_state["marca"], st.session_state["modelo"]
    errores = validar_entrada(set(sintomas), marca, modelo)
    if errores:
        st.session_state["resultado"] = {"errores": errores}
        return
    with st.spinner("Analizando síntomas…"):
        hechos, aplicadas, registro = ejecutar(tuple(sorted(sintomas)), marca, modelo)
    iniciales = set(sintomas) | ({"marca_" + marca} if marca else set())
    st.session_state["resultado"] = {"errores": [], "hechos": hechos, "aplicadas": aplicadas, "registro": registro,
                                     "iniciales": iniciales | {h for h in hechos if PREDICADOS[h][0] == "contexto"},
                                     "sintomas": sintomas, "marca": marca, "modelo": modelo}


# ---------------------------------------------------------------- página
inicializar()
st.title("🏍️ Taller Experto de Motos")
st.caption("Sistema basado en conocimiento · encadenamiento hacia adelante · diagnóstico por marca y modelo")

with st.sidebar:
    st.header("Moto")
    st.selectbox("Marca", options=list(NOMBRE_MARCA), format_func=NOMBRE_MARCA.get, key="marca",
                 on_change=al_cambiar_marca)
    opciones_modelo = [""] + modelos_de_marca(st.session_state["marca"])
    st.selectbox("Modelo", options=opciones_modelo, format_func=nombre_modelo, key="modelo",
                 on_change=al_cambiar_modelo, disabled=not st.session_state["marca"])
    marca_sel, modelo_sel = st.session_state["marca"], st.session_state["modelo"]
    disponibles = [i for i, c in enumerate(CASOS_UI)
                   if c["marca"] in ("", marca_sel) and c["modelo"] in ("", modelo_sel)]
    st.selectbox("Caso precargado", options=[None] + disponibles, key="caso_idx",
                 format_func=lambda i: "— elegir —" if i is None else f"#{CASOS_UI[i]['caso']} · {CASOS_UI[i]['desc']}")
    st.button("Cargar caso y diagnosticar", on_click=cargar_caso)
    st.button("🧹 Limpiar todo", on_click=limpiar)
    st.divider()
    st.caption(f"Base: {len(REGLAS)} reglas · {len(PREDICADOS)} predicados · {len(MARCAS)} marcas · {len(MODELOS)} modelos.")

tab_diag, tab_cat, tab_base, tab_valid, tab_info = st.tabs(
    ["🔧 Diagnóstico", "🏍️ Catálogo", "📚 Base de conocimiento", "✅ Validación", "ℹ️ Acerca de"])

with tab_diag:
    marca, modelo = st.session_state["marca"], st.session_state["modelo"]
    panel_marca(marca)
    if marca:
        catalogo(marca)
    if modelo:
        ficha_modelo(modelo)
    izq, der = st.columns([1, 1.3], gap="large")
    with izq:
        st.subheader("1. Síntomas")
        for grupo, items in GRUPOS.items():
            aplicables = [s for s in items if sintoma_aplica(s, modelo)]
            if aplicables:
                st.multiselect(grupo, options=aplicables, format_func=lambda s: PREDICADOS[s][2],
                               key=CLAVES_GRUPO[grupo], placeholder="Escriba para buscar y elija…")
            else:
                st.caption(f"{grupo}: ningún síntoma aplica a este modelo.")
        st.caption(f"Síntomas seleccionados: {len(seleccionados())}")
        pulsado = st.button("🔧 Diagnosticar", type="primary")
    if pulsado or st.session_state.pop("ejecutar", False):
        diagnosticar_ahora()
    with der:
        st.subheader("2. Resultados")
        if st.session_state["resultado"] is None:
            st.info("Elija marca y modelo (opcional), marque los síntomas y pulse **Diagnosticar**.")
        else:
            mostrar_resultado(st.session_state["resultado"])

with tab_cat:
    st.subheader("Catálogo de modelos")
    f1, f2 = st.columns(2)
    filtro_marca = f1.selectbox("Marca", ["Todas"] + list(MARCAS), format_func=lambda k: k if k == "Todas" else MARCAS[k][0],
                                key="cat_marca")
    filtro_tipo = f2.selectbox("Tipo", ["Todos"] + list(TIPOS), format_func=lambda k: k if k == "Todos" else TIPOS[k],
                               key="cat_tipo")
    filas = [{"Marca": MARCAS[m["marca"]][0], "Modelo": m["nombre"], "Tipo": TIPOS[m["tipo"]], "Cilindrada (cc)": m["cc"],
              "Motor": m["motor"], "Transmisión": m["transmision"], "Refrigeración": m["refrigeracion"],
              "Alimentación": m["alimentacion"] or "—"}
             for m in MODELOS.values()
             if filtro_marca in ("Todas", m["marca"]) and filtro_tipo in ("Todos", m["tipo"])]
    st.caption(f"{len(filas)} de {len(MODELOS)} modelos · fichas de referencia generales (sin año ni versión).")
    st.dataframe(filas, hide_index=True)
    st.info("Las imágenes son ilustraciones de referencia. Para usar fotos reales, guárdelas en "
            "`assets/modelos/<id>.jpg` (ver `assets/modelos/LEEME.md`).")

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
        es_marca = any(c.startswith("marca_") or c.startswith("modelo_") for c in r["si"]) or dc[4]
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
    st.write("Ejecuta los casos de prueba, el catálogo, una prueba por regla y la exploración sistemática de escenarios "
             "(incluye todos los modelos).")
    if st.button("▶️ Ejecutar validación completa"):
        with st.spinner("Validando (puede tardar unos segundos)…"):
            casos_res, sin_cubrir, explor, prob_cat = validacion_completa()
        ok = sum(1 for r in casos_res if r["ok"])
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Casos aprobados", f"{ok} / {len(casos_res)}")
        m2.metric("Reglas sin cubrir", len(sin_cubrir))
        m3.metric("Problemas del catálogo", len(prob_cat))
        m4.metric("Escenarios explorados", f"{explor['total']:,}", delta=f"{len(explor['violaciones'])} violaciones",
                  delta_color="inverse")
        st.caption(f"De ellos, {explor['escenarios_modelo']:,} corresponden a los {explor['modelos']} modelos del catálogo.")
        st.dataframe([{"#": r["caso"], "Descripción": r["desc"], "Marca": r["marca"] or "-",
                       "Modelo": r["modelo"] or "-",
                       "Reglas disparadas": ", ".join(r["reglas"]) or ("(error esperado)" if r["error_esperado"] else "ninguna"),
                       "Estado": "✓" if r["ok"] else "✗"} for r in casos_res], hide_index=True)

with tab_info:
    st.markdown("""
**Cómo funciona.** El motor parte de los síntomas, la marca y el modelo (todos son hechos) y dispara reglas
`SI … ENTONCES …` hasta que no se pueden derivar hechos nuevos (*encadenamiento hacia adelante*).
Cada conclusión conserva la regla que la produjo, de modo que el botón **¿Por qué?** reconstruye la cadena completa.

**El modelo filtra.** Al elegir un modelo: (1) se ocultan los síntomas que no aplican a su ficha (por ejemplo, la cadena en un
scooter o el refrigerante en un motor enfriado por aire), (2) se descartan diagnósticos incompatibles y (3) se activan
reglas que dependen de sus atributos o del modelo concreto.

**Certeza.** `mínimo(certezas de las condiciones) × certeza de la regla`. Síntomas, marca y modelo valen 1.0.

**Alcance y límites.** Las fallas por marca y modelo son hipótesis de taller, no datos oficiales: deben contrastarse con el
manual de servicio y los llamados a revisión (recall). Las fichas son de referencia general y no distinguen año ni versión.
Las imágenes son ilustraciones; pueden reemplazarse por fotos con licencia.
""")
