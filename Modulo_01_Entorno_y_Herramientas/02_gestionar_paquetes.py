"""
Módulo 1 - Ejercicio 2: Gestión de Paquetes con pip
====================================================

Este script demuestra cómo gestionar paquetes de Python
y muestra información sobre los paquetes instalados.

NOTA: Ejecuta este script en un entorno virtual para
evitar modificar tu instalación global de Python.
"""

import subprocess
import sys
import json


def ejecutar_comando_pip(comando):
    """
    Ejecuta un comando de pip y retorna el resultado.
    
    Args:
        comando (list): Lista con el comando y argumentos
        
    Returns:
        tuple: (stdout, stderr, return_code)
    """
    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return resultado.stdout, resultado.stderr, resultado.returncode
    except Exception as e:
        return "", str(e), 1


def listar_paquetes_instalados():
    """Lista todos los paquetes instalados en el entorno actual."""
    
    print("\n" + "=" * 60)
    print("PAQUETES INSTALADOS EN EL ENTORNO ACTUAL")
    print("=" * 60 + "\n")
    
    stdout, stderr, code = ejecutar_comando_pip([sys.executable, "-m", "pip", "list"])
    
    if code == 0:
        print(stdout)
    else:
        print(f"❌ Error al listar paquetes: {stderr}")
    
    print("=" * 60)


def mostrar_info_paquete(nombre_paquete):
    """
    Muestra información detallada sobre un paquete específico.
    
    Args:
        nombre_paquete (str): Nombre del paquete a consultar
    """
    
    print(f"\n" + "=" * 60)
    print(f"INFORMACIÓN DEL PAQUETE: {nombre_paquete}")
    print("=" * 60 + "\n")
    
    stdout, stderr, code = ejecutar_comando_pip(
        [sys.executable, "-m", "pip", "show", nombre_paquete]
    )
    
    if code == 0 and stdout.strip():
        print(stdout)
    else:
        print(f"❌ El paquete '{nombre_paquete}' no está instalado")
        print(f"   Instálalo con: pip install {nombre_paquete}")
    
    print("=" * 60)


def listar_paquetes_desactualizados():
    """Lista los paquetes que tienen actualizaciones disponibles."""
    
    print("\n" + "=" * 60)
    print("PAQUETES CON ACTUALIZACIONES DISPONIBLES")
    print("=" * 60 + "\n")
    
    stdout, stderr, code = ejecutar_comando_pip(
        [sys.executable, "-m", "pip", "list", "--outdated"]
    )
    
    if code == 0:
        if stdout.strip():
            print(stdout)
            print("\n💡 Para actualizar un paquete:")
            print("   pip install --upgrade nombre_paquete")
        else:
            print("✅ Todos los paquetes están actualizados")
    else:
        print(f"❌ Error al verificar actualizaciones: {stderr}")
    
    print("=" * 60)


def mostrar_dependencias_paquete(nombre_paquete):
    """
    Muestra las dependencias de un paquete específico.
    
    Args:
        nombre_paquete (str): Nombre del paquete
    """
    
    print(f"\n" + "=" * 60)
    print(f"DEPENDENCIAS DE: {nombre_paquete}")
    print("=" * 60 + "\n")
    
    # Usar pip show para obtener información
    stdout, stderr, code = ejecutar_comando_pip(
        [sys.executable, "-m", "pip", "show", nombre_paquete]
    )
    
    if code == 0 and stdout.strip():
        for linea in stdout.split('\n'):
            if linea.startswith('Requires:'):
                dependencias = linea.replace('Requires:', '').strip()
                if dependencias:
                    print(f"📦 Dependencias requeridas:")
                    for dep in dependencias.split(', '):
                        print(f"   - {dep}")
                else:
                    print("✅ Este paquete no tiene dependencias")
                break
            if linea.startswith('Required-by:'):
                requerido_por = linea.replace('Required-by:', '').strip()
                if requerido_por:
                    print(f"\n📦 Paquetes que dependen de {nombre_paquete}:")
                    for dep in requerido_por.split(', '):
                        print(f"   - {dep}")
                else:
                    print(f"\n✅ Ningún paquete instalado depende de {nombre_paquete}")
    else:
        print(f"❌ El paquete '{nombre_paquete}' no está instalado")
    
    print("\n" + "=" * 60)


