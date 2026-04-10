# 🧪 Laboratorio - Módulo 2: Herramientas de Calidad de Código

## 🎯 Objetivos del Laboratorio

En este laboratorio aprenderás a:
- ✅ Crear un proyecto Python profesional con **Poetry**
- ✅ Configurar herramientas de formateo: **black**, **isort**, **ruff**
- ✅ Implementar **pre-commit hooks** para validación automática
- ✅ Identificar y corregir infracciones de **PEP 8**
- ✅ Establecer un flujo de trabajo de calidad de código

**Duración estimada:** 60-90 minutos

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener:
- ✅ Python 3.8 o superior instalado
- ✅ pip actualizado: `python -m pip install --upgrade pip`
- ✅ PowerShell o Terminal con permisos adecuados
- ✅ Editor de código (VS Code recomendado)

---

## 🚀 Parte 1: Instalación de Poetry

### ¿Qué es Poetry?

**Poetry** es una herramienta moderna de gestión de dependencias y empaquetado para Python que simplifica:
- Gestión de dependencias
- Creación de entornos virtuales
- Empaquetado de proyectos
- Publicación en PyPI

### Instalación

#### Windows (PowerShell)
```powershell
# Instalar Poetry
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Agregar Poetry al PATH (reinicia PowerShell después)
$env:Path += ";$env:APPDATA\Python\Scripts"
```

#### Verificar instalación
```powershell
# Verificar versión
poetry --version

# Ver ayuda
poetry --help
```

### Configuración Inicial de Poetry

```powershell
# Configurar Poetry para crear venv en el directorio del proyecto
poetry config virtualenvs.in-project true

# Verificar configuración
poetry config --list
```

---

## 🏗️ Parte 2: Crear Proyecto con Poetry

### Paso 1: Crear el proyecto

```powershell
# Navegar al directorio donde quieres crear el proyecto
cd c:\Users\jared.trejo\Documents\GitHub\Axity\Python

# Crear nuevo proyecto
poetry new calculadora_profesional

# Estructura creada automáticamente:
# calculadora_profesional/
# ├── calculadora_profesional/
# │   └── __init__.py
# ├── tests/
# │   └── __init__.py
# ├── pyproject.toml
# └── README.md
```

### Paso 2: Explorar el proyecto

```powershell
# Entrar al directorio
cd calculadora_profesional

# Ver contenido del directorio
ls

# Ver pyproject.toml
type pyproject.toml
```

**Contenido de `pyproject.toml`:**
```toml
[tool.poetry]
name = "calculadora-profesional"
version = "0.1.0"
description = ""
authors = ["Tu Nombre <tu@email.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.8"

[tool.poetry.group.dev.dependencies]

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### Paso 3: Crear el entorno virtual

```powershell
# Crear e instalar dependencias
poetry install

# Verificar que se creó .venv
ls -Force

# Activar el entorno virtual
poetry shell

# Verificar Python del entorno
where python
# Debe mostrar: ...\calculadora_profesional\.venv\Scripts\python.exe
```

---

## 🛠️ Parte 3: Instalar Herramientas de Calidad

### Herramientas que instalaremos

| Herramienta | Propósito |
|-------------|-----------|
| **black** | Formateador de código automático |
| **isort** | Ordena imports automáticamente |
| **ruff** | Linter ultra-rápido (reemplaza flake8, pylint) |
| **pre-commit** | Ejecuta validaciones antes de commits |

### Instalación con Poetry

```powershell
# Asegúrate de estar en el entorno virtual (poetry shell)

# Instalar herramientas de desarrollo
poetry add --group dev black
poetry add --group dev isort
poetry add --group dev ruff
poetry add --group dev pre-commit

# Ver dependencias instaladas
poetry show --tree
```

**El `pyproject.toml` ahora incluye:**
```toml
[tool.poetry.group.dev.dependencies]
black = "^24.0.0"
isort = "^5.13.0"
ruff = "^0.3.0"
pre-commit = "^3.6.0"
```

---

## 📝 Parte 4: Crear Código con Infracciones PEP 8

### Crear archivo con código "malo"

Crea `calculadora_profesional/calculadora.py` con código que viola PEP 8:

```python
# calculadora_profesional/calculadora.py

import sys
import os
from typing import Union
import math,random
import json

def suma(a,b):
    """suma dos numeros"""
    return a+b

def resta( a, b ):
    return a-b

def multiplicacion(x,y):
    resultado=x*y
    return resultado

