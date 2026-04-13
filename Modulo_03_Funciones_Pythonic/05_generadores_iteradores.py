"""
Módulo 3 - Ejemplo 5: Generadores e Iteradores
==============================================

Este script demuestra iteradores y generadores en Python.
"""

import sys
from collections.abc import Iterator, Iterable


def seccion(titulo):
    """Helper para mostrar títulos de sección."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70 + "\n")


def demo_protocolo_iterador():
    """Demuestra el protocolo de iterador."""
    seccion("PROTOCOLO DE ITERADOR")
    
    print("📌 Iteración con for (detrás de escena):")
    numeros = [1, 2, 3, 4, 5]
    
    # Lo que hace for internamente
    print("Lista:", numeros)
    iterador = iter(numeros)  # __iter__()
    print(f"Iterador creado: {iterador}")
    
    try:
        print(f"next() -> {next(iterador)}")  # __next__()
        print(f"next() -> {next(iterador)}")
        print(f"next() -> {next(iterador)}")
        print(f"next() -> {next(iterador)}")
        print(f"next() -> {next(iterador)}")
        print(f"next() -> {next(iterador)}")  # StopIteration
    except StopIteration:
        print("StopIteration: fin de la iteración")


def demo_clase_iterador():
    """Demuestra iterador personalizado."""
    seccion("CLASE ITERADOR PERSONALIZADA")
    
    class Contador:
        """Iterador que cuenta del inicio al fin."""
        
        def __init__(self, inicio, fin):
            """Inicializa el contador."""
            self.actual = inicio
            self.fin = fin
        
        def __iter__(self):
            """Retorna el iterador (self)."""
            return self
        
        def __next__(self):
            """Retorna el siguiente valor."""
            if self.actual > self.fin:
                raise StopIteration
            valor = self.actual
            self.actual += 1
            return valor
    
    print("📌 Iterador personalizado (Contador):")
    contador = Contador(1, 5)
    
    print("Usando for:")
    for num in contador:
        print(f"  {num}")
    
    # Crear nuevo iterador (el anterior se agotó)
    print("\nUsando next() manualmente:")
    contador2 = Contador(10, 12)
    print(f"  {next(contador2)}")
    print(f"  {next(contador2)}")
    print(f"  {next(contador2)}")
    
    # Clase iterable que produce iteradores
    class Rango:
        """Clase iterable que produce iteradores."""
        
        def __init__(self, inicio, fin):
            """Inicializa el rango."""
            self.inicio = inicio
            self.fin = fin
        
        def __iter__(self):
            """Retorna un nuevo iterador cada vez."""
            return Contador(self.inicio, self.fin)
    
    print("\n📌 Clase iterable (puede iterarse múltiples veces):")
    rango = Rango(1, 3)
    
    print("Primera iteración:")
    for num in rango:
        print(f"  {num}")
    
    print("Segunda iteración (funciona porque crea nuevo iterador):")
    for num in rango:
        print(f"  {num}")


def demo_generador_basico():
    """Demuestra generadores con yield."""
    seccion("GENERADORES CON YIELD")
    
    # Función generadora
    def contar(inicio, fin):
        """Generador que cuenta del inicio al fin."""
        actual = inicio
        while actual <= fin:
            yield actual
            actual += 1
    
    print("📌 Generador simple:")
    print("Función generadora:", contar)
    
    generador = contar(1, 5)
    print(f"Objeto generador: {generador}")
    print(f"Tipo: {type(generador)}")
    
    print("\nUsando next():")
    print(f"  {next(generador)}")
    print(f"  {next(generador)}")
    print(f"  {next(generador)}")
    
    print("\nUsando for para el resto:")
    for num in generador:
        print(f"  {num}")
    
    # Nuevo generador para demostrar que se pueden reutilizar
    print("\n📌 Nuevo generador:")
    for num in contar(10, 12):
        print(f"  {num}")


def demo_generador_vs_lista():
    """Demuestra diferencias entre generador y lista."""
    seccion("GENERADOR VS LISTA (MEMORIA)")
    
    # Lista - consume memoria
    def crear_lista(n):
        """Crea lista de cuadrados."""
        return [x**2 for x in range(n)]
    
    # Generador - no consume memoria por adelantado
    def crear_generador(n):
        """Genera cuadrados bajo demanda."""
        for x in range(n):
            yield x**2
    
    n = 1000000
    
    print(f"📌 Comparación con n={n:,}:")
    
    # Tamaño de lista
    lista = crear_lista(100)  # Menos elementos para no esperar mucho
    print(f"Lista (100 elementos): {sys.getsizeof(lista)} bytes")
    
    # Tamaño de generador
    generador = crear_generador(n)
    print(f"Generador: {sys.getsizeof(generador)} bytes")
    
    print("\n✅ Generador usa memoria constante, lista crece con n")
    
    # Usar generador
    print("\n📌 Primeros 10 valores del generador:")
    gen = crear_generador(100)
    for i, valor in enumerate(gen):
        if i >= 10:
            break
        print(f"  {valor}")


def demo_generador_fibonacci():
    """Demuestra generador de Fibonacci."""
    seccion("GENERADOR FIBONACCI")
    
    def fibonacci(limite=None):
        """
        Genera secuencia de Fibonacci.
        
        Args:
            limite: Cantidad de números a generar (None = infinito)
        """
        a, b = 0, 1
        contador = 0
        
        while limite is None or contador < limite:
            yield a
            a, b = b, a + b
            contador += 1
    
    print("📌 Primeros 10 números de Fibonacci:")
    for num in fibonacci(10):
        print(f"  {num}")
    
    print("\n📌 Fibonacci infinito (primeros 15):")
    gen_infinito = fibonacci()
    for i in range(15):
        print(f"  {next(gen_infinito)}")


def demo_generador_expresion():
    """Demuestra expresiones generadoras."""
    seccion("EXPRESIONES GENERADORAS")
    
    # Lista por comprensión
    print("📌 Lista por comprensión:")
    cuadrados_lista = [x**2 for x in range(10)]
    print(f"Tipo: {type(cuadrados_lista)}")
    print(f"Contenido: {cuadrados_lista}")
    print(f"Tamaño: {sys.getsizeof(cuadrados_lista)} bytes")
    
    # Expresión generadora (paréntesis en lugar de corchetes)
    print("\n📌 Expresión generadora:")
    cuadrados_gen = (x**2 for x in range(10))
    print(f"Tipo: {type(cuadrados_gen)}")
    print(f"Contenido: {cuadrados_gen}")
    print(f"Tamaño: {sys.getsizeof(cuadrados_gen)} bytes")
    
    print("\nIterando el generador:")
    for num in cuadrados_gen:
        print(f"  {num}")
    
    # Uso con funciones
    print("\n📌 Con sum():")
    suma = sum(x**2 for x in range(10))
    print(f"Suma de cuadrados 0-9: {suma}")
    
    print("\n📌 Con max():")
    maximo = max(x**2 for x in range(10))
    print(f"Máximo: {maximo}")


def demo_generador_send():
    """Demuestra método send() del generador."""
    seccion("MÉTODO SEND() DE GENERADORES")
    
    def eco():
        """Generador que hace eco de valores enviados."""
        print("  Generador iniciado")
        while True:
            valor = yield
            if valor is None:
                break
            print(f"  Eco: {valor}")
    
    print("📌 Generador bidireccional con send():")
    generador = eco()
    
    # Iniciar el generador
    next(generador)
    
    # Enviar valores
    generador.send("Hola")
    generador.send("Mundo")
    generador.send(42)
    generador.send(None)  # Finaliza
    
    # Generador contador mejorado
    def contador_avanzado():
        """Contador que puede recibir comandos."""
        total = 0
        while True:
            incremento = yield total
            if incremento is None:
                incremento = 1
            total += incremento
    
    print("\n📌 Contador con send():")
    contador = contador_avanzado()
    print(f"Inicio: {next(contador)}")
    print(f"Incrementar 1: {contador.send(1)}")
    print(f"Incrementar 5: {contador.send(5)}")
    print(f"Incrementar 10: {contador.send(10)}")
    print(f"Incrementar 1 (default): {next(contador)}")


def demo_generador_yield_from():
    """Demuestra yield from."""
    seccion("YIELD FROM")
    
    def generador1():
        """Primer generador."""
        yield 1
        yield 2
        yield 3
    
    def generador2():
        """Segundo generador."""
        yield 'a'
        yield 'b'
        yield 'c'
    
    # Sin yield from
    def combinar_manual():
        """Combina generadores manualmente."""
        for valor in generador1():
            yield valor
        for valor in generador2():
            yield valor
    
    print("📌 Sin yield from:")
    for valor in combinar_manual():
        print(f"  {valor}")
    
    # Con yield from
    def combinar_yield_from():
        """Combina generadores con yield from."""
        yield from generador1()
        yield from generador2()
    
    print("\n📌 Con yield from (más limpio):")
    for valor in combinar_yield_from():
        print(f"  {valor}")
    
    # Caso de uso: aplanar lista anidada
    def aplanar(lista):
        """Aplana lista recursivamente."""
        for elemento in lista:
            if isinstance(elemento, list):
                yield from aplanar(elemento)
            else:
                yield elemento
    
    print("\n📌 Aplanar lista anidada:")
    anidada = [1, [2, 3, [4, 5]], 6, [7, [8, 9]]]
    print(f"Original: {anidada}")
    plana = list(aplanar(anidada))
    print(f"Aplanada: {plana}")


def demo_pipeline_generadores():
    """Demuestra pipeline de generadores."""
    seccion("PIPELINE DE GENERADORES")
    
    def leer_numeros(datos):
        """Simula lectura de datos."""
        for linea in datos:
            yield int(linea)
    
    def filtrar_pares(numeros):
        """Filtra solo números pares."""
        for num in numeros:
            if num % 2 == 0:
                yield num
    
    def elevar_cuadrado(numeros):
        """Eleva al cuadrado."""
        for num in numeros:
            yield num ** 2
    
    def formatear(numeros):
        """Formatea para impresión."""
        for num in numeros:
            yield f"[{num}]"
    
    print("📌 Pipeline: leer -> filtrar pares -> cuadrado -> formatear:")
    
    datos = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    print(f"Datos originales: {datos}")
    
    # Crear pipeline
    pipeline = formatear(
        elevar_cuadrado(
            filtrar_pares(
                leer_numeros(datos)
            )
        )
    )
    
    print("\nResultado:")
    for resultado in pipeline:
        print(f"  {resultado}")
    
    print("\n✅ Cada etapa procesa bajo demanda (lazy evaluation)")


def demo_generador_infinito():
    """Demuestra generadores infinitos."""
    seccion("GENERADORES INFINITOS")
    
    def contador_infinito(inicio=0):
        """Contador que nunca termina."""
        n = inicio
        while True:
            yield n
            n += 1
    
    print("📌 Contador infinito (primeros 10):")
    contador = contador_infinito()
    for i in range(10):
        print(f"  {next(contador)}")
    
    # Ciclo infinito
    def ciclo(iterable):
        """Cicla infinitamente sobre un iterable."""
        while True:
            for elemento in iterable:
                yield elemento
    
    print("\n📌 Ciclo infinito (primeros 15):")
    colores = ['rojo', 'verde', 'azul']
    ciclo_colores = ciclo(colores)
    for i in range(15):
        print(f"  {next(ciclo_colores)}")


def ejercicio_practico():
    """Ejercicio práctico integrando conceptos."""
    seccion("EJERCICIO PRÁCTICO: Procesador de Logs")
    
    def leer_logs(archivo_simulado):
        """Simula lectura de archivo de logs."""
        for linea in archivo_simulado:
            yield linea.strip()
    
    def parsear_log(lineas):
        """Parsea líneas de log."""
        for linea in lineas:
            partes = linea.split('|')
            if len(partes) == 3:
                nivel, timestamp, mensaje = partes
                yield {
                    'nivel': nivel.strip(),
                    'timestamp': timestamp.strip(),
                    'mensaje': mensaje.strip()
                }
    
    def filtrar_errores(logs):
        """Filtra solo errores."""
        for log in logs:
            if log['nivel'] == 'ERROR':
                yield log
    
    def formatear_reporte(logs):
        """Formatea logs para reporte."""
        for log in logs:
            yield f"[{log['timestamp']}] {log['mensaje']}"
    
    print("📌 Sistema de procesamiento de logs:")
    
    # Datos de prueba
    logs_simulados = [
        "INFO | 2024-05-01 10:00:00 | Aplicación iniciada",
        "DEBUG | 2024-05-01 10:00:05 | Conectando a base de datos",
        "ERROR | 2024-05-01 10:00:10 | Conexión fallida",
        "INFO | 2024-05-01 10:00:15 | Reintentando conexión",
        "ERROR | 2024-05-01 10:00:20 | Timeout en operación",
        "INFO | 2024-05-01 10:00:25 | Conexión establecida",
    ]
    
    # Pipeline de procesamiento
    pipeline = formatear_reporte(
        filtrar_errores(
            parsear_log(
                leer_logs(logs_simulados)
            )
        )
    )
    
    print("Errores encontrados:")
    for error in pipeline:
        print(f"  🔴 {error}")
    
    print("\n✅ Pipeline eficiente: procesa bajo demanda, memoria constante")


def main():
    """Función principal."""
    print("\n" + "🐍" * 35)
    print("          GENERADORES E ITERADORES EN PYTHON")
    print("🐍" * 35)
    
    demo_protocolo_iterador()
    demo_clase_iterador()
    demo_generador_basico()
    demo_generador_vs_lista()
    demo_generador_fibonacci()
    demo_generador_expresion()
    demo_generador_send()
    demo_generador_yield_from()
    demo_pipeline_generadores()
    demo_generador_infinito()
    ejercicio_practico()
    
    print("\n" + "=" * 70)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("=" * 70)
    print("\n💡 Puntos clave:")
    print("   • Iterador: objeto con __iter__() y __next__()")
    print("   • Generador: función con yield (iterador automático)")
    print("   • Expresión generadora: (x for x in iterable)")
    print("   • Ventaja: memoria eficiente (lazy evaluation)")
    print("   • yield from: delega a otro generador")
    print("   • send(): comunicación bidireccional")
    print("   • Pipeline: combinar generadores para procesamiento")
    print("   • Ideal para archivos grandes y datos infinitos\n")


if __name__ == "__main__":
    main()
