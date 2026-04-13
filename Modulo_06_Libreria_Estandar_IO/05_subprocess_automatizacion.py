"""
Módulo 6.5: subprocess y Automatización
========================================

Ejecutar comandos externos y automatizar tareas del sistema operativo.

Temas:
- subprocess.run() y subprocess.Popen()
- Capturar stdout y stderr
- Manejo de errores y timeouts
- Pipelines y comunicación entre procesos
- Automatización de tareas comunes
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional, List


# =============================================================================
# 1. subprocess.run() Básico
# =============================================================================

def ejemplo_run_basico():
    """Uso básico de subprocess.run()."""
    print("=== subprocess.run() Básico ===\n")
    
    # Ejecutar comando simple
    resultado = subprocess.run(
        ["python", "--version"],
        capture_output=True,
        text=True
    )
    
    print(f"Código de salida: {resultado.returncode}")
    print(f"Salida: {resultado.stdout}")
    print(f"Errores: {resultado.stderr}")


def ejemplo_capturar_salida():
    """Capturar stdout y stderr."""
    print("\n=== Capturar Salida ===\n")
    
    # Listar archivos del directorio
    resultado = subprocess.run(
        ["dir" if sys.platform == "win32" else "ls", "-l"],
        capture_output=True,
        text=True,
        shell=True if sys.platform == "win32" else False
    )
    
    print("Archivos en el directorio:")
    print(resultado.stdout)


def ejemplo_check_errors():
    """Manejo de errores con check=True."""
    print("\n=== Manejo de Errores ===\n")
    
    try:
        # Comando que fallará
        resultado = subprocess.run(
            ["python", "archivo_que_no_existe.py"],
            capture_output=True,
            text=True,
            check=True  # Lanza excepción si returncode != 0
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Comando falló con código: {e.returncode}")
        print(f"Error: {e.stderr}")
    
    # Ejecutar comando exitoso
    try:
        resultado = subprocess.run(
            ["python", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Comando exitoso: {resultado.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Error inesperado: {e}")


# =============================================================================
# 2. Timeout y Control
# =============================================================================

def ejemplo_timeout():
    """Ejecutar comandos con timeout."""
    print("\n=== Timeout ===\n")
    
    try:
        # Comando que tarda mucho (ping con muchas repeticiones)
        resultado = subprocess.run(
            ["ping", "-n", "10", "127.0.0.1"] if sys.platform == "win32" 
            else ["ping", "-c", "10", "127.0.0.1"],
            capture_output=True,
            text=True,
            timeout=2  # Timeout de 2 segundos
        )
        print("Comando completado")
    except subprocess.TimeoutExpired:
        print("⏱️ Comando excedió el timeout de 2 segundos")


# =============================================================================
# 3. Trabajar con Directorios
# =============================================================================

def ejemplo_cambiar_directorio():
    """Ejecutar comandos en diferentes directorios."""
    print("\n=== Cambiar Directorio ===\n")
    
    # Crear directorio temporal
    temp_dir = Path("temp_subprocess")
    temp_dir.mkdir(exist_ok=True)
    
    # Ejecutar comando en ese directorio
    resultado = subprocess.run(
        ["git", "init"],
        cwd=str(temp_dir),
        capture_output=True,
        text=True
    )
    
    if resultado.returncode == 0:
        print(f"✅ Git inicializado en: {temp_dir}")
    else:
        print(f"Error: {resultado.stderr}")
    
    # Limpiar
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)


# =============================================================================
# 4. Variables de Entorno
# =============================================================================

def ejemplo_variables_entorno():
    """Ejecutar comandos con variables de entorno personalizadas."""
    print("\n=== Variables de Entorno ===\n")
    
    import os
    
    # Crear copia del entorno actual
    env = os.environ.copy()
    env["MI_VARIABLE"] = "valor_personalizado"
    
    # Ejecutar Python con variable de entorno
    script = 'import os; print(f"MI_VARIABLE={os.environ.get(\'MI_VARIABLE\', \'no definida\')}")'
    
    resultado = subprocess.run(
        ["python", "-c", script],
        env=env,
        capture_output=True,
        text=True
    )
    
    print(f"Salida: {resultado.stdout}")


# =============================================================================
# 5. Pipelines y Comunicación
# =============================================================================

def ejemplo_pipeline():
    """Crear pipelines entre comandos."""
    print("\n=== Pipelines ===\n")
    
    # Primer comando
    p1 = subprocess.Popen(
        ["echo", "Hola Mundo"],
        stdout=subprocess.PIPE,
        text=True
    )
    
    # Segundo comando que consume la salida del primero
    p2 = subprocess.Popen(
        ["python", "-c", "import sys; print(sys.stdin.read().upper())"],
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
        text=True
    )
    
    # Esperar y obtener resultado
    salida, _ = p2.communicate()
    print(f"Resultado del pipeline: {salida}")


# =============================================================================
# 6. Ejemplos de Automatización
# =============================================================================

def ejemplo_git_status():
    """Ver estado de git."""
    print("\n=== Git Status ===\n")
    
    resultado = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True
    )
    
    if resultado.returncode == 0:
        print("Estado de Git:")
        print(resultado.stdout if resultado.stdout else "  (sin cambios)")
    else:
        print("❌ No es un repositorio git")


def ejemplo_ejecutar_tests():
    """Ejecutar tests con pytest."""
    print("\n=== Ejecutar Tests ===\n")
    
    resultado = subprocess.run(
        ["python", "-m", "pytest", "--version"],
        capture_output=True,
        text=True
    )
    
    if resultado.returncode == 0:
        print(f"pytest disponible: {resultado.stdout.strip()}")
    else:
        print("pytest no instalado")


def ejemplo_backup_automatico():
    """Crear backup automático de archivos."""
    print("\n=== Backup Automático ===\n")
    
    from datetime import datetime
    
    # Crear directorio de backups
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    
    # Timestamp para el nombre del backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"backup_{timestamp}.zip"
    
    # Crear archivo ZIP con los archivos .py
    if sys.platform == "win32":
        # En Windows
        comando = ["powershell", "Compress-Archive", "-Path", "*.py", "-DestinationPath", str(backup_file)]
    else:
        # En Linux/Mac
        comando = ["zip", "-r", str(backup_file), "*.py"]
    
    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True
    )
    
    if resultado.returncode == 0 and backup_file.exists():
        tamano = backup_file.stat().st_size
        print(f"✅ Backup creado: {backup_file}")
        print(f"   Tamaño: {tamano} bytes")
    else:
        print(f"❌ Error al crear backup")


# =============================================================================
# 7. Utilidades de Automatización
# =============================================================================

def ejecutar_comando(comando: List[str], descripcion: str = "") -> Optional[str]:
    """
    Ejecuta un comando y retorna su salida.
    
    Args:
        comando: Lista con el comando y sus argumentos.
        descripcion: Descripción del comando para logging.
    
    Returns:
        Salida del comando o None si falló.
    """
    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            check=True
        )
        return resultado.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {descripcion or comando[0]}: {e.stderr}")
        return None


def ejemplo_utilidad_ejecutar():
    """Usar utilidad para ejecutar comandos."""
    print("\n=== Utilidad Ejecutar Comando ===\n")
    
    # Ejecutar varios comandos
    comandos = [
        (["python", "--version"], "Versión de Python"),
        (["pip", "--version"], "Versión de pip"),
        (["git", "--version"], "Versión de git"),
    ]
    
    for comando, descripcion in comandos:
        salida = ejecutar_comando(comando, descripcion)
        if salida:
            print(f"✅ {descripcion}: {salida.strip()}")


# =============================================================================
# 8. Mejores Prácticas
# =============================================================================

def ejemplo_mejores_practicas():
    """Mejores prácticas con subprocess."""
    print("\n=== Mejores Prácticas ===\n")
    
    # ✅ BUENO: Usar lista en lugar de string
    subprocess.run(["python", "--version"], capture_output=True)
    print("✅ Comando como lista (seguro)")
    
    # ❌ MALO: shell=True puede ser peligroso
    # subprocess.run("python --version", shell=True)
    print("❌ shell=True (evitar, riesgo de injection)")
    
    # ✅ BUENO: Capturar errores
    try:
        subprocess.run(
            ["comando_inexistente"],
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"✅ Error capturado correctamente: {e.returncode}")
    except FileNotFoundError:
        print("✅ Comando no encontrado (capturado)")
    
    # ✅ BUENO: Usar timeout
    try:
        subprocess.run(
            ["python", "--version"],
            timeout=5,
            capture_output=True
        )
        print("✅ Timeout configurado")
    except subprocess.TimeoutExpired:
        print("Timeout excedido")
    
    # ✅ BUENO: Especificar encoding
    subprocess.run(
        ["python", "--version"],
        capture_output=True,
        text=True,  # O encoding="utf-8"
    )
    print("✅ Encoding especificado")


# =============================================================================
# Main
# =============================================================================

def main():
    """Ejecuta todos los ejemplos."""
    ejemplos = [
        ejemplo_run_basico,
        ejemplo_capturar_salida,
        ejemplo_check_errors,
        ejemplo_timeout,
        ejemplo_cambiar_directorio,
        ejemplo_variables_entorno,
        ejemplo_pipeline,
        ejemplo_git_status,
        ejemplo_ejecutar_tests,
        ejemplo_backup_automatico,
        ejemplo_utilidad_ejecutar,
        ejemplo_mejores_practicas,
    ]
    
    for ejemplo in ejemplos:
        try:
            ejemplo()
        except Exception as e:
            print(f"❌ Error en {ejemplo.__name__}: {e}")
        print("\n" + "="*70)


if __name__ == "__main__":
    main()
