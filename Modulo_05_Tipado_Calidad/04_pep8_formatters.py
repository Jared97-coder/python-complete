"""
Módulo 5.4: PEP 8, Formatters y Linters
=======================================

Conceptos:
- PEP 8: Guía de estilo de Python
- PEP 20: Zen of Python (principios de diseño)
- Black: Formateo automático
- isort: Ordenar imports
- Ruff: Linter ultrarrápido
- Documentar excepciones con # noqa

COMANDOS ÚTILES:
    black archivo.py              # Formatear archivo
    black --check .               # Verificar sin modificar
    
    isort archivo.py              # Ordenar imports
    isort --check-only .          # Solo verificar
    
    ruff check archivo.py         # Lint
    ruff check --fix .            # Auto-fix
    ruff format archivo.py        # Formatear (alternativa a black)
"""

# ============================================================================
# 1. PEP 8 - CONVENCIONES DE ESTILO
# ============================================================================

# NOMBRES:
# - Constantes: MAYÚSCULAS_CON_GUIONES
# - Clases: PascalCase
# - Funciones y variables: snake_case
# - Privados: _prefijo_con_guion_bajo

MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30.0
API_VERSION = "v1"


class UserManager:
    """Nombres de clases en PascalCase."""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self._connection = None  # Privado
    
    def get_user_by_id(self, user_id: int) -> dict:
        """Métodos y parámetros en snake_case."""
        return {"id": user_id, "name": "Usuario"}


# LONGITUD DE LÍNEA: máximo 88 caracteres (Black) o 79 (PEP 8 original)
def funcion_con_muchos_parametros(
    parametro1: str,
    parametro2: int,
    parametro3: float,
    parametro4: bool,
) -> dict:
    """Dividir líneas largas con parámetros en múltiples líneas."""
    return {
        "param1": parametro1,
        "param2": parametro2,
        "param3": parametro3,
        "param4": parametro4,
    }


# ESPACIADO:
# - 2 líneas en blanco entre definiciones de nivel superior
# - 1 línea en blanco entre métodos de clase


class EjemploEspaciado:
    """Ejemplo de espaciado correcto."""
    
    def metodo1(self) -> None:
        """Primer método."""
        pass
    
    def metodo2(self) -> None:
        """Segundo método."""
        pass


# Función de nivel superior (2 líneas en blanco antes)


def funcion_nivel_superior() -> None:
    """Función en nivel superior."""
    pass


# ============================================================================
# 2. PEP 20 - ZEN OF PYTHON
# ============================================================================

"""
Principios del Zen of Python (import this):

1. Beautiful is better than ugly
2. Explicit is better than implicit
3. Simple is better than complex
4. Complex is better than complicated
5. Flat is better than nested
6. Sparse is better than dense
7. Readability counts
8. Special cases aren't special enough to break the rules
9. Although practicality beats purity
10. Errors should never pass silently
11. Unless explicitly silenced
12. In the face of ambiguity, refuse the temptation to guess
13. There should be one-- and preferably only one --obvious way to do it
14. Although that way may not be obvious at first unless you're Dutch
15. Now is better than never
16. Although never is often better than *right* now
17. If the implementation is hard to explain, it's a bad idea
18. If the implementation is easy to explain, it may be a good idea
19. Namespaces are one honking great idea -- let's do more of those!
"""

# Ejemplo 1: Explicit is better than implicit
# ❌ MAL (implícito)
def get_data():
    """No sabemos qué retorna."""
    return [1, 2, 3]


# ✅ BIEN (explícito)
def get_user_ids() -> list[int]:
    """Explícito: retorna lista de IDs de usuario."""
    return [1, 2, 3]


# Ejemplo 2: Simple is better than complex
# ❌ MAL (complejo)
def es_par_complejo(n: int) -> bool:
    if n % 2 == 0:
        return True
    else:
        return False


# ✅ BIEN (simple)
def es_par_simple(n: int) -> bool:
    return n % 2 == 0


# Ejemplo 3: Flat is better than nested
# ❌ MAL (anidado)
def procesar_pedido_mal(pedido: dict) -> str:
    if pedido:
        if "items" in pedido:
            if len(pedido["items"]) > 0:
                return "Procesando"
            else:
                return "Sin items"
        else:
            return "Sin items"
    else:
        return "Pedido inválido"


# ✅ BIEN (flat - guard clauses)
def procesar_pedido_bien(pedido: dict) -> str:
    if not pedido:
        return "Pedido inválido"
    
    if "items" not in pedido or not pedido["items"]:
        return "Sin items"
    
    return "Procesando"


# Ejemplo 4: Readability counts
# ❌ MAL (difícil de leer)
def f(x,y,z):return x*y+z if x>0 else 0


# ✅ BIEN (legible)
def calcular_formula(base: float, multiplicador: float, ajuste: float) -> float:
    """Calcula: (base * multiplicador) + ajuste si base es positiva."""
    if base <= 0:
        return 0.0
    return (base * multiplicador) + ajuste