class Calculadora:
    def __init__(self,nombre):
        self.nombre=nombre
        self.historial=[]
    
    def dividir(self,a,b):
        if b==0:
            return None
        resultado=a/b
        self.historial.append({'operacion':'division','resultado':resultado})
        return resultado
    
    def potencia(self, base, exponente):
        """calcula potencia"""
        return base**exponente
    
    def obtener_historial( self ):
        return self.historial

def main():
    calc=Calculadora('MiCalc')
    
    print("Suma:", suma(10,5))
    print("Resta:", resta(10,5))
    print("Multiplicación:", multiplicacion(10,5))
    print("División:", calc.dividir(10,2))
    print("Potencia:", calc.potencia(2,3))
    
    historial=calc.obtener_historial()
    print("Historial:",historial)

if __name__=="__main__":
    main()
```

### Infracciones presentes:
1. ❌ Imports desordenados y en una línea (math,random)
2. ❌ Imports no utilizados (sys, os, json, random)
3. ❌ Falta espacios alrededor de operadores
4. ❌ Espacios inconsistentes en parámetros
5. ❌ Nombres de variables no descriptivos
6. ❌ Docstrings incompletos
7. ❌ Líneas muy largas (>79 caracteres)
8. ❌ Falta espacios después de comas

---

## 🔍 Parte 5: Detectar Infracciones

### Usar Ruff para análisis

```powershell
# Analizar el código
ruff check calculadora_profesional/

# Ver detalles de cada error
ruff check calculadora_profesional/ --show-source

# Generar reporte completo
ruff check calculadora_profesional/ --output-format=text
```

**Salida esperada:**
```
calculadora_profesional/calculadora.py:4:1: F401 [*] `sys` imported but unused
calculadora_profesional/calculadora.py:5:1: F401 [*] `os` imported but unused
calculadora_profesional/calculadora.py:7:13: E401 Multiple imports on one line
calculadora_profesional/calculadora.py:7:18: F401 [*] `random` imported but unused
calculadora_profesional/calculadora.py:8:1: F401 [*] `json` imported but unused
calculadora_profesional/calculadora.py:10:11: E231 Missing whitespace after ','
calculadora_profesional/calculadora.py:12:12: E225 Missing whitespace around operator
...
```

### Usar Black para ver cambios necesarios

```powershell
# Ver qué cambiaría Black (sin modificar)
black --check calculadora_profesional/

# Ver diff de cambios
black --diff calculadora_profesional/
```

### Usar isort para ver orden de imports

```powershell
# Ver qué cambiaría isort
isort --check-only calculadora_profesional/

# Ver diff
isort --diff calculadora_profesional/
```

---

## ⚙️ Parte 6: Configurar Herramientas

### Configuración en `pyproject.toml`

Agrega al final de `pyproject.toml`:

```toml
# ============================================================================
# CONFIGURACIÓN DE HERRAMIENTAS DE CALIDAD
# ============================================================================

[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311', 'py312']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directorios a ignorar
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
skip_gitignore = true

[tool.ruff]
# Reglas a habilitar
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings  
    "F",   # pyflakes
    "I",   # isort
    "C",   # flake8-comprehensions
    "B",   # flake8-bugbear
    "UP",  # pyupgrade
]

# Reglas a ignorar
ignore = [
    "E501",  # line too long (manejado por black)
]

# Longitud de línea
line-length = 88

# Directorios a excluir
exclude = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".hg",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "venv",
]

# Python version
target-version = "py38"

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]  # Permitir imports no usados en __init__.py
```

---

## 🔧 Parte 7: Corregir Infracciones Automáticamente

### Paso 1: Ordenar imports con isort

```powershell
# Corregir imports
isort calculadora_profesional/

# Verificar cambios
isort --check calculadora_profesional/
```

### Paso 2: Formatear código con Black

```powershell
# Formatear código
black calculadora_profesional/

# Verificar que está formateado
black --check calculadora_profesional/
```

### Paso 3: Corregir con Ruff

```powershell
# Corregir automáticamente lo posible
ruff check --fix calculadora_profesional/

# Ver errores restantes
ruff check calculadora_profesional/
```

### Código Corregido

Después de ejecutar las herramientas, el código debería verse así:

```python
# calculadora_profesional/calculadora.py
"""
Módulo de calculadora con operaciones básicas.
"""
import math
from typing import Union


