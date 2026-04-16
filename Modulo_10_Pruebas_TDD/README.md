# 🧪 Módulo 10: Pruebas y TDD (Test-Driven Development)

## 📋 Índice

1. [Introducción al Testing](#introducción-al-testing)
2. [Test-Driven Development (TDD)](#test-driven-development-tdd)
3. [pytest - Framework de Testing](#pytest---framework-de-testing)
4. [Fixtures y Parametrización](#fixtures-y-parametrización)
5. [Mocking y Test Doubles](#mocking-y-test-doubles)
6. [Property-Based Testing](#property-based-testing)
7. [Cobertura de Código](#cobertura-de-código)
8. [Integración Continua (CI)](#integración-continua-ci)
9. [Best Practices](#best-practices)
10. [Recursos Adicionales](#recursos-adicionales)

---

## 🎯 Objetivos del Módulo

Al finalizar este módulo, serás capaz de:

✅ Comprender los principios de TDD (Red-Green-Refactor)  
✅ Escribir tests efectivos con pytest  
✅ Utilizar fixtures, parametrización y markers  
✅ Aplicar mocking para aislar unidades de código  
✅ Implementar property-based testing con Hypothesis  
✅ Medir y mejorar cobertura de código  
✅ Integrar tests en pipelines de CI/CD  

---

## 📚 Introducción al Testing

### ¿Por qué Testing?

#### **Beneficios del Testing**

| Beneficio | Descripción |
|-----------|-------------|
| 🛡️ **Confianza** | Detectar bugs antes de producción |
| 🔄 **Refactoring seguro** | Cambiar código sin miedo a romper funcionalidad |
| 📖 **Documentación viva** | Los tests muestran cómo usar el código |
| 🚀 **Velocidad** | Menos tiempo debuggeando manualmente |
| 💰 **Costo** | Arreglar bugs en desarrollo es 100x más barato que en producción |

### **Tipos de Tests**

```
        Pirámide de Testing
              /\
             /  \    E2E (End-to-End)
            /    \   - Lentos, frágiles
           /      \  - Pocos tests
          /--------\
         / Integra- \ Integration Tests
        / ción      \  - Moderados
       /            \  - Más tests
      /--------------\
     /   Unit Tests   \ Unit Tests
    /                  \ - Rápidos, aislados
   /____________________\ - Muchos tests
```

#### **1. Unit Tests (Pruebas Unitarias)**
- Prueban una **unidad** de código aislada (función, método, clase)
- Rápidos (< 1ms cada uno)
- Sin dependencias externas (DB, API, archivos)

```python
# Ejemplo: Unit test
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
```

#### **2. Integration Tests (Pruebas de Integración)**
- Prueban interacción entre componentes
- Moderadamente rápidos
- Pueden usar DB real, APIs, etc.

```python
# Ejemplo: Integration test
def test_create_user_in_database(db_session):
    user = User(username="test")
    db_session.add(user)
    db_session.commit()
    
    retrieved = db_session.query(User).filter_by(username="test").first()
    assert retrieved is not None
```

#### **3. E2E Tests (Pruebas End-to-End)**
- Prueban flujo completo de usuario
- Lentos (simulan navegador, etc.)
- Frágiles (muchas dependencias)

```python
# Ejemplo: E2E test con Selenium
def test_user_can_login(browser):
    browser.get("http://localhost:8000/login")
    browser.find_element_by_id("username").send_keys("user")
    browser.find_element_by_id("password").send_keys("pass")
    browser.find_element_by_id("submit").click()
    
    assert "Welcome" in browser.page_source
```

### **Estrategia de Testing**

- **70% Unit Tests**: Base sólida, rápidos, aislados
- **20% Integration Tests**: Verificar integración entre componentes
- **10% E2E Tests**: Flujos críticos de usuario

---

## 🔄 Test-Driven Development (TDD)

### **Ciclo Red-Green-Refactor**

```
    1. RED          2. GREEN        3. REFACTOR
   ┌─────────┐    ┌─────────┐     ┌─────────┐
   │ Escribir│    │ Escribir│     │  Mejorar│
   │  Test   │───▶│  Código │────▶│  Código │
   │ (Falla) │    │ (Pasa)  │     │ (Limpio)│
   └─────────┘    └─────────┘     └─────────┘
        ▲                               │
        └───────────────────────────────┘
```

### **Paso a Paso**

#### **1. 🔴 RED - Escribir Test que Falla**

```python
# test_calculator.py
def test_divide():
    """Test división (aún no implementada)."""
    result = divide(10, 2)
    assert result == 5
```

Ejecutar: `pytest test_calculator.py`  
**Resultado**: ❌ `NameError: name 'divide' is not defined`

#### **2. 🟢 GREEN - Implementar lo Mínimo para Pasar**

```python
# calculator.py
def divide(a, b):
    return a / b  # Implementación mínima
```

Ejecutar: `pytest test_calculator.py`  
**Resultado**: ✅ PASSED

#### **3. 🔵 REFACTOR - Mejorar el Código**

```python
# calculator.py
def divide(a, b):
    """Divide a by b, handling zero division."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

Agregar test para caso edge:

```python
def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
```

### **Ventajas de TDD**

✅ **Diseño mejor**: Pensar en la API antes de implementar  
✅ **Cobertura alta**: Código sin test no existe  
✅ **Refactoring confiado**: Tests aseguran que no rompiste nada  
✅ **Menos bugs**: Detectar problemas desde el inicio  

### **Desventajas de TDD**

⚠️ **Curva de aprendizaje**: Requiere práctica  
⚠️ **Tiempo inicial**: Más lento al principio  
⚠️ **Over-testing**: Riesgo de testear trivialidades  

---

## 🔬 pytest - Framework de Testing

### **¿Por qué pytest?**

| Característica | unittest (builtin) | pytest |
|----------------|-------------------|--------|
| Sintaxis | `self.assertEqual(a, b)` | `assert a == b` |
| Fixtures | `setUp()/tearDown()` | Decoradores flexibles |
| Parametrización | Manual | `@pytest.mark.parametrize` |
| Plugins | Pocos | Ecosistema enorme |
| Output | Básico | Rico y detallado |

### **Instalación**

```bash
pip install pytest pytest-asyncio pytest-cov pytest-xdist
```

### **Estructura de Tests**

```
proyecto/
├── src/
│   ├── __init__.py
│   └── calculator.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures compartidas
│   ├── test_calculator.py   # Tests del módulo
│   └── test_integration.py
├── pytest.ini               # Configuración pytest
└── pyproject.toml
```

### **Configuración pytest.ini**

```ini
[pytest]
# Directorios a testear
testpaths = tests

# Patrón de archivos de test
python_files = test_*.py *_test.py

# Patrón de clases de test
python_classes = Test*

# Patrón de funciones de test
python_functions = test_*

# Opciones por defecto
addopts = 
    -v                    # Verbose
    --strict-markers      # Error en markers no registrados
    --tb=short            # Traceback corto
    --cov=src             # Cobertura del src/
    --cov-report=html     # Reporte HTML
    --cov-report=term     # Reporte en terminal

# Markers personalizados
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### **Comandos Básicos**

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con verbose
pytest -v

# Ejecutar archivo específico
pytest tests/test_calculator.py

# Ejecutar test específico
pytest tests/test_calculator.py::test_add

# Ejecutar tests que coincidan con patrón
pytest -k "add or subtract"

# Ejecutar tests con marker
pytest -m "unit"

# Ejecutar en paralelo (requiere pytest-xdist)
pytest -n auto

# Detener en primer fallo
pytest -x

# Modo verbose con stdout
pytest -v -s

# Reporte de cobertura
pytest --cov=src --cov-report=html
```

### **Assertions en pytest**

pytest usa `assert` nativo de Python con introspección detallada:

```python
def test_assertions():
    # Comparaciones
    assert 2 + 2 == 4
    assert "hello" != "world"
    
    # Membresía
    assert "a" in "abc"
    assert 1 in [1, 2, 3]
    
    # Excepciones
    with pytest.raises(ValueError):
        int("not a number")
    
    # Excepciones con mensaje
    with pytest.raises(ValueError, match="invalid literal"):
        int("not a number")
    
    # Aproximación (floats)
    assert 0.1 + 0.2 == pytest.approx(0.3)
    
    # Warnings
    import warnings
    with pytest.warns(UserWarning):
        warnings.warn("something", UserWarning)
```

### **Mensajes de Error Detallados**

```python
def test_with_context():
    expected = [1, 2, 3]
    actual = [1, 2, 4]
    
    assert actual == expected
    # Output detallado de pytest:
    # AssertionError: assert [1, 2, 4] == [1, 2, 3]
    #   At index 2 diff: 4 != 3
```

---

## 🧰 Fixtures y Parametrización

### **Fixtures en pytest**

Fixtures permiten **setup/teardown** reutilizable:

```python
import pytest

@pytest.fixture
def sample_data():
    """Fixture simple: retorna datos."""
    return {"name": "Test User", "age": 30}

def test_with_fixture(sample_data):
    """Test recibe fixture como argumento."""
    assert sample_data["name"] == "Test User"
```

### **Fixture con Setup/Teardown**

```python
@pytest.fixture
def database_connection():
    """Fixture con cleanup."""
    # Setup
    db = Database()
    db.connect()
    
    yield db  # Test usa db aquí
    
    # Teardown (siempre se ejecuta)
    db.disconnect()

def test_query(database_connection):
    result = database_connection.query("SELECT * FROM users")
    assert len(result) > 0
```

### **Fixture Scopes**

| Scope | Descripción | Uso |
|-------|-------------|-----|
| `function` | **Default**. Nueva instancia por test | Setup barato |
| `class` | Una instancia por clase de tests | Setup moderado |
| `module` | Una instancia por archivo | Setup costoso |
| `session` | Una instancia por sesión de pytest | DB global, config |

```python
@pytest.fixture(scope="session")
def database():
    """DB compartida para toda la sesión."""
    db = create_database()
    yield db
    db.drop()

@pytest.fixture(scope="module")
def api_client():
    """Cliente API compartido por módulo."""
    client = APIClient()
    yield client
    client.close()
```

### **Fixture Factories**

```python
@pytest.fixture
def make_user():
    """Factory para crear múltiples usuarios."""
    users = []
    
    def _make_user(username, email):
        user = User(username=username, email=email)
        users.append(user)
        return user
    
    yield _make_user
    
    # Cleanup: eliminar todos los usuarios creados
    for user in users:
        user.delete()

def test_multiple_users(make_user):
    user1 = make_user("alice", "alice@example.com")
    user2 = make_user("bob", "bob@example.com")
    
    assert user1.username != user2.username
```

### **Parametrización**

Ejecutar mismo test con diferentes datos:

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
    (-2, 4),
])
def test_square(input, expected):
    assert input ** 2 == expected
```

Ejecutar: genera **4 tests** automáticamente:

```
test_square[2-4] PASSED
test_square[3-9] PASSED
test_square[4-16] PASSED
test_square[-2-4] PASSED
```

### **Parametrización Múltiple**

```python
@pytest.mark.parametrize("base", [2, 3])
@pytest.mark.parametrize("exponent", [2, 3])
def test_power(base, exponent):
    result = base ** exponent
    assert result > 0
# Genera: 2² 2³ 3² 3³ = 4 tests
```

### **IDs Personalizados en Parametrización**

```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (-2, 4),
], ids=["positive", "another_positive", "negative"])
def test_square(input, expected):
    assert input ** 2 == expected

# Output:
# test_square[positive] PASSED
# test_square[another_positive] PASSED
# test_square[negative] PASSED
```

### **Markers Personalizados**

```python
@pytest.mark.slow
def test_slow_operation():
    time.sleep(2)
    assert True

@pytest.mark.integration
def test_database_integration(db):
    assert db.query("SELECT 1") == 1
```

Ejecutar solo tests rápidos:

```bash
pytest -m "not slow"
```

### **Skip y XFail**

```python
@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    assert new_feature() == "result"

@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
def test_pattern_matching():
    match value:
        case 1:
            assert True

@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug():
    assert buggy_function() == "expected"  # Se espera que falle
```

---

## 🎭 Mocking y Test Doubles

### **¿Qué es Mocking?**

**Mocking** = Reemplazar dependencias reales con objetos simulados.

### **Test Doubles**

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Dummy** | Objeto que solo completa parámetros | `None`, `object()` |
| **Stub** | Retorna valores predefinidos | `lambda: 42` |
| **Spy** | Registra llamadas | `unittest.mock.spy` |
| **Mock** | Objeto configurable | `Mock()` |
| **Fake** | Implementación simplificada | In-memory DB |

### **unittest.mock**

Python incluye `unittest.mock` (builtin):

```python
from unittest.mock import Mock, patch, MagicMock

# Crear mock simple
mock_user = Mock()
mock_user.name = "Test User"
mock_user.get_age.return_value = 30

assert mock_user.name == "Test User"
assert mock_user.get_age() == 30

# Verificar llamadas
mock_user.get_age.assert_called_once()
```

### **Patch: Reemplazar Funciones**

```python
from unittest.mock import patch

# Código original
def get_user_from_api(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

# Test con mock
@patch('requests.get')
def test_get_user(mock_get):
    # Configurar mock
    mock_get.return_value.json.return_value = {"id": 1, "name": "Alice"}
    
    # Llamar código real
    user = get_user_from_api(user_id=1)
    
    # Verificar
    assert user["name"] == "Alice"
    mock_get.assert_called_once_with("https://api.example.com/users/1")
```

### **Context Manager Patch**

```python
def test_with_context_manager():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"id": 1}
        
        user = get_user_from_api(1)
        assert user["id"] == 1
```

### **Patch de Objetos**

```python
class EmailService:
    def send_email(self, to, subject, body):
        # Código real que envía email
        pass

def notify_user(user, message):
    email_service = EmailService()
    email_service.send_email(user.email, "Notification", message)

# Test
@patch.object(EmailService, 'send_email')
def test_notify_user(mock_send):
    user = Mock(email="test@example.com")
    
    notify_user(user, "Hello!")
    
    mock_send.assert_called_once_with("test@example.com", "Notification", "Hello!")
```

### **Side Effects**

```python
# Simular excepción
mock_api = Mock()
mock_api.get.side_effect = ConnectionError("API down")

with pytest.raises(ConnectionError):
    mock_api.get()

# Retornar valores diferentes en cada llamada
mock_random = Mock(side_effect=[1, 2, 3])
assert mock_random() == 1
assert mock_random() == 2
assert mock_random() == 3
```

### **MagicMock**

`MagicMock` soporta métodos mágicos (`__len__`, `__iter__`, etc.):

```python
from unittest.mock import MagicMock

mock_list = MagicMock()
mock_list.__len__.return_value = 3
mock_list.__iter__.return_value = iter([1, 2, 3])

assert len(mock_list) == 3
assert list(mock_list) == [1, 2, 3]
```

### **pytest-mock**

Plugin que mejora mocking en pytest:

```bash
pip install pytest-mock
```

```python
def test_with_mocker(mocker):
    # mocker.patch automáticamente cleanup
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.json.return_value = {"id": 1}
    
    user = get_user_from_api(1)
    assert user["id"] == 1
```

---

## 🎲 Property-Based Testing

### **¿Qué es Property-Based Testing?**

En lugar de testear casos específicos, defines **propiedades** que siempre deben cumplirse:

```python
# Example-based testing (tradicional)
def test_reverse_list():
    assert reverse([1, 2, 3]) == [3, 2, 1]
    assert reverse([]) == []

# Property-based testing
from hypothesis import given
import hypothesis.strategies as st

@given(st.lists(st.integers()))
def test_reverse_twice_is_identity(lst):
    """Revertir dos veces retorna la lista original."""
    assert reverse(reverse(lst)) == lst
```

### **Hypothesis**

```bash
pip install hypothesis
```

### **Strategies de Hypothesis**

```python
from hypothesis import given, strategies as st

# Integers
@given(st.integers())
def test_abs_positive(n):
    assert abs(n) >= 0

# Integers con rango
@given(st.integers(min_value=0, max_value=100))
def test_age_valid(age):
    assert 0 <= age <= 100

# Strings
@given(st.text())
def test_upper_lower(s):
    assert s.upper().lower() == s.lower()

# Lists
@given(st.lists(st.integers(), min_size=1))
def test_max_in_list(lst):
    assert max(lst) in lst

# Tuples
@given(st.tuples(st.integers(), st.text()))
def test_tuple(pair):
    num, text = pair
    assert isinstance(num, int)
    assert isinstance(text, str)

# Dictionaries
@given(st.dictionaries(st.text(), st.integers()))
def test_dict(d):
    for key in d:
        assert isinstance(key, str)
```

### **Propiedades Comunes**

#### **1. Idempotencia**
```python
@given(st.lists(st.integers()))
def test_sort_idempotent(lst):
    """Ordenar dos veces da mismo resultado."""
    assert sorted(sorted(lst)) == sorted(lst)
```

#### **2. Inverso**
```python
@given(st.text())
def test_encode_decode_inverse(s):
    """Encode + decode retorna original."""
    assert decode(encode(s)) == s
```

#### **3. Invariantes**
```python
@given(st.lists(st.integers()))
def test_length_preserved(lst):
    """Reverse preserva longitud."""
    assert len(reverse(lst)) == len(lst)
```

#### **4. Conmutatividad**
```python
@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert a + b == b + a
```

### **Shrinking: Minimizar Casos de Fallo**

Hypothesis automáticamente **reduce** el input que causa fallo:

```python
@given(st.lists(st.integers()))
def test_all_positive(lst):
    assert all(x > 0 for x in lst)

# Falla con: []  (lista vacía, caso minimal)
# No falla con lista gigante aleatoría
```

### **Example() y @example()**

Combinar property-based con casos específicos:

```python
from hypothesis import given, example

@given(st.integers())
@example(0)  # Asegurar que 0 se prueba
@example(-1)  # Asegurar que -1 se prueba
def test_abs(n):
    assert abs(n) >= 0
```

---

## 📊 Cobertura de Código

### **¿Qué es Cobertura?**

**Cobertura** = % de código ejecutado por tests.

### **Tipos de Cobertura**

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Line Coverage** | % de líneas ejecutadas | `if x > 0: y = 1` → ejecutar línea |
| **Branch Coverage** | % de ramas ejecutadas | `if/else` → ejecutar ambas ramas |
| **Function Coverage** | % de funciones llamadas | Todas las funciones testeadas |
| **Path Coverage** | Todos los caminos posibles | Combinaciones completas |

### **pytest-cov**

```bash
pip install pytest-cov
```

```bash
# Cobertura de src/
pytest --cov=src

# Reporte HTML
pytest --cov=src --cov-report=html

# Reporte con líneas faltantes
pytest --cov=src --cov-report=term-missing

# Fallo si cobertura < 80%
pytest --cov=src --cov-fail-under=80
```

### **Ejemplo de Reporte**

```
---------- coverage: platform win32, python 3.11 -----------
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
src/calculator.py      20      2    90%   45-46
src/utils.py           15      0   100%
-------------------------------------------------
TOTAL                  35      2    94%
```

### **Configuración en pyproject.toml**

```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=html --cov-report=term"

[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "venv/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

### **Cobertura como Métrica**

⚠️ **Advertencia**: Cobertura **NO** garantiza calidad.

```python
# 100% cobertura, pero test inútil
def add(a, b):
    return a + b

def test_add():
    add(2, 3)  # No hay assert! 😱
```

**Meta realista**: 80-90% cobertura con tests significativos.

---

## 🔄 Integración Continua (CI)

### **¿Qué es CI?**

**Continuous Integration** = Ejecutar tests automáticamente en cada push/PR.

### **GitHub Actions**

`.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          pytest --cov=src --cov-report=xml
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

### **GitLab CI**

`.gitlab-ci.yml`:

```yaml
image: python:3.11

stages:
  - test

test:
  stage: test
  script:
    - pip install -r requirements.txt
    - pytest --cov=src --cov-report=term
  coverage: '/TOTAL.*\s+(\d+%)$/'
```

### **Pre-commit Hooks**

Ejecutar tests locales antes de commit:

```bash
pip install pre-commit
```

`.pre-commit-config.yaml`:

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
```

---

## ✅ Best Practices

### **DO ✅**

1. **Nombres descriptivos**
   ```python
   # ❌ Mal
   def test_1():
       assert func() == 5
   
   # ✅ Bien
   def test_calculate_total_with_tax_returns_correct_amount():
       assert calculate_total(100, tax_rate=0.1) == 110
   ```

2. **Arrange-Act-Assert (AAA)**
   ```python
   def test_add_user():
       # Arrange: Setup
       db = Database()
       user = User(name="Alice")
       
       # Act: Ejecutar acción
       db.add(user)
       
       # Assert: Verificar resultado
       assert db.get_user_count() == 1
   ```

3. **Tests independientes**
   ```python
   # ❌ Mal: Test depende de orden
   def test_create():
       global user_id
       user_id = create_user()
   
   def test_update():
       update_user(user_id)  # Falla si test_create no corrió
   
   # ✅ Bien: Usar fixtures
   @pytest.fixture
   def user():
       return create_user()
   
   def test_update(user):
       update_user(user.id)
   ```

4. **Un concepto por test**
   ```python
   # ❌ Mal: Test hace demasiado
   def test_user_operations():
       user = create_user()
       update_user(user.id)
       delete_user(user.id)
       assert True
   
   # ✅ Bien: Separar en múltiples tests
   def test_create_user():
       user = create_user()
       assert user.id is not None
   
   def test_update_user():
       user = create_user()
       update_user(user.id, name="Bob")
       assert get_user(user.id).name == "Bob"
   ```

5. **Tests rápidos**
   - Unit tests < 10ms
   - Suite completa < 1min

### **DON'T ❌**

1. **No testear detalles de implementación**
   ```python
   # ❌ Mal: Test acoplado a implementación
   def test_sort_uses_quicksort():
       assert sort.algorithm == "quicksort"
   
   # ✅ Bien: Test comportamiento
   def test_sort_returns_sorted_list():
       assert sort([3, 1, 2]) == [1, 2, 3]
   ```

2. **No usar lógica en tests**
   ```python
   # ❌ Mal: If/for en tests
   def test_all_positive():
       numbers = [1, 2, 3]
       for n in numbers:
           assert n > 0
   
   # ✅ Bien: Parametrizar
   @pytest.mark.parametrize("n", [1, 2, 3])
   def test_positive(n):
       assert n > 0
   ```

3. **No mockear lo que no controlas**
   - Mock **tus** dependencias, no librerías de terceros

4. **No ignorar tests que fallan**
   ```python
   # ❌ Mal
   @pytest.mark.skip("Falla a veces, arreglar después")
   def test_flaky():
       ...
   
   # ✅ Bien: Arreglar o eliminar
   ```

---

## 📚 Recursos Adicionales

### **Documentación Oficial**
- [pytest](https://docs.pytest.org/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Hypothesis](https://hypothesis.readthedocs.io/)
- [Coverage.py](https://coverage.readthedocs.io/)

### **Libros**
- "Test Driven Development by Example" - Kent Beck
- "Growing Object-Oriented Software, Guided by Tests" - Freeman & Pryce
- "Python Testing with pytest" - Brian Okken

### **Artículos**
- [Effective Python Testing With Pytest](https://realpython.com/pytest-python-testing/)
- [Getting Started With Testing in Python](https://realpython.com/python-testing/)

### **Videos**
- [pytest: Conventions, Best Practices, and Plugins](https://www.youtube.com/watch?v=3bSWH6yOgpA)

---

## 🎯 Resumen

| Concepto | Herramienta | Uso Principal |
|----------|-------------|---------------|
| **Unit Testing** | pytest | Tests aislados, rápidos |
| **TDD** | Red-Green-Refactor | Diseño guiado por tests |
| **Fixtures** | `@pytest.fixture` | Setup/teardown reutilizable |
| **Parametrización** | `@pytest.mark.parametrize` | Múltiples casos de test |
| **Mocking** | `unittest.mock` | Aislar dependencias |
| **Property Testing** | Hypothesis | Tests generativos |
| **Cobertura** | pytest-cov | Medir líneas ejecutadas |
| **CI/CD** | GitHub Actions | Automatizar tests |

---

## 🚀 Próximos Pasos

1. **Practicar TDD** con ejercicio simple (calculadora, etc.)
2. **Implementar laboratorio** completo con TDD
3. **Agregar property-based tests** con Hypothesis
4. **Configurar CI/CD** en tu proyecto
5. **Medir cobertura** y apuntar a 80%+

---

**¡A testear!** 🧪✨
