"""
Módulo 2 - Ejemplo 3: Entrada y Salida de Datos
===============================================

Este script demuestra cómo trabajar con entrada (input)
y salida (print) de datos en Python.
"""


def seccion(titulo):
    """Helper para mostrar títulos de sección."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70 + "\n")


def demo_print_basico():
    """Demuestra uso básico de print()."""
    seccion("SALIDA: print() - Uso Básico")
    
    # Impresión simple
    print("Hola, Mundo!")
    
    # Múltiples valores
    nombre = "Juan"
    edad = 25
    print("Nombre:", nombre, "Edad:", edad)
    
    # Variables sin texto adicional
    x, y, z = 1, 2, 3
    print(x, y, z)
    
    # Diferentes tipos
    print("Entero:", 42, "Float:", 3.14, "Bool:", True, "None:", None)


def demo_print_parametros():
    """Demuestra parámetros de print()."""
    seccion("PARÁMETROS DE print()")
    
    print("📌 Parámetro sep (separador):")
    print("-" * 70)
    
    # Separador por defecto (espacio)
    print("uno", "dos", "tres")
    
    # Separador personalizado
    print("uno", "dos", "tres", sep="-")
    print("uno", "dos", "tres", sep=" | ")
    print("uno", "dos", "tres", sep="\n")  # Cada uno en línea diferente
    print("2026", "04", "10", sep="/")  # Fecha
    
    print("\n📌 Parámetro end (final de línea):")
    print("-" * 70)
    
    # Por defecto termina con \n (nueva línea)
    print("Primera línea")
    print("Segunda línea")
    
    # Cambiar el final
    print("En la misma línea", end=" ")
    print("continuación")
    
    # Sin salto de línea en bucle
    print("\nNúmeros del 0 al 9:", end=" ")
    for i in range(10):
        print(i, end=" ")
    print()  # Nueva línea al final
    
    # Puntos suspensivos para progreso
    print("\nCargando", end="")
    for _ in range(5):
        print(".", end="", flush=True)
        import time
        time.sleep(0.3)
    print(" ¡Listo!")
    
    print("\n📌 Combinando sep y end:")
    print("-" * 70)
    print("A", "B", "C", sep="-", end=" >>> ")
    print("X", "Y", "Z", sep="+")


def demo_print_formateo():
    """Demuestra formateo de strings para impresión."""
    seccion("FORMATEO DE STRINGS")
    
    nombre = "Ana"
    edad = 30
    altura = 1.65
    
    print("📌 f-strings (Python 3.6+) - RECOMENDADO:")
    print("-" * 70)
    
    # Básico
    print(f"Hola, soy {nombre} y tengo {edad} años")
    
    # Con expresiones
    print(f"El próximo año tendré {edad + 1} años")
    print(f"Mi nombre tiene {len(nombre)} letras")
    print(f"2 + 2 = {2 + 2}")
    
    # Llamadas a funciones
    print(f"Nombre en mayúsculas: {nombre.upper()}")
    
    # Formateo de números
    precio = 1234.56789
    print(f"\nFormato de números:")
    print(f"Precio: ${precio:.2f}")  # 2 decimales
    print(f"Precio: ${precio:,.2f}")  # Con separador de miles
    print(f"Precio: ${precio:>10.2f}")  # Alineado a derecha, ancho 10
    print(f"Precio: ${precio:<10.2f}")  # Alineado a izquierda
    print(f"Precio: ${precio:^10.2f}")  # Centrado
    
    # Porcentajes
    tasa = 0.755
    print(f"Tasa: {tasa:.1%}")  # 75.5%
    
    # Notación científica
    grande = 1234567890
    print(f"Número grande: {grande:.2e}")
    
    # Formato de fechas
    from datetime import datetime
    ahora = datetime.now()
    print(f"\nFecha y hora: {ahora:%Y-%m-%d %H:%M:%S}")
    print(f"Solo fecha: {ahora:%d/%m/%Y}")
    print(f"Solo hora: {ahora:%H:%M}")
    
    print("\n📌 str.format() - Método alternativo:")
    print("-" * 70)
    
    # Básico
    print("Hola, soy {} y tengo {} años".format(nombre, edad))
    
    # Con índices
    print("Hola, soy {0} y tengo {1} años. Me llamo {0}".format(nombre, edad))
    
    # Con nombres
    print("Hola, soy {n} y tengo {e} años".format(n=nombre, e=edad))
    
    # Formateo de números
    print("Altura: {:.2f}m".format(altura))
    print("Precio: ${:,.2f}".format(precio))
    
    print("\n📌 % (estilo antiguo):")
    print("-" * 70)
    
    print("Hola, soy %s y tengo %d años" % (nombre, edad))
    print("Altura: %.2fm" % altura)
    print("Precio: $%.2f" % precio)


def demo_print_especial():
    """Demuestra casos especiales de print."""
    seccion("CASOS ESPECIALES DE print()")
    
    print("📌 Imprimir caracteres especiales:")
    print("-" * 70)
    
    print("Línea 1\nLínea 2")  # Nueva línea
    print("Columna1\tColumna2\tColumna3")  # Tabulación
    print("Comillas: \"texto entre comillas\"")  # Comillas
    print("Apóstrofe: 'texto'")
    print("Barra invertida: \\")  # Backslash
    
    print("\n📌 Raw strings:")
    print("-" * 70)
    
    ruta = r"C:\Users\Juan\Desktop\archivo.txt"
    print(f"Ruta Windows: {ruta}")
    
    regex = r"\d{3}-\d{4}"
    print(f"Regex: {regex}")
    
    print("\n📌 Strings multilínea:")
    print("-" * 70)
    
    poema = """
    Roses are red,
    Violets are blue,
    Python is awesome,
    And so are you!
    """
    print(poema)
    
    # Con indentación controlada
    texto = """
    Primera línea
    Segunda línea
    Tercera línea
    """.strip()  # Remove leading/trailing whitespace
    print(texto)
    
    print("\n📌 Imprimir estructuras de datos:")
    print("-" * 70)
    
    lista = [1, 2, 3, 4, 5]
    diccionario = {'nombre': 'Juan', 'edad': 30}
    tupla = (10, 20, 30)
    
    print(f"Lista: {lista}")
    print(f"Diccionario: {diccionario}")
    print(f"Tupla: {tupla}")
    
    # Pretty print
    import pprint
    datos_complejos = {
        'usuarios': [
            {'nombre': 'Juan', 'edad': 30, 'ciudad': 'Madrid'},
            {'nombre': 'Ana', 'edad': 25, 'ciudad': 'Barcelona'}
        ],
        'configuracion': {
            'debug': True,
            'max_usuarios': 100
        }
    }
    
    print("\nDiccionario complejo (print normal):")
    print(datos_complejos)
    
    print("\nDiccionario complejo (pretty print):")
    pprint.pprint(datos_complejos, width=50, indent=2)


def demo_input_basico():
    """Demuestra uso básico de input()."""
    seccion("ENTRADA: input() - Uso Básico")
    
    print("La función input() siempre retorna una STRING\n")
    
    # Descomentar para probar interactivamente
    print("📌 Ejemplo básico (comentado para demo):")
    print("-" * 70)
    print("# nombre = input('¿Cuál es tu nombre? ')")
    print("# print(f'Hola, {nombre}!')")
    
    # Simular entrada
    nombre = "Usuario"  # En realidad vendría de input()
    print(f"\nSimulación: nombre = '{nombre}'")
    print(f"Salida: Hola, {nombre}!")
    
    print("\n📌 Input retorna string:")
    print("-" * 70)
    print("# edad_str = input('¿Cuántos años tienes? ')")
    print("# print(f'Tipo: {type(edad_str)}')")  # <class 'str'>
    edad_str = "25"  # Simular
    print(f"\nSimulación: edad_str = '{edad_str}'")
    print(f"Tipo: {type(edad_str)}")


def demo_input_conversion():
    """Demuestra conversión de input."""
    seccion("CONVERSIÓN DE input()")
    
    print("📌 Convertir a número:")
    print("-" * 70)
    
    # Simular entrada
    edad_str = "25"
    print(f"edad_str = '{edad_str}'  (tipo: {type(edad_str).__name__})")
    
    # Convertir a int
    edad = int(edad_str)
    print(f"edad = int(edad_str) = {edad}  (tipo: {type(edad).__name__})")
    
    # Ahora podemos hacer operaciones
    print(f"En 5 años tendrás {edad + 5} años")
    
    print("\n📌 En una línea:")
    print("-" * 70)
    print("# edad = int(input('¿Cuántos años tienes? '))")
    
    print("\n📌 Convertir a float:")
    print("-" * 70)
    altura_str = "1.75"
    altura = float(altura_str)
    print(f"altura_str = '{altura_str}'")
    print(f"altura = float(altura_str) = {altura}")
    print(f"Tipo: {type(altura)}")


def demo_input_validacion():
    """Demuestra validación de input."""
    seccion("VALIDACIÓN DE input()")
    
    print("📌 Problema: input inválido causa errores")
    print("-" * 70)
    
    print("# edad = int(input('Edad: '))")
    print("# Si el usuario ingresa 'abc', obtendrás ValueError\n")
    
    print("📌 Solución 1: Try-except")
    print("-" * 70)
    
    print("""
