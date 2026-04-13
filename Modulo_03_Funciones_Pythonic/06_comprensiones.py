"""
Módulo 3 - Ejemplo 6: Comprensiones (List, Dict, Set)
=====================================================

Este script demuestra comprehensions en Python: listas, diccionarios y conjuntos.
"""

import time


def seccion(titulo):
    """Helper para mostrar títulos de sección."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70 + "\n")


def demo_list_comprehension_basico():
    """Demuestra list comprehensions básicas."""
    seccion("LIST COMPREHENSION - BÁSICO")
    
    # Forma tradicional
    print("📌 Forma tradicional (con for):")
    cuadrados_tradicional = []
    for x in range(10):
        cuadrados_tradicional.append(x ** 2)
    print(cuadrados_tradicional)
    
    # Con list comprehension
    print("\n📌 Con list comprehension:")
    cuadrados = [x ** 2 for x in range(10)]
    print(cuadrados)
    
    # Más ejemplos
    print("\n📌 Convertir a mayúsculas:")
    palabras = ["hola", "mundo", "python"]
    mayusculas = [palabra.upper() for palabra in palabras]
    print(f"Original: {palabras}")
    print(f"Mayúsculas: {mayusculas}")
    
    print("\n📌 Obtener longitudes:")
    longitudes = [len(palabra) for palabra in palabras]
    print(f"Longitudes: {longitudes}")


def demo_list_comprehension_con_filtro():
    """Demuestra list comprehensions con condiciones."""
    seccion("LIST COMPREHENSION - CON FILTRO")
    
    # Filtrar números pares
    print("📌 Solo números pares:")
    numeros = range(20)
    pares = [x for x in numeros if x % 2 == 0]
    print(f"Números: {list(numeros)}")
    print(f"Pares: {pares}")
    
    # Múltiples condiciones
    print("\n📌 Múltiplos de 3 pero no de 6:")
    resultado = [x for x in range(30) if x % 3 == 0 and x % 6 != 0]
    print(resultado)
    
    # Filtrar strings
    print("\n📌 Palabras largas (>4 caracteres):")
    palabras = ["sol", "python", "es", "genial", "muy", "poderoso"]
    largas = [p for p in palabras if len(p) > 4]
    print(f"Original: {palabras}")
    print(f"Largas: {largas}")
    
    # Filtrar con métodos
    print("\n📌 Solo strings numéricos:")
    datos = ["123", "abc", "456", "def", "789"]
    numericos = [d for d in datos if d.isdigit()]
    print(f"Datos: {datos}")
    print(f"Numéricos: {numericos}")


def demo_list_comprehension_ifelse():
    """Demuestra list comprehensions con if-else."""
    seccion("LIST COMPREHENSION - IF-ELSE")
    
    # if-else en la expresión (no filtro)
    print("📌 Par o Impar:")
    numeros = range(10)
    etiquetas = ["Par" if x % 2 == 0 else "Impar" for x in numeros]
    for num, etiqueta in zip(numeros, etiquetas):
        print(f"  {num}: {etiqueta}")
    
    # Ajustar valores
    print("\n📌 Limitar valores (0-100):")
    valores = [-10, 50, 150, 75, 200, 30]
    limitados = [max(0, min(100, v)) for v in valores]
    print(f"Original: {valores}")
    print(f"Limitados: {limitados}")
    
    # Transformación condicional
    print("\n📌 Transformación condicional:")
    texto = "Hola Mundo Python"
    resultado = [c.lower() if c.isupper() else c.upper() for c in texto]
    print(f"Original: {texto}")
    print(f"Invertido: {''.join(resultado)}")


def demo_list_comprehension_anidada():
    """Demuestra list comprehensions anidadas."""
    seccion("LIST COMPREHENSION - ANIDADA")
    
    # Crear matriz
    print("📌 Crear matriz 3x3:")
    matriz = [[i * 3 + j for j in range(3)] for i in range(3)]
    for fila in matriz:
        print(f"  {fila}")
    
    # Aplanar matriz
    print("\n📌 Aplanar matriz:")
    plana = [elemento for fila in matriz for elemento in fila]
    print(f"Matriz: {matriz}")
    print(f"Plana: {plana}")
    
    # Productos cartesianos
    print("\n📌 Producto cartesiano:")
    colores = ["rojo", "verde"]
    tamaños = ["S", "M", "L"]
    productos = [f"{color}-{tamaño}" for color in colores for tamaño in tamaños]
    for producto in productos:
        print(f"  {producto}")
    
    # Coordenadas
    print("\n📌 Coordenadas (x, y):")
    coordenadas = [(x, y) for x in range(3) for y in range(3)]
    for coord in coordenadas:
        print(f"  {coord}")


def demo_dict_comprehension():
    """Demuestra dict comprehensions."""
    seccion("DICT COMPREHENSION")
    
    # Crear diccionario básico
    print("📌 Cuadrados:")
    cuadrados = {x: x ** 2 for x in range(6)}
    print(cuadrados)
    
    # De lista a diccionario
    print("\n📌 Palabras con su longitud:")
    palabras = ["python", "es", "genial"]
    longitudes = {palabra: len(palabra) for palabra in palabras}
    print(longitudes)
    
    # Invertir diccionario
    print("\n📌 Invertir diccionario:")
    original = {'a': 1, 'b': 2, 'c': 3}
    invertido = {valor: clave for clave, valor in original.items()}
    print(f"Original: {original}")
    print(f"Invertido: {invertido}")
    
    # Con condición
    print("\n📌 Solo números pares:")
    numeros = {x: x ** 2 for x in range(10) if x % 2 == 0}
    print(numeros)


def demo_dict_comprehension_transformar():
    """Demuestra transformaciones con dict comprehensions."""
    seccion("DICT COMPREHENSION - TRANSFORMACIONES")
    
    # Transformar valores
    print("📌 Duplicar valores:")
    precios = {'manzana': 1.5, 'banana': 0.8, 'naranja': 2.0}
    precios_dobles = {k: v * 2 for k, v in precios.items()}
    print(f"Original: {precios}")
    print(f"Doble: {precios_dobles}")
    
    # Transformar claves
    print("\n📌 Claves en mayúsculas:")
    mayusculas = {k.upper(): v for k, v in precios.items()}
    print(mayusculas)
    
    # Filtrar y transformar
    print("\n📌 Solo frutas caras (>1.0) con descuento 20%:")
    con_descuento = {k: v * 0.8 for k, v in precios.items() if v > 1.0}
    print(con_descuento)
    
    # De dos listas
    print("\n📌 De dos listas a diccionario:")
    claves = ['nombre', 'edad', 'ciudad']
    valores = ['Ana', 25, 'Madrid']
    persona = {k: v for k, v in zip(claves, valores)}
    print(persona)


def demo_set_comprehension():
    """Demuestra set comprehensions."""
    seccion("SET COMPREHENSION")
    
    # Set básico
    print("📌 Cuadrados únicos:")
    cuadrados = {x ** 2 for x in range(10)}
    print(cuadrados)  # Set (sin orden específico)
    
    # Eliminar duplicados automáticamente
    print("\n📌 Números únicos:")
    numeros = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    unicos = {x for x in numeros}
    print(f"Lista: {numeros}")
    print(f"Set: {unicos}")
    
    # Con transformación
    print("\n📌 Primeras letras únicas:")
    palabras = ["ana", "antonio", "beatriz", "bruno", "carlos", "ana"]
    primeras = {p[0].upper() for p in palabras}
    print(f"Palabras: {palabras}")
    print(f"Primeras letras: {primeras}")
    
    # Con filtro
    print("\n📌 Números impares únicos:")
    impares = {x for x in range(20) if x % 2 != 0}
    print(impares)


def demo_comparacion_performance():
    """Compara performance de comprensiones vs loops."""
    seccion("PERFORMANCE: COMPREHENSION VS LOOP")
    
    n = 100000
    
    # List comprehension
    inicio = time.time()
    resultado1 = [x ** 2 for x in range(n)]
    tiempo1 = time.time() - inicio
    
    # Loop tradicional
    inicio = time.time()
    resultado2 = []
    for x in range(n):
        resultado2.append(x ** 2)
    tiempo2 = time.time() - inicio
    
    print(f"📌 Creando lista de {n:,} cuadrados:")
    print(f"List comprehension: {tiempo1:.4f}s")
    print(f"Loop tradicional:   {tiempo2:.4f}s")
    print(f"Speedup: {tiempo2/tiempo1:.2f}x")
    
    # Dict comprehension vs loop
    inicio = time.time()
    dict1 = {x: x ** 2 for x in range(n)}
    tiempo1 = time.time() - inicio
    
    inicio = time.time()
    dict2 = {}
    for x in range(n):
        dict2[x] = x ** 2
    tiempo2 = time.time() - inicio
    
    print(f"\n📌 Creando diccionario de {n:,} cuadrados:")
    print(f"Dict comprehension: {tiempo1:.4f}s")
    print(f"Loop tradicional:   {tiempo2:.4f}s")
    print(f"Speedup: {tiempo2/tiempo1:.2f}x")
    
    print("\n✅ Comprehensions son más rápidas y legibles")


def demo_casos_complejos():
    """Demuestra casos de uso complejos."""
    seccion("CASOS DE USO COMPLEJOS")
    
    # Parsear datos
    print("📌 Parsear CSV:")
    csv_data = [
        "nombre,edad,ciudad",
        "Ana,25,Madrid",
        "Juan,30,Barcelona",
        "María,22,Valencia"
    ]
    
    # Saltar header y parsear
    registros = [
        dict(zip(csv_data[0].split(','), linea.split(',')))
        for linea in csv_data[1:]
    ]
    
    for registro in registros:
        print(f"  {registro}")
    
    # Agrupar por condición
    print("\n📌 Separar pares e impares:")
    numeros = range(20)
    agrupados = {
        'pares': [x for x in numeros if x % 2 == 0],
        'impares': [x for x in numeros if x % 2 != 0]
    }
    print(f"Pares: {agrupados['pares']}")
    print(f"Impares: {agrupados['impares']}")
    
    # Filtrar diccionario anidado
    print("\n📌 Filtrar estructura anidada:")
    usuarios = [
        {'nombre': 'Ana', 'edad': 25, 'activo': True},
        {'nombre': 'Juan', 'edad': 30, 'activo': False},
        {'nombre': 'María', 'edad': 22, 'activo': True}
    ]
    
    activos = [u['nombre'] for u in usuarios if u['activo']]
    print(f"Usuarios activos: {activos}")
    
    mayores = [u for u in usuarios if u['edad'] >= 25]
    print(f"Mayores de 25: {mayores}")


def demo_limites():
    """Demuestra cuándo NO usar comprehensions."""
    seccion("CUÁNDO NO USAR COMPREHENSIONS")
    
    print("❌ MAL: Comprehension muy compleja:")
    # Muy difícil de leer
    resultado_malo = [
        y for y in [
            x ** 2 if x % 2 == 0 else x ** 3
            for x in range(20)
            if x % 3 == 0 or x % 5 == 0
        ]
        if y > 10 and y < 100
    ]
    print(resultado_malo)
    
    print("\n✅ BIEN: Loop tradicional (más legible):")
    resultado_bueno = []
    for x in range(20):
        if x % 3 == 0 or x % 5 == 0:
            if x % 2 == 0:
                y = x ** 2
            else:
                y = x ** 3
            
            if 10 < y < 100:
                resultado_bueno.append(y)
    
    print(resultado_bueno)
    
    print("\n💡 Regla: Si necesitas explicar la comprehension,")
    print("   probablemente deberías usar un loop tradicional.")


def ejercicio_practico():
    """Ejercicio práctico integrando conceptos."""
    seccion("EJERCICIO PRÁCTICO: Análisis de Datos")
    
    # Dataset de ventas
    ventas = [
        {'producto': 'Laptop', 'cantidad': 2, 'precio': 1000, 'descuento': 0.1},
        {'producto': 'Mouse', 'cantidad': 5, 'precio': 20, 'descuento': 0},
        {'producto': 'Teclado', 'cantidad': 3, 'precio': 50, 'descuento': 0.15},
        {'producto': 'Monitor', 'cantidad': 1, 'precio': 300, 'descuento': 0.05},
        {'producto': 'USB', 'cantidad': 10, 'precio': 10, 'descuento': 0},
    ]
    
    print("📌 Dataset original:")
    for venta in ventas:
        print(f"  {venta}")
    
    # Calcular total por producto
    print("\n📌 Total por producto:")
    totales = {
        v['producto']: v['cantidad'] * v['precio'] * (1 - v['descuento'])
        for v in ventas
    }
    for producto, total in totales.items():
        print(f"  {producto}: ${total:.2f}")
    
    # Productos con descuento
    print("\n📌 Productos con descuento:")
    con_descuento = [v['producto'] for v in ventas if v['descuento'] > 0]
    print(f"  {con_descuento}")
    
    # Ventas mayores a $100
    print("\n📌 Ventas mayores a $100:")
    ventas_grandes = [
        v['producto']
        for v in ventas
        if v['cantidad'] * v['precio'] * (1 - v['descuento']) > 100
    ]
    print(f"  {ventas_grandes}")
    
    # Estadísticas
    print("\n📌 Estadísticas:")
    total_general = sum(totales.values())
    promedio = total_general / len(totales)
    print(f"  Total general: ${total_general:.2f}")
    print(f"  Promedio: ${promedio:.2f}")
    print(f"  Producto más caro: {max(totales, key=totales.get)}")
    print(f"  Producto más barato: {min(totales, key=totales.get)}")
    
    # Crear reporte
    print("\n📌 Reporte resumido:")
    reporte = [
        f"{p}: ${t:.2f} ({'CON' if p in con_descuento else 'SIN'} descuento)"
        for p, t in totales.items()
    ]
    for linea in reporte:
        print(f"  {linea}")


def main():
    """Función principal."""
    print("\n" + "🐍" * 35)
    print("          COMPREHENSIONS EN PYTHON")
    print("🐍" * 35)
    
    demo_list_comprehension_basico()
    demo_list_comprehension_con_filtro()
    demo_list_comprehension_ifelse()
    demo_list_comprehension_anidada()
    demo_dict_comprehension()
    demo_dict_comprehension_transformar()
    demo_set_comprehension()
    demo_comparacion_performance()
    demo_casos_complejos()
    demo_limites()
    ejercicio_practico()
    
    print("\n" + "=" * 70)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("=" * 70)
    print("\n💡 Puntos clave:")
    print("   • List: [expr for item in iterable if condition]")
    print("   • Dict: {key: value for item in iterable if condition}")
    print("   • Set: {expr for item in iterable if condition}")
    print("   • Más rápidas y concisas que loops tradicionales")
    print("   • if-else en expresión vs if como filtro")
    print("   • Pueden ser anidadas (pero cuidado con legibilidad)")
    print("   • No usar si la lógica es muy compleja")
    print("   • Ideal para transformaciones y filtros simples\n")


if __name__ == "__main__":
    main()
