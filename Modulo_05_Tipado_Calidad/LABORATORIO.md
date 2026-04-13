# Laboratorio: Tipado Estático y Calidad de Código

## Objetivos
- Anotar tipos en código existente
- Ejecutar mypy y ruff para encontrar errores
- Configurar pre-commit para validación automática
- Implementar linting y formateo en CI/CD

---

## Ejercicio 1: Anotar Tipos en Código Existente ⭐⭐⭐

### Descripción
Tomar código sin tipos del Módulo 4 y agregar anotaciones de tipos completas.

### Código base (sin tipos)

```python
# sin_tipos.py
def buscar_usuario(usuarios, user_id):
    """Busca un usuario por ID."""
    for usuario in usuarios:
        if usuario["id"] == user_id:
            return usuario
    return None


def calcular_total_orden(items, descuento=0):
    """Calcula el total de una orden con descuento."""
    subtotal = sum(item["precio"] * item["cantidad"] for item in items)
    descuento_monto = subtotal * (descuento / 100)
    return subtotal - descuento_monto


class RepositorioUsuarios:
    def __init__(self):
        self.usuarios = {}
    
    def agregar(self, usuario):
        self.usuarios[usuario["id"]] = usuario
    
    def obtener(self, user_id):
        return self.usuarios.get(user_id)
    
    def listar_activos(self):
        return [u for u in self.usuarios.values() if u.get("activo", False)]
```

### Tareas

**Parte A: Agregar Type Hints Básicos**
1. Agregar tipos a todas las funciones
2. Agregar tipos a parámetros y retornos
3. Usar `List`, `Dict`, `Optional` donde corresponda
4. Anotar atributos de clase

**Parte B: Crear TypedDict para Estructuras**
1. Crear `UsuarioDict` TypedDict con estructura:
   - `id`: int
   - `nombre`: str
   - `email`: str
   - `activo`: bool

2. Crear `ItemOrdenDict` TypedDict:
   - `producto`: str
   - `precio`: float
   - `cantidad`: int

**Parte C: Mejorar con Tipos Avanzados**
1. Usar `Literal` para estados válidos
2. Crear type aliases para tipos complejos
3. Documentar con docstrings incluyendo tipos

### Código esperado (con tipos)

```python
# con_tipos.py
from typing import List, Dict, Optional, TypedDict, Literal

EstadoUsuario = Literal["activo", "inactivo", "suspendido"]


class UsuarioDict(TypedDict):
    """Estructura de usuario."""
    id: int
    nombre: str
    email: str
    activo: bool


class ItemOrdenDict(TypedDict):
    """Item de una orden."""
    producto: str
    precio: float
    cantidad: int


def buscar_usuario(
    usuarios: List[UsuarioDict], 
    user_id: int
) -> Optional[UsuarioDict]:
    """
    Busca un usuario por ID.
    
    Args:
        usuarios: Lista de usuarios donde buscar.
        user_id: ID del usuario a buscar.
    
    Returns:
        Usuario encontrado o None si no existe.
    """
    for usuario in usuarios:
        if usuario["id"] == user_id:
            return usuario
    return None


def calcular_total_orden(
    items: List[ItemOrdenDict], 
    descuento: float = 0.0
) -> float:
    """
    Calcula el total de una orden con descuento.
    
    Args:
        items: Lista de items en la orden.
        descuento: Porcentaje de descuento (0-100).
    
    Returns:
        Total después de aplicar descuento.
    """
    subtotal = sum(item["precio"] * item["cantidad"] for item in items)
    descuento_monto = subtotal * (descuento / 100)
    return subtotal - descuento_monto


class RepositorioUsuarios:
    """Repositorio para gestionar usuarios."""
    
    def __init__(self) -> None:
        self.usuarios: Dict[int, UsuarioDict] = {}
    
    def agregar(self, usuario: UsuarioDict) -> None:
        """Agrega un usuario al repositorio."""
        self.usuarios[usuario["id"]] = usuario
    
    def obtener(self, user_id: int) -> Optional[UsuarioDict]:
        """Obtiene un usuario por ID."""
        return self.usuarios.get(user_id)
    
    def listar_activos(self) -> List[UsuarioDict]:
        """Lista todos los usuarios activos."""
        return [
            u for u in self.usuarios.values() 
            if u.get("activo", False)
        ]
```

### Verificación

```bash
# Verificar con mypy
mypy con_tipos.py

# Debería pasar sin errores
# Success: no issues found in 1 source file
```

---

## Ejercicio 2: Ejecutar mypy y Corregir Errores ⭐⭐⭐

### Descripción
Código con errores de tipos intencionales. Ejecutar mypy y corregir todos los errores.

### Código con errores

