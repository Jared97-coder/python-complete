"""
Módulo 2 - Ejemplo 1: Variables y Tipos de Datos
================================================

Este script demuestra el uso de variables y los diferentes
tipos de datos básicos en Python.
"""

import sys


def seccion(titulo):
    """Helper para mostrar títulos de sección."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70 + "\n")


def demo_variables():
    """Demuestra la declaración y uso de variables."""
    seccion("VARIABLES - Declaración y Asignación")
    
    # Asignación simple
    nombre = "Juan Pérez"
    edad = 25
    altura = 1.75
    es_estudiante = True
    
    print(f"Nombre: {nombre}")
    print(f"Edad: {edad}")
    print(f"Altura: {altura}m")
    print(f"¿Es estudiante?: {es_estudiante}")
    
    # Asignación múltiple
    print("\n📌 Asignación múltiple:")
    x, y, z = 10, 20, 30
    print(f"x={x}, y={y}, z={z}")
    
    # Mismo valor a múltiples variables
    print("\n📌 Mismo valor a múltiples variables:")
    a = b = c = 0
    print(f"a={a}, b={b}, c={c}")
    
    # Intercambiar valores (Pythonic way)
    print("\n📌 Intercambiar valores:")
    x, y = 5, 10
    print(f"Antes: x={x}, y={y}")
    x, y = y, x
    print(f"Después: x={x}, y={y}")
    
    # Variables con nombres descriptivos
    print("\n📌 Nombres descriptivos (PEP 8):")
    nombre_completo = "Ana García"
    edad_usuario = 30
    precio_total = 150.75
    _variable_privada = "interno"
    CONSTANTE_MAXIMA = 100
    
    print(f"nombre_completo: {nombre_completo}")
    print(f"edad_usuario: {edad_usuario}")
    print(f"precio_total: ${precio_total}")
    print(f"_variable_privada: {_variable_privada}")
    print(f"CONSTANTE_MAXIMA: {CONSTANTE_MAXIMA}")


def demo_numeros_enteros():
    """Demuestra el uso de números enteros (int)."""
    seccion("NÚMEROS ENTEROS (int)")
    
    # Enteros básicos
    edad = 25
    temperatura = -10
    poblacion = 1_000_000  # Separador de miles
    
    print(f"Edad: {edad}")
    print(f"Temperatura: {temperatura}°C")
    print(f"Población: {poblacion:,}")
    
    # Diferentes bases
    print("\n📌 Diferentes bases numéricas:")
    decimal = 10
    binario = 0b1010      # Base 2
    octal = 0o12          # Base 8
    hexadecimal = 0xA     # Base 16
    
    print(f"Decimal: {decimal}")
    print(f"Binario 0b1010 = {binario}")
    print(f"Octal 0o12 = {octal}")
    print(f"Hexadecimal 0xA = {hexadecimal}")
    
    # Operaciones
    print("\n📌 Operaciones con enteros:")
    a, b = 10, 3
    print(f"a={a}, b={b}")
    print(f"a + b = {a + b}")
    print(f"a - b = {a - b}")
    print(f"a * b = {a * b}")
    print(f"a / b = {a / b}")  # División (retorna float)
    print(f"a // b = {a // b}")  # División entera
    print(f"a % b = {a % b}")   # Módulo
    print(f"a ** b = {a ** b}")  # Potencia
    
    # Tamaño ilimitado
    print("\n📌 Python soporta enteros de tamaño ilimitado:")
    numero_grande = 10 ** 100
    print(f"10^100 = {numero_grande}")


def demo_numeros_flotantes():
    """Demuestra el uso de números de punto flotante (float)."""
    seccion("NÚMEROS DE PUNTO FLOTANTE (float)")
    
    # Flotantes básicos
    precio = 19.99
    temperatura = -3.5
    pi = 3.14159265359
    
    print(f"Precio: ${precio}")
    print(f"Temperatura: {temperatura}°C")
    print(f"Pi (aproximado): {pi}")
    
    # Notación científica
    print("\n📌 Notación científica:")
    avogadro = 6.022e23
    planck = 6.626e-34
    print(f"Número de Avogadro: {avogadro:.3e}")
    print(f"Constante de Planck: {planck:.3e}")
    
    # Problema de precisión
    print("\n📌 Problema de precisión de flotantes:")
    x = 0.1 + 0.2
    print(f"0.1 + 0.2 = {x}")
    print(f"¿Es igual a 0.3? {x == 0.3}")
    print(f"Diferencia: {abs(x - 0.3):.20f}")
    
    # Solución con Decimal para precisión
    from decimal import Decimal
    print("\n📌 Usando Decimal para precisión:")
    x = Decimal('0.1') + Decimal('0.2')
    print(f"Decimal('0.1') + Decimal('0.2') = {x}")
    print(f"¿Es igual a 0.3? {x == Decimal('0.3')}")
    
    # Redondeo
    print("\n📌 Redondeo:")
    numero = 3.14159
    print(f"Original: {numero}")
    print(f"round(numero, 2): {round(numero, 2)}")
    print(f"round(numero, 4): {round(numero, 4)}")
    
    import math
    print(f"math.floor(numero): {math.floor(numero)}")
    print(f"math.ceil(numero): {math.ceil(numero)}")


def demo_cadenas():
    """Demuestra el uso de cadenas de texto (str)."""
    seccion("CADENAS DE TEXTO (str)")
    
    # Creación de strings
    nombre = 'Juan'
    apellido = "Pérez"
    mensaje = """Este es un string
