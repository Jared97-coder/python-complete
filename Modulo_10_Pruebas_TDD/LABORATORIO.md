# Laboratorio: TDD, Property Testing y Cobertura

## Objetivos

Al finalizar este laboratorio, habrás:

✅ Implementado una feature completa usando **TDD estricto** (Red-Green-Refactor)  
✅ Diseñado **property-based tests** con Hypothesis  
✅ Medido y mejorado **cobertura de código**  
✅ Configurado **CI/CD** con verificación de tests  
✅ Practicado el ciclo completo de desarrollo dirigido por pruebas

---

## 📋 Proyecto: Sistema de Carrito de Compras

Implementarás un sistema de carrito de compras con las siguientes funcionalidades:

### Requerimientos Funcionales

1. **Gestión de Productos**
   - Agregar producto al carrito (nombre, precio, cantidad)
   - Remover producto del carrito
   - Actualizar cantidad de un producto
   - Limpiar carrito completo

2. **Cálculo de Totales**
   - Calcular subtotal (suma de precio × cantidad)
   - Aplicar descuentos:
     - 10% si total > $100
     - 15% si total > $500
     - 20% si total > $1000
   - Calcular impuestos (16% sobre subtotal con descuento)
   - Calcular total final (subtotal - descuento + impuestos)

3. **Validaciones**
   - Precio debe ser > 0
   - Cantidad debe ser > 0
   - No permitir duplicados (mismo producto se acumula)
   - Stock máximo por producto: 100 unidades

4. **Consultas**
   - Obtener cantidad de items diferentes
   - Obtener cantidad total de productos (suma de cantidades)
   - Verificar si carrito está vacío
   - Obtener listado de productos

---

## 🔴🟢🔵 Parte 1: Implementación con TDD Estricto

### Reglas del TDD

**IMPORTANTE**: Debes seguir el ciclo Red-Green-Refactor **estrictamente**:

1. **🔴 RED**: Escribe un test que FALLE
   - El test debe compilar pero fallar
   - Define el comportamiento esperado
   
2. **🟢 GREEN**: Escribe el código MÍNIMO para pasar
   - Solo lo necesario para que el test pase
   - No importa si el código es "feo"
   
3. **🔵 REFACTOR**: Mejora el código SIN cambiar comportamiento
   - Elimina duplicación
   - Mejora nombres
   - Los tests deben seguir pasando

**Prohibido**:
❌ Escribir código de producción sin test previo  
❌ Escribir múltiples tests antes de hacerlos pasar  
❌ Saltarse la fase de refactor

---

### Paso 1: Configuración del Proyecto

```bash
# Crear estructura
mkdir shopping_cart
cd shopping_cart

# Crear archivos
touch shopping_cart.py
touch test_shopping_cart.py
touch test_shopping_cart_properties.py
touch requirements.txt
```

**requirements.txt**:
```
pytest>=7.4.3
pytest-cov>=4.1.0
hypothesis>=6.92.0
```

```bash
# Instalar dependencias
pip install -r requirements.txt
```

---

### Paso 2: TDD - Primera Iteración (Crear Carrito Vacío)

#### 🔴 RED: Test que falla

**test_shopping_cart.py**:
```python
from shopping_cart import ShoppingCart

def test_create_empty_cart():
    """Test 1: Crear un carrito vacío."""
    cart = ShoppingCart()
    assert cart.is_empty() is True
```

Ejecutar:
```bash
$ pytest test_shopping_cart.py::test_create_empty_cart
```

**Resultado esperado**: ❌ FALLA (ImportError o AttributeError)

#### 🟢 GREEN: Código mínimo

**shopping_cart.py**:
```python
class ShoppingCart:
    def __init__(self):
        pass
    
    def is_empty(self):
        return True
```

Ejecutar:
```bash
$ pytest test_shopping_cart.py::test_create_empty_cart
```

**Resultado esperado**: ✅ PASA

#### 🔵 REFACTOR: (Opcional - aún no hay mucho que refactorizar)

---

### Paso 3: TDD - Segunda Iteración (Agregar Producto)

#### 🔴 RED: Test que falla

**test_shopping_cart.py**:
```python
def test_add_product():
    """Test 2: Agregar un producto al carrito."""
    cart = ShoppingCart()
    cart.add_product("Laptop", 1000.0, 1)
    
    assert cart.is_empty() is False
    assert cart.get_item_count() == 1
```

**Resultado esperado**: ❌ FALLA (AttributeError: add_product, get_item_count)

#### 🟢 GREEN: Código mínimo

**shopping_cart.py**:
```python
class ShoppingCart:
    def __init__(self):
        self._items = []
    
    def is_empty(self):
        return len(self._items) == 0
    
    def add_product(self, name, price, quantity):
        self._items.append({"name": name, "price": price, "quantity": quantity})
    
    def get_item_count(self):
        return len(self._items)
```

