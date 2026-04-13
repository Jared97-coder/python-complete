# Módulo 3: Funciones y Programación "Pythonic"

## 📋 Contenido del Módulo

Este módulo te enseñará a escribir código Python elegante y eficiente usando funciones avanzadas y características pythonic.

---

## 🎯 Objetivos de Aprendizaje

Al completar este módulo serás capaz de:

- ✅ Diseñar APIs de funciones claras y expresivas
- ✅ Implementar decoradores y generadores útiles
- ✅ Crear context managers para gestión de recursos
- ✅ Usar comprensiones para código más conciso
- ✅ Aplicar principios pythonic en tu código

---

## 📚 Índice de Contenidos

1. [Funciones Básicas](#1-funciones-básicas)
2. [Argumentos y Parámetros](#2-argumentos-y-parámetros)
3. [*args y **kwargs](#3-args-y-kwargs)
4. [Funciones Lambda](#4-funciones-lambda)
5. [Closures](#5-closures)
6. [Decoradores](#6-decoradores)
7. [Iteradores](#7-iteradores)
8. [Generadores](#8-generadores)
9. [Comprensiones](#9-comprensiones)
10. [Context Managers](#10-context-managers)
11. [Mejores Prácticas](#11-mejores-prácticas)

---

## 1. Funciones Básicas

### Definición de Funciones

Una función es un bloque de código reutilizable que realiza una tarea específica.

```python
def saludar(nombre):
    """
    Saluda a una persona por su nombre.
    
    Args:
        nombre (str): Nombre de la persona
    
    Returns:
        str: Mensaje de saludo
    """
    return f"Hola, {nombre}!"

# Uso
mensaje = saludar("Ana")
print(mensaje)  # Hola, Ana!
```

### Elementos de una Función

```python
def nombre_funcion(parametro1, parametro2):  # Definición
    """Docstring explicando qué hace la función."""  # Documentación
    
    # Cuerpo de la función
    resultado = parametro1 + parametro2
    
    return resultado  # Retorno (opcional)
```

### Funciones sin Retorno

```python
def imprimir_mensaje(texto):
    """Imprime un mensaje sin retornar nada."""
    print(f"Mensaje: {texto}")
    # No tiene return, retorna None implícitamente

resultado = imprimir_mensaje("Hola")
print(resultado)  # None
```

### Múltiples Valores de Retorno

```python
def operaciones(a, b):
    """Retorna múltiples operaciones."""
    suma = a + b
    resta = a - b
    producto = a * b
    return suma, resta, producto  # Retorna tupla

s, r, p = operaciones(10, 5)
print(f"Suma: {s}, Resta: {r}, Producto: {p}")
```

### Scope (Ámbito de Variables)

```python
# Variable global
x = 10

def funcion():
    # Variable local
    y = 5
    print(f"Dentro: x={x}, y={y}")

funcion()
# print(y)  # Error: y no existe aquí

# Modificar variable global
contador = 0

def incrementar():
    global contador  # Declarar que usaremos la global
    contador += 1

incrementar()
print(contador)  # 1
```

---

## 2. Argumentos y Parámetros

### Argumentos Posicionales

```python
def dividir(dividendo, divisor):
    """División con argumentos posicionales."""
    return dividendo / divisor

resultado = dividir(10, 2)  # 10 / 2 = 5.0
```

### Argumentos por Nombre (Keyword Arguments)

```python
def crear_perfil(nombre, edad, ciudad):
    """Crea un perfil de usuario."""
    return {
        'nombre': nombre,
        'edad': edad,
        'ciudad': ciudad
    }

# Argumentos por nombre (puede cambiar el orden)
perfil = crear_perfil(edad=25, nombre="Juan", ciudad="Madrid")
```

### Argumentos por Defecto

```python
def saludar(nombre, saludo="Hola", simbolo="!"):
    """Saluda con valores por defecto."""
    return f"{saludo}, {nombre}{simbolo}"

print(saludar("Ana"))  # Hola, Ana!
print(saludar("Ana", "Buenos días"))  # Buenos días, Ana!
print(saludar("Ana", simbolo="?"))  # Hola, Ana?
```

### Argumentos Solo Posicionales (Python 3.8+)

```python
def funcion(a, b, /, c, d):
    """
    a, b: solo posicionales (antes de /)
    c, d: posicionales o por nombre
    """
    return a + b + c + d

funcion(1, 2, 3, 4)      # ✓ OK
funcion(1, 2, c=3, d=4)  # ✓ OK
# funcion(a=1, b=2, c=3, d=4)  # ✗ Error: a y b deben ser posicionales
```

### Argumentos Solo por Nombre (Keyword-Only)

```python
def crear_usuario(nombre, *, edad, email):
    """
    nombre: posicional o por nombre
    edad, email: solo por nombre (después de *)
    """
    return {
        'nombre': nombre,
        'edad': edad,
        'email': email
    }

crear_usuario("Juan", edad=30, email="juan@email.com")  # ✓ OK
# crear_usuario("Juan", 30, "juan@email.com")  # ✗ Error
```

---

## 3. *args y **kwargs

### *args (Argumentos Variables Posicionales)

Permite pasar un número variable de argumentos posicionales.

```python
def sumar(*numeros):
    """Suma cualquier cantidad de números."""
    total = 0
    for num in numeros:
        total += num
    return total

print(sumar(1, 2, 3))           # 6
print(sumar(1, 2, 3, 4, 5))     # 15
print(sumar())                   # 0
```

### **kwargs (Argumentos Variables por Nombre)

Permite pasar un número variable de argumentos por nombre.

```python
def crear_configuracion(**opciones):
    """Crea configuración con opciones variables."""
    config = {}
    for clave, valor in opciones.items():
        config[clave] = valor
    return config

config = crear_configuracion(
    debug=True,
    timeout=30,
    max_conexiones=100
)
print(config)
# {'debug': True, 'timeout': 30, 'max_conexiones': 100}
```

### Combinando Todo

```python
def funcion_completa(a, b, *args, opcion="default", **kwargs):
    """
    Combina todos los tipos de argumentos.
    
    a, b: posicionales requeridos
    *args: posicionales variables
    opcion: por nombre con default
    **kwargs: por nombre variables
    """
    print(f"a={a}, b={b}")
    print(f"args={args}")
    print(f"opcion={opcion}")
    print(f"kwargs={kwargs}")

funcion_completa(
    1, 2, 3, 4, 5,
    opcion="custom",
    extra1="valor1",
    extra2="valor2"
)
```

### Desempaquetado de Argumentos

```python
def funcion(a, b, c):
    return a + b + c

# Desempaquetar lista/tupla con *
numeros = [1, 2, 3]
resultado = funcion(*numeros)  # funcion(1, 2, 3)

# Desempaquetar diccionario con **
datos = {'a': 1, 'b': 2, 'c': 3}
resultado = funcion(**datos)  # funcion(a=1, b=2, c=3)
```

---

## 4. Funciones Lambda

Funciones anónimas de una sola expresión.

### Sintaxis Básica

```python
# Función normal
def cuadrado(x):
    return x ** 2

# Equivalente con lambda
cuadrado_lambda = lambda x: x ** 2

print(cuadrado(5))         # 25
print(cuadrado_lambda(5))  # 25
```

### Uso Común: Con Funciones de Orden Superior

```python
# map()
numeros = [1, 2, 3, 4, 5]
cuadrados = list(map(lambda x: x ** 2, numeros))
print(cuadrados)  # [1, 4, 9, 16, 25]

# filter()
pares = list(filter(lambda x: x % 2 == 0, numeros))
print(pares)  # [2, 4]

# sorted() con key
palabras = ['Python', 'es', 'genial']
ordenadas = sorted(palabras, key=lambda x: len(x))
print(ordenadas)  # ['es', 'genial', 'Python']
```

### Lambda con Múltiples Argumentos

```python
suma = lambda a, b: a + b
producto = lambda a, b, c: a * b * c

print(suma(3, 5))        # 8
print(producto(2, 3, 4)) # 24
```

### Cuándo NO Usar Lambda

```python
# ❌ MAL: Lambda compleja
calcular = lambda x, y: x ** 2 + y ** 2 if x > 0 else x ** 2 - y ** 2

# ✓ MEJOR: Función normal
def calcular(x, y):
    """Calcula según el signo de x."""
    if x > 0:
        return x ** 2 + y ** 2
    else:
        return x ** 2 - y ** 2
```

---

## 5. Closures

Un closure es una función que "recuerda" las variables de su entorno exterior.

### Concepto Básico

```python
def exterior(x):
    """Función exterior."""
    
    def interior(y):
        """Función interior (closure)."""
        return x + y  # Accede a x del scope exterior
    
    return interior

# Crear closure
sumar_5 = exterior(5)
print(sumar_5(3))  # 8 (5 + 3)
print(sumar_5(10)) # 15 (5 + 10)

sumar_10 = exterior(10)
print(sumar_10(3)) # 13 (10 + 3)
```

### Uso Práctico: Factory Functions

```python
def crear_multiplicador(factor):
    """Crea función multiplicadora."""
    def multiplicar(numero):
        return numero * factor
    return multiplicar

duplicar = crear_multiplicador(2)
triplicar = crear_multiplicador(3)

print(duplicar(5))   # 10
print(triplicar(5))  # 15
```

### Closures con Estado Mutable

```python
def crear_contador():
    """Crea un contador con estado."""
    contador = [0]  # Lista mutable
    
    def incrementar():
        contador[0] += 1
        return contador[0]
    
    return incrementar

contador1 = crear_contador()
print(contador1())  # 1
print(contador1())  # 2
print(contador1())  # 3

contador2 = crear_contador()
print(contador2())  # 1 (independiente)
```

### nonlocal

```python
def crear_contador_v2():
    """Contador usando nonlocal."""
    contador = 0
    
    def incrementar():
        nonlocal contador  # Modificar variable del scope exterior
        contador += 1
        return contador
    
    return incrementar
```

---

## 6. Decoradores

Los decoradores modifican o extienden el comportamiento de funciones.

### Concepto Básico

```python
def mi_decorador(funcion):
    """Decorador simple."""
    def wrapper():
        print("Antes de la función")
        funcion()
        print("Después de la función")
    return wrapper

@mi_decorador
def saludar():
    print("¡Hola!")

# Equivalente a: saludar = mi_decorador(saludar)

saludar()
# Salida:
# Antes de la función
# ¡Hola!
# Después de la función
```

### Decorador con Argumentos de Función

```python
def mi_decorador(funcion):
    def wrapper(*args, **kwargs):
        print(f"Llamando {funcion.__name__} con args={args}, kwargs={kwargs}")
        resultado = funcion(*args, **kwargs)
        print(f"Resultado: {resultado}")
        return resultado
    return wrapper

@mi_decorador
def suma(a, b):
    return a + b

suma(3, 5)
# Llamando suma con args=(3, 5), kwargs={}
# Resultado: 8
```

### Decorador con Parámetros

```python
def repetir(veces):
    """Decorador que repite la ejecución."""
    def decorador(funcion):
        def wrapper(*args, **kwargs):
            for _ in range(veces):
                resultado = funcion(*args, **kwargs)
            return resultado
        return wrapper
    return decorador

@repetir(veces=3)
def saludar(nombre):
    print(f"Hola, {nombre}!")

saludar("Ana")
# Hola, Ana!
# Hola, Ana!
# Hola, Ana!
```

### Preservar Metadata con functools.wraps

```python
from functools import wraps

def mi_decorador(funcion):
    @wraps(funcion)  # Preserva nombre, docstring, etc.
    def wrapper(*args, **kwargs):
        return funcion(*args, **kwargs)
    return wrapper

@mi_decorador
def funcion_importante():
    """Esta es una función importante."""
    pass

print(funcion_importante.__name__)  # funcion_importante
print(funcion_importante.__doc__)   # Esta es una función importante.
```

### Decoradores Útiles Comunes

```python
# Medir tiempo de ejecución
import time
from functools import wraps

def timer(funcion):
    @wraps(funcion)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = funcion(*args, **kwargs)
        fin = time.time()
        print(f"{funcion.__name__} tomó {fin - inicio:.4f} segundos")
        return resultado
    return wrapper

@timer
def proceso_lento():
    time.sleep(1)
    return "Completado"
```

---

## 7. Iteradores

Un iterador es un objeto que puede ser iterado (recorrido).

### Protocolo de Iterador

```python
class MiIterador:
    """Iterador personalizado."""
    
    def __init__(self, limite):
        self.limite = limite
        self.contador = 0
    
    def __iter__(self):
        """Retorna el objeto iterador (self)."""
        return self
    
    def __next__(self):
        """Retorna el siguiente valor."""
        if self.contador < self.limite:
            self.contador += 1
            return self.contador
        else:
            raise StopIteration

# Uso
for num in MiIterador(5):
    print(num)  # 1, 2, 3, 4, 5
```

### iter() y next()

```python
lista = [1, 2, 3, 4, 5]
iterador = iter(lista)

print(next(iterador))  # 1
print(next(iterador))  # 2
print(next(iterador))  # 3
```

---

## 8. Generadores

Los generadores son funciones que producen una secuencia de valores usando `yield`.

### Básico con yield

```python
def contador(limite):
    """Generador simple."""
    n = 1
    while n <= limite:
        yield n
        n += 1

# Uso
for num in contador(5):
    print(num)  # 1, 2, 3, 4, 5

# Crear lista desde generador
numeros = list(contador(3))
print(numeros)  # [1, 2, 3]
```

### Ventajas de Generadores

```python
# ❌ Con lista (mucha memoria)
def numeros_lista(n):
    resultado = []
    for i in range(n):
        resultado.append(i ** 2)
    return resultado

# ✓ Con generador (memoria eficiente)
def numeros_generador(n):
    for i in range(n):
        yield i ** 2

# El generador no carga todo en memoria
gen = numeros_generador(1000000)  # Instantáneo
```

### Expresiones Generadoras

```python
# Lista comprehension (carga todo en memoria)
cuadrados_lista = [x ** 2 for x in range(10)]

# Generador expression (lazy evaluation)
cuadrados_gen = (x ** 2 for x in range(10))

print(type(cuadrados_gen))  # <class 'generator'>

# Consumir generador
for cuadrado in cuadrados_gen:
    print(cuadrado)
```

### Generadores Avanzados

```python
def fibonacci():
    """Generador infinito de Fibonacci."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Tomar primeros 10
import itertools
primeros_10 = list(itertools.islice(fibonacci(), 10))
print(primeros_10)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

---

## 9. Comprensiones

Sintaxis concisa para crear colecciones.

### List Comprehension

```python
# Sintaxis básica
cuadrados = [x ** 2 for x in range(10)]

# Con condición
pares = [x for x in range(20) if x % 2 == 0]

# Con transformación y filtro
palabras = ['Python', 'es', 'genial']
mayusculas = [p.upper() for p in palabras if len(p) > 2]
# ['PYTHON', 'GENIAL']
```

### Dict Comprehension

```python
# Crear diccionario
cuadrados_dict = {x: x ** 2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Invertir diccionario
original = {'a': 1, 'b': 2, 'c': 3}
invertido = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}

# Con condición
numeros = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
pares = {k: v for k, v in numeros.items() if v % 2 == 0}
# {'b': 2, 'd': 4}
```

### Set Comprehension

```python
# Crear set (sin duplicados)
cuadrados_set = {x ** 2 for x in [-2, -1, 0, 1, 2]}
# {0, 1, 4}

# Primeras letras únicas
palabras = ['apple', 'banana', 'avocado', 'cherry']
primeras = {p[0] for p in palabras}
# {'a', 'b', 'c'}
```

### Comprensiones Anidadas

```python
# Matriz 3x3
matriz = [[i * j for j in range(3)] for i in range(3)]
# [[0, 0, 0], [0, 1, 2], [0, 2, 4]]

# Aplanar lista
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
plana = [num for fila in matriz for num in fila]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

## 10. Context Managers

Gestionan recursos automáticamente (apertura/cierre).

### Uso Básico con with

```python
# Sin context manager (propenso a errores)
archivo = open('datos.txt', 'r')
contenido = archivo.read()
archivo.close()  # Fácil de olvidar

# Con context manager (automático)
with open('datos.txt', 'r') as archivo:
    contenido = archivo.read()
# archivo.close() se llama automáticamente
```

### Crear Context Manager con Clase

```python
class MiContextManager:
    """Context manager personalizado."""
    
    def __init__(self, nombre):
        self.nombre = nombre
    
    def __enter__(self):
        """Se ejecuta al entrar al bloque with."""
        print(f"Entrando: {self.nombre}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Se ejecuta al salir del bloque with."""
        print(f"Saliendo: {self.nombre}")
        return False  # Propagar excepciones

# Uso
with MiContextManager("Recurso1") as cm:
    print("Dentro del contexto")
```

### Context Manager con contextlib

```python
from contextlib import contextmanager

@contextmanager
def mi_context_manager(nombre):
    """Context manager usando decorador."""
    print(f"Setup: {nombre}")
    try:
        yield nombre
    finally:
        print(f"Teardown: {nombre}")

# Uso
with mi_context_manager("Recurso") as recurso:
    print(f"Usando: {recurso}")
```

### Context Manager para Temporización

```python
import time
from contextlib import contextmanager

@contextmanager
def timer(nombre="Operación"):
    """Mide tiempo de ejecución."""
    inicio = time.time()
    yield
    fin = time.time()
    print(f"{nombre} tomó {fin - inicio:.4f} segundos")

# Uso
with timer("Proceso"):
    time.sleep(1)
    print("Trabajando...")
```

---

## 11. Mejores Prácticas

### Principios Pythonic

```python
# ✓ PYTHONIC
nombres = ['Ana', 'Juan', 'Pedro']
for nombre in nombres:
    print(nombre)

# ✗ NO PYTHONIC
for i in range(len(nombres)):
    print(nombres[i])
```

### Usar enumerate() para Índices

```python
nombres = ['Ana', 'Juan', 'Pedro']

for indice, nombre in enumerate(nombres):
    print(f"{indice}: {nombre}")
```

### Usar zip() para Iterar en Paralelo

```python
nombres = ['Ana', 'Juan', 'Pedro']
edades = [25, 30, 35]

for nombre, edad in zip(nombres, edades):
    print(f"{nombre} tiene {edad} años")
```

### Desempaquetado Extendido

```python
# Python 3
primero, *resto, ultimo = [1, 2, 3, 4, 5]
print(primero)  # 1
print(resto)    # [2, 3, 4]
print(ultimo)   # 5
```

### Usar get() en Diccionarios

```python
datos = {'nombre': 'Ana', 'edad': 25}

# ✗ Puede causar KeyError
# ciudad = datos['ciudad']

# ✓ Seguro con default
ciudad = datos.get('ciudad', 'Desconocida')
```

---

## 📝 Archivos de Ejemplos

- `01_funciones_basicas.py` - Funciones, parámetros, scope
- `02_args_kwargs.py` - *args, **kwargs, desempaquetado
- `03_lambdas_closures.py` - Funciones lambda y closures
- `04_decoradores.py` - Decoradores con y sin parámetros
- `05_generadores_iteradores.py` - yield, iteradores personalizados
- `06_comprensiones.py` - List, dict, set comprehensions
- `07_context_managers.py` - with statement, gestión de recursos

---

## 📚 Recursos Adicionales

- **PEP 8**: https://peps.python.org/pep-0008/
- **Python Docs - Funciones**: https://docs.python.org/3/tutorial/controlflow.html#defining-functions
- **Real Python - Decorators**: https://realpython.com/primer-on-python-decorators/
- **Python Docs - Iteradores**: https://docs.python.org/3/tutorial/classes.html#iterators
- **Python Docs - Generadores**: https://docs.python.org/3/tutorial/classes.html#generators
