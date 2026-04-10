"""
Módulo 1 - Ejercicio 4: Variables de Entorno
=============================================

Este script demuestra cómo trabajar con variables de entorno
tanto del sistema como usando archivos .env

Para usar este script:
1. Instala python-dotenv: pip install python-dotenv
2. Crea un archivo .env en el mismo directorio
3. Ejecuta el script: python 04_variables_entorno.py
"""

import os
import sys
from pathlib import Path


def mostrar_variables_sistema():
    """Muestra las variables de entorno del sistema."""
    
    print("\n" + "=" * 60)
    print("VARIABLES DE ENTORNO DEL SISTEMA")
    print("=" * 60 + "\n")
    
    # Variables importantes para Windows
    variables_importantes = [
        'PATH', 'PYTHONPATH', 'USERPROFILE', 'USERNAME',
        'TEMP', 'TMP', 'HOMEDRIVE', 'HOMEPATH', 'COMPUTERNAME'
    ]
    
    print("📌 Variables importantes:\n")
    for var in variables_importantes:
        valor = os.environ.get(var, 'No definida')
        if var == 'PATH':
            print(f"{var}:")
            # PATH es muy largo, mostramos cada ruta en una línea
            for path in valor.split(';')[:5]:  # Solo primeras 5
                print(f"   - {path}")
            print(f"   ... y {len(valor.split(';')) - 5} rutas más")
        else:
            print(f"{var}: {valor}")
    
    print("\n" + "=" * 60)


def leer_variables_entorno():
    """Demuestra cómo leer variables de entorno."""
    
    print("\n" + "=" * 60)
    print("LEER VARIABLES DE ENTORNO")
    print("=" * 60 + "\n")
    
    # Método 1: os.environ (dict-like)
    print("📌 Método 1: os.environ")
    print("-" * 60)
    
    # Leer variable (lanza excepción si no existe)
    try:
        username = os.environ['USERNAME']
        print(f"✅ USERNAME = {username}")
    except KeyError:
        print("❌ USERNAME no está definida")
    
    # Método 2: os.environ.get() (más seguro)
    print("\n📌 Método 2: os.environ.get() [RECOMENDADO]")
    print("-" * 60)
    
    # Con valor por defecto
    api_key = os.environ.get('API_KEY', 'no_configurada')
    print(f"API_KEY = {api_key}")
    
    debug_mode = os.environ.get('DEBUG', 'False')
    print(f"DEBUG = {debug_mode}")
    
    # Método 3: os.getenv() (alias de get)
    print("\n📌 Método 3: os.getenv()")
    print("-" * 60)
    
    database_url = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    print(f"DATABASE_URL = {database_url}")
    
    print("\n" + "=" * 60)


def establecer_variables_entorno():
    """Demuestra cómo establecer variables de entorno."""
    
    print("\n" + "=" * 60)
    print("ESTABLECER VARIABLES DE ENTORNO")
    print("=" * 60 + "\n")
    
    print("📌 Durante la ejecución del script (temporal)")
    print("-" * 60)
    
    # Establecer variable
    os.environ['MI_VARIABLE'] = 'Hola Mundo'
    print(f"✅ Variable establecida: MI_VARIABLE = {os.environ['MI_VARIABLE']}")
    
    # Establecer múltiples
    os.environ.update({
        'APP_NAME': 'MiAplicacion',
        'APP_VERSION': '1.0.0',
        'APP_ENV': 'development'
    })
    
    print("\nVariables de la aplicación:")
    print(f"  APP_NAME = {os.getenv('APP_NAME')}")
    print(f"  APP_VERSION = {os.getenv('APP_VERSION')}")
    print(f"  APP_ENV = {os.getenv('APP_ENV')}")
    
    print("\n⚠️  NOTA: Estas variables solo existen durante la ejecución")
    print("   del script y no afectan otras sesiones o procesos.")
    
    print("\n" + "=" * 60)


