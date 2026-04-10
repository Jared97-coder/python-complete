"""
Módulo 2 - Ejemplo 5: Convenciones PEP 8
=========================================

Este script demuestra las convenciones de estilo de código
según PEP 8 (Python Enhancement Proposal 8).

PEP 8 es la guía de estilo oficial para código Python.
"""

# Imports: agrupados y ordenados
# 1. Librería estándar
import os
import sys
from datetime import datetime

# 2. Librerías de terceros (si las hubiera)
# import numpy as np
# import pandas as pd

# 3. Módulos locales
# from mi_modulo import mi_funcion


# =============================================================================
# CONSTANTES
# =============================================================================

# Las constantes se escriben en MAYÚSCULAS con guiones bajos
MAXIMO_INTENTOS = 3
TIMEOUT_SEGUNDOS = 30
PI = 3.14159
MENSAJE_BIENVENIDA = "Bienvenido al sistema"


# =============================================================================
# CLASES
# =============================================================================

class MiClase:
    """
    Los nombres de clases usan CapWords (PascalCase).
    
    Docstring de clase que explica su propósito.
    """
    
    def __init__(self, nombre, edad):
        """
        Constructor de la clase.
        
        Args:
            nombre (str): Nombre de la persona
            edad (int): Edad de la persona
        """
        # Atributos de instancia en snake_case
        self.nombre = nombre
        self.edad = edad
        self.fecha_registro = datetime.now()
    
    def metodo_publico(self):
        """Método público accesible desde fuera."""
        return f"{self.nombre} tiene {self.edad} años"
    
    def _metodo_protegido(self):
        """
        Método protegido (convención, prefijo _).
        Se supone de uso interno pero accesible.
        """
        return "Método protegido"
    
    def __metodo_privado(self):
        """
        Método privado (prefijo __).
        Name mangling: se convierte en _MiClase__metodo_privado
        """
        return "Método privado"


class PersonaEstudiante(MiClase):
    """
    Herencia: también usa CapWords.
    
    Docstring que describe la clase derivada.
    """
    
    def __init__(self, nombre, edad, carrera):
        """Constructor de la clase derivada."""
        super().__init__(nombre, edad)
        self.carrera = carrera
    
    def informacion_completa(self):
        """Retorna información completa del estudiante."""
        return f"{self.nombre}, {self.edad} años, estudia {self.carrera}"


# =============================================================================
# FUNCIONES
# =============================================================================

def funcion_simple():
    """
    Los nombres de funciones usan snake_case.
    
    Docstring explicando qué hace la función.
    """
    return "Hola desde función simple"


def funcion_con_parametros(parametro_uno, parametro_dos):
    """
    Función con parámetros.
    
    Args:
        parametro_uno (tipo): Descripción del primer parámetro
        parametro_dos (tipo): Descripción del segundo parámetro
    
    Returns:
        tipo: Descripción del valor de retorno
    """
    resultado = parametro_uno + parametro_dos
    return resultado


def funcion_con_parametros_default(nombre="Usuario", edad=18, activo=True):
    """
    Función con valores por defecto.
    
    Nota: No usar espacios alrededor del = en argumentos por defecto.
    
    Args:
        nombre (str, optional): Nombre del usuario. Default: "Usuario"
        edad (int, optional): Edad del usuario. Default: 18
        activo (bool, optional): Estado del usuario. Default: True
    
    Returns:
        dict: Diccionario con la información
    """
    return {
        'nombre': nombre,
        'edad': edad,
        'activo': activo
    }


def funcion_con_muchos_parametros(
    parametro_uno,
    parametro_dos,
    parametro_tres,
    parametro_cuatro,
    parametro_cinco=None
):
    """
    Cuando hay muchos parámetros, poner cada uno en su línea.
    
    Esto mejora la legibilidad.
    """
    pass


def calcular_area_rectangulo(base, altura):
    """
    Calcula el área de un rectángulo.
    
    Args:
        base (float): Base del rectángulo
        altura (float): Altura del rectángulo
    
    Returns:
        float: Área del rectángulo
    
    Example:
        >>> calcular_area_rectangulo(5, 10)
        50.0
    """
    # Una operación por línea para claridad
    area = base * altura
    return area


# =============================================================================
# ESPACIADO Y FORMATO
# =============================================================================

