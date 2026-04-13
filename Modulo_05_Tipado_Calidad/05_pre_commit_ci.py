"""
Módulo 5.5: Pre-commit Hooks y CI/CD
====================================

Conceptos:
- Pre-commit hooks para validación automática
- Configuración de hooks (black, ruff, mypy)
- CI/CD con GitHub Actions y Azure Pipelines
- Workflows de desarrollo con calidad automatizada

INSTALACIÓN:
    pip install pre-commit
    pre-commit install
    
COMANDOS ÚTILES:
    pre-commit install           # Instalar hooks en .git/hooks/
    pre-commit run --all-files   # Ejecutar en todos los archivos
    pre-commit run <hook-id>     # Ejecutar hook específico
    pre-commit autoupdate        # Actualizar versiones de hooks
"""

# ============================================================================
# 1. QUÉ ES PRE-COMMIT
# ============================================================================

"""
Pre-commit es un framework para manejar git pre-commit hooks.

BENEFICIOS:
- Validación automática antes de cada commit
- Detección temprana de problemas
- Código formateado consistentemente
- No llegar código malo a CI
- Ahorro de tiempo en revisiones de código

HOOKS COMUNES:
1. trailing-whitespace: Elimina espacios al final de línea
2. end-of-file-fixer: Asegura línea nueva al final de archivo
3. check-yaml: Valida sintaxis YAML
4. check-json: Valida sintaxis JSON
5. black: Formateo de código
6. ruff: Linting
7. mypy: Type checking
8. isort: Ordenar imports
"""


# ============================================================================
# 2. CONFIGURACIÓN .pre-commit-config.yaml
# ============================================================================

EJEMPLO_PRE_COMMIT_CONFIG = """
# .pre-commit-config.yaml
# Ver https://pre-commit.com para más información

repos:
  # Hooks básicos de pre-commit
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace       # Eliminar espacios al final
      - id: end-of-file-fixer         # Nueva línea al final
      - id: check-yaml                # Validar YAML
      - id: check-json                # Validar JSON
      - id: check-toml                # Validar TOML
      - id: check-added-large-files   # Evitar archivos grandes
        args: ['--maxkb=1000']
      - id: check-merge-conflict      # Detectar conflictos de merge
      - id: debug-statements          # Detectar print/pdb
      - id: mixed-line-ending         # Consistencia de line endings

  # Black - Formateo de código
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
        language_version: python3.11
        args: ['--line-length=88']

  # Ruff - Linting y auto-fix
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.2.0
    hooks:
      # Linter
      - id: ruff
        args: ['--fix', '--exit-non-zero-on-fix']
      # Formatear (alternativa a black)
      # - id: ruff-format

  # isort - Ordenar imports
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ['--profile=black']

  # mypy - Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests, types-PyYAML]
        args: ['--ignore-missing-imports']

  # Validación de commits (opcional)
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.0.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]

# Configuración global
default_language_version:
  python: python3.11

# Archivos a excluir
exclude: |
  (?x)^(
      migrations/.*|
      .*/migrations/.*|
      .*_pb2.py|
      docs/.*
  )$
"""


# ============================================================================
# 3. WORKFLOW DE DESARROLLO CON PRE-COMMIT
# ============================================================================

"""
WORKFLOW TÍPICO:

1. Desarrollador hace cambios en código

2. Intenta hacer commit:
   git add archivo.py
   git commit -m "Agregar nueva funcionalidad"

3. Pre-commit se ejecuta automáticamente:
   [INFO] Initializing environment for hooks...
   [INFO] Running hook: trailing-whitespace...Passed
   [INFO] Running hook: black.....................Passed
   [INFO] Running hook: ruff......................Passed
   [INFO] Running hook: mypy......................Passed
   
4a. Si todo pasa: Commit se completa ✅

4b. Si algo falla:
    [INFO] Running hook: black.....................Failed
    - hook id: black
    - files were modified by this hook
    
    Archivos formateados automáticamente.
    
    - El commit NO se completa
    - El desarrollador debe:
      * Revisar los cambios que hizo black/ruff
      * git add archivo.py  (agregar los cambios)
      * git commit -m "..." (reintentar)

5. Push a repositorio remoto

6. CI/CD ejecuta las mismas verificaciones (doble seguridad)
"""


# ============================================================================
# 4. EJECUTAR PRE-COMMIT MANUALMENTE
# ============================================================================

"""
# Ejecutar en archivos staged (por defecto)
pre-commit run

# Ejecutar en TODOS los archivos (primera vez o después de cambios)
pre-commit run --all-files

# Ejecutar hook específico
pre-commit run black --all-files
pre-commit run mypy --all-files

# Ejecutar en archivos específicos
pre-commit run --files src/main.py src/utils.py

# Ver lista de hooks disponibles
pre-commit run --hook-stage manual --all-files

# Saltarse pre-commit en un commit (NO RECOMENDADO)
git commit --no-verify -m "mensaje"
"""


# ============================================================================
# 5. CI/CD - GITHUB ACTIONS
# ============================================================================

EJEMPLO_GITHUB_ACTIONS = """
# .github/workflows/quality.yml
name: Code Quality

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  quality:
    name: Code Quality Checks
    runs-on: ubuntu-latest
    
    steps:
      # Checkout código
      - uses: actions/checkout@v4
      
      # Configurar Python
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      # Instalar dependencias
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install black ruff mypy
      
      # Black - Verificar formato
      - name: Check code formatting with Black
        run: black --check .
      
      # Ruff - Linting
      - name: Lint with Ruff
        run: ruff check .
      
      # mypy - Type checking
      - name: Type check with mypy
        run: mypy .
        continue-on-error: true  # No fallar si hay errores de tipos
      
      # Tests (si hay)
      - name: Run tests
        run: |
          pip install pytest pytest-cov
          pytest --cov=. --cov-report=xml
      
      # Upload coverage (opcional)
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: false

  # Job adicional para verificación de seguridad
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install bandit
        run: pip install bandit
      
      - name: Run security scan
        run: bandit -r . -f json -o bandit-report.json
        continue-on-error: true
      
      - name: Upload security report
        uses: actions/upload-artifact@v3
        with:
          name: bandit-report
          path: bandit-report.json
"""


