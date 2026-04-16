"""
Módulo 10: Pruebas y TDD
05 - Cobertura de Código y CI/CD

COBERTURA (Code Coverage): métrica que mide qué porcentaje del código
es ejecutado por tus tests.

Tipos de cobertura:
- Line Coverage: % de líneas ejecutadas
- Branch Coverage: % de ramas (if/else) ejecutadas
- Function Coverage: % de funciones llamadas
- Path Coverage: % de caminos de ejecución únicos

¿Por qué importa?
✅ Identifica código no testeado
✅ Mejora confianza en refactoring
✅ Detecta código muerto
❌ NO garantiza calidad (100% coverage != bug-free)
❌ NO reemplaza buenos tests (coverage es métrica, no objetivo)

Instalación: pip install pytest-cov coverage[toml]
"""

import pytest
from typing import Optional, List


# =============================================================================
# EJEMPLO 1: Función Simple - Coverage Básico
# =============================================================================

def calculate_discount(price: float, is_member: bool) -> float:
    """
    Calcula descuento: 10% para miembros, 0% para no-miembros.
    
    Cobertura inicial: 50% (solo testea una rama)
    Cobertura mejorada: 100% (testea ambas ramas)
    """
    if is_member:
        return price * 0.9  # 10% descuento
    else:
        return price  # Sin descuento


# Test con cobertura parcial (50%)
def test_discount_member_only():
    """
    Solo testea la rama is_member=True.
    Cobertura: 50% (ejecuta línea 45, NO ejecuta línea 47)
    """
    assert calculate_discount(100, True) == 90


# Tests con cobertura completa (100%)
def test_discount_member():
    """Testea rama is_member=True."""
    assert calculate_discount(100, True) == 90


def test_discount_non_member():
    """Testea rama is_member=False."""
    assert calculate_discount(100, False) == 100


# =============================================================================
# EJEMPLO 2: Branch Coverage - If/Elif/Else
# =============================================================================

def get_grade(score: int) -> str:
    """
    Convierte puntuación a letra.
    
    Ramas a testear: 5 (A, B, C, D, F)
    Branch Coverage = (ramas ejecutadas / ramas totales) * 100
    """
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'


# Tests completos para 100% branch coverage
class TestGradeBranchCoverage:
    """
    Suite que logra 100% branch coverage.
    Cada test ejecuta una rama diferente.
    """
    
    def test_grade_a(self):
        assert get_grade(95) == 'A'
    
    def test_grade_b(self):
        assert get_grade(85) == 'B'
    
    def test_grade_c(self):
        assert get_grade(75) == 'C'
    
    def test_grade_d(self):
        assert get_grade(65) == 'D'
    
    def test_grade_f(self):
        assert get_grade(50) == 'F'


# =============================================================================
# EJEMPLO 3: Código No Alcanzable - Dead Code Detection
# =============================================================================

def process_data(data: Optional[str]) -> str:
    """
    Procesa datos.
    
    Coverage detectará que la línea después del return es inalcanzable.
    """
    if data is None:
        return "Empty"
    
    return data.upper()
    
    # Esta línea NUNCA se ejecutará (dead code)
    # Coverage mostrará 0% para esta línea
    print("This is unreachable")  # pragma: no cover


def test_process_data_none():
    assert process_data(None) == "Empty"


def test_process_data_with_value():
    assert process_data("hello") == "HELLO"


# =============================================================================
# EJEMPLO 4: Mejorando Coverage - De 60% a 100%
# =============================================================================

class Calculator:
    """
    Calculadora con múltiples métodos.
    Ejemplo de cómo ir mejorando coverage paso a paso.
    """
    
    def add(self, a: float, b: float) -> float:
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, base: float, exponent: int) -> float:
        if exponent < 0:
            raise ValueError("Negative exponents not supported")
        return base ** exponent


# Paso 1: Tests iniciales (Coverage ~40%)
class TestCalculatorPhase1:
    """
    Solo testea 2 de 5 métodos.
    Coverage: ~40%
    """
    def setup_method(self):
        self.calc = Calculator()
    
    def test_add(self):
        assert self.calc.add(2, 3) == 5
    
    def test_subtract(self):
        assert self.calc.subtract(5, 3) == 2


# Paso 2: Añadir más tests (Coverage ~80%)
class TestCalculatorPhase2:
    """
    Añade multiply y divide (camino feliz).
    Coverage: ~80% (falta testar excepciones)
    """
    def setup_method(self):
        self.calc = Calculator()
    
    def test_add(self):
        assert self.calc.add(2, 3) == 5
    
    def test_subtract(self):
        assert self.calc.subtract(5, 3) == 2
    
    def test_multiply(self):
        assert self.calc.multiply(4, 5) == 20
    
    def test_divide(self):
        assert self.calc.divide(10, 2) == 5


