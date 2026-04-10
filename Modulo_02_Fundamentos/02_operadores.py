"""
Módulo 2 - Ejemplo 2: Operadores en Python
==========================================

Este script demuestra todos los tipos de operadores
disponibles en Python.
"""


def seccion(titulo):
    """Helper para mostrar títulos de sección."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70 + "\n")


def demo_operadores_aritmeticos():
    """Demuestra operadores aritméticos."""
    seccion("OPERADORES ARITMÉTICOS")
    
    a = 10
    b = 3
    
    print(f"a = {a}, b = {b}\n")
    
    print(f"Suma:              a + b  = {a + b}")
    print(f"Resta:             a - b  = {a - b}")
    print(f"Multiplicación:    a * b  = {a * b}")
    print(f"División:          a / b  = {a / b}")
    print(f"División entera:   a // b = {a // b}")
    print(f"Módulo (resto):    a % b  = {a % b}")
    print(f"Potencia:          a ** b = {a ** b}")
    
    # Operadores de asignación compuesta
    print("\n📌 Operadores de asignación compuesta:")
    x = 10
    print(f"x inicial: {x}")
    
    x += 5  # x = x + 5
    print(f"Después de x += 5:  {x}")
    
    x -= 3  # x = x - 3
    print(f"Después de x -= 3:  {x}")
    
    x *= 2  # x = x * 2
    print(f"Después de x *= 2:  {x}")
    
    x /= 4  # x = x / 4
    print(f"Después de x /= 4:  {x}")
    
    x //= 2  # x = x // 2
    print(f"Después de x //= 2: {x}")
    
    x %= 2  # x = x % 2
    print(f"Después de x %= 2:  {x}")
    
    x = 2
    x **= 3  # x = x ** 3
    print(f"Después de x **= 3 (x era 2): {x}")
    
    # Casos especiales
    print("\n📌 Casos especiales:")
    print(f"Negativo:     -a   = {-a}")
    print(f"Positivo:     +a   = {+a}")
    print(f"Valor abs:    abs(-5) = {abs(-5)}")
    
    # Precedencia
    print("\n📌 Precedencia de operadores:")
    resultado1 = 2 + 3 * 4
    resultado2 = (2 + 3) * 4
    print(f"2 + 3 * 4     = {resultado1}  # La multiplicación primero")
    print(f"(2 + 3) * 4   = {resultado2}  # Los paréntesis primero")
    
    resultado3 = 2 ** 3 ** 2
    resultado4 = (2 ** 3) ** 2
    print(f"2 ** 3 ** 2   = {resultado3}  # Asociatividad derecha")
    print(f"(2 ** 3) ** 2 = {resultado4}")


def demo_operadores_comparacion():
    """Demuestra operadores de comparación."""
    seccion("OPERADORES DE COMPARACIÓN")
    
    a = 5
    b = 3
    c = 5
    
    print(f"a = {a}, b = {b}, c = {c}\n")
    
    print(f"Igual a:           a == b  → {a == b}")
    print(f"Igual a:           a == c  → {a == c}")
    print(f"Diferente de:      a != b  → {a != b}")
    print(f"Mayor que:         a > b   → {a > b}")
    print(f"Menor que:         a < b   → {a < b}")
    print(f"Mayor o igual:     a >= c  → {a >= c}")
    print(f"Menor o igual:     b <= a  → {b <= a}")
    
    # Comparaciones encadenadas
    print("\n📌 Comparaciones encadenadas:")
    x = 5
    print(f"x = {x}")
    print(f"1 < x < 10       → {1 < x < 10}")
    print(f"10 > x >= 3      → {10 > x >= 3}")
    print(f"1 < x < 3        → {1 < x < 3}")
    
    # Comparación de strings
    print("\n📌 Comparación de strings (orden lexicográfico):")
    print(f"'abc' < 'abd'         → {'abc' < 'abd'}")
    print(f"'Python' == 'Python'  → {'Python' == 'Python'}")
    print(f"'Python' == 'python'  → {'Python' == 'python'}")
    print(f"'a' < 'b'             → {'a' < 'b'}")
    print(f"'A' < 'a'             → {'A' < 'a'}  # Mayúsculas < minúsculas")
    
    # Orden de caracteres
    print("\n📌 Valores ord() de caracteres:")
    for char in ['A', 'Z', 'a', 'z', '0', '9']:
        print(f"ord('{char}') = {ord(char)}")


def demo_operadores_logicos():
    """Demuestra operadores lógicos."""
    seccion("OPERADORES LÓGICOS")
    
    print("📌 Operador AND (y lógico):")
    print(f"True and True   → {True and True}")
    print(f"True and False  → {True and False}")
    print(f"False and True  → {False and True}")
    print(f"False and False → {False and False}")
    
    print("\n📌 Operador OR (o lógico):")
    print(f"True or True    → {True or True}")
    print(f"True or False   → {True or False}")
    print(f"False or True   → {False or True}")
    print(f"False or False  → {False or False}")
    
    print("\n📌 Operador NOT (negación):")
    print(f"not True        → {not True}")
    print(f"not False       → {not False}")
    
    # Ejemplos prácticos
    print("\n📌 Ejemplos prácticos:")
    edad = 20
    tiene_licencia = True
    
    puede_conducir = edad >= 18 and tiene_licencia
    print(f"Edad: {edad}, Tiene licencia: {tiene_licencia}")
    print(f"¿Puede conducir? {puede_conducir}")
    
    es_fin_de_semana = True
    es_feriado = False
    puede_descansar = es_fin_de_semana or es_feriado
    print(f"\nEs fin de semana: {es_fin_de_semana}, Es feriado: {es_feriado}")
    print(f"¿Puede descansar? {puede_descansar}")
    
    # Cortocircuito (short-circuit evaluation)
    print("\n📌 Evaluación de cortocircuito:")
    print("Python evalúa solo lo necesario en expresiones lógicas:\n")
    
    def retorna_true():
        print("  → Evaluando retorna_true()")
        return True
    
    def retorna_false():
        print("  → Evaluando retorna_false()")
        return False
    
    print("Evaluando: retorna_false() and retorna_true()")
    resultado = retorna_false() and retorna_true()
    print(f"Resultado: {resultado}\n")
    
    print("Evaluando: retorna_true() or retorna_false()")
    resultado = retorna_true() or retorna_false()
    print(f"Resultado: {resultado}")
    
    # Precedencia
    print("\n📌 Precedencia: not > and > or")
    resultado = True or False and False
    print(f"True or False and False → {resultado}")
    print("  (se evalúa como: True or (False and False))")
    
    resultado = not True or False
    print(f"not True or False → {resultado}")
    print("  (se evalúa como: (not True) or False)")


def demo_operadores_identidad():
    """Demuestra operadores de identidad."""
    seccion("OPERADORES DE IDENTIDAD (is, is not)")
    
    print("📌 Comparan si dos variables apuntan al mismo objeto en memoria\n")
    
    # Con números pequeños (Python los cachea)
    a = 5
    b = 5
    c = a
    
    print(f"a = {a}, id(a) = {id(a)}")
    print(f"b = {b}, id(b) = {id(b)}")
    print(f"c = a,  id(c) = {id(c)}")
    print(f"\na is b → {a is b}  # Python cachea números pequeños")
    print(f"a is c → {a is c}")
    print(f"a == b → {a == b}")
    
    # Con listas (objetos mutables)
    print("\n📌 Con listas:")
    lista1 = [1, 2, 3]
    lista2 = [1, 2, 3]
    lista3 = lista1
    
    print(f"lista1 = {lista1}, id = {id(lista1)}")
    print(f"lista2 = {lista2}, id = {id(lista2)}")
    print(f"lista3 = lista1,   id = {id(lista3)}")
    print(f"\nlista1 is lista2 → {lista1 is lista2}  # Objetos diferentes")
    print(f"lista1 is lista3 → {lista1 is lista3}  # Mismo objeto")
    print(f"lista1 == lista2 → {lista1 == lista2}  # Mismo contenido")
    
    # Con None
    print("\n📌 Con None (uso común):")
    resultado = None
    print(f"resultado = {resultado}")
    print(f"resultado is None     → {resultado is None}")
    print(f"resultado is not None → {resultado is not None}")
    print(f"resultado == None     → {resultado == None}  # Funciona pero no es idiomático")
    
    # Diferencia entre is y ==
    print("\n📌 Diferencia clave:")
    print("  'is'  compara identidad (mismo objeto en memoria)")
    print("  '=='  compara valor (mismo contenido)")


def demo_operadores_pertenencia():
    """Demuestra operadores de pertenencia."""
    seccion("OPERADORES DE PERTENENCIA (in, not in)")
    
    print("📌 Con strings:")
    texto = "Python es genial"
    print(f"texto = '{texto}'")
    print(f"'Python' in texto      → {'Python' in texto}")
    print(f"'Java' in texto        → {'Java' in texto}")
    print(f"'es' in texto          → {'es' in texto}")
    print(f"'xyz' not in texto     → {'xyz' not in texto}")
    
    print("\n📌 Con listas:")
    numeros = [1, 2, 3, 4, 5]
    print(f"numeros = {numeros}")
    print(f"3 in numeros           → {3 in numeros}")
    print(f"10 in numeros          → {10 in numeros}")
    print(f"10 not in numeros      → {10 not in numeros}")
    
    print("\n📌 Con tuplas:")
    coordenadas = (10, 20, 30)
    print(f"coordenadas = {coordenadas}")
    print(f"20 in coordenadas      → {20 in coordenadas}")
    print(f"40 in coordenadas      → {40 in coordenadas}")
    
    print("\n📌 Con diccionarios (verifica llaves):")
    persona = {'nombre': 'Juan', 'edad': 30, 'ciudad': 'Madrid'}
    print(f"persona = {persona}")
    print(f"'nombre' in persona    → {'nombre' in persona}")
    print(f"'Juan' in persona      → {'Juan' in persona}  # No es una llave")
    print(f"'edad' in persona      → {'edad' in persona}")
    
    # Verificar valores en diccionario
    print(f"\n'Juan' in persona.values() → {'Juan' in persona.values()}")
    
    print("\n📌 Con sets:")
    frutas = {'manzana', 'pera', 'uva'}
    print(f"frutas = {frutas}")
    print(f"'pera' in frutas       → {'pera' in frutas}")
    print(f"'banana' in frutas     → {'banana' in frutas}")


def demo_operadores_bitwise():
    """Demuestra operadores a nivel de bits."""
    seccion("OPERADORES BITWISE (Nivel de Bits)")
    
    a = 60  # 0011 1100 en binario
    b = 13  # 0000 1101 en binario
    
    print(f"a = {a:3d} = {bin(a)}")
    print(f"b = {b:3d} = {bin(b)}\n")
    
    print(f"AND    a & b  = {a & b:3d} = {bin(a & b)}")
    print(f"OR     a | b  = {a | b:3d} = {bin(a | b)}")
    print(f"XOR    a ^ b  = {a ^ b:3d} = {bin(a ^ b)}")
    print(f"NOT    ~a     = {~a:3d} = {bin(~a & 0xFF)}")  # Mostrar solo 8 bits
    print(f"LEFT   a << 2 = {a << 2:3d} = {bin(a << 2)}")
    print(f"RIGHT  a >> 2 = {a >> 2:3d} = {bin(a >> 2)}")
    
    print("\n📌 Tabla de verdad AND:")
    print("0 & 0 = 0")
    print("0 & 1 = 0")
    print("1 & 0 = 0")
    print("1 & 1 = 1")
    
    print("\n📌 Tabla de verdad OR:")
    print("0 | 0 = 0")
    print("0 | 1 = 1")
    print("1 | 0 = 1")
    print("1 | 1 = 1")
    
    print("\n📌 Tabla de verdad XOR:")
    print("0 ^ 0 = 0")
    print("0 ^ 1 = 1")
    print("1 ^ 0 = 1")
    print("1 ^ 1 = 0")
    
    # Uso práctico: intercambiar sin variable temporal
    print("\n📌 Truco: Intercambiar valores sin variable temporal:")
    x, y = 5, 10
    print(f"Antes: x={x}, y={y}")
    x = x ^ y
    y = x ^ y
    x = x ^ y
    print(f"Después: x={x}, y={y}")


def demo_precedencia():
    """Demuestra la precedencia de operadores."""
    seccion("PRECEDENCIA DE OPERADORES")
    
    print("📌 De mayor a menor precedencia:\n")
    precedencia = [
        "1. Paréntesis:                ()",
        "2. Exponenciación:            **",
        "3. Unarios:                   +x, -x, not x",
        "4. Multiplicación/División:   *, /, //, %",
        "5. Suma/Resta:                +, -",
        "6. Bitwise shift:             <<, >>",
        "7. Bitwise AND:               &",
        "8. Bitwise XOR:               ^",
        "9. Bitwise OR:                |",
        "10. Comparación:              ==, !=, <, >, <=, >=, is, in",
        "11. Booleano NOT:             not",
        "12. Booleano AND:             and",
        "13. Booleano OR:              or"
    ]
    
    for item in precedencia:
        print(item)
    
    print("\n📌 Ejemplos:")
    
    # Ejemplo 1
    resultado = 2 + 3 * 4
    print(f"\n2 + 3 * 4 = {resultado}")
    print("  Se evalúa como: 2 + (3 * 4) = 2 + 12 = 14")
    
    # Ejemplo 2
    resultado = 2 ** 3 ** 2
    print(f"\n2 ** 3 ** 2 = {resultado}")
    print("  Se evalúa como: 2 ** (3 ** 2) = 2 ** 9 = 512")
    
    # Ejemplo 3
    resultado = 10 - 5 - 2
    print(f"\n10 - 5 - 2 = {resultado}")
    print("  Se evalúa como: (10 - 5) - 2 = 5 - 2 = 3")
    
    # Ejemplo 4
    resultado = True or False and False
    print(f"\nTrue or False and False = {resultado}")
    print("  Se evalúa como: True or (False and False) = True")
    
    # Ejemplo 5
    resultado = 5 > 3 and 10 < 20 or False
    print(f"\n5 > 3 and 10 < 20 or False = {resultado}")
    print("  Se evalúa como: (5 > 3 and 10 < 20) or False = True or False = True")
    
    print("\n💡 Consejo: Usa paréntesis para claridad, aunque no sean necesarios")
    print("   Es mejor: (5 > 3) and (10 < 20)")
    print("   Que:       5 > 3 and 10 < 20")


def ejercicios_practicos():
    """Ejercicios prácticos sobre operadores."""
    seccion("EJERCICIOS PRÁCTICOS")
    
    print("🎯 Ejercicio 1: Calculadora de propinas")
    print("-" * 70)
    cuenta = 50.0
    porcentaje_propina = 15
    propina = cuenta * (porcentaje_propina / 100)
    total = cuenta + propina
    print(f"Cuenta: ${cuenta:.2f}")
    print(f"Propina ({porcentaje_propina}%): ${propina:.2f}")
    print(f"Total: ${total:.2f}")
    
    print("\n🎯 Ejercicio 2: Verificar si un número es par")
    print("-" * 70)
    numero = 42
    es_par = numero % 2 == 0
    print(f"¿El número {numero} es par? {es_par}")
    
    print("\n🎯 Ejercicio 3: Verificar rango de edad")
    print("-" * 70)
    edad = 25
    es_adulto_joven = 18 <= edad <= 35
    print(f"Edad: {edad}")
    print(f"¿Es adulto joven (18-35)? {es_adulto_joven}")
    
    print("\n🎯 Ejercicio 4: Conversión de temperatura")
    print("-" * 70)
    celsius = 25
    fahrenheit = (celsius * 9/5) + 32
    print(f"{celsius}°C = {fahrenheit}°F")
    
    print("\n🎯 Ejercicio 5: Calcular descuento")
    print("-" * 70)
    precio_original = 100.0
    porcentaje_descuento = 20
    descuento = precio_original * (porcentaje_descuento / 100)
    precio_final = precio_original - descuento
    print(f"Precio original: ${precio_original:.2f}")
    print(f"Descuento ({porcentaje_descuento}%): ${descuento:.2f}")
    print(f"Precio final: ${precio_final:.2f}")


def main():
    """Función principal."""
    print("\n" + "🐍" * 35)
    print("          OPERADORES EN PYTHON")
    print("🐍" * 35)
    
    demo_operadores_aritmeticos()
    demo_operadores_comparacion()
    demo_operadores_logicos()
    demo_operadores_identidad()
    demo_operadores_pertenencia()
    demo_operadores_bitwise()
    demo_precedencia()
    ejercicios_practicos()
    
    print("\n" + "=" * 70)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("=" * 70)
    print("\n💡 Puntos clave:")
    print("   • Aritméticos: +, -, *, /, //, %, **")
    print("   • Comparación: ==, !=, <, >, <=, >=")
    print("   • Lógicos: and, or, not")
    print("   • Identidad: is, is not (para objetos)")
    print("   • Pertenencia: in, not in (para secuencias)")
    print("   • Bitwise: &, |, ^, ~, <<, >>")
    print("   • Usa paréntesis para claridad\n")


if __name__ == "__main__":
    main()