def obtener_edad():
    while True:
        try:
            edad = int(input('¿Cuántos años tienes? '))
            if edad > 0:
                return edad
            else:
                print('La edad debe ser positiva')
        except ValueError:
            print('Por favor, ingresa un número válido')
    """)
    
    print("\n📌 Solución 2: Validar con métodos de string")
    print("-" * 70)
    
    print("""
def obtener_edad_v2():
    while True:
        edad_str = input('¿Cuántos años tienes? ')
        if edad_str.isdigit():
            edad = int(edad_str)
            if edad > 0:
                return edad
        print('Por favor, ingresa un número positivo válido')
    """)
    
    print("\n📌 Ejemplo funcional con validación:")
    print("-" * 70)
    
    # Simulación de validación
    entradas_simuladas = ['abc', '-5', '0', '25']
    print("Entradas simuladas:", entradas_simuladas)
    
    for entrada in entradas_simuladas:
        print(f"\nProcesando: '{entrada}'")
        try:
            edad = int(entrada)
            if edad > 0:
                print(f"  ✓ Edad válida: {edad}")
                break
            else:
                print("  ✗ La edad debe ser positiva")
        except ValueError:
            print("  ✗ No es un número válido")


def demo_input_multiple():
    """Demuestra entrada de múltiples valores."""
    seccion("ENTRADA DE MÚLTIPLES VALORES")
    
    print("📌 Método 1: Una línea con split()")
    print("-" * 70)
    
    print("# entrada = input('Ingresa tres números separados por espacio: ')")
    print("# numeros = entrada.split()")
    print("# a, b, c = numeros")
    
    # Simular
    entrada = "10 20 30"
    print(f"\nSimulación: entrada = '{entrada}'")
    numeros = entrada.split()
    print(f"numeros = {numeros}")
    a, b, c = numeros
    print(f"a={a}, b={b}, c={c}")
    
    # Convertir a enteros
    a, b, c = map(int, numeros)
    print(f"\nDespués de map(int, numeros):")
    print(f"a={a}, b={b}, c={c}")
    
    print("\n📌 Método 2: split con separador personalizado")
    print("-" * 70)
    
    entrada = "Juan,30,Madrid"
    print(f"entrada = '{entrada}'")
    nombre, edad, ciudad = entrada.split(',')
    print(f"nombre='{nombre}', edad='{edad}', ciudad='{ciudad}'")
    
    # Limpiar espacios
    nombre = nombre.strip()
    edad = int(edad.strip())
    ciudad = ciudad.strip()
    print(f"\nDespués de strip() y conversión:")
    print(f"nombre='{nombre}', edad={edad}, ciudad='{ciudad}'")
    
    print("\n📌 Método 3: List comprehension")
    print("-" * 70)
    
    entrada = "1 2 3 4 5"
    print(f"entrada = '{entrada}'")
    numeros = [int(x) for x in entrada.split()]
    print(f"numeros = {numeros}")
    print(f"Suma: {sum(numeros)}")


def demo_formateo_avanzado():
    """Demuestra formateo avanzado de salida."""
    seccion("FORMATEO AVANZADO")
    
    print("📌 Tabla con formato:")
    print("-" * 70)
    
    productos = [
        ('Laptop', 999.99, 5),
        ('Mouse', 25.50, 50),
        ('Teclado', 75.00, 30),
        ('Monitor', 299.99, 15)
    ]
    
    # Encabezado
    print(f"{'Producto':<15} {'Precio':>10} {'Stock':>8}")
    print("-" * 70)
    
    # Datos
    for nombre, precio, stock in productos:
        print(f"{nombre:<15} ${precio:>9.2f} {stock:>8}")
    
    # Total
    total_stock = sum(stock for _, _, stock in productos)
    valor_total = sum(precio * stock for _, precio, stock in productos)
    print("-" * 70)
    print(f"{'TOTALES':<15} ${valor_total:>9.2f} {total_stock:>8}")
    
    print("\n📌 Barra de progreso:")
    print("-" * 70)
    
    total = 100
    for i in range(0, 101, 20):
        porcentaje = i / total
        barra_length = 30
        filled = int(barra_length * porcentaje)
        barra = '█' * filled + '░' * (barra_length - filled)
        print(f"\r[{barra}] {i}%", end='', flush=True)
        import time
        time.sleep(0.3)
    print()  # Nueva línea al final
    
    print("\n📌 Alineación y relleno:")
    print("-" * 70)
    
    texto = "Python"
    numero = 42
    
    print(f"'{texto:<10}'  ← Izquierda (ancho 10)")
    print(f"'{texto:>10}'  ← Derecha")
    print(f"'{texto:^10}'  ← Centrado")
    print(f"'{texto:*<10}' ← Relleno con *")
    print(f"'{texto:*>10}' ← Relleno derecha")
    print(f"'{texto:*^10}' ← Relleno centrado")
    print(f"'{numero:05d}'    ← Relleno con ceros")


def ejercicios_practicos():
    """Ejercicios prácticos."""
    seccion("EJERCICIO PRÁCTICO: Calculadora de IMC")
    
    print("Simulación de calculadora de IMC (Índice de Masa Corporal)\n")
    
    # Simular entrada
    peso = 70  # kg
    altura = 1.75  # metros
    
    print(f"Peso: {peso} kg")
    print(f"Altura: {altura} m")
    
    # Calcular IMC
    imc = peso / (altura ** 2)
    
    print(f"\nTu IMC es: {imc:.2f}")
    
    # Clasificación
    if imc < 18.5:
        clasificacion = "Bajo peso"
    elif imc < 25:
        clasificacion = "Peso normal"
    elif imc < 30:
        clasificacion = "Sobrepeso"
    else:
        clasificacion = "Obesidad"
    
    print(f"Clasificación: {clasificacion}")
    
    # Mostrar tabla de referencia
    print("\n📊 Tabla de referencia:")
    print("-" * 40)
    print(f"{'Clasificación':<20} {'IMC':>15}")
    print("-" * 40)
    print(f"{'Bajo peso':<20} {'< 18.5':>15}")
    print(f"{'Normal':<20} {'18.5 - 24.9':>15}")
    print(f"{'Sobrepeso':<20} {'25.0 - 29.9':>15}")
    print(f"{'Obesidad':<20} {'≥ 30.0':>15}")
    print("-" * 40)


def main():
    """Función principal."""
    print("\n" + "🐍" * 35)
    print("       ENTRADA Y SALIDA DE DATOS EN PYTHON")
    print("🐍" * 35)
    
    demo_print_basico()
    demo_print_parametros()
    demo_print_formateo()
    demo_print_especial()
    demo_input_basico()
    demo_input_conversion()
    demo_input_validacion()
    demo_input_multiple()
    demo_formateo_avanzado()
    ejercicios_practicos()
    
    print("\n" + "=" * 70)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("=" * 70)
    print("\n💡 Puntos clave:")
    print("   • print() muestra información en consola")
    print("   • input() siempre retorna string")
    print("   • Usa f-strings para formateo moderno: f'...'")
    print("   • Valida input antes de convertir")
    print("   • sep= y end= personalizan print()")
    print("   • Formateo avanzado: {variable:formato}\n")


if __name__ == "__main__":
    main()