# ============================================================================
# 3. IMPORTS - PEP 8 E ISORT
# ============================================================================

# Orden correcto de imports (isort lo hace automáticamente):
# 1. Librería estándar
# 2. Librerías de terceros
# 3. Imports locales

# Librería estándar
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Terceros (si hubiera)
# import requests
# import pandas as pd

# Locales (si hubiera)
# from .models import Usuario
# from .utils import validar_email


# isort agrupa y ordena automáticamente
# Ejecutar: isort archivo.py

# ============================================================================
# 4. BLACK - FORMATEO AUTOMÁTICO
# ============================================================================

# Black es "opinionated" - tiene pocas opciones de configuración
# Formatea automáticamente según su estilo

# Antes de Black:
def sin_formatear(a,b,c):
    resultado=a+b*c
    lista=[1,2,3,4,5,6,7,8,9,10]
    diccionario={'key1':'value1','key2':'value2','key3':'value3'}
    return resultado,lista,diccionario


# Después de Black (formateado):
def con_black(a: int, b: int, c: int) -> tuple:
    """Black formatea automáticamente."""
    resultado = a + b * c
    lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    diccionario = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
    }
    return resultado, lista, diccionario


# Black usa 88 caracteres por línea (no 79)
# pyproject.toml:
"""
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
    \.git
  | \.mypy_cache
  | \.venv
  | build
  | dist
)/
'''
"""


# ============================================================================
# 5. RUFF - LINTER ULTRARRÁPIDO
# ============================================================================

# Ruff reemplaza varios linters:
# - flake8
# - pylint (parcialmente)
# - isort
# - pyupgrade
# - autoflake
# Y muchos más...

# Ejemplos de reglas de Ruff:

# E501: Line too long (>88 chars)
# linea_muy_larga = "Esta es una línea extremadamente larga que supera los 88 caracteres y debería dividirse en múltiples líneas"  # noqa: E501

# F401: Module imported but unused
# import json  # Si no se usa, ruff lo detecta

# F841: Local variable assigned but never used
def ejemplo_variable_sin_usar() -> None:
    usado = 10
    sin_usar = 20  # ruff: F841
    print(usado)


# E711: Comparison to None should be 'if cond is None:'
def comparacion_none_mal(valor) -> bool:
    if valor == None:  # ❌ MAL - usar 'is None'
        return True
    return False


def comparacion_none_bien(valor) -> bool:
    if valor is None:  # ✅ BIEN
        return True
    return False


# E712: Comparison to True/False should be 'if cond:' or 'if not cond:'
def comparacion_bool_mal(activo: bool) -> str:
    if activo == True:  # ❌ MAL
        return "Activo"
    return "Inactivo"


def comparacion_bool_bien(activo: bool) -> str:
    if activo:  # ✅ BIEN
        return "Activo"
    return "Inactivo"


# ============================================================================
# 6. NOQA Y TYPE: IGNORE - EXCEPCIONES DOCUMENTADAS
# ============================================================================

# # noqa para desactivar reglas de linters
def ejemplo_noqa() -> None:
    """Ejemplos de cuándo usar # noqa."""
    
    # Desactivar regla específica
    x = 1  # noqa: F841  - variable sin usar (OK para ejemplo)
    
    # Desactivar todas las reglas en esta línea
    y = 2  # noqa
    
    # mypy: type: ignore
    dato: int = "string"  # type: ignore  - sabemos que está mal pero lo necesitamos


# Líneas muy largas con URLs (no se pueden romper)
URL = "https://api.ejemplo.com/v1/usuarios?filtro=activo&limite=100&orden=nombre"  # noqa: E501


# ============================================================================
# 7. DOCSTRINGS - PEP 257
# ============================================================================

def funcion_documentada(parametro1: str, parametro2: int) -> str:
    """
    Una línea de resumen concisa.
    
    Descripción más detallada si es necesario. Puede ocupar
    múltiples líneas y explicar el comportamiento de la función.
    
    Args:
        parametro1: Descripción del primer parámetro.
        parametro2: Descripción del segundo parámetro.
    
    Returns:
        Descripción del valor de retorno.
    
    Raises:
        ValueError: Si parametro2 es negativo.
    
    Examples:
        >>> funcion_documentada("hola", 5)
        'hola-5'
    """
    if parametro2 < 0:
        raise ValueError("parametro2 debe ser positivo")
    return f"{parametro1}-{parametro2}"


class ClaseDocumentada:
    """
    Resumen de una línea de la clase.
    
    Descripción más detallada de la clase, su propósito
    y cómo usarla.
    
    Attributes:
        atributo1: Descripción del atributo.
        atributo2: Descripción del otro atributo.
    
    Examples:
        >>> obj = ClaseDocumentada("valor")
        >>> obj.metodo()
        'resultado'
    """
    
    def __init__(self, valor: str):
        """Inicializa la clase con un valor."""
        self.atributo1 = valor
        self.atributo2 = 0
    
    def metodo(self) -> str:
        """
        Método de ejemplo.
        
        Returns:
            String con el resultado.
        """
        return "resultado"