# ============================================================================
# 6. CI/CD - AZURE PIPELINES
# ============================================================================

EJEMPLO_AZURE_PIPELINES = """
# azure-pipelines.yml
trigger:
  - main
  - develop

pool:
  vmImage: 'ubuntu-latest'

variables:
  python.version: '3.11'

stages:
  - stage: Quality
    displayName: 'Code Quality'
    jobs:
      - job: QualityChecks
        displayName: 'Quality Checks'
        
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '$(python.version)'
            displayName: 'Use Python $(python.version)'
          
          - script: |
              python -m pip install --upgrade pip
              pip install -r requirements.txt
              pip install black ruff mypy pytest pytest-cov
            displayName: 'Install dependencies'
          
          - script: |
              black --check .
            displayName: 'Check formatting with Black'
          
          - script: |
              ruff check .
            displayName: 'Lint with Ruff'
          
          - script: |
              mypy . || true
            displayName: 'Type check with mypy'
          
          - script: |
              pytest --cov=. --cov-report=html --cov-report=xml
            displayName: 'Run tests with coverage'
          
          - task: PublishTestResults@2
            inputs:
              testResultsFiles: '**/test-*.xml'
              testRunTitle: 'Python Tests'
            condition: succeededOrFailed()
          
          - task: PublishCodeCoverageResults@1
            inputs:
              codeCoverageTool: 'Cobertura'
              summaryFileLocation: '$(System.DefaultWorkingDirectory)/**/coverage.xml'
"""


# ============================================================================
# 7. CONFIGURACIÓN pyproject.toml COMPLETA
# ============================================================================

EJEMPLO_PYPROJECT_TOML = """
[project]
name = "mi-proyecto"
version = "0.1.0"
description = "Proyecto con calidad de código"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31.0",
]

[project.optional-dependencies]
dev = [
    "black>=24.0.0",
    "ruff>=0.2.0",
    "mypy>=1.8.0",
    "pre-commit>=3.6.0",
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
]

# Black
[tool.black]
line-length = 88
target-version = ['py311']
include = '\\.pyi?$'
extend-exclude = '''
/(
    \\.git
  | \\.mypy_cache
  | \\.venv
  | build
  | dist
)/
'''

# Ruff
[tool.ruff]
target-version = "py311"
line-length = 88
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by black)
]
exclude = [
    ".git",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]
"tests/*" = ["S101"]

# mypy
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
check_untyped_defs = true

[[tool.mypy.overrides]]
module = ["requests.*"]
ignore_missing_imports = true

# pytest
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--cov=src",
    "--cov-report=term-missing",
]

# Coverage
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/venv/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
"""


# ============================================================================
# 8. BADGE DE CALIDAD EN README
# ============================================================================

EJEMPLO_README_BADGES = """
# Mi Proyecto

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![type-checked: mypy](https://img.shields.io/badge/type--checked-mypy-blue.svg)](https://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![CI](https://github.com/usuario/proyecto/workflows/CI/badge.svg)](https://github.com/usuario/proyecto/actions)
[![codecov](https://codecov.io/gh/usuario/proyecto/branch/main/graph/badge.svg)](https://codecov.io/gh/usuario/proyecto)

## Instalación

```bash
pip install -r requirements.txt
pip install -e ".[dev]"  # Dependencias de desarrollo
```

## Calidad de Código

Este proyecto utiliza:
- **Black** para formateo automático
- **Ruff** para linting
- **mypy** para type checking
- **pre-commit** para validación automática

Ejecutar verificaciones:
```bash
black .
ruff check .
mypy .
```

O usar pre-commit:
```bash
pre-commit run --all-files
```
"""


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    """Información sobre pre-commit y CI/CD."""
    print("=" * 70)
    print("PRE-COMMIT Y CI/CD")
    print("=" * 70)
    
    print("\n📋 PASOS PARA CONFIGURAR PRE-COMMIT:\n")
    print("1. Crear archivo .pre-commit-config.yaml en raíz del proyecto")
    print("2. pip install pre-commit")
    print("3. pre-commit install")
    print("4. pre-commit run --all-files (primera vez)")
    print("5. Hacer commits normalmente")
    
    print("\n🔧 CONFIGURACIÓN EN pyproject.toml:\n")
    print("- [tool.black] para Black")
    print("- [tool.ruff] para Ruff")
    print("- [tool.mypy] para mypy")
    print("- [tool.pytest.ini_options] para pytest")
    
    print("\n☁️  INTEGRACIÓN CI/CD:\n")
    print("- GitHub Actions: .github/workflows/quality.yml")
    print("- Azure Pipelines: azure-pipelines.yml")
    print("- Ejecutar mismas verificaciones que pre-commit")
    
    print("\n✅ BENEFICIOS:\n")
    print("- Código consistente en todo el equipo")
    print("- Detección temprana de errores")
    print("- Menos tiempo en code reviews")
    print("- Documentación viva con badges")
    
    print("\n" + "=" * 70)
    print("VER EJEMPLOS DE CONFIGURACIÓN EN ESTE ARCHIVO")
    print("=" * 70)


if __name__ == "__main__":
    main()
