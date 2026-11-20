# 🏍️ Sistema Experto para un Taller Mecánico de Motos (multimarca)

Sistema basado en conocimiento con **encadenamiento hacia adelante** e interfaz web en **Streamlit**.
Recibe síntomas (y opcionalmente la marca: KTM, Aprilia, BMW, Ducati, Triumph, Yamaha, Honda, Kawasaki, Suzuki, Harley-Davidson)
y entrega alertas de seguridad, diagnósticos, recomendaciones con nivel de certeza y la cadena de razonamiento (**¿Por qué?**).

- 147 reglas · 61 síntomas · 68 diagnósticos (37 generales + 31 por marca) · 4 alertas · 10 marcas
- 78 casos de prueba + una prueba por regla + 56.000 escenarios explorados automáticamente

> Las fallas por marca son hipótesis de taller: confirmar con el manual de servicio y los llamados a revisión (recall) del fabricante.

## 1. Requisitos
| Componente | Requisito |
|---|---|
| Python | 3.9 o superior (probado en 3.12) |
| Motor y base de conocimiento | **ninguno** (Python puro, sin imports) |
| Interfaz web | `streamlit>=1.35,<2` (ver `requirements.txt`) |
| Pruebas (opcional) | `pytest` (`requirements-dev.txt`); también corren con `python tests/test_sbc.py` |

## 2. Instalación y ejecución local
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run src/app.py           # se abre en http://localhost:8501
```
Para verlo desde otro equipo de la misma red: `streamlit run src/app.py --server.address 0.0.0.0` y abrir `http://IP-DEL-PC:8501`.

## 3. Pruebas
```bash
python tests/test_sbc.py           # sin dependencias
pytest                             # opcional
```
Los resultados detallados de los casos están en `tests/casos_prueba.md`.

## 4. Cómo exponerlo (despliegue)
**Opción A · Streamlit Community Cloud (gratis, recomendada para la entrega)**
1. Subir el proyecto a un repositorio de GitHub (`requirements.txt` debe quedar en la raíz).
2. Entrar a https://share.streamlit.io con la cuenta de GitHub → *Create app*.
3. Repositorio, rama `main`, **Main file path: `src/app.py`**, elegir Python 3.11 o 3.12 en *Advanced settings* → *Deploy*.
4. Se obtiene una URL pública `https://<nombre>.streamlit.app` para incluir en el README y en Blackboard.
   Cada `git push` redespliega automáticamente. Las apps gratuitas se duermen por inactividad: abrirla unos minutos antes de la sustentación.

**Opción B · Docker (Render, Railway, Fly.io, Hugging Face Spaces, VPS)**
```bash
docker build -t taller-motos .
docker run -p 8501:8501 taller-motos
```
En Render/Railway: servicio web desde el repositorio usando el `Dockerfile`; puerto 8501.

**Opción C · Túnel temporal desde el computador (para una demo)**
Con la app corriendo localmente: `cloudflared tunnel --url http://localhost:8501` (o `ngrok http 8501`) entrega una URL pública mientras el túnel esté abierto.

## 5. Estructura
```
proyecto-final-sbc/
├── README.md · requirements.txt · requirements-dev.txt · Dockerfile · .gitignore
├── .streamlit/config.toml        # tema y modo headless
├── src/
│   ├── base_conocimiento.py      # marcas, predicados y reglas (Python puro)
│   ├── motor_inferencia.py       # encadenamiento hacia adelante, porque(), que_falta()... (Python puro)
│   ├── casos_prueba.py           # casos de prueba (datos + ejecutor)
│   ├── validacion.py             # cobertura por regla y exploración de escenarios
│   └── app.py                    # interfaz Streamlit (única que importa streamlit)
├── tests/
│   ├── test_sbc.py
│   └── casos_prueba.md
└── docs/                         # documentacion_tecnica.pdf y manual_usuario.pdf (ver pendientes)
```

## 6. Patrones de diseño usados
- **Capas:** `app.py` solo dibuja; el motor no conoce a Streamlit, por eso se puede probar sin web y reutilizar en el notebook.
- **Base de conocimiento como datos:** reglas = diccionarios `si`/`entonces`/`certeza`; agregar una regla o marca no toca el motor ni la interfaz.
- **La marca es un hecho** (`marca_ktm`), no un motor distinto.
- **Estado:** `st.session_state` guarda selecciones y último resultado; los botones *Cargar caso* y *Limpiar* usan `on_click` (único momento seguro para cambiar el valor de un widget existente).
- **Caché:** `@st.cache_data` en el diagnóstico y en la validación completa.
- **Un `multiselect` por sistema** de la moto (incluye buscador) en lugar de 61 casillas.

## 7. Autoría
Integrantes: ______________________ · ______________________
