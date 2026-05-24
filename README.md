# Proyecto 8: LLM — Tutor Virtual Inteligente

Tutor virtual con NLP (TF-IDF + similitud coseno) que responde preguntas de
estudiantes sobre **programación, matemáticas y ciencia de datos**.

## 📂 Proyecto completo

👉 **El proyecto está en la carpeta [`tutor_virtual_inteligente/`](tutor_virtual_inteligente/)**

- 📖 [README del proyecto](tutor_virtual_inteligente/README.md) — documentación completa
- 🖥️ [`app.py`](tutor_virtual_inteligente/app.py) — tutor por terminal
- 🌐 [`streamlit_app.py`](tutor_virtual_inteligente/streamlit_app.py) — interfaz web
- 📓 [`notebooks/desarrollo.ipynb`](tutor_virtual_inteligente/notebooks/desarrollo.ipynb) — desarrollo paso a paso
- 🧠 [`utils/funciones.py`](tutor_virtual_inteligente/utils/funciones.py) — lógica de NLP
- 🗂️ [`data/conocimientos.csv`](tutor_virtual_inteligente/data/conocimientos.csv) — base de conocimientos

## ✨ Características

- Base de conocimientos con **68 conceptos** y **330 formas de preguntar**.
- Reconoce **varias formas de preguntar lo mismo** (variantes separadas por `|`).
- **Tolera errores de escritura** automáticamente (modelo híbrido TF-IDF por
  palabras + n-gramas de caracteres).
- Funciona desde **terminal** y desde una **interfaz web** con Streamlit.

## 🚀 Cómo ejecutarlo

```bash
cd tutor_virtual_inteligente

# Windows
python -m venv venv && venv\Scripts\activate
# Linux / Mac
python3 -m venv venv && source venv/bin/activate

pip install -r requirements.txt
python app.py
```

Para los objetivos, tecnologías, ejemplos y la interfaz web con Streamlit,
consulta el [README del proyecto](tutor_virtual_inteligente/README.md).
