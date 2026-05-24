# -*- coding: utf-8 -*-
"""
app.py
======
Aplicación de TERMINAL del Tutor Virtual Inteligente.

Este es el punto de entrada que se ejecuta con:  python app.py

Su trabajo es sencillo: crear el "cerebro" (TutorVirtual), mostrar un menú de
bienvenida y entrar en un bucle donde el estudiante escribe preguntas y el
tutor responde, hasta que el estudiante decida salir.

Toda la lógica de NLP vive en utils/funciones.py; aquí solo manejamos la
interacción con el usuario (entradas y salidas por consola).
"""

# ---------------------------------------------------------------------------
# IMPORTACIONES
# ---------------------------------------------------------------------------
import os    # Para construir la ruta del CSV sin importar desde dónde se ejecute.
import sys   # Para terminar el programa con un código de salida si algo falla.

# Importamos el cerebro del tutor desde nuestro paquete utils.
from utils.funciones import TutorVirtual


# ---------------------------------------------------------------------------
# RUTAS DEL PROYECTO
# ---------------------------------------------------------------------------
# BASE_DIR es la carpeta donde está este archivo app.py.
# Lo calculamos así para que el programa funcione aunque lo ejecutes desde
# otra carpeta (evita el típico error "no se encuentra el archivo CSV").
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta completa al archivo de la base de conocimientos.
RUTA_CSV = os.path.join(BASE_DIR, "data", "conocimientos.csv")

# Palabras que el usuario puede escribir para cerrar el programa.
COMANDOS_SALIR = {"salir", "exit", "quit", "adios", "adiós", "q"}


# ---------------------------------------------------------------------------
# FUNCIONES DE INTERFAZ (presentación por consola)
# ---------------------------------------------------------------------------
def mostrar_bienvenida() -> None:
    """Imprime el encabezado y las instrucciones iniciales."""
    print("=" * 60)
    print("        🎓  TUTOR VIRTUAL INTELIGENTE  🎓")
    print("=" * 60)
    print("Hazme preguntas sobre:")
    print("   • Programación   • Matemáticas   • Ciencia de Datos")
    print()
    print("Escribe 'salir' para terminar la sesión.")
    print("-" * 60)


def mostrar_ejemplos() -> None:
    """Muestra algunas preguntas de ejemplo para guiar al estudiante."""
    print("\nEjemplos de preguntas que puedes hacer:")
    print("   - ¿Qué es una variable en programación?")
    print("   - ¿Para qué sirve un bucle for?")
    print("   - ¿Qué es la media en estadística?")
    print("   - ¿Qué es el aprendizaje supervisado?")
    print("-" * 60)


def imprimir_respuesta(resultado: dict) -> None:
    """
    Da formato bonito a la respuesta del tutor.

    Parámetros
    ----------
    resultado : dict
        Diccionario devuelto por TutorVirtual.responder().
    """
    print("\n🤖 Tutor:")
    print(f"   {resultado['respuesta']}")

    # Si encontró una buena coincidencia, mostramos algo de contexto.
    if resultado["encontrada"]:
        print(f"\n   (Tema: {resultado['categoria']} | "
              f"similitud: {resultado['similitud']})")
    print("-" * 60)


# ---------------------------------------------------------------------------
# FUNCIÓN PRINCIPAL
# ---------------------------------------------------------------------------
def main() -> None:
    """Crea el tutor y ejecuta el bucle de preguntas y respuestas."""

    # --- 1) Intentamos crear el tutor. Si el CSV falla, avisamos y salimos. ---
    try:
        tutor = TutorVirtual(RUTA_CSV)
    except FileNotFoundError as error:
        # Error típico: no existe el archivo CSV.
        print(f"[ERROR] {error}")
        print("Verifica que exista el archivo data/conocimientos.csv")
        sys.exit(1)  # Terminamos con código 1 (error).
    except ValueError as error:
        # Error típico: el CSV está mal formado o vacío.
        print(f"[ERROR] {error}")
        sys.exit(1)
    except Exception as error:  # Cualquier otro error inesperado.
        print(f"[ERROR inesperado] {error}")
        sys.exit(1)

    # --- 2) Mostramos bienvenida y ejemplos. ---
    mostrar_bienvenida()
    mostrar_ejemplos()

    # --- 3) Bucle principal: seguimos preguntando hasta que el usuario salga. ---
    while True:
        try:
            # input() detiene el programa y espera a que el estudiante escriba.
            pregunta = input("\n🧑 Tú: ").strip()
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C o Ctrl+D: salimos de forma elegante sin mostrar un error feo.
            print("\n\n¡Hasta luego! 👋")
            break

        # Si el usuario no escribió nada, volvemos a pedir una pregunta.
        if not pregunta:
            print("   (Escribe una pregunta o 'salir' para terminar.)")
            continue

        # Si escribió un comando de salida, terminamos el bucle.
        if pregunta.lower() in COMANDOS_SALIR:
            print("\n¡Gracias por estudiar conmigo! ¡Éxito! 🎉")
            break

        # --- 4) Preguntamos al tutor y mostramos la respuesta. ---
        try:
            resultado = tutor.responder(pregunta)
            imprimir_respuesta(resultado)
        except Exception as error:
            # Si algo falla durante la respuesta, lo informamos pero NO cerramos.
            print(f"[ERROR al procesar la pregunta] {error}")


# ---------------------------------------------------------------------------
# PUNTO DE ENTRADA
# ---------------------------------------------------------------------------
# Esta condición asegura que main() solo se ejecute cuando corremos el archivo
# directamente (python app.py) y no cuando se importa desde otro módulo.
if __name__ == "__main__":
    main()
