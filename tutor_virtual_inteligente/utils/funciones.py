# -*- coding: utf-8 -*-
"""
funciones.py
============
Núcleo de Procesamiento de Lenguaje Natural (NLP) del Tutor Virtual Inteligente.

Aquí vive TODA la lógica "inteligente" del proyecto:

1. Normalización del texto (limpieza del idioma español).
2. Carga de la base de conocimientos desde un archivo CSV.
3. Vectorización de las preguntas con TF-IDF (TfidfVectorizer).
4. Búsqueda de la pregunta más parecida usando similitud coseno
   (cosine_similarity).

La idea es separar la "inteligencia" (este archivo) de la "interfaz"
(app.py para terminal y streamlit_app.py para web). Así el mismo cerebro
se reutiliza en cualquier lado.
"""

# ---------------------------------------------------------------------------
# IMPORTACIONES
# ---------------------------------------------------------------------------
import os            # Para trabajar con rutas de archivos de forma portable.
import re            # Expresiones regulares: limpiar signos de puntuación.
import unicodedata   # Para quitar tildes/acentos de las palabras.

import pandas as pd  # Pandas: leer y manipular el CSV como una tabla (DataFrame).

# TfidfVectorizer convierte texto en una matriz numérica de pesos TF-IDF.
from sklearn.feature_extraction.text import TfidfVectorizer
# cosine_similarity mide qué tan parecidos son dos vectores (0 = nada, 1 = igual).
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------------------------------
# LISTA DE PALABRAS VACÍAS (STOPWORDS) EN ESPAÑOL
# ---------------------------------------------------------------------------
# Las "stopwords" son palabras muy comunes (el, la, de, que...) que no aportan
# significado para distinguir un tema de otro. Scikit-Learn solo trae stopwords
# en inglés, así que definimos nuestra propia lista en español.
STOPWORDS_ES = {
    "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como", "con",
    "contra", "cual", "cuando", "de", "del", "desde", "donde", "durante", "e",
    "el", "ella", "ellas", "ellos", "en", "entre", "era", "es", "esa", "ese",
    "eso", "esta", "estas", "este", "esto", "estos", "ha", "hay", "la", "las",
    "le", "les", "lo", "los", "mas", "me", "mi", "mis", "mucho", "muy", "nada",
    "ni", "no", "nos", "o", "otra", "otro", "para", "pero", "poco", "por",
    "porque", "que", "quien", "se", "ser", "si", "sin", "sobre", "su", "sus",
    "tan", "te", "tu", "tus", "un", "una", "uno", "unos", "y", "ya", "yo",
    "me", "mí", "qué", "cómo", "cuál", "cuándo", "dónde", "quién",
}


# ---------------------------------------------------------------------------
# FUNCIÓN: normalizar_texto
# ---------------------------------------------------------------------------
def normalizar_texto(texto: str) -> str:
    """
    Limpia y normaliza un texto para que el modelo lo entienda mejor.

    Pasos (explicados línea por línea dentro de la función):
      1. Convertir a minúsculas  -> "Python" y "python" son lo mismo.
      2. Quitar acentos/tildes    -> "función" y "funcion" son lo mismo.
      3. Eliminar signos raros    -> dejar solo letras, números y espacios.
      4. Compactar espacios       -> evitar dobles espacios.

    Parámetros
    ----------
    texto : str
        Texto original escrito por el usuario o leído del CSV.

    Retorna
    -------
    str
        Texto limpio y listo para vectorizar.
    """
    # Si llega algo que no es texto (None, número, NaN...) lo convertimos a "".
    if not isinstance(texto, str):
        texto = str(texto) if texto is not None else ""

    # 1) Pasar todo a minúsculas.
    texto = texto.lower()

    # 2) Descomponer los caracteres acentuados (á -> a + ´) y luego eliminar
    #    los acentos (categoría "Mn" = Mark, nonspacing) usando unicodedata.
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")

    # 3) Sustituir todo lo que NO sea letra, número o espacio por un espacio.
    texto = re.sub(r"[^a-z0-9ñ\s]", " ", texto)

    # 4) Reemplazar múltiples espacios por uno solo y recortar los extremos.
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


