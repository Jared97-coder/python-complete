# Módulo 2: Fundamentos del Lenguaje Python

## 📋 Tabla de Contenidos
1. [Introducción](#introducción)
2. [Variables y Tipos de Datos](#variables-y-tipos-de-datos)
3. [Operadores](#operadores)
4. [Entrada y Salida de Datos](#entrada-y-salida-de-datos)
5. [Conversión de Tipos](#conversión-de-tipos)
6. [Comentarios y Documentación](#comentarios-y-documentación)
7. [Convenciones de Código (PEP 8)](#convenciones-de-código-pep-8)
8. [Buenas Prácticas](#buenas-prácticas)
9. [Ejercicios Prácticos](#ejercicios-prácticos)

---

## 🎯 Introducción

Python es un lenguaje de **tipado dinámico** y **fuertemente tipado**:
- **Tipado dinámico**: No necesitas declarar el tipo de variable
- **Fuertemente tipado**: No permite operaciones entre tipos incompatibles sin conversión explícita

### Objetivos del Módulo
- ✅ Entender variables y tipos de datos básicos
- ✅ Dominar operadores aritméticos y lógicos
- ✅ Manejar entrada y salida de datos
- ✅ Aplicar conversiones entre tipos
- ✅ Escribir código limpio siguiendo PEP 8
- ✅ Documentar código apropiadamente

---

## 📦 Variables y Tipos de Datos

### Variables

Una **variable** es un contenedor que almacena un valor.

#### Declaración y Asignación

```python
# Asignación simple
nombre = "Juan"
edad = 25
altura = 1.75
es_estudiante = True

# Asignación múltiple
x, y, z = 1, 2, 3

# Mismo valor a múltiples variables
a = b = c = 0

# Intercambiar valores (Python idiomático)
x, y = y, x
```

#### Reglas para Nombres de Variables

✅ **Permitido:**
```python
nombre = "Ana"
edad_usuario = 30
precio_total = 100.50
_privado = "valor"
usuario123 = "user"
CONSTANTE = 3.14159
```

❌ **No permitido:**
```python
2nombre = "Error"      # No puede comenzar con número
nombre-usuario = "Error"  # No puede tener guiones
class = "Error"        # No puede ser palabra reservada
nombre usuario = "Error"  # No puede tener espacios
```

#### Convenciones de Nombres

```python
# Variables y funciones: snake_case
nombre_completo = "Juan Pérez"
calcular_precio_total()

# Constantes: MAYÚSCULAS
PI = 3.14159
MAX_INTENTOS = 3

# Clases: PascalCase
class UsuarioRegistrado:
    pass

# Variables privadas: prefijo _
_variable_privada = 10
```

### Tipos de Datos Básicos

#### 1. Números (Numeric Types)

##### Enteros (int)
```python
# Números enteros
edad = 25
temperatura = -10
poblacion = 1_000_000  # Separador de miles (Python 3.6+)

# Diferentes bases
binario = 0b1010      # Base 2 = 10
octal = 0o12          # Base 8 = 10
hexadecimal = 0xA     # Base 16 = 10

print(f"Binario {binario}, Octal {octal}, Hex {hexadecimal}")
# Salida: Binario 10, Octal 10, Hex 10
```

##### Flotantes (float)
```python
# Números decimales
precio = 19.99
temperatura = -3.5
avogadro = 6.022e23   # Notación científica

# Precisión limitada
x = 0.1 + 0.2
print(x)  # 0.30000000000000004 (problema conocido)

# Usar Decimal para precisión financiera
from decimal import Decimal
precio1 = Decimal('19.99')
precio2 = Decimal('10.01')
total = precio1 + precio2  # Decimal('30.00')
```

##### Complejos (complex)
```python
# Números complejos
z = 3 + 4j
print(z.real)  # 3.0
print(z.imag)  # 4.0

# Operaciones
z1 = 2 + 3j
z2 = 1 - 2j
suma = z1 + z2  # (3+1j)
```

#### 2. Cadenas de Texto (str)

```python
# Comillas simples o dobles (indistinto)
nombre = 'Juan'
apellido = "Pérez"

# Comillas triples para múltiples líneas
descripcion = """
Este es un texto
de múltiples líneas.
Muy útil para documentación.
"""

# Caracteres de escape
texto = "Línea 1\nLínea 2\tTabulado"
ruta = "C:\\Users\\Juan\\Desktop"  # Escapar backslash
raw_string = r"C:\Users\Juan\Desktop"  # Raw string (no escapa)

# Concatenación
nombre_completo = nombre + " " + apellido
saludo = "Hola " * 3  # "Hola Hola Hola "

# Indexación y slicing
texto = "Python"
print(texto[0])      # 'P' (primer carácter)
print(texto[-1])     # 'n' (último carácter)
print(texto[0:3])    # 'Pyt' (índice 0 a 2)
print(texto[2:])     # 'thon' (desde índice 2)
print(texto[:4])     # 'Pyth' (hasta índice 3)
print(texto[::2])    # 'Pto' (cada 2 caracteres)
print(texto[::-1])   # 'nohtyP' (invertido)

# Métodos útiles
texto = "  Hola Mundo  "
print(texto.upper())        # "  HOLA MUNDO  "
print(texto.lower())        # "  hola mundo  "
print(texto.strip())        # "Hola Mundo" (sin espacios)
print(texto.replace("o", "0"))  # "  H0la Mund0  "
print(texto.split())        # ['Hola', 'Mundo']
print(len(texto))           # 14 (longitud)

# Verificaciones
print("Hola".startswith("H"))  # True
print("Mundo".endswith("o"))   # True
print("Python".isalpha())      # True
print("123".isdigit())         # True
```

#### 3. Booleanos (bool)

```python
# Solo dos valores posibles
verdadero = True
falso = False

# Valores que evalúan a False
bool(0)           # False
bool(0.0)         # False
bool("")          # False (string vacío)
bool([])          # False (lista vacía)
bool({})          # False (dict vacío)
bool(None)        # False

# Valores que evalúan a True
bool(1)           # True
bool(-1)          # True
bool("texto")     # True
bool([1, 2])      # True
bool({"a": 1})    # True

# Operaciones lógicas
print(True and False)   # False
print(True or False)    # True
print(not True)         # False
```

#### 4. None (Tipo Nulo)

```python
# Representa ausencia de valor
resultado = None

def funcion_sin_return():
    pass

valor = funcion_sin_return()
print(valor)  # None

# Verificar si es None
if resultado is None:
    print("No hay resultado")

# No confundir con False
print(None == False)   # False
print(None is False)   # False
```

### Verificar Tipo de Dato

```python
# type() retorna el tipo
numero = 42
print(type(numero))     # <class 'int'>

texto = "Hola"
print(type(texto))      # <class 'str'>

# isinstance() verifica tipo
print(isinstance(numero, int))      # True
print(isinstance(texto, str))       # True
print(isinstance(numero, (int, float)))  # True (cualquiera de los tipos)
```

**Archivo de ejemplo**: `01_variables_tipos.py`

---

## ➕ Operadores

### Operadores Aritméticos

```python
a = 10
b = 3

# Operaciones básicas
suma = a + b        # 13
resta = a - b       # 7
multiplicacion = a * b  # 30
division = a / b    # 3.3333... (siempre retorna float)
division_entera = a // b  # 3 (división sin decimales)
modulo = a % b      # 1 (resto de la división)
potencia = a ** b   # 1000 (10^3)

# Operadores de asignación compuesta
x = 5
x += 3   # x = x + 3  →  8
x -= 2   # x = x - 2  →  6
x *= 4   # x = x * 4  →  24
x /= 3   # x = x / 3  →  8.0
x //= 2  # x = x // 2  →  4.0
x %= 3   # x = x % 3  →  1.0
x **= 2  # x = x ** 2  →  1.0
```

### Operadores de Comparación

```python
# Retornan valores booleanos (True/False)
a = 5
b = 3

print(a == b)   # False (igual a)
print(a != b)   # True (diferente de)
print(a > b)    # True (mayor que)
print(a < b)    # False (menor que)
print(a >= b)   # True (mayor o igual)
print(a <= b)   # False (menor o igual)

# Comparaciones encadenadas
x = 5
print(1 < x < 10)    # True (equivale a: 1 < x and x < 10)
print(10 > x >= 3)   # True

# Comparación de strings (lexicográfica)
print("abc" < "abd")      # True
print("Python" == "python")  # False (case-sensitive)
```

### Operadores Lógicos

```python
# and: retorna True si ambos son True
print(True and True)    # True
print(True and False)   # False
print(5 > 3 and 10 > 7)  # True

# or: retorna True si al menos uno es True
print(True or False)    # True
print(False or False)   # False
print(5 > 10 or 3 > 1)  # True

# not: invierte el valor booleano
print(not True)         # False
print(not False)        # True
print(not (5 > 3))      # False

# Cortocircuito (short-circuit)
edad = 20
print(edad >= 18 and edad < 65)  # Si edad < 18, no evalúa la segunda parte

# Precedencia
resultado = 5 > 3 or 2 > 4 and 1 < 0
# and tiene mayor precedencia que or
# Equivale a: (5 > 3) or ((2 > 4) and (1 < 0))
print(resultado)  # True
```

### Operadores de Identidad

```python
# is: verifica si son el mismo objeto en memoria
a = [1, 2, 3]
b = a           # b apunta al mismo objeto
c = [1, 2, 3]   # c es un objeto diferente

print(a is b)       # True (mismo objeto)
print(a is c)       # False (objetos diferentes)
print(a == c)       # True (mismo contenido)

# is not
x = None
print(x is None)     # True
print(x is not None) # False

# Importante con strings y números pequeños
x = 5
y = 5
print(x is y)  # True (Python cachea números pequeños)

a = "hola"
b = "hola"
print(a is b)  # True (Python cachea strings literales)
```

### Operadores de Pertenencia

```python
# in: verifica si un elemento está en una secuencia
texto = "Python"
print('P' in texto)      # True
print('x' in texto)      # False

numeros = [1, 2, 3, 4, 5]
print(3 in numeros)      # True
print(10 in numeros)     # False

# not in
print('x' not in texto)  # True
print(3 not in numeros)  # False

# Con diccionarios (verifica llaves)
persona = {'nombre': 'Juan', 'edad': 30}
print('nombre' in persona)    # True
print('Juan' in persona)      # False (no es una llave)
```

### Operadores Bitwise (Bit a Bit)

```python
# Para operaciones a nivel de bits
a = 60  # 0011 1100 en binario
b = 13  # 0000 1101 en binario

print(a & b)   # 12  (AND)  → 0000 1100
print(a | b)   # 61  (OR)   → 0011 1101
print(a ^ b)   # 49  (XOR)  → 0011 0001
print(~a)      # -61 (NOT)  → invierte bits
print(a << 2)  # 240 (shift izquierda) → 1111 0000
print(a >> 2)  # 15  (shift derecha)   → 0000 1111
```

### Precedencia de Operadores

De mayor a menor precedencia:

```python
# 1. Paréntesis
# 2. Exponenciación (**)
# 3. Unario (+, -, not)
# 4. Multiplicación, División (*, /, //, %)
# 5. Suma, Resta (+, -)
# 6. Comparación (<, <=, >, >=, ==, !=)
# 7. Lógicos (and, or)

# Ejemplo
resultado = 2 + 3 * 4 ** 2
# Se resuelve como: 2 + (3 * (4 ** 2)) = 2 + 48 = 50

# Usar paréntesis para claridad
resultado = (2 + 3) * (4 ** 2)  # 5 * 16 = 80
```

**Archivo de ejemplo**: `02_operadores.py`

---

## 💬 Entrada y Salida de Datos

### Salida: print()

```python
# Uso básico
print("Hola Mundo")

# Múltiples valores
nombre = "Juan"
edad = 25
print("Nombre:", nombre, "Edad:", edad)
# Salida: Nombre: Juan Edad: 25

# Parámetro sep (separador)
print("uno", "dos", "tres", sep="-")
# Salida: uno-dos-tres

# Parámetro end (final de línea)
print("Primera línea", end=" ")
print("Segunda línea")
# Salida: Primera línea Segunda línea

# Sin salto de línea
for i in range(5):
    print(i, end=" ")  # 0 1 2 3 4

# Formateo con f-strings (Python 3.6+)
nombre = "Ana"
edad = 30
print(f"Hola, soy {nombre} y tengo {edad} años")

# Expresiones dentro de f-strings
precio = 100
print(f"Precio con IVA: ${precio * 1.16:.2f}")
# Salida: Precio con IVA: $116.00

# Formato con format()
print("Hola, soy {} y tengo {} años".format(nombre, edad))
print("Hola, soy {0} y tengo {1} años. Me llamo {0}".format(nombre, edad))

# Formato con %
print("Hola, soy %s y tengo %d años" % (nombre, edad))
```

#### Formato de Números

```python
numero = 3.14159265

# Especificar decimales
print(f"{numero:.2f}")     # 3.14
print(f"{numero:.4f}")     # 3.1416

# Notación científica
grande = 1234567890
print(f"{grande:.2e}")     # 1.23e+09

# Separador de miles
print(f"{grande:,}")       # 1,234,567,890

# Relleno y alineación
print(f"{numero:10.2f}")   # "      3.14" (ancho 10)
print(f"{numero:<10.2f}")  # "3.14      " (izquierda)
print(f"{numero:>10.2f}")  # "      3.14" (derecha)
print(f"{numero:^10.2f}")  # "   3.14   " (centro)
print(f"{numero:0>10.2f}") # "0000003.14" (relleno con 0)

# Porcentajes
fraccion = 0.75
print(f"{fraccion:.1%}")   # 75.0%
```

### Entrada: input()

```python
# Siempre retorna string
nombre = input("¿Cuál es tu nombre? ")
print(f"Hola, {nombre}")

# Convertir a número
edad_str = input("¿Cuántos años tienes? ")
edad = int(edad_str)
print(f"En 5 años tendrás {edad + 5} años")

# En una línea
edad = int(input("¿Cuántos años tienes? "))

# Validación básica
while True:
    try:
        edad = int(input("Ingresa tu edad: "))
        if edad > 0:
            break
        else:
            print("La edad debe ser positiva")
    except ValueError:
        print("Por favor, ingresa un número válido")

# Múltiples valores
datos = input("Ingresa nombre, edad y ciudad (separados por coma): ")
nombre, edad, ciudad = datos.split(',')
print(f"Nombre: {nombre.strip()}")
print(f"Edad: {edad.strip()}")
print(f"Ciudad: {ciudad.strip()}")
```

**Archivo de ejemplo**: `03_entrada_salida.py`

---

## 🔄 Conversión de Tipos (Type Casting)

### Conversiones Explícitas

```python
# String a número
numero_str = "42"
numero_int = int(numero_str)      # 42
numero_float = float(numero_str)  # 42.0

# Número a string
edad = 25
edad_str = str(edad)              # "25"

# Float a int (trunca decimales)
precio = 19.99
precio_int = int(precio)          # 19 (no redondea, trunca)

# Redondear
import math
precio_redondeado = round(precio)     # 20
precio_arriba = math.ceil(precio)     # 20
precio_abajo = math.floor(precio)     # 19

# String a lista
texto = "Hola"
lista = list(texto)   # ['H', 'o', 'l', 'a']

# Lista a string
lista = ['H', 'o', 'l', 'a']
texto = ''.join(lista)  # "Hola"

# String a bool
print(bool(""))       # False (string vacío)
print(bool("False"))  # True (cualquier string no vacío)

# Número a bool
print(bool(0))        # False
print(bool(1))        # True
print(bool(-5))       # True
```

### Conversiones con Bases

```python
# Decimal a otras bases
numero = 10

# A binario (string)
binario = bin(numero)      # '0b1010'
binario_sin_prefijo = bin(numero)[2:]  # '1010'

# A octal
octal = oct(numero)        # '0o12'

# A hexadecimal
hexadecimal = hex(numero)  # '0xa'

# De otras bases a decimal
binario_str = '1010'
decimal = int(binario_str, 2)    # 10

octal_str = '12'
decimal = int(octal_str, 8)      # 10

hex_str = 'a'
decimal = int(hex_str, 16)       # 10
```

### Manejo de Errores en Conversión

```python
# ValueError si no se puede convertir
try:
    numero = int("abc")
except ValueError as e:
    print(f"Error: {e}")  # invalid literal for int()

# Validar antes de convertir
valor = "123"
if valor.isdigit():
    numero = int(valor)
    print(f"Número válido: {numero}")
else:
    print("No es un número válido")

# Para negativos y decimales
def es_numero(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False

print(es_numero("123"))      # True
print(es_numero("-45.67"))   # True
print(es_numero("abc"))      # False
```

**Archivo de ejemplo**: `04_conversion_tipos.py`

---

## 📝 Comentarios y Documentación

### Comentarios de Una Línea

```python
# Este es un comentario de una línea

edad = 25  # Comentario al final de la línea

# Evitar comentarios obvios
x = 5  # ❌ asigna 5 a x

# Escribir comentarios útiles
x = 5  # ✅ número máximo de intentos permitidos
```

### Comentarios de Múltiples Líneas

```python
# Opción 1: Múltiples líneas con #
# Este es un comentario
# de varias líneas
# usando múltiples #

# Opción 2: String multilínea (no es técnicamente un comentario)
"""
Este es un string multilínea.
No es procesado si no se asigna ni usa.
A menudo se usa como comentario.
"""
```

### Docstrings (Documentation Strings)

```python
def calcular_area_rectangulo(base, altura):
    """
    Calcula el área de un rectángulo.
    
    Args:
        base (float): La base del rectángulo.
        altura (float): La altura del rectángulo.
    
    Returns:
        float: El área del rectángulo (base * altura).
    
    Raises:
        ValueError: Si base o altura son negativos.
    
    Ejemplos:
        >>> calcular_area_rectangulo(5, 3)
        15.0
        >>> calcular_area_rectangulo(4.5, 2.0)
        9.0
    """
    if base < 0 or altura < 0:
        raise ValueError("Base y altura deben ser positivos")
    return base * altura

# Acceder al docstring
print(calcular_area_rectangulo.__doc__)

# Docstring de clase
class Persona:
    """
    Representa una persona con nombre y edad.
    
    Attributes:
        nombre (str): Nombre de la persona.
        edad (int): Edad de la persona en años.
    """
    
    def __init__(self, nombre, edad):
        """Inicializa una nueva instancia de Persona."""
        self.nombre = nombre
        self.edad = edad

# Docstring de módulo (al inicio del archivo)
"""
modulo_ejemplo.py
~~~~~~~~~~~~~~~~~

Este módulo proporciona funciones para cálculos geométricos.

Contiene:
    - calcular_area_rectangulo()
    - calcular_area_circulo()
"""
```

### Buenas Prácticas de Comentarios

```python
# ❌ MAL: Comentario obvio
i = i + 1  # incrementa i en 1

# ✅ BIEN: Explica el "por qué"
i = i + 1  # compensar por índice basado en 0

# ❌ MAL: Código comentado sin razón
# x = calcular_algo()
# y = procesar(x)
y = procesar_directamente()

# ✅ BIEN: Explicar código complejo
# Usamos bisect para mantener la lista ordenada de forma eficiente
# en lugar de sort() después de cada inserción (O(log n) vs O(n log n))
import bisect
bisect.insort(lista_ordenada, nuevo_elemento)

# ✅ BIEN: TODOs y FIXMEs
# TODO: Optimizar esta función para listas grandes
# FIXME: Este algoritmo falla con números negativos
# HACK: Solución temporal hasta refactorizar
# NOTE: Este comportamiento es intencional debido a...
```

---

## 📏 Convenciones de Código (PEP 8)

PEP 8 es la guía de estilo oficial de Python. Seguir estas convenciones hace que tu código sea más legible y profesional.

### Indentación

```python
# ✅ Usar 4 espacios por nivel
def mi_funcion():
    if True:
        print("Correcto")

# ❌ No usar tabs ni mezclar
def mi_funcion():
	print("No usar tabs")  # ❌
    
# ✅ Continuación de línea alineada
resultado = (variable_uno + variable_dos +
             variable_tres + variable_cuatro)

# ✅ Continuación con indentación extra
def funcion_larga(
        parametro_uno, parametro_dos,
        parametro_tres):
    print("Correcto")
```

### Longitud de Línea

```python
# Máximo 79 caracteres por línea (preferiblemente 72)

# ❌ Línea muy larga
mensaje = "Este es un mensaje extremadamente largo que supera los 79 caracteres y es difícil de leer"

# ✅ Dividir en múltiples líneas
mensaje = (
    "Este es un mensaje largo "
    "dividido en varias líneas "
    "para mejor legibilidad"
)

# ✅ Con paréntesis implícitos
texto = ("Primera parte "
         "segunda parte "
         "tercera parte")

# ✅ Con f-strings
nombre = "Juan"
mensaje = (
    f"Hola {nombre}, este es un mensaje largo "
    f"que se extiende por múltiples líneas"
)
```

### Espacios en Blanco

```python
# ✅ Espacios alrededor de operadores
x = 1 + 2
y = x * 3
resultado = (x + y) * (x - y)

# ❌ Sin espacios apropiados
x=1+2
y=x*3

# ✅ Sin espacios inmediatamente dentro de paréntesis/corchetes
spam(ham[1], {eggs: 2})

# ❌ Con espacios extras
spam( ham[ 1 ], { eggs: 2 } )

# ✅ Sin espacio antes de coma/dos puntos
diccionario = {'nombre': 'Juan', 'edad': 30}

# ❌ Espacio antes de coma
diccionario = {'nombre' : 'Juan' , 'edad' : 30}

# ✅ Sin espacio antes de paréntesis en llamadas
funcion(argumento)
lista[indice]

# ❌ Con espacio
funcion (argumento)
lista [indice]

# ✅ Para prioridad, agrupar sin espacios
x = 1 + 2*3
y = (1+2) * 3

# ✅ Uno o ningún espacio alrededor de = en argumentos
def funcion(arg1, arg2=None, arg3='default'):
    pass

# ✅ Para type hints, espacios alrededor de ->
def funcion(x: int) -> int:
    return x * 2
```

### Líneas en Blanco

```python
# ✅ Dos líneas en blanco entre funciones de nivel superior y clases
def funcion_uno():
    pass


def funcion_dos():
    pass


class MiClase:
    pass


# ✅ Una línea en blanco entre métodos
class MiClase:
    def metodo_uno(self):
        pass
    
    def metodo_dos(self):
        pass


# ✅ Usar líneas en blanco para separar secciones lógicas
def funcion_compleja():
    # Preparación
    x = 1
    y = 2
    
    # Procesamiento
    resultado = x + y
    resultado *= 2
    
    # Return
    return resultado
```

### Imports

```python
# ✅ Imports al inicio del archivo (después del docstring)
# ✅ Orden: biblioteca estándar, terceros, locales
# ✅ Una línea por import

# Biblioteca estándar
import os
import sys
from datetime import datetime

# Paquetes de terceros
import numpy as np
import pandas as pd

# Módulos locales
from mi_modulo import mi_funcion


# ❌ Múltiples imports en una línea
import os, sys  # No hacer esto

# ✅ Excepción: múltiples clases del mismo módulo
from datetime import datetime, timedelta, timezone

# ✅ Imports absolutos (preferidos)
from modulo.submodulo import funcion

# ⚠️ Imports relativos (usar solo en paquetes)
from . import modulo_hermano
from .. import modulo_padre
```

### Naming Conventions

```python
# Variables y funciones: snake_case
nombre_usuario = "Juan"
calcular_precio_total()

# Constantes: UPPER_CASE
MAX_OVERFLOW = 100
PI = 3.14159

# Clases: PascalCase
class MiClase:
    pass

class CalculadoraAvanzada:
    pass

# Variables "privadas": prefijo _
_variable_interna = 10

def _metodo_privado():
    pass

# Variables "muy privadas": prefijo __
__variable_muy_privada = 20

# Ejemplos completos
class CuentaBancaria:
    # Constante de clase
    TASA_INTERES = 0.05
    
    def __init__(self, titular, saldo_inicial):
        # Atributos públicos
        self.titular = titular
        # Atributos "privados"
        self._saldo = saldo_inicial
        # Atributos "muy privados"
        self.__id_cuenta = self._generar_id()
    
    def depositar(self, monto):
        """Método público."""
        self._saldo += monto
    
    def _generar_id(self):
        """Método privado (convención)."""
        return id(self)
```

### Comparaciones

```python
# ✅ Usar 'is' para comparar con None
if variable is None:
    pass

# ❌ No usar ==
if variable == None:  # Evitar
    pass

# ✅ is not
if variable is not None:
    pass

# ✅ Verificaciones booleanas
if lista:  # verdadero si no está vacía
    pass

if not lista:  # verdadero si está vacía
    pass

# ❌ Comparaciones explícitas innecesarias
if len(lista) > 0:  # Evitar
    pass

if lista == []:  # Evitar
    pass
```

**Archivo de ejemplo**: `05_pep8_ejemplos.py`

---

## ✅ Buenas Prácticas

### Nombres Descriptivos

```python
# ❌ MAL: Nombres no descriptivos
x = 86400
t = time.time()
def calc(a, b):
    return a * b

# ✅ BIEN: Nombres descriptivos
SECONDS_PER_DAY = 86400
current_timestamp = time.time()
def calcular_area_rectangulo(base, altura):
    return base * altura
```

### Funciones Pequeñas y Enfocadas

```python
# ✅ Una función, una responsabilidad
def validar_email(email):
    """Valida formato de email."""
    return '@' in email and '.' in email

def enviar_email(destinatario, asunto, cuerpo):
    """Envía un email."""
    if not validar_email(destinatario):
        raise ValueError("Email inválido")
    # ... código para enviar
```

### DRY (Don't Repeat Yourself)

```python
# ❌ MAL: Repetición
nombre1 = input("Nombre 1: ").strip().title()
nombre2 = input("Nombre 2: ").strip().title()
nombre3 = input("Nombre 3: ").strip().title()

# ✅ BIEN: Función reutilizable
def obtener_nombre(prompt):
    return input(prompt).strip().title()

nombre1 = obtener_nombre("Nombre 1: ")
nombre2 = obtener_nombre("Nombre 2: ")
nombre3 = obtener_nombre("Nombre 3: ")
```

### Programación Defensiva

```python
def dividir(a, b):
    """Divide a entre b con validación."""
    # Validar tipos
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Los argumentos deben ser números")
    
    # Validar división por cero
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    
    return a / b

# Uso con manejo de errores
try:
    resultado = dividir(10, 2)
    print(f"Resultado: {resultado}")
except (TypeError, ValueError) as e:
    print(f"Error: {e}")
```

### Constantes Nombradas

```python
# ❌ MAL: Números mágicos
if edad >= 18:
    print("Mayor de edad")

precio_final = precio * 1.16

# ✅ BIEN: Constantes nombradas
EDAD_MAYOR_DE_EDAD = 18
TASA_IVA = 0.16

if edad >= EDAD_MAYOR_DE_EDAD:
    print("Mayor de edad")

precio_final = precio * (1 + TASA_IVA)
```

---

## 📚 Resumen del Módulo

### Conceptos Clave

| Concepto | Descripción | Ejemplo |
|----------|-------------|---------|
| **Variable** | Contenedor de datos | `nombre = "Juan"` |
| **Tipo de dato** | Naturaleza del valor | `int`, `str`, `bool` |
| **Operador** | Símbolo que opera datos | `+`, `-`, `==`, `and` |
| **Casting** | Conversión de tipos | `int("5")` |
| **PEP 8** | Guía de estilo | snake_case para variables |

### Tipos de Datos Básicos

```python
# Numéricos
entero = 42                    # int
flotante = 3.14               # float
complejo = 2 + 3j             # complex

# Texto
texto = "Hola"                # str

# Booleano
verdadero = True              # bool
falso = False

# Nulo
nada = None                   # NoneType
```

### Operadores Principales

```python
# Aritméticos: +, -, *, /, //, %, **
# Comparación: ==, !=, <, >, <=, >=
# Lógicos: and, or, not
# Identidad: is, is not
# Pertenencia: in, not in
```

### Checklist de Dominio

- [ ] Puedo crear y usar variables correctamente
- [ ] Entiendo los tipos de datos básicos
- [ ] Domino los operadores aritméticos y lógicos
- [ ] Sé usar input() y print()
- [ ] Puedo convertir entre tipos de datos
- [ ] Escribo código siguiendo PEP 8
- [ ] Documento mi código apropiadamente

---

## ➡️ Próximo Módulo

**Módulo 3: Estructuras de Control**
- Condicionales (if, elif, else)
- Bucles (for, while)
- Control de flujo (break, continue, pass)
- Comprensiones

---

## 📚 Recursos Adicionales

- [PEP 8 – Style Guide](https://pep8.org/)
- [Python Documentation - Built-in Types](https://docs.python.org/3/library/stdtypes.html)
- [Real Python - Variables](https://realpython.com/python-variables/)
- [Python String Formatting](https://pyformat.info/)

---

*Última actualización: Abril 2026*
