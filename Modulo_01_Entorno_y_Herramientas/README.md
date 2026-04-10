# Módulo 1: Entorno y Herramientas de Python

## 📋 Tabla de Contenidos
1. [Introducción](#introducción)
2. [Instalación de Python](#instalación-de-python)
3. [IDEs y Editores](#ides-y-editores)
4. [Gestión de Paquetes con pip](#gestión-de-paquetes-con-pip)
5. [Entornos Virtuales](#entornos-virtuales)
6. [Variables de Entorno](#variables-de-entorno)
7. [Primeros Pasos](#primeros-pasos)
8. [Ejercicios Prácticos](#ejercicios-prácticos)

---

## 🎯 Introducción

Python es un lenguaje de programación de alto nivel, interpretado y de propósito general. Para trabajar eficientemente con Python, es fundamental configurar correctamente el entorno de desarrollo.

### Objetivos del Módulo
- ✅ Instalar y configurar Python correctamente
- ✅ Conocer las herramientas esenciales para desarrollo
- ✅ Dominar la gestión de paquetes y dependencias
- ✅ Crear y usar entornos virtuales
- ✅ Configurar variables de entorno

---

## 🔧 Instalación de Python

### Windows

#### Opción 1: Desde python.org (Recomendado)
1. Visita [python.org/downloads](https://www.python.org/downloads/)
2. Descarga la última versión estable (Python 3.11+)
3. **IMPORTANTE**: Marca "Add Python to PATH"
4. Ejecuta el instalador y selecciona "Install Now"

#### Opción 2: Usando Microsoft Store
```powershell
# Busca "Python" en Microsoft Store e instala
```

#### Opción 3: Usando winget
```powershell
winget install Python.Python.3.11
```

### Verificar Instalación

```powershell
# Verificar versión de Python
python --version

# Verificar versión de pip
pip --version

# Verificar ubicación de Python
where python
```

**Archivo de ejemplo**: `01_verificar_instalacion.py`

---

## 💻 IDEs y Editores

### Visual Studio Code (Recomendado para este curso)

#### Extensiones Esenciales
1. **Python** (Microsoft) - Soporte completo para Python
2. **Pylance** - IntelliSense mejorado
3. **Python Indent** - Auto-indentación inteligente
4. **autoDocstring** - Generación automática de docstrings

#### Configuración en VS Code
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.analysis.typeCheckingMode": "basic"
}
```

### Otras Opciones Populares
- **PyCharm** - IDE completo y potente
- **Jupyter Notebook** - Ideal para análisis de datos
- **Spyder** - Enfocado en ciencia de datos
- **Sublime Text** - Ligero y rápido

---

## 📦 Gestión de Paquetes con pip

### ¿Qué es pip?
`pip` (Package Installer for Python) es el gestor de paquetes estándar de Python.

### Comandos Esenciales

```powershell
# Instalar un paquete
pip install nombre_paquete

# Instalar una versión específica
pip install nombre_paquete==1.2.3

# Instalar desde requirements.txt
pip install -r requirements.txt

# Listar paquetes instalados
pip list

# Mostrar información de un paquete
pip show nombre_paquete

# Actualizar un paquete
pip install --upgrade nombre_paquete

# Desinstalar un paquete
pip uninstall nombre_paquete

# Congelar dependencias (crear requirements.txt)
pip freeze > requirements.txt
```

### requirements.txt
Archivo que lista todas las dependencias del proyecto:

```text
requests==2.31.0
numpy>=1.24.0
pandas==2.0.1
```

**Archivo de ejemplo**: `02_gestionar_paquetes.py`

---

## 🌍 Entornos Virtuales

### ¿Por qué usar entornos virtuales?
- Aislamiento de dependencias entre proyectos
- Evita conflictos de versiones
- Facilita la reproducibilidad
- Mantiene limpio el Python global

### Crear Entorno Virtual con venv

```powershell
# Crear entorno virtual
python -m venv nombre_entorno

# Activar entorno (Windows)
nombre_entorno\Scripts\activate

# Activar entorno (PowerShell)
nombre_entorno\Scripts\Activate.ps1

# Desactivar entorno
deactivate
```

### Ejemplo Completo

```powershell
# 1. Crear proyecto
mkdir mi_proyecto
cd mi_proyecto

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno
venv\Scripts\activate

# 4. Instalar dependencias
pip install requests pandas

# 5. Guardar dependencias
pip freeze > requirements.txt

# 6. Trabajar en el proyecto...

# 7. Desactivar cuando termines
deactivate
```

### Alternativas a venv
- **virtualenv** - Más rápido y con más opciones
- **conda** - Incluye gestión de paquetes no-Python
- **pipenv** - Combina pip y virtualenv
- **poetry** - Gestión moderna de dependencias

**Archivo de ejemplo**: `03_entornos_virtuales.md`

---

## 🔐 Variables de Entorno

### ¿Qué son?
Variables que configuran el comportamiento del sistema operativo y las aplicaciones.

### Variables Importantes para Python

#### PYTHONPATH
Define dónde Python busca módulos:

```powershell
# Windows (temporal)
$env:PYTHONPATH = "C:\ruta\a\modulos"

# Windows (permanente) - System Properties > Environment Variables
setx PYTHONPATH "C:\ruta\a\modulos"
```

#### PATH
Asegura que Python sea ejecutable desde cualquier ubicación.

### Usando python-dotenv

```python
# Instalar
pip install python-dotenv

# Crear archivo .env
"""
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=mi_clave_secreta_123
DEBUG=True
"""

# Usar en el código
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')
debug = os.getenv('DEBUG', 'False') == 'True'
```

**Archivos de ejemplo**: 
- `04_variables_entorno.py`
- `.env.example`

---

## 🚀 Primeros Pasos

### Hola Mundo

```python
# hola_mundo.py
print("¡Hola, mundo!")
```

Ejecutar:
```powershell
python hola_mundo.py
```

### REPL (Read-Eval-Print Loop)

```powershell
# Iniciar intérprete interactivo
python

>>> print("Hola desde REPL")
>>> 2 + 2
>>> exit()
```

### Estructura de un Proyecto Python

```
mi_proyecto/
│
├── venv/                  # Entorno virtual (no versionar)
├── src/                   # Código fuente
│   ├── __init__.py
│   └── main.py
├── tests/                 # Pruebas
│   └── test_main.py
├── .env                   # Variables de entorno (no versionar)
├── .gitignore            # Archivos a ignorar en git
├── requirements.txt       # Dependencias
└── README.md             # Documentación
```

### .gitignore para Python

```gitignore
# Entornos virtuales
venv/
env/
ENV/

# Archivos Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Variables de entorno
.env

# IDEs
.vscode/
.idea/
*.swp

# Distribución
dist/
build/
*.egg-info/
```

**Archivo de ejemplo**: `05_primer_programa.py`

---

## 📝 Ejercicios Prácticos

### Ejercicio 1: Configuración Inicial
1. Verifica que Python está instalado correctamente
2. Crea un entorno virtual llamado `mi_primer_entorno`
3. Actívalo e instala `requests` y `beautifulsoup4`
4. Genera un archivo `requirements.txt`

### Ejercicio 2: Proyecto con Variables de Entorno
1. Crea un nuevo proyecto llamado `gestor_config`
2. Configura un entorno virtual
3. Instala `python-dotenv`
4. Crea un archivo `.env` con variables de configuración
5. Escribe un script que lea y muestre estas variables

### Ejercicio 3: Exploración de pip
1. Lista todos los paquetes instalados en tu entorno
2. Busca información sobre el paquete `requests`
3. Instala una versión específica de `numpy` (1.24.0)
4. Actualízala a la última versión

---

## 🎓 Resumen del Módulo

### Conceptos Clave Aprendidos
✅ **Python**: Lenguaje interpretado de alto nivel  
✅ **pip**: Gestor de paquetes de Python  
✅ **venv**: Herramienta para crear entornos virtuales  
✅ **requirements.txt**: Archivo de dependencias  
✅ **Variables de entorno**: Configuración del sistema  
✅ **VS Code**: Editor/IDE recomendado  

### Comandos Esenciales

```powershell
# Verificación
python --version
pip --version

# Entornos virtuales
python -m venv venv
venv\Scripts\activate
deactivate

# Gestión de paquetes
pip install paquete
pip freeze > requirements.txt
pip install -r requirements.txt
pip list
```

### Checklist de Preparación
- [ ] Python instalado y en PATH
- [ ] VS Code con extensión de Python
- [ ] Sabes crear y activar entornos virtuales
- [ ] Puedes instalar paquetes con pip
- [ ] Entiendes el uso de requirements.txt
- [ ] Sabes usar variables de entorno

---

## 📚 Recursos Adicionales

- [Documentación Oficial de Python](https://docs.python.org/3/)
- [pip Documentation](https://pip.pypa.io/)
- [Python Package Index (PyPI)](https://pypi.org/)
- [Real Python - Tutorials](https://realpython.com/)
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)

---

## ➡️ Próximo Módulo

**Módulo 2: Fundamentos de Python**
- Variables y tipos de datos
- Operadores
- Estructuras de control
- Funciones básicas

---

*Última actualización: Abril 2026*
