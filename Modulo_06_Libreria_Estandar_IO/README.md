# Módulo 6: Librería Estándar y E/S

## 📋 Descripción

Dominio de la librería estándar de Python para operaciones de entrada/salida, manejo de archivos, parseo de formatos comunes, trabajo con fechas y logging estructurado.

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- ✅ Manipular archivos y rutas de forma segura con `pathlib`
- ✅ Leer y escribir CSV, JSON y YAML
- ✅ Trabajar con fechas, horas y zonas horarias
- ✅ Configurar logging estructurado y profesional
- ✅ Automatizar tareas con `subprocess`
- ✅ Gestionar contextos con context managers
- ✅ Implementar serialización/deserialización de datos

## 📚 Contenidos

### 1. pathlib y Manejo de Archivos
**Archivo:** [`01_pathlib_archivos.py`](01_pathlib_archivos.py)

**Temas cubiertos:**
- `pathlib.Path` vs `os.path`
- Operaciones con rutas (join, resolve, exists)
- Leer y escribir archivos de texto
- Manejo de archivos binarios
- Context managers (`with` statement)
- Operaciones atómicas y seguras
- Trabajo con archivos temporales
- Globbing y búsqueda de archivos

**Conceptos clave:**
```python
from pathlib import Path

# Path moderno y multiplataforma
archivo = Path("datos") / "usuarios.json"
if archivo.exists():
    contenido = archivo.read_text(encoding="utf-8")
```

---

### 2. CSV, JSON y YAML
**Archivo:** [`02_csv_json_yaml.py`](02_csv_json_yaml.py)

**Temas cubiertos:**
- Lectura y escritura de CSV (`csv`, `DictReader`, `DictWriter`)
- JSON: parseo, serialización, `JSONEncoder` custom
- YAML: PyYAML para configuraciones
- Manejo de encodings
- Streaming de datos grandes
- Validación con Pydantic

**Conceptos clave:**
```python
import json
import csv
from pathlib import Path

# JSON type-safe
data = json.loads(Path("config.json").read_text())

# CSV con diccionarios
with open("datos.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["nombre"])
```

---

### 3. datetime y Zonas Horarias
**Archivo:** [`03_datetime_timezones.py`](03_datetime_timezones.py)

**Temas cubiertos:**
- `datetime`, `date`, `time`, `timedelta`
- Parsing y formateo de fechas (strptime/strftime)
- Zonas horarias con `zoneinfo` (Python 3.9+)
- Timestamps Unix
- Comparaciones y aritmética de fechas
- Fechas relativas (pendulum, dateutil)

**Conceptos clave:**
```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# Fechas timezone-aware
ahora_utc = datetime.now(timezone.utc)
ahora_mx = ahora_utc.astimezone(ZoneInfo("America/Mexico_City"))
```

---

### 4. Logging y Configuración
**Archivo:** [`04_logging_config.py`](04_logging_config.py)

**Temas cubiertos:**
- Módulo `logging` de la stdlib
- Niveles de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Loggers, Handlers, Formatters
- Logging a archivo y consola
- Rotating file handlers
- JSON structured logging
- Logging en aplicaciones production

**Conceptos clave:**
```python
import logging

# Configuración básica
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
logger.info("Aplicación iniciada")
```

---

### 5. subprocess y Automatización
**Archivo:** [`05_subprocess_automatizacion.py`](05_subprocess_automatizacion.py)

**Temas cubiertos:**
- Ejecutar comandos externos con `subprocess`
- `subprocess.run()`, `Popen()`
- Capturar stdout/stderr
- Pipelines y comunicación entre procesos
- Timeout y manejo de errores
- Automatización de tareas del sistema
- Alternativas: `sh`, `invoke`

**Conceptos clave:**
```python
import subprocess

# Ejecutar comando y capturar salida
resultado = subprocess.run(
    ["git", "status"],
    capture_output=True,
    text=True,
    check=True
)
print(resultado.stdout)
```

---

## 🛠️ Requisitos

### Librerías Necesarias
```bash
pip install -r requirements.txt
```

