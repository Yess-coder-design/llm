# -*- coding: utf-8 -*-
"""
streamlit_app.py
================
MEJORA OPCIONAL: interfaz web del Tutor Virtual Inteligente con Streamlit.

Reutiliza exactamente el mismo cerebro (TutorVirtual) que la versión de
terminal, pero lo muestra en una página web donde el estudiante puede escribir
sus preguntas en una caja de texto.

Cómo ejecutarlo:
    streamlit run streamlit_app.py

Streamlit abrirá automáticamente el navegador en http://localhost:8501
"""

import os
import streamlit as st  # Framework para crear apps web de datos con Python.

from utils.funciones import TutorVirtual

# ---------------------------------------------------------------------------
# RUTAS
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(BASE_DIR, "data", "conocimientos.csv")


# ---------------------------------------------------------------------------
# CARGA DEL TUTOR (con caché para no reentrenar en cada interacción)
# ---------------------------------------------------------------------------
@st.cache_resource  # Guarda el tutor en memoria: se entrena una sola vez.
def cargar_tutor():
    """Crea y devuelve el objeto TutorVirtual."""
    return TutorVirtual(RUTA_CSV)


# ---------------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Tutor Virtual Inteligente", page_icon="🎓")

# Título y descripción visibles en la web.
st.title("🎓 Tutor Virtual Inteligente")
st.write(
    "Hazme preguntas sobre **programación**, **matemáticas** o "
    "**ciencia de datos** y buscaré la mejor respuesta en mi base de conocimientos."
)

# Intentamos cargar el tutor; si falla, mostramos el error en pantalla.
try:
    tutor = cargar_tutor()
except Exception as error:
    st.error(f"No se pudo cargar el tutor: {error}")
    st.stop()  # Detiene la app si no hay base de conocimientos.

# ---------------------------------------------------------------------------
# BARRA LATERAL CON EJEMPLOS
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("💡 Ejemplos de preguntas")
    st.markdown(
        "- ¿Qué es una variable en programación?\n"
        "- ¿Para qué sirve un bucle for?\n"
        "- ¿Qué es la media o promedio?\n"
        "- ¿Qué es el aprendizaje supervisado?\n"
        "- ¿Qué es TF-IDF?"
    )

# ---------------------------------------------------------------------------
# CAJA DE TEXTO Y RESPUESTA
# ---------------------------------------------------------------------------
# text_input crea una caja donde el usuario escribe su pregunta.
pregunta = st.text_input("✍️ Escribe tu pregunta:")

# Cuando hay texto, calculamos y mostramos la respuesta.
if pregunta:
    resultado = tutor.responder(pregunta)

    if resultado["encontrada"]:
        # Mostramos la respuesta en un recuadro verde de éxito.
        st.success(resultado["respuesta"])
        # Mostramos detalles (categoría, similitud, pregunta más parecida).
        st.caption(
            f"Tema: {resultado['categoria']} · "
            f"Similitud: {resultado['similitud']} · "
            f"Pregunta más parecida: «{resultado['pregunta_similar']}»"
        )
    else:
        # Si no hubo buena coincidencia, mostramos un aviso amarillo.
        st.warning(resultado["respuesta"])
