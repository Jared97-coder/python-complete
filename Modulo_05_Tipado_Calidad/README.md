# Módulo 5: Tipado Estático Opcional y Calidad de Código

## Objetivos de aprendizaje
- Anotar tipos y verificar estáticamente con mypy/pyright
- Hacer cumplir PEP 8 y documentar excepciones
- Integrar linters/formatters en CI/CD
- Aplicar PEP 20 (Zen of Python) como guía de diseño
- Automatizar verificaciones de calidad con pre-commit

## Contenidos

### 1. Type Hints Básicos
**Archivo:** `01_type_hints_basicos.py`

Conceptos fundamentales:
- Anotaciones de tipos para variables, funciones y métodos
- Tipos básicos: int, str, float, bool, None
- Tipos compuestos: List, Dict, Set, Tuple
- Optional y Union
- Type aliases
- Beneficios y limitaciones del tipado gradual

### 2. Typing Avanzado
**Archivo:** `02_typing_avanzado.py`

Conceptos avanzados:
- **Union** y tipos de unión (| en Python 3.10+)
- **Literal** para valores literales específicos
- **TypedDict** para diccionarios con estructura conocida
- **Protocol** para duck typing estructurado
- **Generic** y **TypeVar** para tipos genéricos
- **Callable** para funciones como tipos
- **overload** para múltiples firmas
- **NewType** para tipos distintos semánticamente
- **Any** y **cast** (usar con precaución)

### 3. Verificadores de Tipos Estáticos
**Archivo:** `03_mypy_pyright.py`

**mypy:**
- Configuración y uso básico
- Strict mode y configuraciones incrementales
- Type ignore comments y cuándo usarlos
- Manejo de librerías sin tipos (stubs)
- Errores comunes y cómo solucionarlos

**pyright/pylance:**
- Integración con VS Code
- Modos de análisis (basic, standard, strict)
- Ventajas sobre mypy
- Configuración en pyproject.toml

### 4. PEP 8 y Herramientas de Calidad
**Archivo:** `04_pep8_formatters.py`

**Formateadores:**
- **Black** - The Uncompromising Code Formatter
- **isort** - Ordenar imports automáticamente
- Configuración y personalización mínima

**Linters:**
- **Ruff** - Linter ultrarrápido (reemplaza flake8, pylint, isort)
- **pylint** - Análisis exhaustivo (opcional)
- Reglas importantes de PEP 8
- Documentar excepciones con # noqa y # type: ignore

**PEP 20 - Zen of Python:**
- Principios de diseño de código Pythonic
- Aplicación práctica de los principios

### 5. Pre-commit y CI/CD
**Archivo:** `05_pre_commit_ci.py`

**Pre-commit hooks:**
- Instalación y configuración
- Hooks comunes (black, ruff, mypy)
- Crear hooks personalizados
- Workflow de desarrollo

**CI/CD:**
- GitHub Actions para verificación de calidad
- Azure Pipelines
- Cacheo de dependencias
- Reportes de cobertura

## Estructura de archivos
```
Modulo_05_Tipado_Calidad/
├── 01_type_hints_basicos.py       # Type hints fundamentales
├── 02_typing_avanzado.py          # Union, Literal, Protocol, etc.
├── 03_mypy_pyright.py             # Verificadores de tipos
├── 04_pep8_formatters.py          # PEP 8, black, ruff
├── 05_pre_commit_ci.py            # Automatización de calidad
├── ejemplos/
│   ├── antes_tipos.py             # Código sin tipos
│   ├── despues_tipos.py           # Mismo código con tipos
│   ├── antes_format.py            # Código sin formatear
│   └── despues_format.py          # Código formateado
├── config/
│   ├── pyproject.toml             # Configuración centralizada
│   ├── .pre-commit-config.yaml   # Pre-commit hooks
│   └── mypy.ini                   # Configuración de mypy (alternativa)
├── LABORATORIO.md                 # Ejercicios prácticos
├── EJERCICIOS.md                  # Ejercicios adicionales
├── README.md                      # Este archivo
└── requirements.txt               # Dependencias del módulo
```

## Instalación de dependencias
```bash
pip install -r requirements.txt
```

## Instalación de pre-commit
```bash
# Instalar pre-commit hooks
pre-commit install

# Ejecutar en todos los archivos
pre-commit run --all-files
```

## Comandos útiles

### Type checking
```bash
# mypy
mypy archivo.py
mypy . --strict

# pyright
pyright archivo.py
pyright --stats
```

### Formateo y linting
```bash
# Black (formatear)
black archivo.py
black .

# isort (ordenar imports)
isort archivo.py
isort .

# Ruff (lint y fix)
ruff check archivo.py
ruff check . --fix

# Ruff también puede formatear (alternativa a black)
ruff format archivo.py
```

### Verificación completa
```bash
# Ejecutar todas las verificaciones
black --check .
ruff check .
mypy .
```

## Progresión sugerida
1. **01_type_hints_basicos.py** - Fundamentos de type hints
2. **02_typing_avanzado.py** - Conceptos avanzados
3. **03_mypy_pyright.py** - Verificación estática
4. **04_pep8_formatters.py** - Calidad de código
5. **05_pre_commit_ci.py** - Automatización
6. **LABORATORIO.md** - Aplicación práctica

## Recursos adicionales
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [PEP 8 - Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [PEP 20 - Zen of Python](https://www.python.org/dev/peps/pep-0020/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Black Documentation](https://black.readthedocs.io/)
- [pre-commit](https://pre-commit.com/)

## Notas importantes

### Tipado gradual
Python es de tipado dinámico, los type hints son **opcionales** y **no se verifican en runtime**:
- Úsalos como documentación viva
- Detecta errores en desarrollo, no en producción
- Adopción incremental: puedes empezar con lo mínimo

### Herramientas recomendadas
- **Para proyectos nuevos**: Usar `ruff` (todo en uno, ultrarrápido)
- **Para proyectos existentes**: Migración incremental con configuración flexible
- **Pre-commit**: Obligatorio para equipos

### Filosofía
> "Explicit is better than implicit" - PEP 20

Los type hints y las herramientas de calidad hacen el código más:
- **Legible**: Documentación en el código
- **Mantenible**: Detectar errores temprano
- **Confiable**: Menos bugs en producción
- **Colaborativo**: Estándares compartidos