**Incluye:**
- `pyyaml` - Parseo de archivos YAML
- `python-dateutil` - Utilidades avanzadas de fechas
- `pytz` - Zonas horarias (legacy, usar `zoneinfo` en 3.9+)

**Opcional:**
- `pendulum` - API moderna para fechas
- `arrow` - Fechas más amigables
- `python-json-logger` - Logging JSON estructurado

---

## 📝 Laboratorio

### Ejercicio Principal: Sistema de Ingesta de Datos
**Archivo:** [`LABORATORIO.md`](LABORATORIO.md)

**Objetivo:** Crear un sistema que:
1. Lee archivos CSV con datos de ventas
2. Procesa y valida los datos
3. Genera métricas y estadísticas
4. Exporta resultados a JSON
5. Implementa logging estructurado en múltiples niveles

**Componentes:**
- Ingesta de CSV con validación
- Transformación de datos
- Cálculo de métricas (totales, promedios, tendencias)
- Exportación a JSON con formato custom
- Logging a consola y archivo
- Manejo de errores y recuperación

**Duración estimada:** 2-3 horas

---

## 🎓 Ejercicios Adicionales

**Archivo:** [`EJERCICIOS.md`](EJERCICIOS.md)

1. **Sincronización de Archivos** ⭐⭐⭐
   - Comparar directorios y sincronizar cambios

2. **Parser de Logs** ⭐⭐⭐
   - Analizar logs con regex y generar reportes

3. **Gestor de Configuración** ⭐⭐⭐⭐
   - Sistema multi-formato (JSON/YAML/ENV)

4. **ETL Pipeline** ⭐⭐⭐⭐⭐
   - Extract, Transform, Load con logging completo

5. **Sistema de Backups Automático** ⭐⭐⭐⭐
   - Backups incrementales con compresión

6. **Conversor de Formatos** ⭐⭐⭐
   - CSV ↔ JSON ↔ YAML con validación

7. **Agregador de Logs** ⭐⭐⭐⭐
   - Centralizar logs de múltiples fuentes

8. **Scheduler de Tareas** ⭐⭐⭐⭐⭐
   - Ejecutar comandos programados

---

## 💡 Mejores Prácticas

### Manejo de Archivos
```python
# ✅ BUENO: Context manager garantiza cierre
from pathlib import Path

archivo = Path("datos.txt")
with archivo.open("r", encoding="utf-8") as f:
    contenido = f.read()

# ✅ BUENO: Más simple con Path
contenido = Path("datos.txt").read_text(encoding="utf-8")

# ❌ MALO: Puede dejar archivo abierto
f = open("datos.txt")
contenido = f.read()
# f nunca se cierra si hay error
```

### Rutas Multiplataforma
```python
# ✅ BUENO: pathlib es multiplataforma
from pathlib import Path

ruta = Path("datos") / "usuarios" / "perfil.json"

# ❌ MALO: Hardcodear separadores
ruta = "datos\\usuarios\\perfil.json"  # Solo Windows
ruta = "datos/usuarios/perfil.json"    # Solo Unix
```

### Fechas con Timezone
```python
# ✅ BUENO: Siempre timezone-aware
from datetime import datetime, timezone

ahora = datetime.now(timezone.utc)

# ❌ MALO: datetime naive (sin timezone)
ahora = datetime.now()  # ¿Qué timezone es?
```

### Logging Estructurado
```python
# ✅ BUENO: Logging con contexto
logger.info(
    "Usuario autenticado",
    extra={"user_id": 123, "ip": "192.168.1.1"}
)

# ❌ MALO: String concatenation
logger.info(f"Usuario {user_id} autenticado desde {ip}")
```

### subprocess Seguro
```python
# ✅ BUENO: Lista para evitar injection
subprocess.run(["git", "log", "--oneline"], check=True)

# ❌ MALO: shell=True es peligroso
subprocess.run(f"git log --oneline", shell=True)
```

---

## 🔍 Casos de Uso Reales