def suma(a: float, b: float) -> float:
    """
    Suma dos números.

    Args:
        a: Primer número
        b: Segundo número

    Returns:
        Suma de a y b
    """
    return a + b


def resta(a: float, b: float) -> float:
    """
    Resta dos números.

    Args:
        a: Primer número
        b: Segundo número

    Returns:
        Diferencia de a y b
    """
    return a - b


def multiplicacion(x: float, y: float) -> float:
    """
    Multiplica dos números.

    Args:
        x: Primer número
        y: Segundo número

    Returns:
        Producto de x e y
    """
    resultado = x * y
    return resultado


class Calculadora:
    """
    Calculadora con historial de operaciones.

    Attributes:
        nombre: Nombre de la calculadora
        historial: Lista de operaciones realizadas
    """

    def __init__(self, nombre: str):
        """
        Inicializa la calculadora.

        Args:
            nombre: Nombre para identificar la calculadora
        """
        self.nombre = nombre
        self.historial = []

    def dividir(self, a: float, b: float) -> Union[float, None]:
        """
        Divide dos números.

        Args:
            a: Dividendo
            b: Divisor

        Returns:
            Cociente de a/b, o None si b es 0
        """
        if b == 0:
            return None
        resultado = a / b
        self.historial.append({"operacion": "division", "resultado": resultado})
        return resultado

    def potencia(self, base: float, exponente: float) -> float:
        """
        Calcula la potencia de un número.

        Args:
            base: Base de la potencia
            exponente: Exponente de la potencia

        Returns:
            base elevado a exponente
        """
        return base**exponente

    def obtener_historial(self) -> list:
        """
        Obtiene el historial de operaciones.

        Returns:
            Lista con el historial de operaciones
        """
        return self.historial


def main():
    """Función principal de demostración."""
    calc = Calculadora("MiCalc")

    print("Suma:", suma(10, 5))
    print("Resta:", resta(10, 5))
    print("Multiplicación:", multiplicacion(10, 5))
    print("División:", calc.dividir(10, 2))
    print("Potencia:", calc.potencia(2, 3))

    historial = calc.obtener_historial()
    print("Historial:", historial)


if __name__ == "__main__":
    main()
```

---

## 🔐 Parte 8: Configurar Pre-commit Hooks

### ¿Qué es Pre-commit?

**Pre-commit** ejecuta automáticamente validaciones antes de cada commit, asegurando que solo código de calidad llegue al repositorio.

### Paso 1: Crear archivo de configuración

Crea `.pre-commit-config.yaml` en la raíz del proyecto:

```yaml
# .pre-commit-config.yaml

repos:
  # Hooks básicos de pre-commit
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
        name: Eliminar espacios en blanco al final
      - id: end-of-file-fixer
        name: Asegurar nueva línea al final
      - id: check-yaml
        name: Verificar sintaxis YAML
      - id: check-json
        name: Verificar sintaxis JSON
      - id: check-toml
        name: Verificar sintaxis TOML
      - id: check-added-large-files
        name: Detectar archivos grandes
        args: ['--maxkb=500']
      - id: check-merge-conflict
        name: Detectar marcadores de merge
      - id: debug-statements
        name: Detectar declaraciones de debug

  # Black - Formateador de código
  - repo: https://github.com/psf/black
    rev: 24.2.0
    hooks:
      - id: black
        name: Formatear código con Black
        language_version: python3

  # isort - Ordenar imports
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        name: Ordenar imports con isort
        args: ["--profile", "black"]

  # Ruff - Linter
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        name: Lint con Ruff
        args: [--fix, --exit-non-zero-on-fix]
```

### Paso 2: Instalar los hooks

```powershell
# Instalar hooks de pre-commit
pre-commit install

# Verificar instalación
pre-commit --version

# Ver hooks instalados
ls .git\hooks
# Deberías ver: pre-commit
```

### Paso 3: Ejecutar pre-commit manualmente

```powershell
# Ejecutar en todos los archivos
pre-commit run --all-files

# Ejecutar solo en archivos modificados
pre-commit run

# Ejecutar un hook específico
pre-commit run black --all-files
pre-commit run isort --all-files
pre-commit run ruff --all-files
```

**Salida esperada:**
```
Eliminar espacios en blanco al final.................................Passed
Asegurar nueva línea al final.......................................Passed
Verificar sintaxis YAML..............................................Passed
Verificar sintaxis JSON..............................................Passed
Verificar sintaxis TOML..............................................Passed
Detectar archivos grandes............................................Passed
Detectar marcadores de merge.........................................Passed
Detectar declaraciones de debug......................................Passed
Formatear código con Black...........................................Passed
Ordenar imports con isort............................................Passed
Lint con Ruff........................................................Passed
```

### Paso 4: Probar pre-commit con un commit

```powershell
# Inicializar git (si no está inicializado)
git init