def exportar_requirements():
    """Genera un archivo requirements.txt con los paquetes instalados."""
    
    print("\n" + "=" * 60)
    print("EXPORTAR REQUIREMENTS.TXT")
    print("=" * 60 + "\n")
    
    stdout, stderr, code = ejecutar_comando_pip(
        [sys.executable, "-m", "pip", "freeze"]
    )
    
    if code == 0:
        # Guardar en archivo
        try:
            with open("requirements.txt", "w", encoding="utf-8") as f:
                f.write(stdout)
            
            print("✅ Archivo requirements.txt generado exitosamente")
            print("\nContenido:")
            print("-" * 60)
            print(stdout)
            print("-" * 60)
            print("\n💡 Para instalar estos paquetes en otro entorno:")
            print("   pip install -r requirements.txt")
        except Exception as e:
            print(f"❌ Error al guardar el archivo: {e}")
    else:
        print(f"❌ Error al generar requirements: {stderr}")
    
    print("=" * 60)


def verificar_entorno_virtual():
    """Verifica si estamos en un entorno virtual."""
    
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DE ENTORNO VIRTUAL")
    print("=" * 60 + "\n")
    
    # Verificar si estamos en un entorno virtual
    en_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if en_venv:
        print("✅ Estás trabajando en un ENTORNO VIRTUAL")
        print(f"📌 Prefijo del entorno: {sys.prefix}")
        print(f"📌 Prefijo base: {sys.base_prefix}")
        print("\n💡 Es seguro instalar paquetes aquí")
    else:
        print("⚠️  Estás en la instalación GLOBAL de Python")
        print(f"📌 Prefijo: {sys.prefix}")
        print("\n⚠️  RECOMENDACIÓN: Crea y activa un entorno virtual antes")
        print("   de instalar paquetes para evitar conflictos.")
        print("\n   Comandos:")
        print("   python -m venv mi_entorno")
        print("   mi_entorno\\Scripts\\activate  (Windows)")
    
    print("\n" + "=" * 60)


def mostrar_comandos_utiles():
    """Muestra una guía de comandos útiles de pip."""
    
    print("\n" + "=" * 60)
    print("GUÍA RÁPIDA DE COMANDOS PIP")
    print("=" * 60 + "\n")
    
    comandos = {
        "Instalación": [
            ("pip install paquete", "Instala un paquete"),
            ("pip install paquete==1.2.3", "Instala versión específica"),
            ("pip install paquete>=1.2.0", "Instala versión mínima"),
            ("pip install -r requirements.txt", "Instala desde archivo"),
            ("pip install -e .", "Instala en modo desarrollo"),
        ],
        "Actualización": [
            ("pip install --upgrade paquete", "Actualiza un paquete"),
            ("pip install --upgrade pip", "Actualiza pip mismo"),
        ],
        "Información": [
            ("pip list", "Lista paquetes instalados"),
            ("pip show paquete", "Muestra info del paquete"),
            ("pip freeze", "Lista con versiones exactas"),
            ("pip list --outdated", "Muestra paquetes desactualizados"),
        ],
        "Desinstalación": [
            ("pip uninstall paquete", "Desinstala un paquete"),
            ("pip uninstall -r requirements.txt", "Desinstala desde archivo"),
        ],
        "Búsqueda": [
            ("pip search término", "Busca paquetes (deprecado)"),
            ("Usar https://pypi.org", "Buscar en el sitio web"),
        ],
    }
    
    for categoria, lista_comandos in comandos.items():
        print(f"\n📌 {categoria}:")
        print("-" * 60)
        for comando, descripcion in lista_comandos:
            print(f"  {comando:40} → {descripcion}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    print("\n📦 GESTOR DE PAQUETES PYTHON (pip) 📦\n")
    
    # Verificar si estamos en entorno virtual
    verificar_entorno_virtual()
    
    # Listar paquetes instalados
    listar_paquetes_instalados()
    
    # Mostrar paquetes desactualizados
    listar_paquetes_desactualizados()
    
    # Ejemplos con paquetes comunes (si están instalados)
    paquetes_ejemplo = ['pip', 'setuptools']
    
    for paquete in paquetes_ejemplo:
        mostrar_info_paquete(paquete)
        mostrar_dependencias_paquete(paquete)
    
    # Exportar requirements
    exportar_requirements()
    
    # Mostrar guía de comandos
    mostrar_comandos_utiles()
    
    print("\n" + "=" * 60)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("=" * 60)
    print("\n💡 Próximos pasos:")
    print("   1. Practica instalando paquetes en un entorno virtual")
    print("   2. Experimenta con pip install, pip list, pip show")
    print("   3. Crea tu propio requirements.txt para un proyecto")
    print("\n" + "=" * 60 + "\n")