de múltiples líneas.
Muy útil para textos largos."""
    
    print(f"Nombre: {nombre}")
    print(f"Apellido: {apellido}")
    print(f"Mensaje:\n{mensaje}")
    
    # Caracteres de escape
    print("\n📌 Caracteres de escape:")
    print("Línea 1\nLínea 2")  # \n = nueva línea
    print("Columna1\tColumna2")  # \t = tabulación
    print("Comillas: \"texto\"")  # \" = comilla
    print("Backslash: \\")  # \\ = backslash
    
    # Raw strings
    print("\n📌 Raw strings (r):")
    ruta_normal = "C:\\Users\\Juan\\Desktop"
    ruta_raw = r"C:\Users\Juan\Desktop"
    print(f"Normal: {ruta_normal}")
    print(f"Raw: {ruta_raw}")
    
    # Concatenación
    print("\n📌 Concatenación:")
    nombre_completo = nombre + " " + apellido
    print(f"Nombre completo: {nombre_completo}")
    saludo = "Hola " * 3
    print(f"Repetición: {saludo}")
    
    # Indexación y slicing
    print("\n📌 Indexación y slicing:")
    texto = "Python"
    print(f"Texto: {texto}")
    print(f"texto[0]: {texto[0]}")      # Primer carácter
    print(f"texto[-1]: {texto[-1]}")    # Último carácter
    print(f"texto[0:3]: {texto[0:3]}")  # Substring
    print(f"texto[2:]: {texto[2:]}")    # Desde índice 2
    print(f"texto[:4]: {texto[:4]}")    # Hasta índice 4
    print(f"texto[::2]: {texto[::2]}")  # Cada 2 caracteres
    print(f"texto[::-1]: {texto[::-1]}")  # Invertido
    
    # Métodos útiles
    print("\n📌 Métodos de strings:")
    texto = "  Hola Mundo  "
    print(f"Original: '{texto}'")
    print(f"upper(): '{texto.upper()}'")
    print(f"lower(): '{texto.lower()}'")
    print(f"strip(): '{texto.strip()}'")
    print(f"replace('o', '0'): '{texto.replace('o', '0')}'")
    print(f"split(): {texto.split()}")
    print(f"len(): {len(texto)}")
    
    # Verificaciones
    print("\n📌 Verificaciones:")
    print(f"'Hola'.startswith('H'): {'Hola'.startswith('H')}")
    print(f"'Mundo'.endswith('o'): {'Mundo'.endswith('o')}")
    print(f"'Python'.isalpha(): {'Python'.isalpha()}")
    print(f"'123'.isdigit(): {'123'.isdigit()}")
    print(f"'Python123'.isalnum(): {'Python123'.isalnum()}")
    
    # Formateo
    print("\n📌 Formateo de strings:")
    nombre = "Ana"
    edad = 30
    
    # f-strings (Python 3.6+)
    print(f"Hola, soy {nombre} y tengo {edad} años")
    
    # format()
    print("Hola, soy {} y tengo {} años".format(nombre, edad))
    
    # % (antiguo)
    print("Hola, soy %s y tengo %d años" % (nombre, edad))


def demo_booleanos():
    """Demuestra el uso de booleanos (bool)."""
    seccion("BOOLEANOS (bool)")
    
    # Valores booleanos
    verdadero = True
    falso = False
    
    print(f"verdadero = {verdadero} (tipo: {type(verdadero)})")
    print(f"falso = {falso} (tipo: {type(falso)})")
    
    # Valores que evalúan a False
    print("\n📌 Valores que evalúan a False:")
    valores_falsos = [
        0,
        0.0,
        "",
        [],
        {},
        set(),
        None
    ]
    
    for valor in valores_falsos:
        print(f"bool({repr(valor):20}) = {bool(valor)}")
    
    # Valores que evalúan a True
    print("\n📌 Valores que evalúan a True:")
    valores_verdaderos = [
        1,
        -1,
        0.1,
        "texto",
        [1, 2],
        {"a": 1},
        {1, 2}
    ]
    
    for valor in valores_verdaderos:
        print(f"bool({repr(valor):20}) = {bool(valor)}")
    
    # Operaciones lógicas
    print("\n📌 Operaciones lógicas:")
    print(f"True and True = {True and True}")
    print(f"True and False = {True and False}")
    print(f"True or False = {True or False}")
    print(f"False or False = {False or False}")
    print(f"not True = {not True}")
    print(f"not False = {not False}")
    
    # Comparaciones
    print("\n📌 Comparaciones (retornan bool):")
    a, b = 5, 3
    print(f"a={a}, b={b}")
    print(f"a > b = {a > b}")
    print(f"a < b = {a < b}")
    print(f"a == b = {a == b}")
    print(f"a != b = {a != b}")


def demo_none():
    """Demuestra el uso de None."""
    seccion("NONE (Tipo Nulo)")
    
    # None representa ausencia de valor
    resultado = None
    print(f"resultado = {resultado}")
    print(f"tipo: {type(resultado)}")
    
    # Función sin return explícito
    def funcion_sin_return():
        pass
    
    valor = funcion_sin_return()
    print(f"\nValor retornado por función sin return: {valor}")
    
    # Verificar None
    print("\n📌 Verificar si es None:")
    if resultado is None:
        print("✓ resultado es None")
    
    if resultado is not None:
        print("✗ Esto no se ejecuta")
    else:
        print("✓ resultado es None (verificación con 'is not')")
    
    # None vs False
    print("\n📌 None vs False:")
    print(f"None == False: {None == False}")
    print(f"None is False: {None is False}")
    print(f"bool(None): {bool(None)}")
    print(f"bool(False): {bool(False)}")


def demo_type_checking():
    """Demuestra cómo verificar tipos de datos."""
    seccion("VERIFICACIÓN DE TIPOS")
    
    # type() - obtener el tipo
    print("📌 Función type():")
    valores = [42, 3.14, "texto", True, None, [1, 2], {'a': 1}]
    
    for valor in valores:
        print(f"type({repr(valor):20}) = {type(valor).__name__}")
    
    # isinstance() - verificar tipo
    print("\n📌 Función isinstance():")
    numero = 42
    print(f"isinstance({numero}, int): {isinstance(numero, int)}")
    print(f"isinstance({numero}, float): {isinstance(numero, float)}")
    print(f"isinstance({numero}, (int, float)): {isinstance(numero, (int, float))}")
    
    texto = "Hola"
    print(f"isinstance('{texto}', str): {isinstance(texto, str)}")
    print(f"isinstance('{texto}', (str, int)): {isinstance(texto, (str, int))}")
    
    # Diferencia entre type() e isinstance()
    print("\n📌 type() vs isinstance():")
    
    class Animal:
        pass
    
    class Perro(Animal):
        pass
    
    mi_perro = Perro()
    
    print(f"type(mi_perro) == Perro: {type(mi_perro) == Perro}")
    print(f"type(mi_perro) == Animal: {type(mi_perro) == Animal}")
    print(f"isinstance(mi_perro, Perro): {isinstance(mi_perro, Perro)}")
    print(f"isinstance(mi_perro, Animal): {isinstance(mi_perro, Animal)}")


def demo_memoria():
    """Demuestra cómo Python maneja la memoria de variables."""
    seccion("GESTIÓN DE MEMORIA Y REFERENCIAS")
    
    # id() - dirección de memoria
    print("📌 Función id() (dirección en memoria):")
    x = 42
    y = 42
    z = x
    
    print(f"x = {x}, id(x) = {id(x)}")
    print(f"y = {y}, id(y) = {id(y)}")
    print(f"z = {z}, id(z) = {id(z)}")
    print(f"x is y: {x is y}  # Python cachea números pequeños")
    print(f"x is z: {x is z}  # z apunta al mismo objeto que x")
    
    # Con objetos mutables
    print("\n📌 Con listas (objetos mutables):")
    lista1 = [1, 2, 3]
    lista2 = [1, 2, 3]
    lista3 = lista1
    
    print(f"lista1: {lista1}, id: {id(lista1)}")
    print(f"lista2: {lista2}, id: {id(lista2)}")
    print(f"lista3: {lista3}, id: {id(lista3)}")
    print(f"lista1 == lista2: {lista1 == lista2}  # Mismo contenido")
    print(f"lista1 is lista2: {lista1 is lista2}  # Objetos diferentes")
    print(f"lista1 is lista3: {lista1 is lista3}  # Mismo objeto")
    
    # Tamaño en bytes
    print("\n📌 Tamaño en memoria (sys.getsizeof):")
    objetos = [
        42,
        3.14,
        "Hola",
        [1, 2, 3],
        {'a': 1, 'b': 2}
    ]
    
    for obj in objetos:
        tamaño = sys.getsizeof(obj)
        print(f"{repr(obj):30} → {tamaño} bytes")


def main():
    """Función principal que ejecuta todas las demostraciones."""
    print("\n" + "🐍" * 35)
    print("     VARIABLES Y TIPOS DE DATOS EN PYTHON")
    print("🐍" * 35)
    
    demo_variables()
    demo_numeros_enteros()
    demo_numeros_flotantes()
    demo_cadenas()
    demo_booleanos()
    demo_none()
    demo_type_checking()
    demo_memoria()
    
    print("\n" + "=" * 70)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("=" * 70)
    print("\n💡 Puntos clave:")
    print("   • Python tiene tipado dinámico (no declaras tipos)")
    print("   • Los tipos básicos son: int, float, str, bool, None")
    print("   • Usa nombres descriptivos para variables (snake_case)")
    print("   • type() obtiene el tipo, isinstance() lo verifica")
    print("   • Python maneja la memoria automáticamente\n")


if __name__ == "__main__":
    main()