def usar_dotenv():
    """Demuestra el uso de python-dotenv para archivos .env."""
    
    print("\n" + "=" * 60)
    print("USANDO ARCHIVOS .ENV")
    print("=" * 60 + "\n")
    
    try:
        from dotenv import load_dotenv, find_dotenv, dotenv_values
        
        print("✅ python-dotenv está instalado\n")
        
        # Buscar archivo .env
        env_path = Path('.') / '.env'
        
        if env_path.exists():
            print(f"📄 Archivo .env encontrado: {env_path.absolute()}\n")
            
            # Cargar variables del archivo .env
            load_dotenv()
            print("✅ Variables cargadas desde .env\n")
            
            # Leer variables cargadas
            print("Variables del archivo .env:")
            print("-" * 60)
            
            # Método 1: Leer como dict (no carga en os.environ)
            config = dotenv_values('.env')
            for key, value in config.items():
                print(f"  {key} = {value}")
            
            # Método 2: Ya están en os.environ gracias a load_dotenv()
            print("\nAcceso directo con os.getenv():")
            print("-" * 60)
            for key in config.keys():
                print(f"  {key} = {os.getenv(key, 'No encontrada')}")
            
        else:
            print(f"⚠️  No se encontró archivo .env en: {env_path.absolute()}")
            print("\n💡 Crea un archivo .env con el siguiente contenido:")
            print("-" * 60)
            print("""
# Configuración de la aplicación
APP_NAME=MiAplicacion
APP_VERSION=1.0.0
DEBUG=True

# Base de datos
DATABASE_URL=postgresql://user:pass@localhost/dbname
DATABASE_POOL_SIZE=10

# API Keys (¡NO compartir en producción!)
API_KEY=tu_clave_secreta_aqui
SECRET_KEY=otra_clave_super_secreta

# Configuración de email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=tu_email@gmail.com
EMAIL_PASSWORD=tu_password
            """)
            print("-" * 60)
        
    except ImportError:
        print("❌ python-dotenv no está instalado")
        print("\n💡 Para instalarlo:")
        print("   pip install python-dotenv")
        print("\n💡 Para usarlo en tu código:")
        print("-" * 60)
        print("""
from dotenv import load_dotenv
import os

# Cargar variables desde .env
load_dotenv()

# Usar las variables
api_key = os.getenv('API_KEY')
debug = os.getenv('DEBUG', 'False') == 'True'
        """)
        print("-" * 60)
    
    print("\n" + "=" * 60)


def ejemplo_configuracion_app():
    """Ejemplo de clase de configuración usando variables de entorno."""
    
    print("\n" + "=" * 60)
    print("EJEMPLO: CLASE DE CONFIGURACIÓN")
    print("=" * 60 + "\n")
    
    print("💡 Patrón recomendado para aplicaciones:\n")
    print("-" * 60)
    
    codigo = '''
import os
from typing import Optional

class Config:
    """Configuración de la aplicación desde variables de entorno."""
    
    # Aplicación
    APP_NAME: str = os.getenv('APP_NAME', 'MiApp')
    APP_VERSION: str = os.getenv('APP_VERSION', '0.1.0')
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Base de datos
    DATABASE_URL: str = os.getenv(
        'DATABASE_URL',
        'sqlite:///default.db'
    )
    
    # Seguridad
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-CHANGE-THIS')
    API_KEY: Optional[str] = os.getenv('API_KEY')
    
    # Email
    EMAIL_HOST: str = os.getenv('EMAIL_HOST', 'localhost')
    EMAIL_PORT: int = int(os.getenv('EMAIL_PORT', '25'))
    EMAIL_USER: Optional[str] = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD: Optional[str] = os.getenv('EMAIL_PASSWORD')
    
    @classmethod
    def validate(cls):
        """Valida que las variables críticas estén configuradas."""
        errors = []
        
        if cls.SECRET_KEY == 'dev-secret-key-CHANGE-THIS':
            errors.append("SECRET_KEY debe ser cambiada en producción")
        
        if cls.DEBUG and not cls.API_KEY:
            errors.append("API_KEY es requerida en modo DEBUG")
        
        if errors:
            raise ValueError("Errores de configuración:\\n" + "\\n".join(errors))
        
        return True

# Uso:
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    config = Config()
    
    try:
        config.validate()
        print(f"✅ Aplicación: {config.APP_NAME} v{config.APP_VERSION}")
        print(f"✅ Debug mode: {config.DEBUG}")
        print(f"✅ Database: {config.DATABASE_URL}")
    except ValueError as e:
        print(f"❌ Error: {e}")
    '''
    
    print(codigo)
    print("-" * 60)
    
    print("\n" + "=" * 60)


