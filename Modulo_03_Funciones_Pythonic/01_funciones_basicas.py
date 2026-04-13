"""
Módulo 3 - Ejemplo 1: Funciones Básicas en Python
=================================================

Este script demuestra los fundamentos de las funciones en Python.
"""


def seccion(titulo):
    """Helper para mostrar títulos de sección."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70 + "\n")


def demo_funciones_basicas():
    """Demuestra funciones básicas."""
    seccion("FUNCIONES BÁSICAS")
    
    # Función simple
    def saludar():
        """Saluda al mundo."""
        print("¡Hola, Mundo!")
    
    print("📌 Función sin parámetros ni retorno:")
    saludar()
    
    # Función con parámetro
    def saludar_persona(nombre):
        """Saluda a una persona específica."""
        print(f"¡Hola, {nombre}!")
    
    print("\n📌 Función con un parámetro:")
    saludar_persona("Ana")
    saludar_persona("Juan")
    
    # Función con return
    def suma(a, b):
        """Suma dos números y retorna el resultado."""
        resultado = a + b
        return resultado
    
    print("\n📌 Función con return:")
    resultado = suma(5, 3)
    print(f"5 + 3 = {resultado}")
    
    # Sin return explícito
    def funcion_sin_return():
        """Esta función no tiene return explícito."""
        x = 10
        # No hay return
    
    print("\n📌 Función sin return (retorna None):")
    resultado = funcion_sin_return()
    print(f"Resultado: {resultado}")
    print(f"Tipo: {type(resultado)}")


def demo_multiples_parametros():
    """Demuestra funciones con múltiples parámetros."""
    seccion("MÚLTIPLES PARÁMETROS")
    
    def informacion_persona(nombre, edad, ciudad):
        """Crea mensaje con información personal."""
        return f"{nombre} tiene {edad} años y vive en {ciudad}"
    
    print("📌 Función con 3 parámetros:")
    mensaje = informacion_persona("Carlos", 28, "Madrid")
    print(mensaje)
    
    # Argumentos posicionales
    print("\n📌 Argumentos posicionales:")
    print(informacion_persona("Laura", 25, "Barcelona"))
    
    # Argumentos por nombre (keyword arguments)
    print("\n📌 Argumentos por nombre:")
    print(informacion_persona(nombre="Pedro", edad=30, ciudad="Valencia"))
    print(informacion_persona(ciudad="Sevilla", nombre="María", edad=27))


def demo_valores_por_defecto():
    """Demuestra parámetros con valores por defecto."""
    seccion("VALORES POR DEFECTO")
    
    def saludar(nombre, saludo="Hola", simbolo="!"):
        """Saluda con valores por defecto."""
        return f"{saludo}, {nombre}{simbolo}"
    
    print("📌 Usando todos los valores por defecto:")
    print(saludar("Ana"))  # Hola, Ana!
    
    print("\n📌 Sobreescribiendo el saludo:")
    print(saludar("Ana", "Buenos días"))  # Buenos días, Ana!
    
    print("\n📌 Sobreescribiendo el símbolo:")
    print(saludar("Ana", simbolo="?"))  # Hola, Ana?
    
    print("\n📌 Sobreescribiendo todo:")
    print(saludar("Ana", "Hey", "..."))  # Hey, Ana...
    
    # Función con varios defaults
    def crear_usuario(nombre, edad=18, activo=True, rol="usuario"):
        """Crea un usuario con configuración por defecto."""
        return {
            'nombre': nombre,
            'edad': edad,
            'activo': activo,
            'rol': rol
        }
    
    print("\n📌 Usuario con defaults:")
    usuario1 = crear_usuario("Juan")
    print(usuario1)
    
    print("\n📌 Usuario personalizado:")
    usuario2 = crear_usuario("Ana", edad=25, rol="admin")
    print(usuario2)


def demo_retorno_multiple():
    """Demuestra funciones que retornan múltiples valores."""
    seccion("RETORNO DE MÚLTIPLES VALORES")
    
    def operaciones_basicas(a, b):
        """Realiza operaciones básicas y retorna todos los resultados."""
        suma = a + b
        resta = a - b
        multiplicacion = a * b
        division = a / b if b != 0 else None
        return suma, resta, multiplicacion, division
    
    print("📌 Función que retorna tupla:")
    a, b = 10, 5
    print(f"Números: {a}, {b}")
    
    # Desempaquetar en variables
    suma, resta, mult, div = operaciones_basicas(a, b)
    print(f"Suma: {suma}")
    print(f"Resta: {resta}")
    print(f"Multiplicación: {mult}")
    print(f"División: {div}")
    
    # Obtener como tupla
    print("\n📌 Como tupla:")
    resultados = operaciones_basicas(a, b)
    print(f"Tipo: {type(resultados)}")
    print(f"Resultados: {resultados}")
    
    # Desempaquetar parcialmente
    print("\n📌 Desempaquetado parcial:")
    s, r, *resto = operaciones_basicas(a, b)
    print(f"Suma: {s}, Resta: {r}, Resto: {resto}")


def demo_docstrings():
    """Demuestra el uso de docstrings."""
    seccion("DOCSTRINGS (Documentación)")
    
    def calcular_area_rectangulo(base, altura):
        """
        Calcula el área de un rectángulo.
        
        Args:
            base (float): Base del rectángulo
            altura (float): Altura del rectángulo
        
        Returns:
            float: Área del rectángulo (base * altura)
        
        Example:
            >>> calcular_area_rectangulo(5, 10)
            50.0
        """
        return base * altura
    
    print("📌 Función con docstring:")
    area = calcular_area_rectangulo(5, 10)
    print(f"Área: {area}")
    
    print("\n📌 Acceder al docstring:")
    print(f"Nombre: {calcular_area_rectangulo.__name__}")
    print(f"\nDocstring:\n{calcular_area_rectangulo.__doc__}")
    
    # help() también muestra el docstring
    print("\n📌 Usando help():")
    help(calcular_area_rectangulo)


def demo_scope():
    """Demuestra el scope (ámbito) de variables."""
    seccion("SCOPE (ÁMBITO DE VARIABLES)")
    
    # Variable global
    x = 10
    print(f"📌 Variable global x = {x}")
    
    def funcion_local():
        """Función con variable local."""
        y = 5  # Variable local
        print(f"  Dentro de la función: x = {x}, y = {y}")
    
    print("\n📌 Acceso a variable global desde función:")
    funcion_local()
    
    print(f"\n📌 Variable local no existe fuera:")
    print(f"x = {x}")
    # print(f"y = {y}")  # Esto daría error
    
    # Variable local con mismo nombre
    def funcion_sombra():
        """Función con variable local que 'sombrea' la global."""
        x = 20  # Variable local, diferente de la global
        print(f"  Dentro: x = {x}")
    
    print("\n📌 Variable local 'sombrea' global:")
    funcion_sombra()
    print(f"Fuera: x = {x}")  # La global no cambia
    
    # Modificar variable global
    def modificar_global():
        """Modifica variable global usando 'global'."""
        global x
        x = 30
        print(f"  Modificando global: x = {x}")
    
    print("\n📌 Modificar variable global con 'global':")
    print(f"Antes: x = {x}")
    modificar_global()
    print(f"Después: x = {x}")


def demo_funciones_como_objetos():
    """Demuestra que las funciones son objetos de primera clase."""
    seccion("FUNCIONES COMO OBJETOS")
    
    def saludar(nombre):
        """Función de saludo."""
        return f"Hola, {nombre}!"
    
    def despedir(nombre):
        """Función de despedida."""
        return f"Adiós, {nombre}!"
    
    print("📌 Asignar función a variable:")
    mi_funcion = saludar
    print(mi_funcion("Juan"))  # Hola, Juan!
    
    print("\n📌 Funciones en estructuras de datos:")
    funciones = [saludar, despedir]
    for func in funciones:
        print(f"  {func.__name__}: {func('Ana')}")
    
    # Diccionario de funciones
    operaciones = {
        'saludar': saludar,
        'despedir': despedir
    }
    
    print("\n📌 Diccionario de funciones:")
    for nombre, func in operaciones.items():
        print(f"  {nombre}: {func('Carlos')}")
    
    # Función como argumento
    def ejecutar_dos_veces(funcion, argumento):
        """Ejecuta una función dos veces."""
        print(f"  Primera: {funcion(argumento)}")
        print(f"  Segunda: {funcion(argumento)}")
    
    print("\n📌 Pasar función como argumento:")
    ejecutar_dos_veces(saludar, "María")


def demo_funciones_anidadas():
    """Demuestra funciones anidadas."""
    seccion("FUNCIONES ANIDADAS")
    
    def exterior(x):
        """Función exterior."""
        print(f"📌 En función exterior, x = {x}")
        
        def interior(y):
            """Función interior (anidada)."""
            print(f"  En función interior, x = {x}, y = {y}")
            return x + y
        
        resultado = interior(5)
        print(f"  Resultado de interior: {resultado}")
        return resultado
    
    print("Llamando a función exterior:")
    resultado = exterior(10)
    print(f"Resultado final: {resultado}")
    
    # Las funciones interiores no son accesibles desde fuera
    # interior(5)  # Esto daría error


def ejercicio_practico():
    """Ejercicio práctico integrando conceptos."""
    seccion("EJERCICIO PRÁCTICO: Calculadora")
    
    def calculadora(operacion, a, b):
        """
        Calculadora simple.
        
        Args:
            operacion (str): 'suma', 'resta', 'multiplicacion', 'division'
            a (float): Primer número
            b (float): Segundo número
        
        Returns:
            float: Resultado de la operación
        """
        if operacion == 'suma':
            return a + b
        elif operacion == 'resta':
            return a - b
        elif operacion == 'multiplicacion':
            return a * b
        elif operacion == 'division':
            if b == 0:
                return "Error: División por cero"
            return a / b
        else:
            return "Operación no válida"
    
    print("📌 Usando la calculadora:")
    print(f"10 + 5 = {calculadora('suma', 10, 5)}")
    print(f"10 - 5 = {calculadora('resta', 10, 5)}")
    print(f"10 * 5 = {calculadora('multiplicacion', 10, 5)}")
    print(f"10 / 5 = {calculadora('division', 10, 5)}")
    print(f"10 / 0 = {calculadora('division', 10, 0)}")


def main():
    """Función principal."""
    print("\n" + "🐍" * 35)
    print("          FUNCIONES BÁSICAS EN PYTHON")
    print("🐍" * 35)
    
    demo_funciones_basicas()
    demo_multiples_parametros()
    demo_valores_por_defecto()
    demo_retorno_multiple()
    demo_docstrings()
    demo_scope()
    demo_funciones_como_objetos()
    demo_funciones_anidadas()
    ejercicio_practico()
    
    print("\n" + "=" * 70)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("=" * 70)
    print("\n💡 Puntos clave:")
    print("   • Las funciones encapsulan código reutilizable")
    print("   • Usa def para definir funciones")
    print("   • return devuelve valores (opcional)")
    print("   • Los parámetros pueden tener valores por defecto")
    print("   • Puedes retornar múltiples valores (tupla)")
    print("   • Usa docstrings para documentar")
    print("   • Scope: local vs global")
    print("   • Las funciones son objetos de primera clase\n")


if __name__ == "__main__":
    main()
