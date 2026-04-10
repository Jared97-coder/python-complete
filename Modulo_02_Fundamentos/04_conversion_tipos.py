"""
Módulo 2 - Ejemplo 4: Conversión de Tipos (Type Casting)
========================================================

Este script demuestra cómo convertir entre diferentes
tipos de datos en Python.
"""


def seccion(titulo):
    """Helper para mostrar títulos de sección."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70 + "\n")


def demo_conversion_a_int():
    """Demuestra conversión a enteros."""
    seccion("CONVERSIÓN A INT (ENTEROS)")
    
    print("📌 Desde float:")
    print("-" * 70)
    
    numero_float = 3.14
    numero_int = int(numero_float)
    print(f"float: {numero_float} → int: {numero_int}")
    print("⚠️  Se trunca, no se redondea\n")
    
    print(f"int(3.9) = {int(3.9)}")
    print(f"int(3.1) = {int(3.1)}")
    print(f"int(-3.9) = {int(-3.9)}")
    
    print("\n📌 Desde string:")
    print("-" * 70)
    
    edad_str = "25"
    edad_int = int(edad_str)
    print(f"string: '{edad_str}' → int: {edad_int}")
    print(f"Tipo: {type(edad_int)}")
    
    # Con espacios
    numero_str = "  42  "
    numero = int(numero_str)  # strip automático
    print(f"string con espacios: '{numero_str}' → int: {numero}")
    
    print("\n📌 Desde diferentes bases:")
    print("-" * 70)
    
    # Binario
    binario_str = "1010"
    numero = int(binario_str, 2)
    print(f"Binario '1010' → decimal: {numero}")
    
    # Octal
    octal_str = "17"
    numero = int(octal_str, 8)
    print(f"Octal '17' → decimal: {numero}")
    
    # Hexadecimal
    hex_str = "FF"
    numero = int(hex_str, 16)
    print(f"Hexadecimal 'FF' → decimal: {numero}")
    
    print("\n📌 Desde bool:")
    print("-" * 70)
    
    print(f"int(True) = {int(True)}")
    print(f"int(False) = {int(False)}")
    
    print("\n⚠️  Errores comunes:")
    print("-" * 70)
    
    try:
        resultado = int("3.14")
    except ValueError as e:
        print(f"int('3.14') → ValueError: {e}")
    
    try:
        resultado = int("abc")
    except ValueError as e:
        print(f"int('abc') → ValueError: {e}")


def demo_conversion_a_float():
    """Demuestra conversión a float."""
    seccion("CONVERSIÓN A FLOAT (FLOTANTES)")
    
    print("📌 Desde int:")
    print("-" * 70)
    
    numero_int = 42
    numero_float = float(numero_int)
    print(f"int: {numero_int} → float: {numero_float}")
    print(f"Tipo: {type(numero_float)}")
    
    print("\n📌 Desde string:")
    print("-" * 70)
    
    altura_str = "1.75"
    altura = float(altura_str)
    print(f"string: '{altura_str}' → float: {altura}")
    
    # Notación científica
    cientifico_str = "1.5e3"
    numero = float(cientifico_str)
    print(f"string: '{cientifico_str}' → float: {numero}")
    
    # Con espacios
    precio_str = "  99.99  "
    precio = float(precio_str)
    print(f"string con espacios: '{precio_str}' → float: {precio}")
    
    print("\n📌 Valores especiales:")
    print("-" * 70)
    
    infinito = float('inf')
    neg_infinito = float('-inf')
    no_numero = float('nan')
    
    print(f"float('inf') = {infinito}")
    print(f"float('-inf') = {neg_infinito}")
    print(f"float('nan') = {no_numero}")
    
    # Verificar valores especiales
    import math
    print(f"\nmath.isinf({infinito}) = {math.isinf(infinito)}")
    print(f"math.isnan({no_numero}) = {math.isnan(no_numero)}")
    
    print("\n📌 Desde bool:")
    print("-" * 70)
    
    print(f"float(True) = {float(True)}")
    print(f"float(False) = {float(False)}")
    
    print("\n⚠️  Errores comunes:")
    print("-" * 70)
    
    try:
        resultado = float("abc")
    except ValueError as e:
        print(f"float('abc') → ValueError: {e}")


def demo_conversion_a_str():
    """Demuestra conversión a string."""
    seccion("CONVERSIÓN A STR (STRINGS)")
    
    print("📌 Desde números:")
    print("-" * 70)
    
    numero_int = 42
    numero_float = 3.14
    
    str_int = str(numero_int)
    str_float = str(numero_float)
    
    print(f"int {numero_int} → str '{str_int}'")
    print(f"float {numero_float} → str '{str_float}'")
    print(f"Tipo: {type(str_int)}, {type(str_float)}")
    
    # Ahora son strings, no se pueden sumar como números
    print(f"\n'42' + '3.14' = '{str_int + str_float}'  # Concatenación")
    print(f"42 + 3.14 = {numero_int + numero_float}  # Suma numérica")
    
    print("\n📌 Desde bool:")
    print("-" * 70)
    
    print(f"str(True) = '{str(True)}'")
    print(f"str(False) = '{str(False)}'")
    
    print("\n📌 Desde None:")
    print("-" * 70)
    
    print(f"str(None) = '{str(None)}'")
    
    print("\n📌 Desde listas, tuplas, diccionarios:")
    print("-" * 70)
    
    lista = [1, 2, 3]
    tupla = (4, 5, 6)
    diccionario = {'a': 1, 'b': 2}
    
    print(f"Lista: {lista} → '{str(lista)}'")
    print(f"Tupla: {tupla} → '{str(tupla)}'")
    print(f"Dict: {diccionario} → '{str(diccionario)}'")
    
    print("\n📌 Conversión de números a diferentes bases:")
    print("-" * 70)
    
    numero = 255
    print(f"Decimal: {numero}")
    print(f"Binario: {bin(numero)}")  # '0b11111111'
    print(f"Octal: {oct(numero)}")    # '0o377'
    print(f"Hexadecimal: {hex(numero)}")  # '0xff'
    
    # Sin prefijo
    print(f"\nBinario sin prefijo: {bin(numero)[2:]}")
    print(f"Hex sin prefijo: {hex(numero)[2:]}")
    print(f"Hex mayúsculas: {hex(numero)[2:].upper()}")


def demo_conversion_a_bool():
    """Demuestra conversión a booleano."""
    seccion("CONVERSIÓN A BOOL (BOOLEANOS)")
    
    print("📌 Regla general:")
    print("-" * 70)
    print("  • Valores 'vacíos' o 'cero' → False")
    print("  • Todo lo demás → True\n")
    
    print("📌 Desde números:")
    print("-" * 70)
    
    print(f"bool(0) = {bool(0)}")
    print(f"bool(1) = {bool(1)}")
    print(f"bool(42) = {bool(42)}")
    print(f"bool(-10) = {bool(-10)}")
    print(f"bool(0.0) = {bool(0.0)}")
    print(f"bool(3.14) = {bool(3.14)}")
    
    print("\n📌 Desde strings:")
    print("-" * 70)
    
    print(f"bool('') = {bool('')}  # String vacío")
    print(f"bool('texto') = {bool('texto')}")
    print(f"bool('False') = {bool('False')}  # ⚠️ String no vacío!")
    print(f"bool('0') = {bool('0')}  # ⚠️ String no vacío!")
    print(f"bool(' ') = {bool(' ')}  # Espacio cuenta como no vacío")
    
    print("\n📌 Desde None:")
    print("-" * 70)
    
    print(f"bool(None) = {bool(None)}")
    
    print("\n📌 Desde colecciones:")
    print("-" * 70)
    
    print(f"bool([]) = {bool([])}  # Lista vacía")
    print(f"bool([1, 2, 3]) = {bool([1, 2, 3])}")
    print(f"bool(()) = {bool(())}  # Tupla vacía")
    print(f"bool((1,)) = {bool((1,))}")
    print(f"bool({{}}) = {bool({})}  # Dict vacío")
    print(f"bool({{'a': 1}}) = {bool({'a': 1})}")
    print(f"bool(set()) = {bool(set())}  # Set vacío")
    print(f"bool({{1, 2}}) = {bool({1, 2})}")
    
    print("\n📌 Tabla resumen:")
    print("-" * 70)
    
    valores_false = [
        ("0", 0),
        ("0.0", 0.0),
        ("''", ''),
        ("[]", []),
        ("()", ()),
        ("{}", {}),
        ("set()", set()),
        ("None", None),
        ("False", False)
    ]
    
    print(f"{'Valor':<15} {'bool()':<10}")
    print("-" * 25)
    for nombre, valor in valores_false:
        print(f"{nombre:<15} {bool(valor)!s:<10}")


def demo_conversiones_implicitas():
    """Demuestra conversiones implícitas."""
    seccion("CONVERSIONES IMPLÍCITAS (COERCIÓN)")
    
    print("📌 int + float → float:")
    print("-" * 70)
    
    a = 10  # int
    b = 3.5  # float
    resultado = a + b
    
    print(f"{a} (int) + {b} (float) = {resultado} (tipo: {type(resultado).__name__})")
    
    print("\n📌 bool + int → int:")
    print("-" * 70)
    
    print(f"True + 5 = {True + 5}")
    print(f"False + 5 = {False + 5}")
    print(f"True + True = {True + True}")
    
    print("\n📌 bool + float → float:")
    print("-" * 70)
    
    print(f"True + 3.5 = {True + 3.5}")
    print(f"False + 3.5 = {False + 3.5}")
    
    print("\n⚠️  str NO se convierte implícitamente:")
    print("-" * 70)
    
    try:
        resultado = "5" + 3
    except TypeError as e:
        print(f"'5' + 3 → TypeError: {e}")
    
    print("Solución: convertir explícitamente")
    print(f"int('5') + 3 = {int('5') + 3}")
    print(f"'5' + str(3) = {'5' + str(3)}")


def demo_conversiones_seguras():
    """Demuestra cómo hacer conversiones seguras."""
    seccion("CONVERSIONES SEGURAS CON MANEJO DE ERRORES")
    
    print("📌 Funciones helper seguras:\n")
    
    def to_int_safe(valor, default=0):
        """Convierte a int de forma segura."""
        try:
            return int(valor)
        except (ValueError, TypeError):
            return default
    
    def to_float_safe(valor, default=0.0):
        """Convierte a float de forma segura."""
        try:
            return float(valor)
        except (ValueError, TypeError):
            return default
    
    # Ejemplos
    valores_prueba = ["42", "3.14", "abc", None, "", "  100  "]
    
    print("Conversión segura a int:")
    print("-" * 70)
    for valor in valores_prueba:
        resultado = to_int_safe(valor)
        print(f"to_int_safe({valor!r:12}) = {resultado}")
    
    print("\nConversión segura a float:")
    print("-" * 70)
    for valor in valores_prueba:
        resultado = to_float_safe(valor)
        print(f"to_float_safe({valor!r:12}) = {resultado}")
    
    print("\n📌 Validación antes de convertir:")
    print("-" * 70)
    
    texto = "12345"
    if texto.isdigit():
        numero = int(texto)
        print(f"'{texto}' es dígito → {numero}")
    else:
        print(f"'{texto}' no es dígito")
    
    texto = "abc"
    if texto.isdigit():
        numero = int(texto)
        print(f"'{texto}' es dígito → {numero}")
    else:
        print(f"'{texto}' NO es dígito")
    
    print("\n📌 Métodos de validación de strings:")
    print("-" * 70)
    
    ejemplos = [
        ("12345", "isdigit"),
        ("123.45", "isdigit"),
        ("abc123", "isalnum"),
        ("abc", "isalpha"),
        ("   ", "isspace"),
        ("Hello", "istitle")
    ]
    
    for texto, metodo in ejemplos:
        funcion = getattr(texto, metodo)
        print(f"'{texto}'.{metodo}() = {funcion()}")


def demo_conversiones_avanzadas():
    """Demuestra conversiones avanzadas."""
    seccion("CONVERSIONES AVANZADAS")
    
    print("📌 list(), tuple(), set():")
    print("-" * 70)
    
    texto = "Python"
    print(f"String: '{texto}'")
    print(f"list('{texto}') = {list(texto)}")
    print(f"tuple('{texto}') = {tuple(texto)}")
    print(f"set('{texto}') = {set(texto)}  # Orden no garantizado")
    
    numeros = [1, 2, 2, 3, 3, 3]
    print(f"\nLista: {numeros}")
    print(f"tuple({numeros}) = {tuple(numeros)}")
    print(f"set({numeros}) = {set(numeros)}  # Elimina duplicados")
    
    print("\n📌 dict() desde listas de tuplas:")
    print("-" * 70)
    
    pares = [('a', 1), ('b', 2), ('c', 3)]
    diccionario = dict(pares)
    print(f"Pares: {pares}")
    print(f"dict(pares) = {diccionario}")
    
    # Desde dos listas con zip
    claves = ['nombre', 'edad', 'ciudad']
    valores = ['Juan', 30, 'Madrid']
    diccionario = dict(zip(claves, valores))
    print(f"\nClaves: {claves}")
    print(f"Valores: {valores}")
    print(f"dict(zip(claves, valores)) = {diccionario}")
    
    print("\n📌 Conversión con comprensiones:")
    print("-" * 70)
    
    # String a lista de enteros
    texto = "12345"
    numeros = [int(c) for c in texto]
    print(f"String '{texto}' → lista de ints: {numeros}")
    
    # Lista a dict con índices
    frutas = ['manzana', 'pera', 'uva']
    dict_frutas = {i: fruta for i, fruta in enumerate(frutas)}
    print(f"\nLista: {frutas}")
    print(f"Dict con índices: {dict_frutas}")
    
    print("\n📌 bytes y bytearray:")
    print("-" * 70)
    
    texto = "Hola"
    bytes_texto = texto.encode('utf-8')
    print(f"String: '{texto}'")
    print(f"encode('utf-8'): {bytes_texto}")
    print(f"decode('utf-8'): '{bytes_texto.decode('utf-8')}'")
    
    # Lista de enteros a bytes
    numeros = [72, 111, 108, 97]  # "Hola" en ASCII
    bytes_numeros = bytes(numeros)
    print(f"\nLista: {numeros}")
    print(f"bytes(): {bytes_numeros}")
    print(f"decode('ascii'): '{bytes_numeros.decode('ascii')}'")


def ejercicios_practicos():
    """Ejercicios prácticos."""
    seccion("EJERCICIOS PRÁCTICOS")
    
    print("🎯 Ejercicio 1: Calculadora de área")
    print("-" * 70)
    
    # Simular entrada del usuario
    base_str = "5.5"
    altura_str = "10"
    
    print(f"Base (string): '{base_str}'")
    print(f"Altura (string): '{altura_str}'")
    
    # Convertir a números
    base = float(base_str)
    altura = float(altura_str)
    
    area = (base * altura) / 2
    print(f"\nÁrea del triángulo: {area:.2f} unidades²")
    
    print("\n🎯 Ejercicio 2: Validar y convertir entrada")
    print("-" * 70)
    
    entradas = ["42", "3.14", "abc", "-10", "0", ""]
    
    for entrada in entradas:
        print(f"\nProcesando: {entrada!r}")
        
        # Intentar convertir a int
        try:
            numero = int(entrada)
            print(f"  → Entero válido: {numero}")
            if numero > 0:
                print(f"  → Es positivo")
        except ValueError:
            # Intentar convertir a float
            try:
                numero = float(entrada)
                print(f"  → Decimal válido: {numero}")
            except ValueError:
                print(f"  → No es un número válido")
    
    print("\n🎯 Ejercicio 3: Procesar datos mixtos")
    print("-" * 70)
    
    datos = ["Juan", "30", "1.75", "True", "100.50"]
    print(f"Datos crudos: {datos}\n")
    
    nombre = datos[0]  # Ya es string
    edad = int(datos[1])
    altura = float(datos[2])
    activo = datos[3] == "True"  # Conversión manual
    saldo = float(datos[4])
    
    print(f"Nombre: {nombre} (tipo: {type(nombre).__name__})")
    print(f"Edad: {edad} años (tipo: {type(edad).__name__})")
    print(f"Altura: {altura} m (tipo: {type(altura).__name__})")
    print(f"Activo: {activo} (tipo: {type(activo).__name__})")
    print(f"Saldo: ${saldo:.2f} (tipo: {type(saldo).__name__})")
    
    # Operaciones
    print(f"\nEn 5 años tendrá {edad + 5} años")
    print(f"IMC: {saldo / (altura ** 2):.2f}")


def main():
    """Función principal."""
    print("\n" + "🐍" * 35)
    print("       CONVERSIÓN DE TIPOS EN PYTHON")
    print("🐍" * 35)
    
    demo_conversion_a_int()
    demo_conversion_a_float()
    demo_conversion_a_str()
    demo_conversion_a_bool()
    demo_conversiones_implicitas()
    demo_conversiones_seguras()
    demo_conversiones_avanzadas()
    ejercicios_practicos()
    
    print("\n" + "=" * 70)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("=" * 70)
    print("\n💡 Puntos clave:")
    print("   • int(): convierte a entero (trunca float)")
    print("   • float(): convierte a decimal")
    print("   • str(): convierte a string")
    print("   • bool(): False para 'vacío', True para el resto")
    print("   • Siempre valida antes de convertir")
    print("   • Usa try-except para conversiones seguras")
    print("   • Python hace conversiones implícitas con números")
    print("   • str NO se convierte implícitamente\n")


if __name__ == "__main__":
    main()
