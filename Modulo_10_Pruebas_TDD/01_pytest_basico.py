"""
Módulo 10.1 - pytest Básico

Fundamentos de testing con pytest:
- Estructura de tests
- Assertions
- Excepciones y warnings
- Markers y skip
- Comandos básicos

Para ejecutar:
    pytest 01_pytest_basico.py -v
    pytest 01_pytest_basico.py::test_add -v  # Test específico
    pytest 01_pytest_basico.py -k "add" -v   # Tests que coincidan con patrón
"""

import pytest
import sys
import warnings

# =============================================================================
# CÓDIGO A TESTEAR (Sistema bajo prueba / SUT)
# =============================================================================

def add(a, b):
    """Suma dos números."""
    return a + b


def subtract(a, b):
    """Resta dos números."""
    return a - b


def multiply(a, b):
    """Multiplica dos números."""
    return a * b


def divide(a, b):
    """Divide a por b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def is_even(n):
    """Verifica si un número es par."""
    return n % 2 == 0


def get_grade(score):
    """Retorna letra según score (0-100)."""
    if not 0 <= score <= 100:
        raise ValueError("Score must be between 0 and 100")
    
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


def deprecated_function():
    """Función deprecada que genera warning."""
    warnings.warn("This function is deprecated", DeprecationWarning)
    return "old behavior"


class Calculator:
    """Calculadora simple con historial."""
    
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def clear_history(self):
        self.history.clear()
    
    def get_history(self):
        return self.history.copy()


# =============================================================================
# Ejemplo 1: Tests Básicos
# =============================================================================

def test_add():
    """Test básico de suma."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract():
    """Test básico de resta."""
    assert subtract(5, 3) == 2
    assert subtract(10, 10) == 0
    assert subtract(0, 5) == -5


def test_multiply():
    """Test básico de multiplicación."""
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6
    assert multiply(0, 100) == 0


print("=== Ejemplo 1: Tests Básicos ===")
print("test_add, test_subtract, test_multiply")
print("Ejecutar: pytest 01_pytest_basico.py::test_add -v\n")


# =============================================================================
# Ejemplo 2: Assertions Avanzados
# =============================================================================

def test_assertions_comparisons():
    """Tests de comparaciones."""
    assert 5 > 3
    assert 10 >= 10
    assert 2 < 5
    assert 3 <= 3
    
    # Comparación de floats con aproximación
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert 3.14159 == pytest.approx(3.14, abs=0.01)


def test_assertions_membership():
    """Tests de membresía."""
    assert 'a' in 'abc'
    assert 'x' not in 'abc'
    
    assert 1 in [1, 2, 3]
    assert 'key' in {'key': 'value'}


def test_assertions_type():
    """Tests de tipos."""
    assert isinstance(5, int)
    assert isinstance("hello", str)
    assert isinstance([1, 2], list)
    
    assert type(5) == int
    assert type("hello") == str


def test_assertions_boolean():
    """Tests de booleanos."""
    assert True
    assert not False
    
    assert is_even(4)
    assert not is_even(5)
    
    # Truthy/Falsy
    assert [1, 2, 3]  # Lista no vacía es truthy
    assert not []     # Lista vacía es falsy
    assert "text"     # String no vacío
    assert not ""     # String vacío


print("=== Ejemplo 2: Assertions Avanzados ===")
print("test_assertions_comparisons, test_assertions_membership")
print("test_assertions_type, test_assertions_boolean\n")


# =============================================================================
# Ejemplo 3: Testing de Excepciones
# =============================================================================

def test_divide_by_zero():
    """Test que verifica que se levanta excepción."""
    with pytest.raises(ValueError):
        divide(10, 0)