# Agregar archivos
git add .

# Intentar hacer commit
git commit -m "Initial commit con código de calidad"

# Pre-commit se ejecutará automáticamente antes del commit
```

Si hay errores, pre-commit:
1. ❌ Bloquea el commit
2. 🔧 Intenta corregir automáticamente
3. 📝 Te pide que revises y vuelvas a agregar los archivos

```powershell
# Si hubo correcciones automáticas
git add .
git commit -m "Initial commit con código de calidad"
```

---

## 📊 Parte 9: Verificación y Reportes

### Crear script de verificación

Crea `scripts/check_quality.py`:

```python
"""
Script para verificar calidad de código.
"""
import subprocess
import sys


def run_command(command: list, description: str) -> bool:
    """
    Ejecuta un comando y reporta el resultado.

    Args:
        command: Lista con el comando y argumentos
        description: Descripción del comando

    Returns:
        True si exitoso, False si falla
    """
    print(f"\n{'='*70}")
    print(f"🔍 {description}")
    print(f"{'='*70}")

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ {description}: PASSED")
        if result.stdout:
            print(result.stdout)
        return True
    else:
        print(f"❌ {description}: FAILED")
        if result.stderr:
            print(result.stderr)
        if result.stdout:
            print(result.stdout)
        return False


def main():
    """Función principal."""
    print("\n" + "🐍" * 35)
    print("    VERIFICACIÓN DE CALIDAD DE CÓDIGO")
    print("🐍" * 35)

    checks = [
        (["black", "--check", "calculadora_profesional/"], "Black - Formato"),
        (["isort", "--check-only", "calculadora_profesional/"], "isort - Imports"),
        (["ruff", "check", "calculadora_profesional/"], "Ruff - Linting"),
    ]

    results = []
    for command, description in checks:
        results.append(run_command(command, description))

    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)

    total = len(results)
    passed = sum(results)
    failed = total - passed

    print(f"Total de verificaciones: {total}")
    print(f"✅ Exitosas: {passed}")
    print(f"❌ Fallidas: {failed}")

    if all(results):
        print("\n🎉 ¡Todas las verificaciones pasaron!")
        sys.exit(0)
    else:
        print("\n⚠️  Algunas verificaciones fallaron. Revisa los errores arriba.")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### Ejecutar verificación

```powershell
# Ejecutar script de verificación
python scripts/check_quality.py
```

---

## 📚 Parte 10: Recursos y Comandos Útiles

### Comandos Rápidos

```powershell
# Formatear todo el proyecto
black .
isort .

# Verificar sin modificar
black --check .
isort --check-only .
ruff check .

# Ver diferencias
black --diff .
isort --diff .

# Corregir automáticamente
ruff check --fix .

# Actualizar pre-commit hooks
pre-commit autoupdate

# Limpiar cache de pre-commit
pre-commit clean
```

### Scripts útiles en pyproject.toml

Agrega estos scripts a `pyproject.toml`:

```toml
[tool.poetry.scripts]
format = "scripts:format_code"
lint = "scripts:lint_code"
check = "scripts:check_quality"
```

Crea `scripts/__init__.py`:

```python
"""Scripts de utilidad."""
import subprocess


def format_code():
    """Formatear código."""
    subprocess.run(["black", "."])
    subprocess.run(["isort", "."])


def lint_code():
    """Ejecutar linting."""
    subprocess.run(["ruff", "check", "."])


def check_quality():
    """Verificar calidad."""
    subprocess.run(["black", "--check", "."])
    subprocess.run(["isort", "--check-only", "."])
    subprocess.run(["ruff", "check", "."])
```

Uso:
```powershell
poetry run format  # Formatear
poetry run lint    # Lint
poetry run check   # Verificar
```


---

## 📖 Referencias

- **Poetry:** https://python-poetry.org/docs/
- **Black:** https://black.readthedocs.io/
- **isort:** https://pycqa.github.io/isort/
- **Ruff:** https://docs.astral.sh/ruff/
- **Pre-commit:** https://pre-commit.com/
- **PEP 8:** https://peps.python.org/pep-0008/

---
