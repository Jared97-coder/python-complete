"""
Módulo 1 - Ejercicio 1: Verificar Instalación de Python
=========================================================

Este script verifica que Python está correctamente instalado
y muestra información sobre la instalación.
"""

import sys
import platform
import os

def mostrar_info_python():
    """Muestra información detallada sobre la instalación de Python."""
    
    print("=" * 60)
    print("INFORMACIÓN DE INSTALACIÓN DE PYTHON")
    print("=" * 60)
    
    # Versión de Python
    print(f"\n📌 Versión de Python: {sys.version}")
    print(f"📌 Versión corta: {platform.python_version()}")
    
    # Información de la implementación
    print(f"\n📌 Implementación: {platform.python_implementation()}")
    print(f"📌 Compilador: {platform.python_compiler()}")
    
    # Ubicación del ejecutable
    print(f"\n📌 Ubicación de Python: {sys.executable}")
    print(f"📌 Prefijo de instalación: {sys.prefix}")
    
    # Sistema operativo
    print(f"\n📌 Sistema Operativo: {platform.system()}")
    print(f"📌 Versión del SO: {platform.version()}")
    print(f"📌 Arquitectura: {platform.machine()}")
    
    # Rutas de búsqueda de módulos
    print(f"\n📌 Rutas de búsqueda de módulos (sys.path):")
    for i, path in enumerate(sys.path, 1):
        print(f"   {i}. {path}")
    
    # Variables de entorno relacionadas
    print(f"\n📌 Variables de entorno de Python:")
    python_env_vars = {k: v for k, v in os.environ.items() if 'PYTHON' in k.upper()}
    if python_env_vars:
        for key, value in python_env_vars.items():
            print(f"   {key} = {value}")
    else:
        print("   No se encontraron variables PYTHON específicas")
    
    print("\n" + "=" * 60)
    print("✅ Python está correctamente instalado y funcionando!")
    print("=" * 60)


def verificar_pip():
    """Verifica que pip está instalado."""
    
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DE PIP")
    print("=" * 60)
    
    try:
        import pip
        print(f"\n✅ pip está instalado")
        print(f"📌 Versión: {pip.__version__}")
        print(f"📌 Ubicación: {pip.__file__}")
    except ImportError:
        print("\n⚠️  pip NO está instalado")
        print("   Instálalo con: python -m ensurepip --upgrade")
    
    print("=" * 60)


def verificar_modulos_estandar():
    """Verifica algunos módulos de la biblioteca estándar."""
    
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DE MÓDULOS ESTÁNDAR")
    print("=" * 60)
    
    modulos_comunes = [
        'os', 'sys', 'json', 'datetime', 'math', 'random',
        'collections', 're', 'urllib', 'pathlib'
    ]
    
    print("\nVerificando módulos de la biblioteca estándar:\n")
    
    for modulo in modulos_comunes:
        try:
            __import__(modulo)
            print(f"✅ {modulo:15} - Disponible")
        except ImportError:
            print(f"❌ {modulo:15} - NO disponible")
    
    print("\n" + "=" * 60)


def ejecutar_prueba_basica():
    """Ejecuta una prueba básica de código Python."""
    
    print("\n" + "=" * 60)
    print("PRUEBA BÁSICA DE FUNCIONALIDAD")
    print("=" * 60)
    
    # Operaciones matemáticas
    resultado = 2 + 2
    print(f"\n✅ Operación matemática: 2 + 2 = {resultado}")
    
    # Listas
    mi_lista = [1, 2, 3, 4, 5]
    print(f"✅ Lista creada: {mi_lista}")
    print(f"✅ Suma de la lista: {sum(mi_lista)}")
    
    # Diccionarios
    mi_dict = {"nombre": "Python", "tipo": "Lenguaje", "año": 1991}
    print(f"✅ Diccionario creado: {mi_dict}")
    
    # Comprensión de listas
    cuadrados = [x**2 for x in range(5)]
    print(f"✅ Comprensión de lista: {cuadrados}")
    
    print("\n" + "=" * 60)
    print("✅ Todas las pruebas básicas pasaron correctamente!")
    print("=" * 60)


if __name__ == "__main__":
    print("\n🐍 VERIFICADOR DE INSTALACIÓN DE PYTHON 🐍\n")
    
    # Ejecutar todas las verificaciones
    mostrar_info_python()
    verificar_pip()
    verificar_modulos_estandar()
    ejecutar_prueba_basica()
    
    print("\n" + "=" * 60)
    print("🎉 ¡VERIFICACIÓN COMPLETADA!")
    print("=" * 60)
    print("\nSi llegaste hasta aquí sin errores, tu instalación")
    print("de Python está lista para comenzar el aprendizaje.")
    print("\n¡Feliz coding! 🚀")
    print("=" * 60 + "\n")