# ============================================================================
# 8. CONFIGURACIÓN DE RUFF
# ============================================================================

# pyproject.toml para Ruff:
"""
[tool.ruff]
# Target Python 3.11
target-version = "py311"

# Longitud de línea
line-length = 88

# Directorios a excluir
exclude = [
    ".git",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "__pycache__",
    "build",
    "dist",
]

# Reglas a activar
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "N",   # pep8-naming
]

# Reglas a ignorar
ignore = [
    "E501",  # Line too long (Black se encarga)
    "B008",  # Function call in argument defaults
]

# Auto-fix
fix = true
fixable = ["ALL"]
unfixable = []

[tool.ruff.format]
# Like Black
quote-style = "double"
indent-style = "space"
line-ending = "auto"

[tool.ruff.lint.isort]
known-first-party = ["mi_proyecto"]

[tool.ruff.lint.per-file-ignores]
# Ignorar imports no usados en __init__.py
"__init__.py" = ["F401"]
# Ignorar en tests
"tests/*" = ["S101"]  # Use of assert
"""


# ============================================================================
# 9. EJEMPLO COMPLETO: CÓDIGO DE CALIDAD
# ============================================================================

from dataclasses import dataclass
from enum import Enum


class EstadoUsuario(Enum):
    """Estados posibles de un usuario."""
    
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    SUSPENDIDO = "suspendido"


@dataclass
class Usuario:
    """
    Representa un usuario del sistema.
    
    Attributes:
        id: Identificador único del usuario.
        nombre: Nombre completo del usuario.
        email: Correo electrónico del usuario.
        estado: Estado actual del usuario.
    """
    
    id: int
    nombre: str
    email: str
    estado: EstadoUsuario = EstadoUsuario.ACTIVO
    
    def activar(self) -> None:
        """Activa el usuario."""
        self.estado = EstadoUsuario.ACTIVO
    
    def suspender(self) -> None:
        """Suspende el usuario."""
        self.estado = EstadoUsuario.SUSPENDIDO
    
    def esta_activo(self) -> bool:
        """Verifica si el usuario está activo."""
        return self.estado == EstadoUsuario.ACTIVO


class GestorUsuarios:
    """
    Gestiona operaciones con usuarios.
    
    Proporciona funcionalidades para crear, buscar y administrar
    usuarios en el sistema.
    """
    
    def __init__(self) -> None:
        """Inicializa el gestor con almacenamiento vacío."""
        self._usuarios: Dict[int, Usuario] = {}
    
    def crear_usuario(
        self,
        id: int,
        nombre: str,
        email: str,
    ) -> Usuario:
        """
        Crea un nuevo usuario en el sistema.
        
        Args:
            id: ID único del usuario.
            nombre: Nombre completo del usuario.
            email: Email del usuario.
        
        Returns:
            El usuario creado.
        
        Raises:
            ValueError: Si el ID ya existe.
        """
        if id in self._usuarios:
            raise ValueError(f"Usuario con ID {id} ya existe")
        
        usuario = Usuario(id=id, nombre=nombre, email=email)
        self._usuarios[id] = usuario
        return usuario
    
    def obtener_usuario(self, id: int) -> Optional[Usuario]:
        """
        Obtiene un usuario por su ID.
        
        Args:
            id: ID del usuario a buscar.
        
        Returns:
            El usuario si existe, None en caso contrario.
        """
        return self._usuarios.get(id)
    
    def listar_activos(self) -> List[Usuario]:
        """
        Lista todos los usuarios activos.
        
        Returns:
            Lista de usuarios con estado ACTIVO.
        """
        return [
            usuario
            for usuario in self._usuarios.values()
            if usuario.esta_activo()
        ]


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    """Función principal para demostrar el código."""
    print("=" * 70)
    print("PEP 8 Y CALIDAD DE CÓDIGO")
    print("=" * 70)
    
    gestor = GestorUsuarios()
    
    # Crear usuarios
    usuario1 = gestor.crear_usuario(1, "Ana García", "ana@example.com")
    usuario2 = gestor.crear_usuario(2, "Juan Pérez", "juan@example.com")
    
    print(f"Usuario creado: {usuario1.nombre}")
    
    # Suspender usuario
    usuario2.suspender()
    
    # Listar activos
    activos = gestor.listar_activos()
    print(f"\nUsuarios activos: {len(activos)}")
    for usuario in activos:
        print(f"  - {usuario.nombre} ({usuario.email})")
    
    print("\n" + "=" * 70)
    print("EJECUTA:")
    print("  black 04_pep8_formatters.py")
    print("  ruff check 04_pep8_formatters.py")
    print("  isort 04_pep8_formatters.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