def demo_espaciado():
    """Demuestra reglas de espaciado según PEP 8."""
    
    # ✅ CORRECTO: Espacios alrededor de operadores
    resultado = 10 + 20
    es_mayor = resultado > 15
    multiplicacion = 5 * 3
    
    # ✅ CORRECTO: Sin espacios en slicing
    texto = "Python"
    subcadena = texto[0:3]
    
    # ✅ CORRECTO: Sin espacios antes de paréntesis de funciones
    print("Hola")
    len(texto)
    
    # ✅ CORRECTO: Sin espacios antes de corchetes
    lista = [1, 2, 3, 4, 5]
    elemento = lista[0]
    
    # ✅ CORRECTO: Sin espacios antes de coma, un espacio después
    tupla = (1, 2, 3)
    diccionario = {'a': 1, 'b': 2, 'c': 3}
    
    # ✅ CORRECTO: Espacios alrededor de = en asignaciones
    x = 5
    y = 10
    
    # ✅ CORRECTO: Sin espacios en argumentos con valor por defecto
    def funcion(param=5):
        return param
    
    # ✅ CORRECTO: En llamadas a funciones con keywords
    resultado = funcion_con_parametros_default(
        nombre="Juan",
        edad=30,
        activo=True
    )
    
    # ❌ INCORRECTO (ejemplos que NO debes seguir):
    # resultado=10+20  # Sin espacios
    # resultado = 10+20  # Inconsistente
    # print ("Hola")  # Espacio antes del paréntesis
    # lista [0]  # Espacio antes del corchete
    # tupla = (1,2,3)  # Sin espacios después de comas
    
    return resultado


def demo_longitud_linea():
    """Demuestra cómo manejar líneas largas."""
    
    # ✅ CORRECTO: Máximo 79 caracteres por línea
    mensaje_corto = "Este es un mensaje que cabe en una línea"
    
    # ✅ CORRECTO: Para líneas largas, usar paréntesis implícitos
    mensaje_largo = (
        "Este es un mensaje muy largo que necesita "
        "ser dividido en múltiples líneas para "
        "mantener la legibilidad del código"
    )
    
    # ✅ CORRECTO: Listas largas
    lista_larga = [
        'elemento_uno',
        'elemento_dos',
        'elemento_tres',
        'elemento_cuatro',
        'elemento_cinco'
    ]
    
    # ✅ CORRECTO: Diccionarios largos
    configuracion = {
        'timeout': 30,
        'max_intentos': 3,
        'debug': False,
        'logging': True,
        'archivo_log': '/var/log/app.log'
    }
    
    # ✅ CORRECTO: Llamadas a funciones con muchos argumentos
    resultado = funcion_con_muchos_parametros(
        parametro_uno="valor1",
        parametro_dos="valor2",
        parametro_tres="valor3",
        parametro_cuatro="valor4",
        parametro_cinco="valor5"
    )
    
    # ✅ CORRECTO: Condiciones largas
    if (edad >= 18 and edad <= 65 and
        tiene_licencia and
        not tiene_multas):
        print("Puede conducir")
    
    return mensaje_largo


def demo_lineas_en_blanco():
    """
    Demuestra uso de líneas en blanco.
    
    - 2 líneas en blanco antes de definiciones de clases y funciones top-level
    - 1 línea en blanco entre métodos de una clase
    - Líneas en blanco para separar secciones lógicas dentro de funciones
    """
    
    # Sección 1: Inicialización
    nombre = "Python"
    version = "3.12"
    
    # Sección 2: Procesamiento (línea en blanco para separar)
    mensaje = f"{nombre} {version}"
    
    # Sección 3: Resultado
    return mensaje


# =============================================================================
# COMENTARIOS
# =============================================================================

def demo_comentarios():
    """Demuestra buenos comentarios."""
    
    # ✅ CORRECTO: Comentario de una línea
    # Inicia con # y un espacio, en su propia línea
    x = 10
    
    # ✅ CORRECTO: Comentario inline (usar con moderación)
    y = 20  # Valor inicial
    
    # ✅ CORRECTO: Comentario multilínea para explicaciones complejas
    # Este es un algoritmo complejo que requiere explicación.
    # Primera línea de explicación.
    # Segunda línea de explicación.
    resultado = x + y
    
    # ❌ INCORRECTO (ejemplos a evitar):
    #Sin espacio después del #
    # z=30  # Comentario sin espacio antes del #
    
    # ✅ MEJOR: Usar nombres descriptivos en lugar de comentarios
    # Mal:
    # t = 30  # tiempo en segundos
    
    # Bien:
    tiempo_en_segundos = 30
    
    return resultado


def funcion_con_docstring(parametro1, parametro2):
    """
    ✅ CORRECTO: Docstring con triple comilla doble.
    
    Primera línea: resumen breve de una línea.
    
    Línea en blanco después del resumen.
    
    Luego descripción más detallada si es necesaria.
    Puede tener múltiples párrafos.
    
    Args:
        parametro1 (tipo): Descripción del parámetro 1
        parametro2 (tipo): Descripción del parámetro 2
    
    Returns:
        tipo: Descripción del valor de retorno
    
    Raises:
        TipoError: Cuándo se lanza este error
    
    Example:
        >>> funcion_con_docstring(1, 2)
        3
    """
    return parametro1 + parametro2


# =============================================================================
# CONVENCIONES DE NOMBRES
# =============================================================================