# Paso 3: Tests completos (Coverage 100%)
class TestCalculatorPhase3:
    """
    Suite completa con todos los métodos y edge cases.
    Coverage: 100%
    """
    def setup_method(self):
        self.calc = Calculator()
    
    def test_add(self):
        assert self.calc.add(2, 3) == 5
    
    def test_subtract(self):
        assert self.calc.subtract(5, 3) == 2
    
    def test_multiply(self):
        assert self.calc.multiply(4, 5) == 20
    
    def test_divide(self):
        assert self.calc.divide(10, 2) == 5
    
    def test_divide_by_zero(self):
        """Testea rama de excepción."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)
    
    def test_power(self):
        assert self.calc.power(2, 3) == 8
    
    def test_power_negative_exponent(self):
        """Testea rama de excepción."""
        with pytest.raises(ValueError, match="Negative exponents"):
            self.calc.power(2, -1)


# =============================================================================
# EJEMPLO 5: Excluding Code from Coverage - pragma: no cover
# =============================================================================

def debug_function(data):
    """
    Función que solo se usa en debugging.
    Usamos 'pragma: no cover' para excluirla de coverage.
    """
    if __debug__:  # pragma: no cover
        print(f"Debug: {data}")
        return "debug_mode"
    return "production_mode"


def main():  # pragma: no cover
    """
    Entry point que no necesita coverage.
    CLI/main functions típicamente se excluyen.
    """
    print("Running application...")
    # Código de inicialización
    pass


# =============================================================================
# EJEMPLO 6: Coverage en Código Asíncrono
# =============================================================================

import asyncio


async def fetch_data(url: str) -> str:
    """
    Simula petición asíncrona.
    Coverage funciona igual con código async.
    """
    await asyncio.sleep(0.1)
    
    if url.startswith("https://"):
        return f"Data from {url}"
    else:
        raise ValueError("Only HTTPS supported")


@pytest.mark.asyncio
async def test_fetch_data_success():
    """Testea rama exitosa."""
    result = await fetch_data("https://api.example.com")
    assert "Data from" in result


@pytest.mark.asyncio
async def test_fetch_data_invalid_protocol():
    """Testea rama de error."""
    with pytest.raises(ValueError, match="Only HTTPS"):
        await fetch_data("http://api.example.com")


# =============================================================================
# EJEMPLO 7: Coverage con Context Managers
# =============================================================================

class FileHandler:
    """
    Context manager para manejo de archivos.
    Coverage debe incluir __enter__ y __exit__.
    """
    
    def __init__(self, filename: str):
        self.filename = filename
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, 'w')
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        
        # Manejar excepciones
        if exc_type is ValueError:
            print(f"Handled ValueError: {exc_val}")
            return True  # Suprimir excepción
        return False  # Propagar otras excepciones


def test_file_handler_success(tmp_path):
    """Testea uso normal del context manager."""
    filepath = tmp_path / "test.txt"
    
    with FileHandler(str(filepath)) as f:
        f.write("Hello")
    
    assert filepath.read_text() == "Hello"


def test_file_handler_with_exception(tmp_path):
    """Testea rama de manejo de excepciones en __exit__."""
    filepath = tmp_path / "test.txt"
    
    # ValueError es manejado por __exit__ (retorna True)
    with FileHandler(str(filepath)):
        raise ValueError("Test error")
    
    # El archivo debe cerrarse correctamente
    assert filepath.exists()


# =============================================================================
# CONFIGURACIÓN DE COVERAGE
# =============================================================================

"""
# pyproject.toml
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__main__.py",
]
branch = true  # Habilita branch coverage

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
fail_under = 80  # Falla si coverage < 80%

exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstractmethod",
]

[tool.coverage.html]
directory = "htmlcov"

[tool.coverage.xml]
output = "coverage.xml"
"""

# =============================================================================
# PYTEST-COV COMMANDS
# =============================================================================

"""
COMANDOS BÁSICOS:
==================

# Ejecutar tests con coverage
pytest --cov=src

# Coverage con reporte en terminal
pytest --cov=src --cov-report=term

# Coverage con líneas faltantes
pytest --cov=src --cov-report=term-missing

# Coverage con HTML (genera htmlcov/index.html)
pytest --cov=src --cov-report=html

