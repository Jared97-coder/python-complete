"""
Módulo 3 - Ejemplo 3: Lambdas y Closures
=========================================

Este script demuestra funciones lambda (anónimas) y closures en Python.
"""


def seccion(titulo):
    """Helper para mostrar títulos de sección."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70 + "\n")


def demo_lambda_basico():
    """Demuestra funciones lambda básicas."""
    seccion("FUNCIONES LAMBDA - BÁSICO")
    
    # Función normal
    def suma_normal(a, b):
        """Suma dos números."""
        return a + b
    
    # Equivalente con lambda
    suma_lambda = lambda a, b: a + b
    
    print("📌 Función normal vs Lambda:")
    print(f"Normal: suma_normal(3, 5) = {suma_normal(3, 5)}")
    print(f"Lambda: suma_lambda(3, 5) = {suma_lambda(3, 5)}")
    
    # Lambda sin argumentos
    print("\n📌 Lambda sin argumentos:")
    obtener_pi = lambda: 3.14159
    print(f"obtener_pi() = {obtener_pi()}")
    
    # Lambda con un argumento
    print("\n📌 Lambda con un argumento:")
    cuadrado = lambda x: x ** 2
    print(f"cuadrado(5) = {cuadrado(5)}")
    
    triple = lambda x: x * 3
    print(f"triple(4) = {triple(4)}")
    
    # Lambda con múltiples argumentos
    print("\n📌 Lambda con múltiples argumentos:")
    multiplicar = lambda x, y, z: x * y * z
    print(f"multiplicar(2, 3, 4) = {multiplicar(2, 3, 4)}")
    
    # Lambda con expresiones complejas
    print("\n📌 Lambda con expresiones:")
    es_par = lambda x: "Par" if x % 2 == 0 else "Impar"
    print(f"es_par(4) = {es_par(4)}")
    print(f"es_par(7) = {es_par(7)}")
    
    mayor = lambda a, b: a if a > b else b
    print(f"mayor(10, 15) = {mayor(10, 15)}")


def demo_lambda_con_map():
    """Demuestra lambda con map()."""
    seccion("LAMBDA CON MAP()")
    
    # map() aplica una función a cada elemento
    numeros = [1, 2, 3, 4, 5]
    
    print("📌 Elevar al cuadrado con map:")
    print(f"Original: {numeros}")
    cuadrados = list(map(lambda x: x ** 2, numeros))
    print(f"Cuadrados: {cuadrados}")
    
    # Múltiples iterables
    print("\n📌 map con múltiples listas:")
    lista1 = [1, 2, 3]
    lista2 = [10, 20, 30]
    print(f"Lista 1: {lista1}")
    print(f"Lista 2: {lista2}")
    sumas = list(map(lambda x, y: x + y, lista1, lista2))
    print(f"Sumas: {sumas}")
    
    # Transformaciones de strings
    print("\n📌 Transformar strings:")
    nombres = ["ana", "juan", "maría"]
    print(f"Original: {nombres}")
    capitalizados = list(map(lambda s: s.capitalize(), nombres))
    print(f"Capitalizados: {capitalizados}")


def demo_lambda_con_filter():
    """Demuestra lambda con filter()."""
    seccion("LAMBDA CON FILTER()")
    
    # filter() selecciona elementos que cumplen condición
    numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print("📌 Filtrar números pares:")
    print(f"Original: {numeros}")
    pares = list(filter(lambda x: x % 2 == 0, numeros))
    print(f"Pares: {pares}")
    
    print("\n📌 Filtrar números mayores que 5:")
    mayores = list(filter(lambda x: x > 5, numeros))
    print(f"Mayores que 5: {mayores}")
    
    # Filtrar strings
    print("\n📌 Filtrar strings por longitud:")
    palabras = ["hola", "python", "es", "genial", "muy", "poderoso"]
    print(f"Original: {palabras}")
    largas = list(filter(lambda s: len(s) > 3, palabras))
    print(f"Más de 3 letras: {largas}")


def demo_lambda_con_sorted():
    """Demuestra lambda con sorted()."""
    seccion("LAMBDA CON SORTED()")
    
    # Ordenar por clave personalizada
    print("📌 Ordenar tuplas por segundo elemento:")
    pares = [(1, 'b'), (2, 'a'), (3, 'd'), (4, 'c')]
    print(f"Original: {pares}")
    ordenados = sorted(pares, key=lambda x: x[1])
    print(f"Ordenados: {ordenados}")
    
    # Ordenar objetos complejos
    print("\n📌 Ordenar diccionarios por edad:")
    personas = [
        {'nombre': 'Ana', 'edad': 25},
        {'nombre': 'Juan', 'edad': 30},
        {'nombre': 'María', 'edad': 22}
    ]
    por_edad = sorted(personas, key=lambda p: p['edad'])
    for persona in por_edad:
        print(f"  {persona['nombre']}: {persona['edad']} años")
    
    # Ordenar strings por longitud
    print("\n📌 Ordenar por longitud:")
    palabras = ["python", "es", "un", "lenguaje", "muy", "expresivo"]
    print(f"Original: {palabras}")
    por_longitud = sorted(palabras, key=lambda s: len(s))
    print(f"Por longitud: {por_longitud}")
    
    # Orden inverso
    print("\n📌 Orden inverso:")
    numeros = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"Original: {numeros}")
    descendente = sorted(numeros, key=lambda x: x, reverse=True)
    print(f"Descendente: {descendente}")


def demo_lambda_limitaciones():
    """Demuestra cuándo NO usar lambdas."""
    seccion("CUÁNDO NO USAR LAMBDAS")
    
    print("❌ NO: Lambda compleja (difícil de leer)")
    # Malo - lambda compleja
    validar_malo = lambda x: True if x is not None and isinstance(x, int) and x > 0 and x < 100 else False
    print(f"validar_malo(50) = {validar_malo(50)}")
    
    print("\n✅ SÍ: Función normal (legible)")
    # Bueno - función normal
    def validar_bueno(x):
        """Valida que x sea entero entre 1 y 99."""
        if x is None:
            return False
        if not isinstance(x, int):
            return False
        if x <= 0 or x >= 100:
            return False
        return True
    
    print(f"validar_bueno(50) = {validar_bueno(50)}")
    
    print("\n❌ NO: Lambda con efectos secundarios")
    # Las lambdas son para expresiones puras, no efectos secundarios
    # Malo (aunque funciona)
    resultados = []
    lista = [1, 2, 3]
    list(map(lambda x: resultados.append(x * 2), lista))  # Antipatrón
    print(f"Usando lambda con append (antipatrón): {resultados}")
    
    print("\n✅ SÍ: Comprensión o función normal")
    # Bueno
    resultados = [x * 2 for x in lista]
    print(f"Usando comprensión: {resultados}")


def demo_closures_basico():
    """Demuestra closures básicos."""
    seccion("CLOSURES - BÁSICO")
    
    print("📌 Closure simple:")
    
    def exterior(x):
        """Función exterior."""
        def interior(y):
            """Función interior que 'recuerda' x."""
            return x + y
        return interior
    
    # Crear closure
    sumar_5 = exterior(5)
    sumar_10 = exterior(10)
    
    print(f"sumar_5(3) = {sumar_5(3)}")  # 5 + 3 = 8
    print(f"sumar_5(7) = {sumar_5(7)}")  # 5 + 7 = 12
    print(f"sumar_10(3) = {sumar_10(3)}")  # 10 + 3 = 13
    
    # Mostrar el closure
    print(f"\n📌 Variables capturadas:")
    print(f"Closure de sumar_5: {sumar_5.__closure__}")
    print(f"Valor capturado: {sumar_5.__closure__[0].cell_contents}")


def demo_closures_factory():
    """Demuestra closures como factory functions."""
    seccion("CLOSURES - FACTORY FUNCTIONS")
    
    # Factory de funciones de multiplicación
    def crear_multiplicador(n):
        """Crea una función que multiplica por n."""
        def multiplicar(x):
            return x * n
        return multiplicar
    
    print("📌 Factory de multiplicadores:")
    doble = crear_multiplicador(2)
    triple = crear_multiplicador(3)
    decuple = crear_multiplicador(10)
    
    print(f"doble(5) = {doble(5)}")
    print(f"triple(5) = {triple(5)}")
    print(f"decuple(5) = {decuple(5)}")
    
    # Factory de saludos
    def crear_saludador(saludo):
        """Crea función de saludo personalizada."""
        def saludar(nombre):
            return f"{saludo}, {nombre}!"
        return saludar
    
    print("\n📌 Factory de saludadores:")
    saludar_formal = crear_saludador("Buenos días")
    saludar_informal = crear_saludador("Hola")
    
    print(saludar_formal("Dr. Smith"))
    print(saludar_informal("Ana"))


def demo_closures_estado():
    """Demuestra closures con estado mutable."""
    seccion("CLOSURES - ESTADO MUTABLE")
    
    # Contador con closure
    def crear_contador():
        """Crea un contador que mantiene estado."""
        count = 0
        
        def incrementar():
            nonlocal count  # Necesario para modificar la variable exterior
            count += 1
            return count
        
        return incrementar
    
    print("📌 Contador con closure:")
    contador1 = crear_contador()
    contador2 = crear_contador()
    
    print(f"Contador 1: {contador1()}")  # 1
    print(f"Contador 1: {contador1()}")  # 2
    print(f"Contador 1: {contador1()}")  # 3
    print(f"Contador 2: {contador2()}")  # 1 (independiente)
    print(f"Contador 2: {contador2()}")  # 2
    
    # Banco con múltiples operaciones
    def crear_cuenta(saldo_inicial=0):
        """Crea una cuenta bancaria simple."""
        saldo = saldo_inicial
        
        def depositar(cantidad):
            nonlocal saldo
            saldo += cantidad
            return f"Depositado: ${cantidad}. Saldo: ${saldo}"
        
        def retirar(cantidad):
            nonlocal saldo
            if cantidad > saldo:
                return f"Fondos insuficientes. Saldo: ${saldo}"
            saldo -= cantidad
            return f"Retirado: ${cantidad}. Saldo: ${saldo}"
        
        def ver_saldo():
            return f"Saldo actual: ${saldo}"
        
        return depositar, retirar, ver_saldo
    
    print("\n📌 Cuenta bancaria con closures:")
    depositar, retirar, ver_saldo = crear_cuenta(100)
    
    print(ver_saldo())
    print(depositar(50))
    print(retirar(30))
    print(ver_saldo())


def demo_closures_decorador_simple():
    """Demuestra closure como base para decoradores."""
    seccion("CLOSURES - BASE PARA DECORADORES")
    
    def crear_decorador():
        """Crea un decorador simple usando closures."""
        def decorador(funcion):
            """Envuelve una función."""
            def envoltura(*args, **kwargs):
                print("  Antes de llamar a la función")
                resultado = funcion(*args, **kwargs)
                print("  Después de llamar a la función")
                return resultado
            return envoltura
        return decorador
    
    print("📌 Decorador creado con closures:")
    
    mi_decorador = crear_decorador()
    
    @mi_decorador
    def saludar(nombre):
        """Función decorada."""
        print(f"  ¡Hola, {nombre}!")
        return "Saludo completado"
    
    resultado = saludar("Ana")
    print(f"Resultado: {resultado}")


def ejercicio_practico():
    """Ejercicio práctico integrando conceptos."""
    seccion("EJERCICIO PRÁCTICO: Procesador de Datos")
    
    # Pipeline de transformaciones con lambdas
    def pipeline(*funciones):
        """Crea un pipeline de transformaciones."""
        def procesar(valor):
            resultado = valor
            for func in funciones:
                resultado = func(resultado)
            return resultado
        return procesar
    
    print("📌 Pipeline de transformaciones:")
    
    # Crear pipeline
    procesar_texto = pipeline(
        lambda s: s.strip(),
        lambda s: s.lower(),
        lambda s: s.replace(" ", "_"),
        lambda s: f"prefijo_{s}_sufijo"
    )
    
    texto = "  Hola Mundo Python  "
    print(f"Original: '{texto}'")
    print(f"Procesado: '{procesar_texto(texto)}'")
    
    # Pipeline numérico
    print("\n📌 Pipeline numérico:")
    procesar_numero = pipeline(
        lambda x: x * 2,      # Duplicar
        lambda x: x + 10,     # Sumar 10
        lambda x: x ** 2,     # Elevar al cuadrado
        lambda x: x / 100     # Dividir por 100
    )
    
    numero = 5
    print(f"Entrada: {numero}")
    print(f"Salida: {procesar_numero(numero)}")
    
    # Factory de validadores
    print("\n📌 Factory de validadores:")
    
    def crear_validador(condicion, mensaje):
        """Crea función validadora."""
        def validar(valor):
            if not condicion(valor):
                return f"❌ {mensaje}"
            return "✅ Válido"
        return validar
    
    validar_positivo = crear_validador(
        lambda x: x > 0,
        "El número debe ser positivo"
    )
    
    validar_longitud = crear_validador(
        lambda s: len(s) >= 3,
        "El texto debe tener al menos 3 caracteres"
    )
    
    print(validar_positivo(10))
    print(validar_positivo(-5))
    print(validar_longitud("Python"))
    print(validar_longitud("Hi"))


def main():
    """Función principal."""
    print("\n" + "🐍" * 35)
    print("          LAMBDAS Y CLOSURES EN PYTHON")
    print("🐍" * 35)
    
    demo_lambda_basico()
    demo_lambda_con_map()
    demo_lambda_con_filter()
    demo_lambda_con_sorted()
    demo_lambda_limitaciones()
    demo_closures_basico()
    demo_closures_factory()
    demo_closures_estado()
    demo_closures_decorador_simple()
    ejercicio_practico()
    
    print("\n" + "=" * 70)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("=" * 70)
    print("\n💡 Puntos clave:")
    print("   • Lambdas: funciones anónimas de una línea")
    print("   • Sintaxis: lambda argumentos: expresión")
    print("   • Útiles con map(), filter(), sorted()")
    print("   • No usar para lógica compleja")
    print("   • Closures: funciones que recuerdan su entorno")
    print("   • nonlocal: modificar variables del closure")
    print("   • Factory functions: crear funciones personalizadas")
    print("   • Base conceptual de decoradores\n")


if __name__ == "__main__":
    main()