def demo_convenciones_nombres():
    """Demuestra convenciones de nombres."""
    
    # ✅ Variables y funciones: snake_case
    mi_variable = 10
    nombre_completo = "Juan Pérez"
    contador_usuarios = 0
    
    # ✅ Constantes: SNAKE_CASE_MAYUSCULAS
    MAX_USUARIOS = 100
    TIMEOUT_DEFAULT = 30
    
    # ✅ Clases: CapWords (PascalCase)
    class MiClaseEjemplo:
        pass
    
    class AdministradorUsuarios:
        pass
    
    # ✅ Métodos y atributos de instancia: snake_case
    class Persona:
        def __init__(self):
            self.nombre_completo = ""
            self.fecha_nacimiento = None
        
        def obtener_edad(self):
            pass
        
        def guardar_en_base_datos(self):
            pass
    
    # ✅ Métodos/atributos "privados": _prefijo_guion_bajo
    class CuentaBancaria:
        def __init__(self):
            self._saldo = 0  # "Privado" por convención
        
        def _validar_transaccion(self):  # Método interno
            pass
    
    # ❌ INCORRECTO (ejemplos a evitar):
    # MiVariable = 10  # No usar CapWords para variables
    # nombreCompleto = "Juan"  # No usar camelCase
    # NombreCompleto = "Juan"  # No usar PascalCase
    # def MiFuncion():  # No usar CapWords para funciones
    #     pass
    
    return mi_variable


# =============================================================================
# COMPARACIONES
# =============================================================================

def demo_comparaciones():
    """Demuestra mejores prácticas en comparaciones."""
    
    # ✅ CORRECTO: Usar "is" para None
    valor = None
    if valor is None:
        print("Valor es None")
    
    if valor is not None:
        print("Valor no es None")
    
    # ❌ INCORRECTO:
    # if valor == None:  # Funciona pero no es idiomático
    
    # ✅ CORRECTO: Usar "is" para comparar booleanos (a veces)
    activo = True
    if activo is True:
        print("Está activo")
    
    # ✅ MEJOR: Aprovechar que es booleano
    if activo:
        print("Está activo")
    
    # ✅ CORRECTO: Verificar secuencias vacías
    lista = []
    if not lista:
        print("Lista vacía")
    
    if lista:
        print("Lista tiene elementos")
    
    # ❌ INCORRECTO:
    # if len(lista) == 0:  # Funciona pero no es idiomático
    # if lista == []:  # Menos eficiente
    
    # ✅ CORRECTO: Verificar strings vacíos
    texto = ""
    if not texto:
        print("String vacío")
    
    # ✅ CORRECTO: Comparaciones encadenadas
    x = 15
    if 10 < x < 20:
        print("x está entre 10 y 20")
    
    # ❌ INCORRECTO:
    # if x > 10 and x < 20:  # Funciona pero menos pythónico
    
    return None


# =============================================================================
# EXPORTS (para módulos)
# =============================================================================

# Lista de nombres públicos del módulo
__all__ = [
    'MiClase',
    'PersonaEstudiante',
    'funcion_simple',
    'calcular_area_rectangulo'
]


# =============================================================================
# FUNCIÓN MAIN
# =============================================================================

def main():
    """
    Función principal del módulo.
    
    Se ejecuta cuando el script se ejecuta directamente.
    """
    print("\n" + "🐍" * 35)
    print("          CONVENCIONES PEP 8")
    print("🐍" * 35)
    
    print("\n" + "=" * 70)
    print("  RESUMEN DE CONVENCIONES PEP 8")
    print("=" * 70)
    
    print("\n📌 NOMBRES:")
    print("   • Variables y funciones: snake_case")
    print("   • Clases: CapWords (PascalCase)")
    print("   • Constantes: SNAKE_CASE_MAYUSCULAS")
    print("   • Privado: _prefijo_guion_bajo")
    
    print("\n📌 ESPACIADO:")
    print("   • Espacios alrededor de operadores: x = 10 + 20")
    print("   • Sin espacios en slicing: texto[0:3]")
    print("   • Sin espacios antes de (): print('Hola')")
    print("   • Un espacio después de comas: [1, 2, 3]")
    
    print("\n📌 LÍNEAS:")
    print("   • Máximo 79 caracteres por línea")
    print("   • 2 líneas en blanco antes de clases/funciones top-level")
    print("   • 1 línea en blanco entre métodos")
    
    print("\n📌 IMPORTS:")
    print("   • Al inicio del archivo")
    print("   • Agrupados: stdlib, terceros, locales")
    print("   • Un import por línea (con excepciones)")
    
    print("\n📌 COMENTARIOS:")
    print("   • Docstrings para módulos, clases, funciones")
    print("   • Comentarios en su propia línea")
    print("   • Actualizados con el código")
    
    print("\n📌 COMPARACIONES:")
    print("   • Usar 'is' para None: if x is None")
    print("   • Aprovechar truthiness: if lista:")
    print("   • Comparaciones encadenadas: if 0 < x < 10:")
    
    print("\n" + "=" * 70)
    print("✅ PEP 8 completo: https://peps.python.org/pep-0008/")
    print("=" * 70)
    
    print("\n💡 Herramientas para verificar PEP 8:")
    print("   • pylint: Analizador de código completo")
    print("   • flake8: Verificador de estilo")
    print("   • black: Formateador automático")
    print("   • autopep8: Formateador automático")
    print("   • VS Code: Extensión Python con linting integrado")
    print()


# Este patrón permite usar el archivo como script o como módulo
if __name__ == "__main__":
    main()