# Coverage con XML (para CI/CD)
pytest --cov=src --cov-report=xml

# Coverage con múltiples formatos
pytest --cov=src --cov-report=term --cov-report=html --cov-report=xml

# Fallar si coverage < 80%
pytest --cov=src --cov-fail-under=80

# Coverage solo para archivos modificados
pytest --cov=src --cov-report=term-missing --cov-branch


LEER REPORTES:
==============

Terminal Report:
----------------
Name                Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------
src/calculator.py      20      2      8      1    85%   45, 67
src/user.py           15      0      4      0   100%

- Stmts: total de statements
- Miss: statements no ejecutados
- Branch: total de ramas
- BrPart: ramas parcialmente cubiertas
- Cover: % de cobertura
- Missing: líneas no cubiertas

HTML Report (htmlcov/index.html):
----------------------------------
- Vista general de todos los archivos
- Drill-down a archivos individuos
- Líneas verdes: cubiertas
- Líneas rojas: no cubiertas
- Líneas amarillas: ramas parciales
- Navegación con teclado: n (next), p (previous)


COVERAGE.PY DIRECTO:
====================

# Ejecutar con coverage
coverage run -m pytest

# Generar reporte
coverage report

# Generar HTML
coverage html

# Ver líneas específicas no cubiertas
coverage report --show-missing

# Combinar coverage de múltiples runs
coverage combine

# Borrar datos de coverage
coverage erase
"""

# =============================================================================
# INTEGRACIÓN CI/CD - GITHUB ACTIONS
# =============================================================================

"""
# .github/workflows/tests.yml

name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests with coverage
      run: |
        pytest --cov=src --cov-report=xml --cov-report=term-missing
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: true
    
    - name: Check coverage threshold
      run: |
        pytest --cov=src --cov-fail-under=80
"""

# =============================================================================
# INTEGRACIÓN CI/CD - GITLAB CI
# =============================================================================

"""
# .gitlab-ci.yml

stages:
  - test
  - coverage

test:
  stage: test
  image: python:3.11
  
  before_script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
  
  script:
    - pytest --cov=src --cov-report=term --cov-report=xml
  
  coverage: '/(?i)total.*? (100(?:\\.0+)?\\%|[1-9]?\\d(?:\\.\\d+)?\\%)$/'
  
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
    paths:
      - htmlcov/
    expire_in: 30 days

coverage_check:
  stage: coverage
  image: python:3.11
  
  before_script:
    - pip install coverage
  
  script:
    - coverage report --fail-under=80
  
  dependencies:
    - test
"""

# =============================================================================
# PRE-COMMIT HOOK PARA COVERAGE
# =============================================================================

"""
# .pre-commit-config.yaml

repos:
  - repo: local
    hooks:
      - id: pytest-coverage
        name: pytest with coverage
        entry: pytest
        args: [--cov=src, --cov-fail-under=80]
        language: system
        pass_filenames: false
        always_run: true
        stages: [commit]
