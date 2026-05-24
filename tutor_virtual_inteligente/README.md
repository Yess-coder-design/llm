# 🎓 Tutor Virtual Inteligente

Proyecto universitario de Inteligencia Artificial aplicado a la educación.
Es un **tutor virtual** que responde preguntas de estudiantes sobre
**programación, matemáticas y ciencia de datos**, buscando la respuesta más
relevante dentro de una base de conocimientos mediante técnicas de
**Procesamiento de Lenguaje Natural (NLP)**.

> Desarrollado por **Yessica Peñaloza**.

---

## 📝 Descripción del proyecto

El Tutor Virtual Inteligente recibe una pregunta escrita en lenguaje natural,
la limpia y la convierte en vectores numéricos con **TF-IDF**, y luego compara
esa pregunta con todas las de su base de conocimientos usando la **similitud
coseno**. Finalmente devuelve la respuesta de la pregunta más parecida.

No depende de internet ni de servicios de pago: todo el "razonamiento" se hace
de forma local con **Scikit-Learn**, lo que lo hace ideal para aprender los
fundamentos de un asistente conversacional.

---

## 🎯 Objetivos

- Aplicar **NLP** para entender preguntas de estudiantes.
- Implementar **TF-IDF** y **similitud coseno** con Scikit-Learn.
- Construir una **base de conocimientos** editable en formato CSV.
- Ofrecer un sistema **ejecutable desde terminal** y, opcionalmente, desde una
  **interfaz web** con Streamlit.
- Practicar buenas prácticas: código comentado, manejo de errores y estructura
  de proyecto ordenada.

---

## 🛠️ Tecnologías utilizadas

| Tecnología        | Uso en el proyecto                                      |
|-------------------|---------------------------------------------------------|
| **Python**        | Lenguaje principal del proyecto.                        |
| **Pandas**        | Lectura y manejo del CSV de conocimientos (DataFrame).  |
| **Scikit-Learn**  | `TfidfVectorizer` y `cosine_similarity`.                |
| **NLP / TF-IDF**  | Vectorización del texto de las preguntas.               |
| **Streamlit**     | Interfaz web sencilla (mejora opcional).                |
| **Jupyter**       | Notebook de desarrollo y experimentación.               |
| **VS Code**       | Editor recomendado para trabajar el proyecto.           |

---

## 📂 Estructura del proyecto

```
tutor_virtual_inteligente/
│
├── app.py                # Aplicación de terminal (punto de entrada)
├── streamlit_app.py      # Interfaz web opcional (Streamlit)
├── requirements.txt      # Dependencias del proyecto
├── README.md             # Este archivo
├── data/
│   └── conocimientos.csv # Base de conocimientos (preguntas y respuestas)
├── notebooks/
│   └── desarrollo.ipynb  # Notebook con el desarrollo paso a paso
└── utils/
    ├── __init__.py       # Convierte utils en un paquete de Python
    └── funciones.py      # Lógica de NLP: TF-IDF, similitud coseno y tutor
```

---

## 🚀 Instrucciones de instalación

### Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

> 💡 El entorno virtual (`venv/`) mantiene aisladas las dependencias del
> proyecto para no mezclarlas con otras instalaciones de Python.

---

## 💬 Cómo probar el tutor

Una vez ejecutado `python app.py`, escribe tus preguntas y presiona Enter.
Para terminar, escribe `salir`.

**Ejemplos de preguntas:**

```
🧑 Tú: ¿Qué es una variable en programación?
🤖 Tutor: Una variable es un espacio en la memoria de la computadora con un
          nombre, que se usa para guardar un valor...

🧑 Tú: ¿Para qué sirve un bucle for?
🤖 Tutor: Un bucle for es una estructura que repite un bloque de código un
          número determinado de veces...

🧑 Tú: ¿Qué es el aprendizaje supervisado?
🤖 Tutor: Es un tipo de machine learning donde el modelo aprende a partir de
          datos etiquetados...
```

Si haces una pregunta fuera de los temas conocidos, el tutor te avisará
amablemente que no encontró información suficiente.

---

## 🌐 Interfaz web (mejora opcional)

Para usar el tutor desde el navegador con Streamlit:

```bash
streamlit run streamlit_app.py
```

Se abrirá una página en `http://localhost:8501` con una caja de texto para
escribir preguntas.

---

## 📓 Notebook de desarrollo

El archivo `notebooks/desarrollo.ipynb` muestra el proceso completo:

1. Carga de datos.
2. Exploración de datos.
3. Vectorización TF-IDF.
4. Cálculo de la similitud coseno.
5. Pruebas del tutor virtual.

Para abrirlo:

```bash
jupyter notebook notebooks/desarrollo.ipynb
```

---

## 🧠 ¿Cómo funciona por dentro?

1. **Normalización:** las preguntas se pasan a minúsculas, se les quitan
   acentos y signos para uniformar el texto.
2. **TF-IDF:** cada pregunta se convierte en un vector numérico que refleja la
   importancia de sus palabras.
3. **Similitud coseno:** la pregunta del estudiante se compara con todas las de
   la base; gana la de mayor similitud.
4. **Umbral:** si la mejor coincidencia es muy baja, el tutor responde que no
   tiene información suficiente, evitando respuestas sin sentido.

---

## ✏️ Ampliar la base de conocimientos

Para enseñarle temas nuevos al tutor, solo edita `data/conocimientos.csv` y
agrega filas con el formato:

```
pregunta,respuesta,categoria
```

¡No hace falta tocar el código! El sistema vuelve a entrenarse automáticamente
al iniciar.

---

## 📄 Licencia

Proyecto académico de uso educativo.
