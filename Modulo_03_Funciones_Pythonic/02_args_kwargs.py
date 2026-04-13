"""
Módulo 3 - Ejemplo 2: *args y **kwargs
======================================

Este script demuestra el uso de *args (argumentos posicionales variables)
y **kwargs (argumentos nombrados variables) en Python.
"""


def seccion(titulo):
    """Helper para mostrar títulos de sección."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70 + "\n")


def demo_args_basico():
    """Demuestra el uso básico de *args."""
    seccion("*ARGS - ARGUMENTOS POSICIONALES VARIABLES")
    
    # Sin *args - limitado
    def suma_dos(a, b):
        """Suma exactamente dos números."""
        return a + b
    
    print("📌 Sin *args (solo 2 números):")
    print(f"suma_dos(1, 2) = {suma_dos(1, 2)}")
    # print(suma_dos(1, 2, 3))  # Error: demasiados argumentos
    
    # Con *args - flexible
    def suma(*numeros):
        """Suma cualquier cantidad de números."""
        total = 0
        for num in numeros:
            total += num
        return total
    
    print("\n📌 Con *args (cantidad variable):")
    print(f"suma() = {suma()}")
    print(f"suma(1) = {suma(1)}")
    print(f"suma(1, 2) = {suma(1, 2)}")
    print(f"suma(1, 2, 3) = {suma(1, 2, 3)}")
    print(f"suma(1, 2, 3, 4, 5) = {suma(1, 2, 3, 4, 5)}")
    
    # *args es una tupla
    def mostrar_args(*args):
        """Muestra el tipo y contenido de args."""
        print(f"  Tipo: {type(args)}")
        print(f"  Contenido: {args}")
        print(f"  Longitud: {len(args)}")
    
    print("\n📌 *args es una tupla:")
    mostrar_args(1, 2, 3, "hola", True)


def demo_args_con_parametros():
    """Demuestra *args combinado con parámetros normales."""
    seccion("*ARGS CON PARÁMETROS NORMALES")
    
    def saludar(saludo, *nombres):
        """Saluda a múltiples personas con el mismo saludo."""
        for nombre in nombres:
            print(f"{saludo}, {nombre}!")
    
    print("📌 Parámetro fijo + *args:")
    saludar("Hola", "Ana", "Juan", "María")
    
    print()
    saludar("Buenos días", "Carlos", "Laura")
    
    # Múltiples parámetros fijos + *args
    def crear_mensaje(titulo, separador='=', *lineas):
        """Crea un mensaje formateado."""
        borde = separador * 50
        print(borde)
        print(f"  {titulo}")
        print(borde)
        for linea in lineas:
            print(f"• {linea}")
    
    print("\n📌 Múltiples parámetros + *args:")
    crear_mensaje(
        "Lista de Tareas",
        lineas=[
            "Completar laboratorio",
            "Estudiar decoradores",
            "Practicar generadores"
        ]
    )


def demo_kwargs_basico():
    """Demuestra el uso básico de **kwargs."""
    seccion("**KWARGS - ARGUMENTOS NOMBRADOS VARIABLES")
    
    def mostrar_info(**info):
        """Muestra información usando **kwargs."""
        print("Información recibida:")
        for clave, valor in info.items():
            print(f"  {clave}: {valor}")
    
    print("📌 **kwargs básico:")
    mostrar_info(nombre="Ana", edad=25, ciudad="Madrid")
    
    print("\n📌 Número variable de kwargs:")
    mostrar_info(producto="Laptop", precio=999, stock=15, marca="Dell")
    
    # **kwargs es un diccionario
    def tipo_kwargs(**kwargs):
        """Muestra el tipo de kwargs."""
        print(f"Tipo: {type(kwargs)}")
        print(f"Contenido: {kwargs}")
    
    print("\n📌 **kwargs es un diccionario:")
    tipo_kwargs(a=1, b=2, c=3)


def demo_kwargs_con_parametros():
    """Demuestra **kwargs combinado con parámetros normales."""
    seccion("**KWARGS CON PARÁMETROS NORMALES")
    
    def crear_usuario(nombre, **atributos):
        """Crea un usuario con atributos opcionales."""
        usuario = {'nombre': nombre}
        usuario.update(atributos)
        return usuario
    
    print("📌 Parámetro fijo + **kwargs:")
    usuario1 = crear_usuario("Ana", edad=25, ciudad="Madrid", activo=True)
    print(usuario1)
    
    usuario2 = crear_usuario("Juan", edad=30, rol="admin")
    print(usuario2)
    
    # Con valores por defecto
    def configurar(modo="produccion", debug=False, **opciones):
        """Configura la aplicación."""
        config = {
            'modo': modo,
            'debug': debug
        }
        config.update(opciones)
        return config
    
    print("\n📌 Parámetros con default + **kwargs:")
    config1 = configurar(puerto=8000, host="localhost")
    print(config1)
    
    config2 = configurar("desarrollo", debug=True, puerto=3000, auto_reload=True)
    print(config2)


def demo_args_y_kwargs():
    """Demuestra *args y **kwargs juntos."""
    seccion("*ARGS Y **KWARGS JUNTOS")
    
    def funcion_completa(a, b, *args, **kwargs):
        """Función que acepta todo tipo de argumentos."""
        print(f"Parámetro a: {a}")
        print(f"Parámetro b: {b}")
        print(f"Args: {args}")
        print(f"Kwargs: {kwargs}")
    
    print("📌 Función con todos los tipos de parámetros:")
    funcion_completa(1, 2, 3, 4, 5, x=10, y=20, z=30)
    
    # Orden importante
    def ejemplo_orden(a, b=2, *args, c, d=4, **kwargs):
        """Muestra el orden correcto de parámetros."""
        print(f"a={a}, b={b}, c={c}, d={d}")
        print(f"args={args}, kwargs={kwargs}")
    
    print("\n📌 Orden correcto de parámetros:")
    ejemplo_orden(1, 10, 20, 30, c=3, d=40, x=100, y=200)


def demo_desempaquetado():
    """Demuestra desempaquetado con * y **."""
    seccion("DESEMPAQUETADO CON * Y **")
    
    def suma(a, b, c):
        """Suma tres números."""
        return a + b + c
    
    # Desempaquetar lista/tupla con *
    print("📌 Desempaquetar secuencia con *:")
    numeros = [1, 2, 3]
    resultado = suma(*numeros)  # Equivale a suma(1, 2, 3)
    print(f"suma(*{numeros}) = {resultado}")
    
    tupla = (5, 10, 15)
    resultado = suma(*tupla)
    print(f"suma(*{tupla}) = {resultado}")
    
    # Desempaquetar diccionario con **
    def saludar(nombre, edad, ciudad):
        """Crea un saludo personalizado."""
        return f"{nombre} ({edad}) de {ciudad}"
    
    print("\n📌 Desempaquetar diccionario con **:")
    datos = {'nombre': 'Ana', 'edad': 25, 'ciudad': 'Madrid'}
    mensaje = saludar(**datos)  # Equivale a saludar(nombre='Ana', edad=25, ciudad='Madrid')
    print(mensaje)
    
    # Mezclar desempaquetado
    print("\n📌 Mezclar empaquetado y desempaquetado:")
    
    def funcion(*args, **kwargs):
        """Recibe y muestra todo."""
        print(f"  args: {args}")
        print(f"  kwargs: {kwargs}")
    
    lista_args = [1, 2, 3]
    dict_kwargs = {'x': 10, 'y': 20}
    
    funcion(*lista_args, **dict_kwargs)


def demo_desempaquetado_avanzado():
    """Demuestra técnicas avanzadas de desempaquetado."""
    seccion("DESEMPAQUETADO AVANZADO")
    
    # Desempaquetar en asignación
    print("📌 Desempaquetar en asignación:")
    valores = [1, 2, 3, 4, 5]
    primero, *resto = valores
    print(f"primero={primero}, resto={resto}")
    
    *inicio, ultimo = valores
    print(f"inicio={inicio}, ultimo={ultimo}")
    
    primero, *medio, ultimo = valores
    print(f"primero={primero}, medio={medio}, ultimo={ultimo}")
    
    # Combinar listas
    print("\n📌 Combinar listas con *:")
    lista1 = [1, 2, 3]
    lista2 = [4, 5, 6]
    combinada = [*lista1, *lista2]
    print(f"{lista1} + {lista2} = {combinada}")
    
    # Combinar diccionarios
    print("\n📌 Combinar diccionarios con **:")
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'c': 3, 'd': 4}
    combinado = {**dict1, **dict2}
    print(f"{dict1} + {dict2} = {combinado}")
    
    # Sobreescribir valores
    dict3 = {'a': 1, 'b': 2}
    dict4 = {'b': 10, 'c': 3}
    combinado = {**dict3, **dict4}  # 'b' se sobreescribe
    print(f"\nSobreescritura: {dict3} + {dict4} = {combinado}")


def demo_casos_uso():
    """Demuestra casos de uso prácticos."""
    seccion("CASOS DE USO PRÁCTICOS")
    
    # Logging flexible
    def log(nivel, mensaje, **contexto):
        """Sistema de logging simple."""
        print(f"[{nivel}] {mensaje}")
        if contexto:
            print(f"  Contexto: {contexto}")
    
    print("📌 Sistema de logging:")
    log("INFO", "Aplicación iniciada")
    log("ERROR", "Conexión fallida", host="localhost", puerto=5432, intentos=3)
    log("WARNING", "Uso alto de memoria", uso_mb=512, limite_mb=1024)
    
    # API wrapper
    def api_request(endpoint, method="GET", **params):
        """Simula petición API."""
        print(f"\n{method} {endpoint}")
        if params:
            print(f"Parámetros: {params}")
        return {"status": 200, "data": "Respuesta simulada"}
    
    print("\n📌 API Wrapper:")
    api_request("/users", usuario_id=123, incluir="perfil")
    api_request("/posts", method="POST", titulo="Nuevo Post", contenido="...")
    
    # Constructor flexible
    def crear_configuracion(*rutas, **opciones):
        """Crea configuración con rutas y opciones."""
        config = {
            'rutas': list(rutas),
            'opciones': opciones
        }
        return config
    
    print("\n📌 Constructor flexible:")
    config = crear_configuracion(
        '/home',
        '/dashboard',
        '/perfil',
        debug=True,
        cache=False,
        timeout=30
    )
    print(config)


def ejercicio_practico():
    """Ejercicio práctico integrando conceptos."""
    seccion("EJERCICIO PRÁCTICO: Sistema de Notificaciones")
    
    def notificar(destinatario, *destinatarios_adicionales, asunto, **metadatos):
        """
        Envía notificación a uno o más destinatarios.
        
        Args:
            destinatario: Destinatario principal
            *destinatarios_adicionales: Destinatarios opcionales
            asunto: Asunto de la notificación (keyword-only)
            **metadatos: Información adicional
        """
        todos_destinatarios = [destinatario] + list(destinatarios_adicionales)
        
        print("📧 NOTIFICACIÓN")
        print(f"Para: {', '.join(todos_destinatarios)}")
        print(f"Asunto: {asunto}")
        
        if metadatos:
            print("Metadatos:")
            for clave, valor in metadatos.items():
                print(f"  {clave}: {valor}")
        print()
    
    print("📌 Sistema de notificaciones:")
    notificar(
        "ana@example.com",
        asunto="Bienvenida",
        prioridad="alta",
        categoria="usuario"
    )
    
    notificar(
        "juan@example.com",
        "maria@example.com",
        "carlos@example.com",
        asunto="Reunión de equipo",
        fecha="2024-05-15",
        hora="15:00",
        ubicacion="Sala 3"
    )


def main():
    """Función principal."""
    print("\n" + "🐍" * 35)
    print("          *ARGS Y **KWARGS EN PYTHON")
    print("🐍" * 35)
    
    demo_args_basico()
    demo_args_con_parametros()
    demo_kwargs_basico()
    demo_kwargs_con_parametros()
    demo_args_y_kwargs()
    demo_desempaquetado()
    demo_desempaquetado_avanzado()
    demo_casos_uso()
    ejercicio_practico()
    
    print("\n" + "=" * 70)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("=" * 70)
    print("\n💡 Puntos clave:")
    print("   • *args: número variable de argumentos posicionales (tupla)")
    print("   • **kwargs: número variable de argumentos nombrados (dict)")
    print("   • Orden: normales, *args, keyword-only, **kwargs")
    print("   • * desempaqueta secuencias, ** desempaqueta diccionarios")
    print("   • Útil para APIs flexibles y wrappers")
    print("   • Permite crear funciones muy genéricas\n")


if __name__ == "__main__":
    main()