def mejores_practicas():
    """Muestra mejores prácticas para variables de entorno."""
    
    print("\n" + "=" * 60)
    print("MEJORES PRÁCTICAS")
    print("=" * 60 + "\n")
    
    practicas = [
        {
            "titulo": "1. Nunca commits .env al repositorio",
            "descripcion": "Los archivos .env contienen información sensible",
            "ejemplo": """
# .gitignore
.env
.env.local
.env.*.local
            """
        },
        {
            "titulo": "2. Crea un .env.example",
            "descripcion": "Documenta qué variables son necesarias sin valores reales",
            "ejemplo": """
# .env.example
APP_NAME=
API_KEY=
DATABASE_URL=
            """
        },
        {
            "titulo": "3. Usa valores por defecto seguros",
            "descripcion": "Siempre proporciona defaults para desarrollo",
            "ejemplo": """
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
PORT = int(os.getenv('PORT', '8000'))
            """
        },
        {
            "titulo": "4. Convierte tipos apropiadamente",
            "descripcion": "os.getenv() siempre retorna strings",
            "ejemplo": """
# ❌ Mal
DEBUG = os.getenv('DEBUG', False)  # Siempre True!

# ✅ Bien
DEBUG = os.getenv('DEBUG', 'False') == 'True'
PORT = int(os.getenv('PORT', '8000'))
THRESHOLD = float(os.getenv('THRESHOLD', '0.5'))
            """
        },
        {
            "titulo": "5. Organiza por categorías",
            "descripcion": "Usa prefijos para agrupar variables relacionadas",
            "ejemplo": """
# Base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
            """
        },
        {
            "titulo": "6. Valida variables críticas al inicio",
            "descripcion": "Falla rápido si faltan configuraciones importantes",
            "ejemplo": """
required_vars = ['DATABASE_URL', 'SECRET_KEY', 'API_KEY']
missing = [var for var in required_vars if not os.getenv(var)]

if missing:
    raise ValueError(f"Faltan variables: {', '.join(missing)}")
            """
        }
    ]
    
    for practica in practicas:
        print(f"📌 {practica['titulo']}")
        print("-" * 60)
        print(f"{practica['descripcion']}\n")
        if practica['ejemplo']:
            print("Ejemplo:")
            print(practica['ejemplo'])
        print()
    
    print("=" * 60)


def comandos_powershell():
    """Muestra comandos PowerShell para trabajar con variables de entorno."""
    
    print("\n" + "=" * 60)
    print("COMANDOS POWERSHELL")
    print("=" * 60 + "\n")
    
    print("📌 Ver variable de entorno:")
    print("-" * 60)
    print("$env:VARIABLE_NAME")
    print("echo $env:PATH\n")
    
    print("📌 Establecer variable (sesión actual):")
    print("-" * 60)
    print("$env:VARIABLE_NAME = 'valor'")
    print("$env:API_KEY = 'mi_clave_123'\n")
    
    print("📌 Establecer variable (permanente - Usuario):")
    print("-" * 60)
    print("[System.Environment]::SetEnvironmentVariable('VARIABLE', 'valor', 'User')")
    print("setx VARIABLE 'valor'\n")
    
    print("📌 Establecer variable (permanente - Sistema):")
    print("-" * 60)
    print("# Requiere ejecutar PowerShell como Administrador")
    print("[System.Environment]::SetEnvironmentVariable('VARIABLE', 'valor', 'Machine')\n")
    
    print("📌 Listar todas las variables:")
    print("-" * 60)
    print("Get-ChildItem Env:")
    print("dir env:\n")
    
    print("📌 Eliminar variable (sesión actual):")
    print("-" * 60)
    print("Remove-Item Env:\\VARIABLE_NAME\n")
    
    print("=" * 60)


if __name__ == "__main__":
    print("\n🔐 VARIABLES DE ENTORNO EN PYTHON 🔐\n")
    
    # Ejecutar todas las demostraciones
    mostrar_variables_sistema()
    leer_variables_entorno()
    establecer_variables_entorno()
    usar_dotenv()
    ejemplo_configuracion_app()
    mejores_practicas()
    comandos_powershell()
    
    print("\n" + "=" * 60)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("=" * 60)
    print("\n💡 Próximos pasos:")
    print("   1. Crea un archivo .env para tu proyecto")
    print("   2. Instala python-dotenv: pip install python-dotenv")
    print("   3. Nunca commits .env al repositorio (agrega a .gitignore)")
    print("   4. Crea .env.example como documentación")
    print("\n" + "=" * 60 + "\n")
