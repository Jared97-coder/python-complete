# Entornos Virtuales en Python - Guía Completa

## 📚 Índice
1. [¿Qué es un entorno virtual?](#qué-es-un-entorno-virtual)
2. [¿Por qué usar entornos virtuales?](#por-qué-usar-entornos-virtuales)
3. [Herramientas disponibles](#herramientas-disponibles)
4. [venv - Tutorial completo](#venv---tutorial-completo)
5. [virtualenv](#virtualenv)
6. [Conda](#conda)
7. [Pipenv](#pipenv)
8. [Poetry](#poetry)
9. [Mejores prácticas](#mejores-prácticas)
10. [Resolución de problemas](#resolución-de-problemas)

---

## 🎯 ¿Qué es un entorno virtual?

Un **entorno virtual** es un directorio que contiene:
- Una instalación de Python específica
- Bibliotecas y paquetes independientes
- Scripts de activación
- Aislamiento del sistema global

### Analogía
Imagina que cada proyecto es una casa 🏠:
- **Sin entorno virtual**: Todas las herramientas están en un garaje compartido (sistema global)
- **Con entorno virtual**: Cada casa tiene su propio garaje con sus propias herramientas

---

## 💡 ¿Por qué usar entornos virtuales?

### Problemas que resuelven

#### ❌ Sin entorno virtual
```
Sistema Global:
├── Django 4.2  ← Proyecto A necesita esta versión
├── Django 3.2  ← Proyecto B necesita esta versión (CONFLICTO!)
├── requests 2.31.0
└── 100+ paquetes mixtos
```

#### ✅ Con entornos virtuales
```
Proyecto A/
└── venv_A/
    └── Django 4.2

Proyecto B/
└── venv_B/
    └── Django 3.2

Sistema Global:
└── (limpio, solo Python base)
```

### Ventajas

| Ventaja | Descripción |
|---------|-------------|
| 🔒 **Aislamiento** | Cada proyecto tiene sus propias dependencias |
| 🔄 **Versionado** | Diferentes versiones del mismo paquete |
| 🧹 **Limpieza** | No contamina la instalación global |
| 📦 **Portabilidad** | Fácil de replicar con `requirements.txt` |
| 🚀 **Experimentación** | Prueba paquetes sin riesgo |
| 👥 **Colaboración** | Todo el equipo usa las mismas versiones |

---

## 🛠️ Herramientas disponibles

| Herramienta | Descripción | Cuándo usar |
|-------------|-------------|-------------|
| **venv** | Incluido en Python 3.3+ | Proyectos Python puros, simplicidad |
| **virtualenv** | Versión más rápida y con más opciones | Alternativa a venv |
| **conda** | Gestor de paquetes y entornos | Data Science, paquetes no-Python |
| **pipenv** | Combina pip y virtualenv | Gestión moderna, Pipfile |
| **poetry** | Gestión moderna de proyectos | Proyectos complejos, publicación |

---

## 📦 venv - Tutorial completo

`venv` es la herramienta estándar incluida en Python 3.3+

### Instalación
Ya está incluido en Python, no necesita instalación.

### Crear entorno virtual

```powershell
# Sintaxis básica
python -m venv nombre_entorno

# Ejemplo: crear entorno llamado "venv"
python -m venv venv

# Ejemplo: crear entorno en ubicación específica
python -m venv C:\Proyectos\mi_app\venv
```

### Estructura creada

```
venv/
├── Include/           # Archivos de cabecera C
├── Lib/              # Bibliotecas Python instaladas
│   └── site-packages/
├── Scripts/          # Ejecutables (Windows)
│   ├── activate      # Script de activación (bash)
│   ├── activate.bat  # Script de activación (cmd)
│   ├── Activate.ps1  # Script de activación (PowerShell)
│   ├── deactivate.bat
│   ├── pip.exe
│   └── python.exe
└── pyvenv.cfg        # Configuración del entorno
```

### Activar entorno virtual

#### Windows - CMD
```cmd
venv\Scripts\activate.bat
```

#### Windows - PowerShell
```powershell
venv\Scripts\Activate.ps1

# Si hay error de políticas de ejecución:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Windows - Git Bash
```bash
source venv/Scripts/activate
```

### Verificar activación

Cuando está activado, verás el prefijo en tu terminal:
```powershell
(venv) PS C:\mi_proyecto>
```

También puedes verificar:
```powershell
# Ver qué Python se está usando
where python
# Resultado: C:\mi_proyecto\venv\Scripts\python.exe

# Ver qué pip se está usando
where pip
# Resultado: C:\mi_proyecto\venv\Scripts\pip.exe
```

### Desactivar entorno

```powershell
deactivate
```

### Flujo de trabajo completo

```powershell
# 1. Crear directorio del proyecto
mkdir mi_proyecto
cd mi_proyecto

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno
venv\Scripts\Activate.ps1

# 4. Actualizar pip (recomendado)
python -m pip install --upgrade pip

# 5. Instalar paquetes
pip install requests flask pandas

# 6. Trabajar en el proyecto
python mi_script.py

# 7. Guardar dependencias
pip freeze > requirements.txt

# 8. Al terminar, desactivar
deactivate
```

### Opciones avanzadas de venv

```powershell
# Crear entorno sin pip (instalas después manualmente)
python -m venv venv --without-pip

# Permitir acceso a paquetes del sistema
python -m venv venv --system-site-packages

# Actualizar scripts del entorno
python -m venv venv --upgrade

# Ver configuración del entorno
type venv\pyvenv.cfg
```

---

## 🔧 virtualenv

Alternativa más potente a venv.

### Instalación
```powershell
pip install virtualenv
```

### Uso básico

```powershell
# Crear entorno
virtualenv venv

# Con versión específica de Python
virtualenv -p python3.11 venv

# Activar (igual que venv)
venv\Scripts\activate
```

### Ventajas sobre venv
- Más rápido
- Soporta más versiones de Python
- Más opciones de configuración
- Funciona en Python 2.7 (ya obsoleto)

---

## 🐍 Conda

Gestor de paquetes y entornos, especialmente popular en Data Science.

### Instalación
Descarga [Anaconda](https://www.anaconda.com/) o [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

### Uso básico

```powershell
# Crear entorno
conda create -n mi_entorno python=3.11

# Activar
conda activate mi_entorno

# Instalar paquetes
conda install numpy pandas matplotlib

# Listar entornos
conda env list

# Desactivar
conda deactivate

# Eliminar entorno
conda env remove -n mi_entorno

# Exportar entorno
conda env export > environment.yml

# Crear desde archivo
conda env create -f environment.yml
```

### Ventajas
- Gestiona paquetes no-Python (C, R, etc.)
- Excelente para Data Science
- Resuelve dependencias complejas
- Incluye muchos paquetes preinstalados

---

## 🔐 Pipenv

Combina pip y virtualenv en una herramienta moderna.

### Instalación
```powershell
pip install pipenv
```

### Uso básico

```powershell
# Crear entorno e instalar paquete
pipenv install requests

# Instalar paquetes de desarrollo
pipenv install --dev pytest black

# Activar shell del entorno
pipenv shell

# Ejecutar comando en el entorno sin activarlo
pipenv run python script.py

# Ver ubicación del entorno
pipenv --venv

# Instalar desde Pipfile
pipenv install

# Generar requirements.txt
pipenv requirements > requirements.txt
```

### Archivos generados

**Pipfile**
```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "*"
flask = "==2.3.0"

[dev-packages]
pytest = "*"
black = "*"

[requires]
python_version = "3.11"
```

**Pipfile.lock**
- Versiones exactas bloqueadas
- Hash de seguridad
- Reproducibilidad garantizada

---

## 📝 Poetry

Herramienta moderna para gestión de dependencias y empaquetado.

### Instalación
```powershell
# Windows PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### Uso básico

```powershell
# Crear nuevo proyecto
poetry new mi_proyecto

# Inicializar en proyecto existente
poetry init

# Instalar dependencias
poetry add requests

# Instalar dependencias de desarrollo
poetry add --group dev pytest

# Instalar desde pyproject.toml
poetry install

# Activar shell
poetry shell

# Ejecutar comando
poetry run python script.py

# Compilar paquete
poetry build

# Publicar en PyPI
poetry publish
```

### pyproject.toml
```toml
[tool.poetry]
name = "mi-proyecto"
version = "0.1.0"
description = ""
authors = ["Tu Nombre <email@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
requests = "^2.31.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.7.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

---

## ✅ Mejores prácticas

### 1. Nombrar entornos
```powershell
# ✅ Bueno: nombres estándar
venv/
.venv/
env/

# ❌ Evitar: nombres únicos por proyecto
mi_proyecto_entorno/
entorno_django/
```

### 2. Gitignore
Siempre excluye entornos del control de versiones:

```gitignore
# Entornos virtuales
venv/
env/
ENV/
.venv/

# Conda
env/
conda/

# Pipenv
.venv/

# Poetry
.venv/
```

### 3. Requirements.txt

```powershell
# Generar
pip freeze > requirements.txt

# Mejora: solo dependencias directas
pip install pipreqs
pipreqs . --force

# Instalar
pip install -r requirements.txt
```

### 4. Estructura de proyecto

```
mi_proyecto/
│
├── venv/                  # ❌ NO versionar
├── src/                   # ✅ Tu código
│   ├── __init__.py
│   └── main.py
├── tests/                 # ✅ Tests
├── .env                   # ❌ NO versionar
├── .env.example           # ✅ Ejemplo sin secretos
├── .gitignore            # ✅ Versionar
├── requirements.txt       # ✅ Versionar
├── README.md             # ✅ Versionar
└── setup.py              # ✅ Si es paquete
```

### 5. Nombrar requirements

```
requirements/
├── base.txt           # Dependencias comunes
├── development.txt    # Para desarrollo
├── production.txt     # Para producción
└── testing.txt        # Para tests
```

**development.txt**
```
-r base.txt
pytest>=7.4.0
black>=23.7.0
pylint>=2.17.0
```

---

## 🔍 Resolución de problemas

### Problema: "Cannot activate venv"

#### Windows PowerShell - Error de política
```powershell
# Ver política actual
Get-ExecutionPolicy

# Cambiar política (ejecutar como administrador)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verificar
Get-ExecutionPolicy
```

### Problema: Entorno no se activa correctamente

```powershell
# Verificar que el entorno existe
Test-Path venv\Scripts\activate.ps1

# Recrear el entorno si es necesario
Remove-Item -Recurse -Force venv
python -m venv venv
```

### Problema: pip no encuentra paquetes

```powershell
# Actualizar pip
python -m pip install --upgrade pip

# Verificar índice PyPI
pip config list

# Usar índice alternativo (si hay problemas)
pip install --index-url https://pypi.org/simple paquete
```

### Problema: Conflictos de versiones

```powershell
# Ver dependencias de un paquete
pip show nombre_paquete

# Usar herramienta de verificación
pip install pip-tools
pip-compile requirements.in

# Usar Poetry para resolver automáticamente
poetry lock
```

---

## 🎓 Resumen y Recomendaciones

### Para principiantes
- **Usar**: `venv` (incluido en Python)
- **Razón**: Simple, estándar, sin instalación extra

### Para proyectos profesionales
- **Usar**: `Poetry` o `Pipenv`
- **Razón**: Mejor gestión de dependencias, reproducibilidad

### Para Data Science
- **Usar**: `conda`
- **Razón**: Maneja paquetes científicos complejos

### Comando rápido para iniciar cualquier proyecto

```powershell
# Crear estructura básica
mkdir mi_proyecto
cd mi_proyecto
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
echo "venv/\n*.pyc\n__pycache__/\n.env" > .gitignore
pip freeze > requirements.txt
```

---

## 📚 Referencias

- [Documentación oficial venv](https://docs.python.org/3/library/venv.html)
- [virtualenv](https://virtualenv.pypa.io/)
- [Conda](https://docs.conda.io/)
- [Pipenv](https://pipenv.pypa.io/)
- [Poetry](https://python-poetry.org/)

---

*Última actualización: Abril 2026*