# ---------------------------------------------------------------------------
# FUNCIÓN: cargar_base_conocimientos
# ---------------------------------------------------------------------------
def cargar_base_conocimientos(ruta_csv: str) -> pd.DataFrame:
    """
    Lee el archivo CSV con las preguntas y respuestas del tutor.

    Parámetros
    ----------
    ruta_csv : str
        Ruta al archivo `conocimientos.csv`.

    Retorna
    -------
    pandas.DataFrame
        Tabla con, al menos, las columnas: pregunta, respuesta, categoria.

    Lanza
    -----
    FileNotFoundError
        Si el archivo CSV no existe.
    ValueError
        Si faltan columnas obligatorias o si el archivo está vacío.
    """
    # Verificamos primero que el archivo exista para dar un error claro.
    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(
            f"No se encontró la base de conocimientos en: {ruta_csv}"
        )

    # Leemos el CSV. encoding='utf-8' respeta tildes y la letra ñ.
    df = pd.read_csv(ruta_csv, encoding="utf-8")

    # Comprobamos que existan las columnas que el sistema necesita.
    columnas_requeridas = {"pregunta", "respuesta", "categoria"}
    if not columnas_requeridas.issubset(df.columns):
        raise ValueError(
            "El CSV debe contener las columnas: pregunta, respuesta, categoria. "
            f"Se encontraron: {list(df.columns)}"
        )

    # Quitamos filas vacías o incompletas para no romper el modelo.
    df = df.dropna(subset=["pregunta", "respuesta"]).reset_index(drop=True)

    # --- Variantes: "varias formas de preguntar lo mismo" ---
    # Una misma celda 'pregunta' puede contener distintas formas de preguntar
    # lo mismo, separadas por el carácter '|'. Por ejemplo:
    #   "¿Qué es una variable? | que es una variable | define variable"
    # Aquí separamos cada forma en su PROPIA fila, conservando la misma
    # respuesta y categoría. Así el tutor reconoce muchas más maneras de
    # preguntar sin necesidad de duplicar el texto de la respuesta.
    df["pregunta"] = df["pregunta"].astype(str).str.split("|")  # lista de variantes
    df = df.explode("pregunta")                # una fila por cada variante
    df["pregunta"] = df["pregunta"].str.strip()  # quitamos espacios sobrantes
    df = df[df["pregunta"] != ""]              # descartamos variantes vacías
    df = df.reset_index(drop=True)             # reindexamos tras separar

    # Si después de limpiar no quedó nada, avisamos.
    if df.empty:
        raise ValueError("La base de conocimientos no tiene filas válidas.")

    return df


