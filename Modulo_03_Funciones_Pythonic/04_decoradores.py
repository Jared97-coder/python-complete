"""
Módulo 3 - Ejemplo 4: Decoradores
==================================

Este script demuestra decoradores en Python: desde básicos hasta avanzados.
"""

import time
import functools
from typing import Callable, Any


def seccion(titulo):
    """Helper para mostrar títulos de sección."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70 + "\n")


def demo_decorador_basico():
    """Demuestra decorador básico."""
    seccion("DECORADOR BÁSICO")
    
    # Decorador simple
    def mi_decorador(func):
        """Decorador que envuelve una función."""
        def envoltura():
            print("  Antes de la función")
            func()
            print("  Después de la función")
        return envoltura
    
    # Aplicar decorador manualmente
    def saludar():
        """Función simple."""
        print("  ¡Hola!")
    
    print("📌 Sin decorador:")
    saludar()
    
    print("\n📌 Con decorador (manual):")
    saludar_decorada = mi_decorador(saludar)
    saludar_decorada()
    
    # Usando sintaxis @ (azúcar sintáctica)
    print("\n📌 Con sintaxis @:")
    
    @mi_decorador
    def despedir():
        """Función decorada con @."""
        print("  ¡Adiós!")
    
    despedir()  # Automáticamente decorada


def demo_decorador_con_argumentos():
    """Demuestra decorador que acepta argumentos de la función."""
    seccion("DECORADOR CON ARGUMENTOS")
    
    def decorador(func):
        """Decorador que maneja argumentos."""
        def envoltura(*args, **kwargs):
            print(f"  Llamando {func.__name__} con args={args}, kwargs={kwargs}")
            resultado = func(*args, **kwargs)
            print(f"  Resultado: {resultado}")
            return resultado
        return envoltura
    
    @decorador
    def suma(a, b):
        """Suma dos números."""
        return a + b
    
    @decorador
    def saludar(nombre, saludo="Hola"):
        """Saluda a alguien."""
        return f"{saludo}, {nombre}!"
    
    print("📌 Función decorada con argumentos:")
    suma(5, 3)
    
    print("\n📌 Con kwargs:")
    saludar("Ana", saludo="Buenos días")


def demo_decorador_timer():
    """Demuestra decorador para medir tiempo."""
    seccion("DECORADOR TIMER")
    
    def timer(func):
        """Mide el tiempo de ejecución de una función."""
        @functools.wraps(func)
        def envoltura(*args, **kwargs):
            inicio = time.time()
            resultado = func(*args, **kwargs)
            fin = time.time()
            print(f"⏱️  {func.__name__} tomó {fin - inicio:.4f} segundos")
            return resultado
        return envoltura
    
    @timer
    def procesar_datos():
        """Simula procesamiento."""
        time.sleep(0.1)
        return "Datos procesados"
    
    @timer
    def calcular_fibonacci(n):
        """Calcula Fibonacci recursivo."""
        if n <= 1:
            return n
        return calcular_fibonacci(n-1) + calcular_fibonacci(n-2)
    
    print("📌 Midiendo tiempo de ejecución:")
    procesar_datos()
    
    print("\n📌 Fibonacci(10):")
    resultado = calcular_fibonacci(10)
    print(f"Resultado: {resultado}")


def demo_functools_wraps():
    """Demuestra la importancia de @functools.wraps."""
    seccion("@FUNCTOOLS.WRAPS")
    
    # Sin @functools.wraps
    def decorador_malo(func):
        """Decorador sin @wraps."""
        def envoltura(*args, **kwargs):
            """Envoltura."""
            return func(*args, **kwargs)
        return envoltura
    
    # Con @functools.wraps
    def decorador_bueno(func):
        """Decorador con @wraps."""
        @functools.wraps(func)
        def envoltura(*args, **kwargs):
            """Envoltura."""
            return func(*args, **kwargs)
        return envoltura
    
    @decorador_malo
    def funcion_mala():
        """Esta es la documentación original."""
        pass
    
    @decorador_bueno
    def funcion_buena():
        """Esta es la documentación original."""
        pass
    
    print("📌 Sin @functools.wraps:")
    print(f"Nombre: {funcion_mala.__name__}")  # 'envoltura'
    print(f"Doc: {funcion_mala.__doc__}")  # 'Envoltura.'
    
    print("\n📌 Con @functools.wraps:")
    print(f"Nombre: {funcion_buena.__name__}")  # 'funcion_buena'
    print(f"Doc: {funcion_buena.__doc__}")  # 'Esta es la documentación original.'


def demo_decorador_con_parametros():
    """Demuestra decorador que acepta parámetros."""
    seccion("DECORADOR CON PARÁMETROS")
    
    def repetir(veces):
        """Decorador que repite la ejecución N veces."""
        def decorador(func):
            @functools.wraps(func)
            def envoltura(*args, **kwargs):
                resultados = []
                for i in range(veces):
                    print(f"  Ejecución {i + 1}/{veces}")
                    resultado = func(*args, **kwargs)
                    resultados.append(resultado)
                return resultados
            return envoltura
        return decorador
    
    @repetir(3)
    def saludar(nombre):
        """Saluda a alguien."""
        return f"¡Hola, {nombre}!"
    
    print("📌 Decorador con parámetro (repetir 3 veces):")
    resultados = saludar("Ana")
    print(f"Resultados: {resultados}")
    
    # Otro parámetro
    def prefijo(texto):
        """Añade prefijo al resultado."""
        def decorador(func):
            @functools.wraps(func)
            def envoltura(*args, **kwargs):
                resultado = func(*args, **kwargs)
                return f"{texto} {resultado}"
            return envoltura
        return decorador
    
    @prefijo("🎉")
    def celebrar(evento):
        """Celebra un evento."""
        return f"¡{evento}!"
    
    print("\n📌 Decorador con prefijo:")
    print(celebrar("Cumpleaños"))


def demo_multiples_decoradores():
    """Demuestra múltiples decoradores en una función."""
    seccion("MÚLTIPLES DECORADORES")
    
    def negrita(func):
        """Envuelve resultado en **."""
        @functools.wraps(func)
        def envoltura(*args, **kwargs):
            resultado = func(*args, **kwargs)
            return f"**{resultado}**"
        return envoltura
    
    def cursiva(func):
        """Envuelve resultado en __."""
        @functools.wraps(func)
        def envoltura(*args, **kwargs):
            resultado = func(*args, **kwargs)
            return f"__{resultado}__"
        return envoltura
    
    def mayusculas(func):
        """Convierte a mayúsculas."""
        @functools.wraps(func)
        def envoltura(*args, **kwargs):
            resultado = func(*args, **kwargs)
            return resultado.upper()
        return envoltura
    
    print("📌 Un decorador:")
    
    @negrita
    def texto1():
        return "Hola"
    
    print(texto1())
    
    print("\n📌 Dos decoradores (orden importante):")
    
    @cursiva
    @negrita
    def texto2():
        return "Hola"
    
    print(texto2())  # __**Hola**__
    
    print("\n📌 Tres decoradores:")
    
    @mayusculas
    @cursiva
    @negrita
    def texto3():
        return "Hola"
    
    print(texto3())  # __**HOLA**__


def demo_decorador_clase():
    """Demuestra decorador como clase."""
    seccion("DECORADOR COMO CLASE")
    
    class Contador:
        """Decorador que cuenta llamadas."""
        
        def __init__(self, func):
            """Inicializa el decorador."""
            functools.update_wrapper(self, func)
            self.func = func
            self.llamadas = 0
        
        def __call__(self, *args, **kwargs):
            """Ejecuta la función decorada."""
            self.llamadas += 1
            print(f"  Llamada #{self.llamadas} a {self.func.__name__}")
            return self.func(*args, **kwargs)
        
        def reset(self):
            """Reinicia el contador."""
            self.llamadas = 0
    
    @Contador
    def saludar(nombre):
        """Saluda."""
        return f"¡Hola, {nombre}!"
    
    print("📌 Decorador como clase:")
    print(saludar("Ana"))
    print(saludar("Juan"))
    print(saludar("María"))
    
    print(f"\nTotal de llamadas: {saludar.llamadas}")
    
    saludar.reset()
    print(f"Después de reset: {saludar.llamadas}")


def demo_decoradores_utiles():
    """Demuestra decoradores útiles comunes."""
    seccion("DECORADORES ÚTILES COMUNES")
    
    # 1. Caché/Memoización
    def memoize(func):
        """Cachea resultados de la función."""
        cache = {}
        
        @functools.wraps(func)
        def envoltura(*args):
            if args not in cache:
                print(f"  Calculando para {args}...")
                cache[args] = func(*args)
            else:
                print(f"  Usando caché para {args}")
            return cache[args]
        
        return envoltura
    
    @memoize
    def fibonacci(n):
        """Fibonacci con memoización."""
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    print("📌 Memoización:")
    print(f"fibonacci(5) = {fibonacci(5)}")
    print(f"fibonacci(5) = {fibonacci(5)}")  # Usa caché
    
    # 2. Validación
    def validar_positivo(func):
        """Valida que los argumentos sean positivos."""
        @functools.wraps(func)
        def envoltura(*args):
            for arg in args:
                if not isinstance(arg, (int, float)) or arg <= 0:
                    raise ValueError(f"Todos los argumentos deben ser positivos: {arg}")
            return func(*args)
        return envoltura
    
    @validar_positivo
    def dividir(a, b):
        """Divide dos números."""
        return a / b
    
    print("\n📌 Validación:")
    print(f"dividir(10, 2) = {dividir(10, 2)}")
    
    try:
        dividir(10, -2)
    except ValueError as e:
        print(f"Error: {e}")
    
    # 3. Logging
    def log(func):
        """Registra llamadas a la función."""
        @functools.wraps(func)
        def envoltura(*args, **kwargs):
            print(f"📝 LOG: Llamando a {func.__name__}")
            print(f"   Args: {args}")
            print(f"   Kwargs: {kwargs}")
            resultado = func(*args, **kwargs)
            print(f"   Resultado: {resultado}")
            return resultado
        return envoltura
    
    @log
    def procesar(dato, formato="json"):
        """Procesa un dato."""
        return f"Procesado {dato} como {formato}"
    
    print("\n📌 Logging:")
    procesar("usuarios", formato="xml")


def demo_decorador_singleton():
    """Demuestra patrón Singleton con decorador."""
    seccion("PATRÓN SINGLETON")
    
    def singleton(cls):
        """Decorador Singleton para clases."""
        instancias = {}
        
        @functools.wraps(cls)
        def obtener_instancia(*args, **kwargs):
            if cls not in instancias:
                print(f"  Creando nueva instancia de {cls.__name__}")
                instancias[cls] = cls(*args, **kwargs)
            else:
                print(f"  Retornando instancia existente de {cls.__name__}")
            return instancias[cls]
        
        return obtener_instancia
    
    @singleton
    class BaseDatos:
        """Conexión a base de datos (singleton)."""
        
        def __init__(self):
            """Inicializa conexión."""
            self.conexiones = 0
            print("  BaseDatos inicializada")
        
        def consultar(self, query):
            """Ejecuta consulta."""
            self.conexiones += 1
            return f"Resultado de '{query}'"
    
    print("📌 Singleton:")
    db1 = BaseDatos()
    db2 = BaseDatos()
    db3 = BaseDatos()
    
    print(f"\ndb1 is db2: {db1 is db2}")
    print(f"db1 is db3: {db1 is db3}")


def ejercicio_practico():
    """Ejercicio práctico integrando conceptos."""
    seccion("EJERCICIO PRÁCTICO: Sistema de Retry")
    
    def retry(max_intentos=3, delay=1):
        """
        Decorador que reintenta una función en caso de error.
        
        Args:
            max_intentos: Número máximo de intentos
            delay: Segundos entre intentos
        """
        def decorador(func):
            @functools.wraps(func)
            def envoltura(*args, **kwargs):
                for intento in range(1, max_intentos + 1):
                    try:
                        print(f"  Intento {intento}/{max_intentos}...")
                        resultado = func(*args, **kwargs)
                        print(f"  ✅ Éxito en intento {intento}")
                        return resultado
                    except Exception as e:
                        print(f"  ❌ Error: {e}")
                        if intento < max_intentos:
                            print(f"  ⏳ Esperando {delay}s antes del siguiente intento...")
                            time.sleep(delay)
                        else:
                            print(f"  ❌ Fallaron todos los intentos")
                            raise
            return envoltura
        return decorador
    
    # Simulador de función que falla
    intentos_realizados = [0]  # Lista para que sea mutable en la función
    
    @retry(max_intentos=3, delay=0.5)
    def operacion_inestable():
        """Función que falla las primeras 2 veces."""
        intentos_realizados[0] += 1
        if intentos_realizados[0] < 3:
            raise ConnectionError("Conexión perdida")
        return "Operación exitosa"
    
    print("📌 Sistema de Retry:")
    try:
        resultado = operacion_inestable()
        print(f"\nResultado final: {resultado}")
    except Exception as e:
        print(f"\nError final: {e}")


def main():
    """Función principal."""
    print("\n" + "🐍" * 35)
    print("          DECORADORES EN PYTHON")
    print("🐍" * 35)
    
    demo_decorador_basico()
    demo_decorador_con_argumentos()
    demo_decorador_timer()
    demo_functools_wraps()
    demo_decorador_con_parametros()
    demo_multiples_decoradores()
    demo_decorador_clase()
    demo_decoradores_utiles()
    demo_decorador_singleton()
    ejercicio_practico()
    
    print("\n" + "=" * 70)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("=" * 70)
    print("\n💡 Puntos clave:")
    print("   • Decoradores modifican/extienden funciones sin alterarlas")
    print("   • Sintaxis: @decorador encima de la función")
    print("   • Usa @functools.wraps para preservar metadatos")
    print("   • Decoradores con parámetros: 3 niveles de funciones")
    print("   • Múltiples decoradores se aplican de abajo hacia arriba")
    print("   • Casos de uso: logging, timing, caché, validación, retry")
    print("   • También pueden decorar clases (ej: singleton)\n")


if __name__ == "__main__":
    main()