### 1. ETL de Datos
```python
"""Extraer datos de CSV, transformar y cargar a JSON."""
import csv
import json
from pathlib import Path

# Extract
with open("ventas.csv") as f:
    ventas = list(csv.DictReader(f))

# Transform
for venta in ventas:
    venta["total"] = float(venta["precio"]) * int(venta["cantidad"])

# Load
Path("ventas_procesadas.json").write_text(
    json.dumps(ventas, indent=2, ensure_ascii=False)
)
```

### 2. Logging de Aplicación Web
```python
"""Configurar logging para producción."""
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("mi_app")
logger.setLevel(logging.INFO)

# Handler para archivo con rotación
handler = RotatingFileHandler(
    "app.log",
    maxBytes=10_000_000,  # 10MB
    backupCount=5
)
handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
))
logger.addHandler(handler)
```

### 3. Automatización de Despliegue
```python
"""Script de deployment con subprocess."""
import subprocess
from pathlib import Path

def deploy():
    """Ejecuta deployment a servidor."""
    commands = [
        ["git", "pull"],
        ["pip", "install", "-r", "requirements.txt"],
        ["python", "manage.py", "migrate"],
        ["systemctl", "restart", "myapp"]
    ]
    
    for cmd in commands:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error en: {' '.join(cmd)}")
            print(result.stderr)
            return False
    
    return True
```

---

## 🧪 Testing

```python
# test_archivos.py
from pathlib import Path
import pytest

def test_leer_archivo_existe(tmp_path):
    """Test lectura de archivo existente."""
    archivo = tmp_path / "test.txt"
    archivo.write_text("Hola Mundo")
    
    assert archivo.read_text() == "Hola Mundo"

def test_archivo_no_existe():
    """Test manejo de archivo inexistente."""
    archivo = Path("no_existe.txt")
    
    with pytest.raises(FileNotFoundError):
        archivo.read_text()
```

---

## 📖 Recursos Adicionales

### Documentación Oficial
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [csv](https://docs.python.org/3/library/csv.html)
- [json](https://docs.python.org/3/library/json.html)
- [datetime](https://docs.python.org/3/library/datetime.html)
- [logging](https://docs.python.org/3/library/logging.html)
- [subprocess](https://docs.python.org/3/library/subprocess.html)
- [zoneinfo](https://docs.python.org/3/library/zoneinfo.html)

### Librerías Recomendadas
- [PyYAML](https://pyyaml.org/) - YAML parsing
- [Pendulum](https://pendulum.eustace.io/) - Fechas mejoradas
- [python-json-logger](https://github.com/madzak/python-json-logger) - JSON logging
- [sh](https://sh.readthedocs.io/) - subprocess mejorado

### Tutoriales
- [Real Python: Working with Files](https://realpython.com/working-with-files-in-python/)
- [Real Python: Python logging](https://realpython.com/python-logging/)
- [Real Python: Python datetime](https://realpython.com/python-datetime/)

---

## 🎯 Evaluación

### Criterios de Dominio

**Nivel Básico:**
- Leer y escribir archivos de texto
- Parsear JSON básico
- Usar logging.basicConfig()
- Ejecutar comandos simples con subprocess

**Nivel Intermedio:**
- Usar pathlib para operaciones complejas
- Trabajar con CSV usando DictReader/DictWriter
- Configurar logging con múltiples handlers
- Trabajar con fechas y timezones

**Nivel Avanzado:**
- Implementar streaming de archivos grandes
- JSON encoders personalizados
- Logging estructurado con contexto
- Pipelines complejos con subprocess
- ETL pipelines completos

---

## 🚀 Siguiente Módulo

**Módulo 7:** Testing y Calidad de Software
- pytest framework
- Fixtures y mocking
- Cobertura de código
- Testing de APIs

---

## 📞 Soporte

¿Dudas o problemas con el módulo?
- Revisa los ejemplos en cada archivo `.py`
- Consulta el laboratorio para casos prácticos
- Experimenta con los ejercicios adicionales

**Tips:**
- Siempre usa `encoding="utf-8"` al leer/escribir archivos
- Prefiere `pathlib.Path` sobre `os.path`
- Usa context managers (`with`) para recursos
- Implementa logging desde el principio en proyectos reales
- Lee la documentación oficial de Python - es excelente