# ---------------------------------------------------------------------------
# CLASE PRINCIPAL: TutorVirtual
# ---------------------------------------------------------------------------
class TutorVirtual:
    """
    Cerebro del Tutor Virtual Inteligente.

    Esta clase carga la base de conocimientos, entrena un modelo TF-IDF con
    todas las preguntas y, cuando un estudiante pregunta algo, devuelve la
    respuesta de la pregunta más parecida usando similitud coseno.

    Ejemplo de uso
    --------------
    >>> tutor = TutorVirtual("data/conocimientos.csv")
    >>> resultado = tutor.responder("¿Qué es una variable?")
    >>> print(resultado["respuesta"])
    """

    def __init__(self, ruta_csv: str, umbral: float = 0.20,
                 peso_palabra: float = 0.6, peso_caracter: float = 0.4):
        """
        Constructor: prepara el tutor en cuanto se crea el objeto.

        Parámetros
        ----------
        ruta_csv : str
            Ruta al CSV de conocimientos.
        umbral : float
            Similitud mínima (entre 0 y 1) para aceptar una respuesta.
            Si la mejor coincidencia queda por debajo, el tutor responde
            que no encontró información suficiente.
        peso_palabra : float
            Peso del modelo por PALABRAS en la similitud final (significado).
        peso_caracter : float
            Peso del modelo por CARACTERES en la similitud final (tolerancia
            a errores de escritura). peso_palabra + peso_caracter debería sumar 1.
        """
        # Guardamos los parámetros como atributos del objeto.
        self.ruta_csv = ruta_csv
        self.umbral = umbral
        self.peso_palabra = peso_palabra
        self.peso_caracter = peso_caracter

        # Cargamos la base de conocimientos (DataFrame de Pandas).
        self.df = cargar_base_conocimientos(ruta_csv)

        # Normalizamos TODAS las preguntas y las guardamos en una columna nueva.
        # Esta es la versión "limpia" que usarán los vectorizadores.
        self.df["pregunta_norm"] = self.df["pregunta"].apply(normalizar_texto)

        # --- Modelo 1: vectorizador TF-IDF por PALABRAS ---
        #   - ngram_range=(1, 2): considera palabras sueltas y pares de palabras.
        #   - stop_words: ignora las palabras vacías en español.
        # Capta el SIGNIFICADO: entiende qué palabras importan en la pregunta.
        self.vectorizador_palabra = TfidfVectorizer(
            stop_words=list(STOPWORDS_ES),
            ngram_range=(1, 2),
        )

        # --- Modelo 2: vectorizador TF-IDF por CARACTERES ---
        #   - analyzer='char_wb': genera n-gramas de caracteres DENTRO de cada
        #     palabra (respetando los límites de palabra).
        #   - ngram_range=(3, 5): fragmentos de 3 a 5 letras.
        # Capta la FORMA de las palabras: aunque haya errores de escritura,
        # 'programacion' y 'progrmacion' comparten casi todos sus fragmentos,
        # así que siguen pareciéndose. Esto da tolerancia AUTOMÁTICA a typos.
        self.vectorizador_caracter = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
        )

        # Entrenamos (fit) ambos vectorizadores con las preguntas normalizadas
        # y guardamos sus matrices TF-IDF (una fila por pregunta de la base).
        self.matriz_palabra = self.vectorizador_palabra.fit_transform(
            self.df["pregunta_norm"]
        )
        self.matriz_caracter = self.vectorizador_caracter.fit_transform(
            self.df["pregunta_norm"]
        )

    # -----------------------------------------------------------------------
    # MÉTODO PRIVADO: _calcular_similitudes
    # -----------------------------------------------------------------------
    def _calcular_similitudes(self, pregunta_norm: str):
        """
        Combina la similitud por palabras y por caracteres en un solo puntaje.

        Devuelve un arreglo con la similitud (0 a 1) de la pregunta del usuario
        contra cada pregunta de la base.

        Idea: el modelo de palabras acierta cuando el usuario escribe bien;
        el modelo de caracteres "rescata" la pregunta cuando hay errores de
        escritura. La mezcla ponderada aprovecha lo mejor de ambos.
        """
        # Transformamos la pregunta con CADA vectorizador (transform, no fit).
        vector_palabra = self.vectorizador_palabra.transform([pregunta_norm])
        vector_caracter = self.vectorizador_caracter.transform([pregunta_norm])

        # Similitud coseno contra toda la base, con cada modelo.
        sim_palabra = cosine_similarity(vector_palabra, self.matriz_palabra)[0]
        sim_caracter = cosine_similarity(vector_caracter, self.matriz_caracter)[0]

        # Mezcla ponderada de ambas similitudes.
        return self.peso_palabra * sim_palabra + self.peso_caracter * sim_caracter

    # -----------------------------------------------------------------------
    # MÉTODO: responder
    # -----------------------------------------------------------------------
    def responder(self, pregunta_usuario: str) -> dict:
        """
        Recibe la pregunta del estudiante y devuelve la mejor respuesta.

        Parámetros
        ----------
        pregunta_usuario : str
            Texto que escribió el estudiante.

        Retorna
        -------
        dict
            Diccionario con:
              - 'respuesta'        : texto de la respuesta encontrada.
              - 'pregunta_similar' : pregunta de la base más parecida.
              - 'categoria'        : categoría del tema.
              - 'similitud'        : qué tan parecida fue (0 a 1).
              - 'encontrada'       : True/False según el umbral.
        """
        # Validamos que el usuario realmente haya escrito algo.
        if not pregunta_usuario or not pregunta_usuario.strip():
            return {
                "respuesta": "Por favor, escribe una pregunta para poder ayudarte.",
                "pregunta_similar": None,
                "categoria": None,
                "similitud": 0.0,
                "encontrada": False,
            }

        # 1) Normalizamos la pregunta del usuario igual que las del CSV.
        pregunta_norm = normalizar_texto(pregunta_usuario)

        # 2-3) Calculamos la similitud COMBINADA (palabras + caracteres) entre
        #      la pregunta del usuario y TODAS las preguntas de la base.
        similitudes = self._calcular_similitudes(pregunta_norm)

        # 4) Buscamos el índice de la pregunta con mayor similitud.
        indice_mejor = int(similitudes.argmax())
        mejor_similitud = float(similitudes[indice_mejor])

        # 5) Si la mejor similitud no supera el umbral, no hay buena respuesta.
        if mejor_similitud < self.umbral:
            return {
                "respuesta": (
                    "Lo siento, no encontré información suficiente sobre eso "
                    "en mi base de conocimientos. ¿Puedes reformular la pregunta "
                    "o preguntar sobre programación, matemáticas o ciencia de datos?"
                ),
                "pregunta_similar": None,
                "categoria": None,
                "similitud": round(mejor_similitud, 3),
                "encontrada": False,
            }

        # 6) Recuperamos la fila de la base que mejor coincidió.
        fila = self.df.iloc[indice_mejor]

        # 7) Devolvemos toda la información en un diccionario ordenado.
        return {
            "respuesta": fila["respuesta"],
            "pregunta_similar": fila["pregunta"],
            "categoria": fila["categoria"],
            "similitud": round(mejor_similitud, 3),
            "encontrada": True,
        }

    # -----------------------------------------------------------------------
    # MÉTODO: top_respuestas (extra, útil para depurar/mostrar alternativas)
    # -----------------------------------------------------------------------
    def top_respuestas(self, pregunta_usuario: str, n: int = 3) -> list:
        """
        Devuelve las `n` preguntas más parecidas (con su similitud).

        Es útil para mostrar "quizás también te interese" o para entender
        cómo está razonando el tutor.
        """
        # Normalizamos la pregunta y calculamos la similitud combinada.
        pregunta_norm = normalizar_texto(pregunta_usuario)
        similitudes = self._calcular_similitudes(pregunta_norm)

        # argsort ordena de menor a mayor; con [::-1] lo invertimos (mayor primero)
        # y nos quedamos con los primeros n índices.
        indices_top = similitudes.argsort()[::-1][:n]

        # Construimos una lista de diccionarios con la información de cada match.
        resultados = []
        for idx in indices_top:
            fila = self.df.iloc[int(idx)]
            resultados.append({
                "pregunta_similar": fila["pregunta"],
                "respuesta": fila["respuesta"],
                "categoria": fila["categoria"],
                "similitud": round(float(similitudes[idx]), 3),
            })
        return resultados