**Resultado esperado**: ✅ PASA

#### 🔵 REFACTOR: (Opcional)

---

### Paso 4: TDD - Tercera Iteración (Calcular Subtotal)

#### 🔴 RED:

```python
def test_calculate_subtotal():
    """Test 3: Calcular subtotal de productos."""
    cart = ShoppingCart()
    cart.add_product("Laptop", 1000.0, 2)
    cart.add_product("Mouse", 25.0, 1)
    
    assert cart.get_subtotal() == 2025.0  # (1000*2) + (25*1)
```

#### 🟢 GREEN:

```python
def get_subtotal(self):
    total = 0
    for item in self._items:
        total += item["price"] * item["quantity"]
    return total
```

#### 🔵 REFACTOR:

```python
def get_subtotal(self):
    return sum(item["price"] * item["quantity"] for item in self._items)
```

---

### Paso 5: Continúa Implementando con TDD

**Tu turno**: Implementa las siguientes funcionalidades siguiendo el ciclo Red-Green-Refactor:

1. **Test 4**: Validar precio positivo
   ```python
   def test_add_product_invalid_price():
       cart = ShoppingCart()
       with pytest.raises(ValueError, match="Price must be positive"):
           cart.add_product("Laptop", -100, 1)
   ```

2. **Test 5**: Validar cantidad positiva

3. **Test 6**: Validar stock máximo (100 unidades)

4. **Test 7**: Remover producto

5. **Test 8**: Actualizar cantidad de producto existente

6. **Test 9**: Descuento 10% si total > $100

7. **Test 10**: Descuento 15% si total > $500

8. **Test 11**: Descuento 20% si total > $1000

9. **Test 12**: Calcular impuestos (16% sobre subtotal con descuento)

10. **Test 13**: Calcular total final

11. **Test 14**: Acumular cantidad si producto ya existe

12. **Test 15**: Limpiar carrito

---

## 🧪 Parte 2: Property-Based Testing

Ahora añadirás tests de propiedades con Hypothesis para verificar **invariantes** y **propiedades matemáticas**.

**test_shopping_cart_properties.py**:

```python
from hypothesis import given, strategies as st, assume
from shopping_cart import ShoppingCart
import pytest


@given(st.lists(st.tuples(
    st.text(min_size=1, max_size=20),  # nombre
    st.floats(min_value=0.01, max_value=10000),  # precio
    st.integers(min_value=1, max_value=100)  # cantidad
), min_size=1, max_size=10))
def test_subtotal_never_negative(products):
    """
    PROPIEDAD: El subtotal siempre debe ser >= 0.
    """
    cart = ShoppingCart()
    for name, price, quantity in products:
        cart.add_product(name, price, quantity)
    
    assert cart.get_subtotal() >= 0


@given(st.lists(st.tuples(
    st.text(min_size=1, max_size=20),
    st.floats(min_value=0.01, max_value=10000),
    st.integers(min_value=1, max_value=100)
), min_size=1, max_size=10))
def test_total_never_exceeds_subtotal_without_taxes(products):
    """
    PROPIEDAD: El total con descuento (sin impuestos) nunca debe exceder el subtotal.
    """
    cart = ShoppingCart()
    for name, price, quantity in products:
        cart.add_product(name, price, quantity)
    
    subtotal = cart.get_subtotal()
    discount = cart.get_discount()
    
    assert subtotal - discount <= subtotal


@given(st.text(min_size=1, max_size=20),
       st.floats(min_value=0.01, max_value=10000),
       st.integers(min_value=1, max_value=100))
def test_adding_and_removing_same_product_is_identity(name, price, quantity):
    """
    PROPIEDAD: Agregar y luego remover el mismo producto deja el carrito igual.
    """
    cart = ShoppingCart()
    
    # Estado inicial
    initial_subtotal = cart.get_subtotal()
    initial_count = cart.get_item_count()
    
    # Agregar producto
    cart.add_product(name, price, quantity)
    
    # Remover producto
    cart.remove_product(name)
    
    # Debe volver al estado inicial
    assert cart.get_subtotal() == initial_subtotal
    assert cart.get_item_count() == initial_count


@given(st.floats(min_value=0.01, max_value=10000),
       st.floats(min_value=0.01, max_value=10000))
def test_adding_products_is_commutative_for_total(price1, price2):
    """
    PROPIEDAD: El orden de agregar productos no afecta el total.
    """
    cart1 = ShoppingCart()
    cart1.add_product("ProductA", price1, 1)
    cart1.add_product("ProductB", price2, 1)
    
    cart2 = ShoppingCart()
    cart2.add_product("ProductB", price2, 1)
    cart2.add_product("ProductA", price1, 1)
    
    assert cart1.get_total() == cart2.get_total()


@given(st.floats(min_value=0.01, max_value=10000))
def test_discount_never_makes_total_negative(price):
    """
    PROPIEDAD: Aplicar descuento nunca resulta en total negativo.
    """
    cart = ShoppingCart()
    cart.add_product("Product", price, 1)
    
    total = cart.get_total()
    assert total >= 0


# Añade más property tests:
# - PROPIEDAD: Duplicar cantidades duplica el subtotal
# - PROPIEDAD: Limpiar carrito siempre deja is_empty() == True
# - PROPIEDAD: get_item_count() >= 0 siempre
# - PROPIEDAD: Remover producto que no existe no cambia el carrito
```