```python
# con_errores.py
from typing import List, Optional

def obtener_primer_elemento(lista: List[str]) -> str:
    """Retorna el primer elemento."""
    return lista[0]  # Error: puede ser IndexError si lista vacía


def procesar_numero(n: int) -> str:
    """Convierte número a string."""
    resultado = n * 2
    return resultado  # Error: retorna int, no str


def buscar_config(clave: str) -> str:
    """Busca valor de configuración."""
    configs = {"host": "localhost", "puerto": 8080}
    return configs.get(clave)  # Error: get() puede retornar None


class Usuario:
    def __init__(self, nombre: str, edad: int):
        self.nombre = nombre
        self.edad = edad
    
    def saludar(self):  # Error: falta tipo de retorno
        return f"Hola, soy {self.nombre}"


def main() -> None:
    # Error: argumento de tipo incorrecto
    numeros = [1, 2, 3]
    primer = obtener_primer_elemento(numeros)
    
    # Error: asignación de tipo incompatible
    resultado: int = procesar_numero(5)
```

### Tareas

1. Ejecutar mypy: `mypy con_errores.py`
2. Leer y entender cada error reportado
3. Corregir todos los errores:
   - Cambiar tipos de retorno incorrectos
   - Agregar tipos de retorno faltantes
   - Usar Optional donde corresponda
   - Manejar casos de None
   - Corregir conversiones de tipos

### Errores esperados de mypy

```
con_errores.py:5: error: Incompatible return value type (got "int", expected "str")
con_errores.py:12: error: Incompatible return value type (got "Optional[Union[str, int]]", expected "str")
con_errores.py:22: error: Function is missing a return type annotation
con_errores.py:28: error: Argument 1 to "obtener_primer_elemento" has incompatible type "List[int]"; expected "List[str]"
con_errores.py:31: error: Incompatible types in assignment (expression has type "str", variable has type "int")
```

### Solución esperada

```python
# corregido.py
from typing import List, Optional, Union


def obtener_primer_elemento(lista: List[str]) -> Optional[str]:
    """Retorna el primer elemento o None si lista vacía."""
    return lista[0] if lista else None


def procesar_numero(n: int) -> str:
    """Convierte número a string."""
    resultado = n * 2
    return str(resultado)  # Convertir a string


def buscar_config(clave: str) -> Optional[Union[str, int]]:
    """Busca valor de configuración."""
    configs: dict[str, Union[str, int]] = {
        "host": "localhost",
        "puerto": 8080
    }
    return configs.get(clave)


class Usuario:
    def __init__(self, nombre: str, edad: int) -> None:
        self.nombre = nombre
        self.edad = edad
    
    def saludar(self) -> str:  # Agregar tipo de retorno
        return f"Hola, soy {self.nombre}"


def main() -> None:
    # Usar lista de strings
    nombres = ["Ana", "Juan", "Pedro"]
    primer = obtener_primer_elemento(nombres)
    
    # tipo correcto
    resultado: str = procesar_numero(5)
    print(resultado)
```

---

## Ejercicio 3: Configurar Ruff y Corregir Problemas ⭐⭐⭐

### Descripción
Código que viola PEP 8. Usar ruff para encontrar y corregir automáticamente.

### Código sin formatear

```python
# sin_formatear.py
import sys
import os
from typing import List,Dict,Optional
import json

MAX_SIZE=100
default_timeout = 30


class   ProductoManager:


    def __init__(self,db_url):
        self.db_url=db_url
        self._productos={}

    def agregar_producto(self,id,nombre,precio):
        if precio<=0:raise ValueError('Precio inválido')
        self._productos[id]={'id':id,'nombre':nombre,'precio':precio}
        return True
    
    def buscar(self,id):
        return self._productos.get(id,None)


def procesar_lista(items):
    resultado=[]
    for item in items:
        if item!=None:
            resultado.append(item)
    return resultado


if __name__=='__main__':
    manager=ProductoManager('sqlite:///:memory:')
    manager.agregar_producto(1,'Laptop',1200.0)
    print('Producto agregado')
```

### Tareas

**Parte A: Verificar con Ruff**
```bash
# Ver todos los problemas
ruff check sin_formatear.py

# Ver con detalles
ruff check sin_formatear.py --verbose
```

**Parte B: Auto-fix automático**
```bash
# Corregir automáticamente lo que se pueda
ruff check sin_formatear.py --fix

# Formatear además del lint
ruff format sin_formatear.py
```

**Parte C: Verificar con Black**
```bash
# Ver qué cambiaría black
black --check sin_formatear.py --diff

# Aplicar cambios
black sin_formatear.py
```

**Parte D: Ordenar imports con isort**
```bash
# Ver cambios de isort
isort sin_formatear.py --check-only --diff

# Aplicar
isort sin_formatear.py
```

### Problemas que ruff debería encontrar

- E501: Line too long
- E701: Multiple statements on one line
- E711: Comparison to None should be `is None`
- E712: Comparison to True/False
- E302: Expected 2 blank lines
- F401: Module imported but unused
- W291: Trailing whitespace
- I001: Import block is un-sorted

