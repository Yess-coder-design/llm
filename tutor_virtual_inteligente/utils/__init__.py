# -*- coding: utf-8 -*-
"""
Paquete `utils` del Tutor Virtual Inteligente.

Convierte la carpeta `utils/` en un paquete de Python para poder importar
sus módulos con la sintaxis:  from utils.funciones import TutorVirtual

Exponemos aquí los objetos más usados para que la importación sea más corta.
"""

# Reexportamos las piezas principales del módulo `funciones`
# para poder escribir, por ejemplo:  from utils import TutorVirtual
from .funciones import TutorVirtual, normalizar_texto, cargar_base_conocimientos

# __all__ define qué nombres se exportan con "from utils import *"
__all__ = ["TutorVirtual", "normalizar_texto", "cargar_base_conocimientos"]