---

## 📊 Parte 3: Cobertura de Código

### Paso 1: Ejecutar Tests con Coverage

```bash
# Coverage básico
pytest --cov=shopping_cart --cov-report=term-missing

# Coverage con HTML
pytest --cov=shopping_cart --cov-report=html

# Abrir reporte HTML
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```

### Paso 2: Analizar Reporte

**Objetivo**: Lograr **mínimo 85% de cobertura**

1. Revisa el reporte HTML
2. Identifica líneas rojas (no cubiertas)
3. Identifica líneas amarillas (ramas parciales)

**Preguntas a responder**:
- ¿Qué líneas no están cubiertas?
- ¿Qué ramas (if/else) faltan testear?
- ¿Hay código muerto (unreachable)?

### Paso 3: Mejorar Cobertura

Escribe tests adicionales para cubrir:
- ✅ Todas las ramas de descuentos (10%, 15%, 20%)
- ✅ Todas las validaciones (precio, cantidad, stock)
- ✅ Edge cases (carrito vacío, un solo producto, 100 productos)
- ✅ Excepciones (remover producto que no existe, etc.)

### Paso 4: Configuración de Calidad

**pyproject.toml**:
```toml
[tool.coverage.run]
source = ["."]
omit = ["test_*.py", "*/__pycache__/*"]

[tool.coverage.report]
precision = 2
show_missing = true
fail_under = 85

exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
]

[tool.coverage.html]
directory = "htmlcov"
```

**Verificar threshold**:
```bash
pytest --cov=shopping_cart --cov-fail-under=85
```

---

## 🚀 Parte 4: Integración CI/CD

### Configurar GitHub Actions

**.github/workflows/tests.yml**:
```yaml
name: Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest -v
    
    - name: Run tests with coverage
      run: |
        pytest --cov=shopping_cart --cov-report=xml --cov-report=term-missing
    
    - name: Check coverage threshold
      run: |
        pytest --cov=shopping_cart --cov-fail-under=85
    
    - name: Upload coverage to Codecov (opcional)
      if: matrix.python-version == '3.11'
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

### Configurar Pre-commit Hook

**.pre-commit-config.yaml**:
```yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
        args: [--cov=shopping_cart, --cov-fail-under=85]
```

**Instalar pre-commit**:
```bash
pip install pre-commit
pre-commit install
```

---

## 📦 Entregables

### 1. Código Fuente

```
shopping_cart/
├── shopping_cart.py           # Implementación completa
├── test_shopping_cart.py      # Tests unitarios (mínimo 15 tests)
├── test_shopping_cart_properties.py  # Property tests (mínimo 5 properties)
├── requirements.txt
├── pyproject.toml             # Configuración de coverage
├── .github/workflows/tests.yml
├── .pre-commit-config.yaml
└── README.md                  # Documentación del proyecto
```

### 2. Reporte de Coverage

- Generar reporte HTML: `pytest --cov=shopping_cart --cov-report=html`
- Incluir captura de pantalla del reporte mostrando **≥85% coverage**
- Documentar en README.md el porcentaje alcanzado

### 3. Historial de Commits

**CRÍTICO**: Tu historial de commits debe demostrar TDD:

```
✅ Buena práctica (commits incrementales):

RED: Add failing test for empty cart
GREEN: Implement is_empty() method
REFACTOR: Extract cart items to property

RED: Add failing test for add_product
GREEN: Implement add_product method
REFACTOR: Validate price and quantity

RED: Add failing test for subtotal calculation
GREEN: Implement get_subtotal method
REFACTOR: Use list comprehension

...
```

```
❌ Mala práctica (commit único):

Implement complete shopping cart with tests
```

---

## 📚 Recursos Adicionales

- [pytest Documentation](https://docs.pytest.org/)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Martin Fowler - TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
- [Kent Beck - Test Driven Development by Example](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)