### Código formateado esperado

```python
# formateado.py
"""Módulo para gestionar productos."""
import json
import os
import sys
from typing import Dict, List, Optional


MAX_SIZE = 100
DEFAULT_TIMEOUT = 30


class ProductoManager:
    """Gestor de productos."""
    
    def __init__(self, db_url: str) -> None:
        """Inicializa el gestor."""
        self.db_url = db_url
        self._productos: Dict[int, Dict[str, str | float]] = {}
    
    def agregar_producto(
        self,
        id: int,
        nombre: str,
        precio: float
    ) -> bool:
        """Agrega un producto."""
        if precio <= 0:
            raise ValueError("Precio inválido")
        
        self._productos[id] = {
            "id": id,
            "nombre": nombre,
            "precio": precio,
        }
        return True
    
    def buscar(self, id: int) -> Optional[Dict[str, str | float]]:
        """Busca un producto por ID."""
        return self._productos.get(id)


def procesar_lista(items: List[Optional[str]]) -> List[str]:
    """Filtra elementos None de una lista."""
    resultado = []
    for item in items:
        if item is not None:
            resultado.append(item)
    return resultado


if __name__ == "__main__":
    manager = ProductoManager("sqlite:///:memory:")
    manager.agregar_producto(1, "Laptop", 1200.0)
    print("Producto agregado")
```

---

## Ejercicio 4: Configurar Pre-commit ⭐⭐⭐⭐

### Descripción
Configurar pre-commit hooks para validación automática en cada commit.

### Tareas

**Parte A: Instalar pre-commit**
```bash
# Instalar
pip install pre-commit

# Verificar instalación
pre-commit --version
```

**Parte B: Crear .pre-commit-config.yaml**

Crear en la raíz del proyecto:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.2.0
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        args: [--ignore-missing-imports]
```

**Parte C: Instalar hooks**
```bash
# Instalar hooks en .git/hooks/
pre-commit install

# Ejecutar en todos los archivos (primera vez)
pre-commit run --all-files
```

**Parte D: Probar el flujo**

1. Modificar un archivo con errores de formato:
```python
# test.py
def suma(a,b):
    return a+b
```

2. Hacer commit:
```bash
git add test.py
git commit -m "Agregar función suma"
```

3. Pre-commit se ejecuta automáticamente:
```
[INFO] Running hook: black.....................Fixed
[INFO] Running hook: ruff......................Fixed

Files were modified by this hook. Review and add them to commit.
```

4. Ver cambios que hizo:
```bash
git diff test.py
```

5. Agregar cambios y re-commitear:
```bash
git add test.py
git commit -m "Agregar función suma"
```

6. Ahora debería pasar:
```
[INFO] Running hook: black.....................Passed
[INFO] Running hook: ruff......................Passed
[main abc1234] Agregar función suma
```

---

## Ejercicio 5: CI/CD con GitHub Actions ⭐⭐⭐⭐⭐

### Descripción
Configurar pipeline de CI/CD para ejecutar verificaciones de calidad.

### Tareas

**Parte A: Crear workflow de GitHub Actions**

Crear `.github/workflows/quality.yml`:

```yaml
name: Code Quality

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  quality:
    name: Quality Checks
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install black ruff mypy
      
      - name: Check formatting with Black
        run: black --check .
      
      - name: Lint with Ruff
        run: ruff check .
      
      - name: Type check with mypy
        run: mypy .
        continue-on-error: true
      
      - name: Run tests
        run: |
          pip install pytest
          pytest
```

**Parte B: Crear archivo requirements.txt para CI**

```text
# requirements.txt
black>=24.0.0
ruff>=0.2.0
mypy>=1.8.0
pytest>=7.4.0
```

**Parte C: Agregar badge al README**

```markdown
# Mi Proyecto

[![Code Quality](https://github.com/usuario/proyecto/workflows/Code%20Quality/badge.svg)](https://github.com/usuario/proyecto/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Setup

```bash
pip install -r requirements.txt
pre-commit install
```
```

---

## Entrega

**Archivos requeridos:**
1. `con_tipos.py` - Código con tipos completos
2. `corregido.py` - Errores de mypy corregidos
3. `formateado.py` - Código formateado
4. `.pre-commit-config.yaml` - Configuración de pre-commit
5. `pyproject.toml` - Configuración de herramientas
6. `.github/workflows/quality.yml` - CI/CD workflow
7. `README.md` - Documentación con badges

**Ejecutar verificación final:**
```bash
# Pre-commit en todos los archivos
pre-commit run --all-files

# mypy
mypy .

# ruff
ruff check .

# black
black --check .
```

**Salida esperada:**
```
✅ Pre-commit: All checks passed
✅ mypy: Success - no issues found
✅ ruff: All checks passed!
✅ black: All done! ✨ 🍰 ✨
```