"""

# =============================================================================
# BADGES DE COVERAGE
# =============================================================================

"""
CODECOV BADGE:
==============
[![codecov](https://codecov.io/gh/username/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/username/repo)

COVERALLS BADGE:
================
[![Coverage Status](https://coveralls.io/repos/github/username/repo/badge.svg?branch=main)](https://coveralls.io/github/username/repo?branch=main)

GITHUB ACTIONS BADGE:
=====================
[![Tests](https://github.com/username/repo/actions/workflows/tests.yml/badge.svg)](https://github.com/username/repo/actions/workflows/tests.yml)
"""

# =============================================================================
# EJEMPLO 8: Estrategia de Coverage en Proyecto Real
# =============================================================================

"""
ESTRATEGIA RECOMENDADA:
=======================

1. OBJETIVO INICIAL: 70-80%
   - Cubre lógica de negocio crítica
   - No desperdicies tiempo en 100% de código trivial

2. PRIORIZAR:
   ✅ Alta prioridad (>90% coverage):
      - Lógica de negocio
      - Cálculos financieros
      - Seguridad / autenticación
      - Procesamiento de datos
   
   ✅ Media prioridad (70-80%):
      - Utilities
      - Helpers
      - Validaciones
   
   ✅ Baja prioridad (50-60%):
      - UI código
      - Scripts de migración
      - Código de configuración

3. EXCLUIR:
   ❌ No testear:
      - Archivos __init__.py vacíos
      - Código de terceros
      - Settings/configuración
      - Debug utilities

4. MONITOREAR:
   - Coverage debe CRECER con el tiempo
   - Nueva features requieren tests (fail_under=current%)
   - PR reviews: incluir chequeo de coverage

5. MÉTRICAS:
   - Line coverage: 80%+
   - Branch coverage: 75%+
   - Método: ningún archivo con <60%


WORKFLOW:
=========

1. Desarrollo con TDD:
   $ pytest --cov=src --cov-report=term-missing
   
2. Identificar gaps:
   $ coverage html
   $ open htmlcov/index.html
   
3. Escribir tests para líneas rojas/amarillas
   
4. Verificar threshold:
   $ pytest --cov=src --cov-fail-under=80
   
5. Commit:
   Pre-commit hook ejecuta tests automáticamente
   
6. CI/CD:
   GitHub Actions ejecuta tests y sube a Codecov


TIPS:
=====

✅ DO:
- Usar coverage como herramienta de exploración
- Combinar con mutation testing (mutmut, cosmic-ray)
- Revisar trends de coverage en el tiempo
- Documentar por qué ciertas líneas tienen pragma: no cover

❌ DON'T:
- Obsesionarse con 100% (rendimientos decrecientes)
- Escribir tests malos solo para coverage
- Ignorar branch coverage (tan importante como line)
- Confiar solo en coverage (necesitas buenos assertions)
"""

# =============================================================================
# EJEMPLO 9: Coverage con Múltiples Módulos
# =============================================================================

# Estructura de proyecto:
"""
project/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── auth.py
│   └── utils/
│       ├── __init__.py
│       └── validators.py
├── tests/
│   ├── __init__.py
│   ├── test_user.py
│   ├── test_auth.py
│   └── test_validators.py
└── pyproject.toml

# Ejecutar coverage para todo el proyecto
$ pytest --cov=src --cov-report=html

# Coverage por paquete
$ pytest --cov=src.models --cov=src.services --cov-report=term

# Coverage incremental (solo archivos modificados)
$ pytest --cov=src --cov-report=term --cov-context=test

# Coverage con filtros
$ pytest --cov=src --cov-report=term --cov-config=.coveragerc
"""

# =============================================================================
# RESUMEN DE CONCEPTOS
# =============================================================================

"""
TIPOS DE COVERAGE:
==================
1. Line Coverage: % líneas ejecutadas
2. Branch Coverage: % ramas if/else ejecutadas
3. Function Coverage: % funciones llamadas
4. Path Coverage: % caminos únicos ejecutados

COMANDOS ESENCIALES:
====================
pytest --cov=src                        # Coverage básico
pytest --cov=src --cov-report=html      # Generar HTML
pytest --cov=src --cov-report=term-missing  # Mostrar líneas faltantes
pytest --cov=src --cov-fail-under=80    # Fallar si <80%
pytest --cov=src --cov-branch           # Branch coverage

CONFIGURACIÓN:
==============
pyproject.toml:
  [tool.coverage.run]
    source = ["src"]
    branch = true
  
  [tool.coverage.report]
    fail_under = 80
    show_missing = true
    exclude_lines = ["pragma: no cover"]

CI/CD:
======
- GitHub Actions: pytest + codecov-action
- GitLab CI: coverage regex + artifacts
- Pre-commit: pytest hook con fail_under

PRAGMAS:
========
# pragma: no cover          # Excluir línea
if __name__ == "__main__":  # Típicamente excluido
    main()  # pragma: no cover

BEST PRACTICES:
===============
✅ DO:
- Apuntar a 80% line coverage
- Priorizar código crítico de negocio
- Usar coverage para encontrar gaps
- Combinar con mutation testing
- Monitorear trends

❌ DON'T:
- Obsesionarse con 100%
- Escribir tests malos por coverage
- Ignorar branch coverage
- Confiar solo en métricas
- Incluir tests en coverage
"""

# =============================================================================
# EJERCICIO PRÁCTICO
# =============================================================================

"""
EJERCICIO: Mejorar Coverage
============================

1. Ejecuta tests actuales:
   $ pytest --cov=. --cov-report=html
   
2. Abre htmlcov/index.html en navegador

3. Identifica archivos con coverage <80%

4. Para cada archivo:
   - Revisa líneas rojas (no cubiertas)
   - Revisa líneas amarillas (ramas parciales)
   - Escribe tests para cubrir esas líneas

5. Verifica mejora:
   $ pytest --cov=. --cov-report=term-missing

6. Objetivo: Lograr 85% de coverage

TIPS:
- Enfócate en lógica de negocio primero
- Tests de excepciones suben coverage rápido
- Branch coverage requiere if/else completo
- Usa parametrize para múltiples casos
"""