def test_divide_by_zero_with_message():
    """Test que verifica excepción y mensaje."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


def test_invalid_grade_score():
    """Test de score inválido."""
    with pytest.raises(ValueError, match="must be between 0 and 100"):
        get_grade(150)
    
    with pytest.raises(ValueError):
        get_grade(-10)


def test_exception_info():
    """Test que captura info de la excepción."""
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    
    # Verificar detalles de la excepción
    assert "Cannot divide by zero" in str(exc_info.value)
    assert exc_info.type == ValueError


print("=== Ejemplo 3: Testing de Excepciones ===")
print("test_divide_by_zero, test_invalid_grade_score")
print("test_exception_info\n")


# =============================================================================
# Ejemplo 4: Testing de Warnings
# =============================================================================

def test_deprecated_warning():
    """Test que verifica warning."""
    with pytest.warns(DeprecationWarning):
        deprecated_function()


def test_deprecated_warning_message():
    """Test que verifica warning con mensaje."""
    with pytest.warns(DeprecationWarning, match="deprecated"):
        deprecated_function()


print("=== Ejemplo 4: Testing de Warnings ===")
print("test_deprecated_warning, test_deprecated_warning_message\n")


# =============================================================================
# Ejemplo 5: Testing de Clases
# =============================================================================

def test_calculator_initialization():
    """Test de inicialización de Calculator."""
    calc = Calculator()
    assert calc.history == []


def test_calculator_add():
    """Test de método add de Calculator."""
    calc = Calculator()
    result = calc.add(2, 3)
    
    assert result == 5
    assert len(calc.history) == 1
    assert "2 + 3 = 5" in calc.history[0]


def test_calculator_history():
    """Test de historial."""
    calc = Calculator()
    
    calc.add(1, 2)
    calc.add(3, 4)
    
    history = calc.get_history()
    assert len(history) == 2
    assert "1 + 2 = 3" in history[0]
    assert "3 + 4 = 7" in history[1]


def test_calculator_clear_history():
    """Test de limpiar historial."""
    calc = Calculator()
    
    calc.add(1, 2)
    assert len(calc.history) == 1
    
    calc.clear_history()
    assert len(calc.history) == 0


print("=== Ejemplo 5: Testing de Clases ===")
print("test_calculator_initialization, test_calculator_add")
print("test_calculator_history, test_calculator_clear_history\n")


# =============================================================================
# Ejemplo 6: Markers - Skip y Skipif
# =============================================================================

@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    """Test de feature futura (skip)."""
    assert future_function() == "result"


@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
def test_python_310_feature():
    """Test que requiere Python 3.10+."""
    # Pattern matching (Python 3.10+)
    value = 1
    match value:
        case 1:
            result = "one"
        case _:
            result = "other"
    
    assert result == "one"


@pytest.mark.skipif(sys.platform != "win32", reason="Windows only")
def test_windows_specific():
    """Test específico de Windows."""
    assert sys.platform == "win32"


print("=== Ejemplo 6: Markers - Skip/Skipif ===")
print("@pytest.mark.skip: Saltar test temporalmente")
print("@pytest.mark.skipif: Saltar condicionalmente\n")


# =============================================================================
# Ejemplo 7: Markers - XFail
# =============================================================================

@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug():
    """Test de bug conocido (se espera que falle)."""
    assert buggy_function() == "expected"  # Función no existe


@pytest.mark.xfail(sys.platform == "darwin", reason="Flaky on macOS")
def test_flaky_on_macos():
    """Test que puede fallar en macOS."""
    assert True


print("=== Ejemplo 7: Markers - XFail ===")
print("@pytest.mark.xfail: Test que se espera que falle")
print("Útil para bugs conocidos pendientes\n")


# =============================================================================
# Ejemplo 8: Markers Personalizados
# =============================================================================

@pytest.mark.slow
def test_slow_operation():
    """Test lento marcado como 'slow'."""
    import time
    time.sleep(0.1)  # Simular operación lenta
    assert True


@pytest.mark.integration
def test_database_integration():
    """Test de integración marcado."""
    # Simular test de integración
    assert True


@pytest.mark.unit
def test_unit_test():
    """Test unitario marcado."""
    assert add(2, 3) == 5


print("=== Ejemplo 8: Markers Personalizados ===")
print("Definir en pytest.ini:")
print("[pytest]")
print("markers =")
print("    slow: marks tests as slow")
print("    integration: integration tests")
print("    unit: unit tests")
print("\nEjecutar: pytest -m 'not slow' -v\n")


# =============================================================================
# Ejemplo 9: Múltiples Assertions
# =============================================================================

def test_grade_system():
    """Test completo del sistema de calificaciones."""
    # Rango A
    assert get_grade(90) == 'A'
    assert get_grade(95) == 'A'
    assert get_grade(100) == 'A'
    
    # Rango B
    assert get_grade(80) == 'B'
    assert get_grade(85) == 'B'
    assert get_grade(89) == 'B'
    
    # Rango C
    assert get_grade(70) == 'C'
    
    # Rango D
    assert get_grade(60) == 'D'
    
    # Rango F
    assert get_grade(0) == 'F'
    assert get_grade(59) == 'F'


print("=== Ejemplo 9: Múltiples Assertions ===")
print("test_grade_system: Verificar múltiples casos\n")


# =============================================================================
# Ejemplo 10: Test de Igualdad de Colecciones
# =============================================================================

def test_list_equality():
    """Test de igualdad de listas."""
    assert [1, 2, 3] == [1, 2, 3]
    assert [1, 2, 3] != [3, 2, 1]


def test_dict_equality():
    """Test de igualdad de diccionarios."""
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'b': 2, 'a': 1}  # Orden diferente
    
    assert dict1 == dict2  # Orden no importa en dicts


def test_set_equality():
    """Test de igualdad de sets."""
    assert {1, 2, 3} == {3, 2, 1}  # Orden no importa


def test_partial_dict_matching():
    """Test de coincidencia parcial de dict."""
    user = {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'}
    
    # Verificar claves específicas
    assert user['name'] == 'Alice'
    assert user['id'] == 1
    
    # Verificar que tiene ciertas claves
    assert 'email' in user
    assert 'password' not in user


print("=== Ejemplo 10: Igualdad de Colecciones ===")
print("test_list_equality, test_dict_equality, test_set_equality\n")


# =============================================================================
# Ejemplo 11: Test de Strings
# =============================================================================

def test_string_operations():
    """Test de operaciones con strings."""
    text = "Hello World"
    
    # Contiene
    assert "Hello" in text
    assert "Bye" not in text
    
    # Case
    assert text.upper() == "HELLO WORLD"
    assert text.lower() == "hello world"
    
    # Empieza/termina
    assert text.startswith("Hello")
    assert text.endswith("World")
    
    # Longitud
    assert len(text) == 11


def test_string_formatting():
    """Test de formateo de strings."""
    name = "Alice"
    age = 30
    
    # f-strings
    result = f"Name: {name}, Age: {age}"
    assert result == "Name: Alice, Age: 30"
    
    # format()
    result = "Name: {}, Age: {}".format(name, age)
    assert result == "Name: Alice, Age: 30"


print("=== Ejemplo 11: Test de Strings ===")
print("test_string_operations, test_string_formatting\n")


# =============================================================================
# Ejemplo 12: Test con Múltiples Pasos (AAA Pattern)
# =============================================================================

def test_calculator_workflow():
    """
    Test completo usando patrón AAA (Arrange-Act-Assert).
    
    AAA Pattern:
    - Arrange: Setup (crear objetos, datos)
    - Act: Ejecutar acción bajo prueba
    - Assert: Verificar resultado
    """
    # ARRANGE: Setup
    calc = Calculator()
    
    # ACT: Ejecutar operaciones
    result1 = calc.add(5, 3)
    result2 = calc.add(10, 20)
    
    # ASSERT: Verificar resultados
    assert result1 == 8
    assert result2 == 30
    assert len(calc.get_history()) == 2


print("=== Ejemplo 12: AAA Pattern ===")
print("Arrange-Act-Assert: Patrón estándar de testing\n")


# =============================================================================
# Ejemplo 13: Test de Edge Cases (Casos Límite)
# =============================================================================

def test_divide_edge_cases():
    """Test de casos límite de división."""
    # División normal
    assert divide(10, 2) == 5.0
    
    # Dividir por 1
    assert divide(10, 1) == 10.0
    
    # Dividir 0
    assert divide(0, 5) == 0.0
    
    # División con negativos
    assert divide(-10, 2) == -5.0
    assert divide(10, -2) == -5.0
    assert divide(-10, -2) == 5.0
    
    # División por cero (debe fallar)
    with pytest.raises(ValueError):
        divide(10, 0)


def test_grade_edge_cases():
    """Test de casos límite de calificaciones."""
    # Límites exactos
    assert get_grade(0) == 'F'
    assert get_grade(100) == 'A'
    
    # Límites de rangos
    assert get_grade(59) == 'F'
    assert get_grade(60) == 'D'
    
    assert get_grade(69) == 'D'
    assert get_grade(70) == 'C'
    
    assert get_grade(79) == 'C'
    assert get_grade(80) == 'B'
    
    assert get_grade(89) == 'B'
    assert get_grade(90) == 'A'


print("=== Ejemplo 13: Edge Cases ===")
print("test_divide_edge_cases, test_grade_edge_cases")
print("Importante: Testear límites y casos especiales\n")


# =============================================================================
# Ejemplo 14: Test que Debe Fallar (Demostración)
# =============================================================================

@pytest.mark.xfail(strict=True, reason="Demostración de fallo")
def test_intentional_failure():
    """Test que falla intencionalmente para demostración."""
    assert 2 + 2 == 5  # Esto fallará


print("=== Ejemplo 14: Test de Fallo Intencional ===")
print("test_intentional_failure: Marcado como xfail\n")


# =============================================================================
# Ejemplo 15: Mensajes de Assertion Personalizados
# =============================================================================

def test_with_custom_messages():
    """Test con mensajes de error personalizados."""
    score = 75
    
    # Mensaje personalizado en assertion
    assert score >= 0, f"Score {score} should not be negative"
    assert score <= 100, f"Score {score} should not exceed 100"
    
    # Mensaje más descriptivo
    expected_grade = 'C'
    actual_grade = get_grade(score)
    assert actual_grade == expected_grade, \
        f"Expected grade {expected_grade} for score {score}, but got {actual_grade}"


print("=== Ejemplo 15: Mensajes Personalizados ===")
print("test_with_custom_messages: assert con mensajes descriptivos\n")


# =============================================================================
# INSTRUCCIONES DE EJECUCIÓN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("PYTEST BÁSICO - MÓDULO 10.1")
    print("=" * 70)
    print("\nComandos de ejecución:")
    print("\n1. Ejecutar todos los tests:")
    print("   pytest 01_pytest_basico.py -v")
    print("\n2. Ejecutar test específico:")
    print("   pytest 01_pytest_basico.py::test_add -v")
    print("\n3. Ejecutar tests que coincidan con patrón:")
    print("   pytest 01_pytest_basico.py -k 'calculator' -v")
    print("\n4. Ejecutar sin tests lentos:")
    print("   pytest 01_pytest_basico.py -m 'not slow' -v")
    print("\n5. Ejecutar solo tests de integración:")
    print("   pytest 01_pytest_basico.py -m integration -v")
    print("\n6. Mostrar output (print statements):")
    print("   pytest 01_pytest_basico.py -v -s")
    print("\n7. Detener en primer fallo:")
    print("   pytest 01_pytest_basico.py -x")
    print("\n8. Ver resumen de tests:")
    print("   pytest 01_pytest_basico.py --tb=short")
    print("\n" + "=" * 70)
    print("Conceptos cubiertos:")
    print("  ✓ Assertions básicos y avanzados")
    print("  ✓ Testing de excepciones y warnings")
    print("  ✓ Testing de clases")
    print("  ✓ Markers (skip, skipif, xfail, custom)")
    print("  ✓ Edge cases y AAA pattern")
    print("  ✓ Mensajes de error personalizados")
    print("=" * 70 + "\n")
    
    # No ejecutar pytest desde aquí (usar CLI)
    # pytest.main([__file__, "-v"])
