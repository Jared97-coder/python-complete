"""
Módulo 10: Pruebas y TDD
04 - Property-based Testing con Hypothesis

Property-based testing: En lugar de escribir casos de prueba específicos,
defines PROPIEDADES que deben cumplirse para todos los inputs posibles.
Hypothesis genera automáticamente casos de prueba y busca contraejemplos.

Ventajas:
- Encuentra edge cases que nunca pensarías manualmente
- Genera cientos de casos de prueba automáticamente
- Shrinking: minimiza automáticamente los casos de fallo
- Regresión: recuerda casos que fallaron anteriormente

Instalación: pip install hypothesis
"""

from hypothesis import given, example, assume, strategies as st, settings
from hypothesis.strategies import composite
import pytest
from typing import List
import json


# =============================================================================
# EJEMPLO 1: Estrategias Básicas - integers, text, floats, booleans
# =============================================================================

@given(st.integers())
def test_integers_basic(n):
    """
    Hypothesis genera integers (positivos, negativos, cero, grandes).
    Propiedad: multiplicar por 0 siempre da 0.
    """
    assert n * 0 == 0


@given(st.integers(min_value=0, max_value=100))
def test_integers_constrained(n):
    """
    Estrategia con restricciones.
    Propiedad: números en rango [0, 100] están en ese rango :)
    """
    assert 0 <= n <= 100
    assert n + 1 <= 101  # Al sumar 1, sigue siendo válido


@given(st.text())
def test_text_basic(s):
    """
    Hypothesis genera strings (vacíos, Unicode, caracteres especiales).
    Propiedad: concatenar string vacío no cambia el string.
    """
    assert s + "" == s
    assert "" + s == s


@given(st.floats(allow_nan=False, allow_infinity=False))
def test_floats_basic(x):
    """
    Floats sin NaN ni infinito.
    Propiedad: sumar 0.0 no cambia el valor.
    """
    assert x + 0.0 == x


# =============================================================================
# EJEMPLO 2: Propiedades - Idempotencia
# =============================================================================

def normalize_text(text: str) -> str:
    """Normaliza texto: lowercase y sin espacios extra."""
    return " ".join(text.lower().split())


@given(st.text())
def test_normalize_idempotent(text):
    """
    Propiedad de IDEMPOTENCIA: aplicar operación múltiples veces = aplicar una vez.
    normalize(normalize(text)) == normalize(text)
    """
    normalized_once = normalize_text(text)
    normalized_twice = normalize_text(normalized_once)
    
    assert normalized_once == normalized_twice


@given(st.lists(st.integers()))
def test_sorted_idempotent(lst):
    """
    Propiedad: sorted es idempotente.
    sorted(sorted(lst)) == sorted(lst)
    """
    assert sorted(sorted(lst)) == sorted(lst)


# =============================================================================
# EJEMPLO 3: Propiedades - Operaciones Inversas
# =============================================================================

def encode_base64(text: str) -> str:
    """Codifica texto en base64."""
    import base64
    return base64.b64encode(text.encode()).decode()


def decode_base64(encoded: str) -> str:
    """Decodifica texto de base64."""
    import base64
    return base64.b64decode(encoded.encode()).decode()


@given(st.text(alphabet=st.characters(min_codepoint=32, max_codepoint=126)))
def test_encode_decode_inverse(text):
    """
    Propiedad de OPERACIONES INVERSAS: decode(encode(x)) == x.
    Usamos alfabeto ASCII imprimible para evitar problemas de encoding.
    """
    encoded = encode_base64(text)
    decoded = decode_base64(encoded)
    
    assert decoded == text


@given(st.lists(st.integers()))
def test_reverse_inverse(lst):
    """
    Propiedad: reverse es su propia inversa.
    reverse(reverse(lst)) == lst
    """
    reversed_once = list(reversed(lst))
    reversed_twice = list(reversed(reversed_once))
    
    assert reversed_twice == lst


# =============================================================================
# EJEMPLO 4: Propiedades - Invariantes
# =============================================================================

@given(st.lists(st.integers()))
def test_reverse_length_invariant(lst):
    """
    Propiedad INVARIANTE: reverse no cambia la longitud.
    len(reverse(lst)) == len(lst)
    """
    reversed_list = list(reversed(lst))
    assert len(reversed_list) == len(lst)


@given(st.lists(st.integers(), min_size=1))
def test_max_in_list_invariant(lst):
    """
    Propiedad INVARIANTE: el máximo está en la lista.
    max(lst) in lst
    """
    maximum = max(lst)
    assert maximum in lst


@given(st.text())
def test_upper_length_invariant(text):
    """
    Propiedad INVARIANTE: upper() no cambia la longitud.
    len(text.upper()) == len(text)
    """
    assert len(text.upper()) == len(text)


# =============================================================================
# EJEMPLO 5: Propiedades - Conmutatividad
# =============================================================================

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """
    Propiedad CONMUTATIVA: a + b == b + a
    """
    assert a + b == b + a


@given(st.sets(st.integers()), st.sets(st.integers()))
def test_set_union_commutative(set1, set2):
    """
    Propiedad: la unión de conjuntos es conmutativa.
    set1 | set2 == set2 | set1
    """
    assert set1 | set2 == set2 | set1


@given(st.integers(), st.integers())
def test_multiplication_commutative(a, b):
    """
    Propiedad: multiplicación es conmutativa.
    a * b == b * a
    """
    assert a * b == b * a


# =============================================================================
# EJEMPLO 6: Propiedades - Asociatividad
# =============================================================================

@given(st.integers(), st.integers(), st.integers())
def test_addition_associative(a, b, c):
    """
    Propiedad ASOCIATIVA: (a + b) + c == a + (b + c)
    """
    assert (a + b) + c == a + (b + c)


@given(st.text(), st.text(), st.text())
def test_string_concatenation_associative(s1, s2, s3):
    """
    Propiedad: concatenación de strings es asociativa.
    (s1 + s2) + s3 == s1 + (s2 + s3)
    """
    assert (s1 + s2) + s3 == s1 + (s2 + s3)


# =============================================================================
# EJEMPLO 7: Estrategias de Colecciones - lists, tuples, dicts, sets
# =============================================================================

@given(st.lists(st.integers(), min_size=1, max_size=10))
def test_list_strategy_constrained(lst):
    """
    Lista con tamaño restringido [1, 10].
    Propiedad: sum de lista vacía es 0, sum de lista no-vacía puede ser cualquier cosa.
    """
    assert 1 <= len(lst) <= 10
    # Propiedad: el sum es la suma de todos los elementos
    assert sum(lst) == sum(x for x in lst)


@given(st.tuples(st.integers(), st.text(), st.booleans()))
def test_tuple_strategy(tup):
    """
    Tupla de tamaño fijo con tipos diferentes.
    Propiedad: tupla tiene exactamente 3 elementos con tipos correctos.
    """
    assert len(tup) == 3
    assert isinstance(tup[0], int)
    assert isinstance(tup[1], str)
    assert isinstance(tup[2], bool)


@given(st.dictionaries(keys=st.text(min_size=1, max_size=10), 
                       values=st.integers()))
def test_dictionary_strategy(d):
    """
    Diccionario con claves string y valores int.
    Propiedad: todas las claves están en dict.keys().
    """
    for key in d:
        assert key in d.keys()
        assert isinstance(d[key], int)


@given(st.sets(st.integers(), min_size=2, max_size=5))
def test_set_strategy(s):
    """
    Set con tamaño [2, 5].
    Propiedad: sets no tienen duplicados.
    """
    assert 2 <= len(s) <= 5
    # Convertir a lista y verificar que no hay duplicados
    lst = list(s)
    assert len(lst) == len(set(lst))


# =============================================================================
# EJEMPLO 8: Shrinking - Minimización Automática de Casos de Fallo
# =============================================================================

def buggy_function(lst: List[int]) -> int:
    """
    Función con bug: falla cuando la lista contiene un 0.
    Hypothesis encontrará el caso mínimo: [0]
    """
    if 0 in lst:
        raise ValueError("Cannot handle zero!")
    return sum(lst)


# Comentar este test para ver el shrinking en acción
# @given(st.lists(st.integers()))
# def test_buggy_function_shrinking(lst):
#     """
#     Si descomentas este test y lo ejecutas, Hypothesis:
#     1. Detectará el fallo cuando hay un 0
#     2. SHRINKING: reducirá el caso de fallo al mínimo
#     3. Reportará: lst=[0] (el caso más simple que reproduce el error)
#     
#     Ejemplo de shrinking:
#     - Caso inicial que falla: [1, 2, 0, 3, 4, 5]
#     - Hypothesis prueba: [0, 3, 4, 5] -> falla
#     - Hypothesis prueba: [0, 4, 5] -> falla
#     - Hypothesis prueba: [0, 5] -> falla
#     - Hypothesis prueba: [0] -> falla
#     - Caso mínimo: [0]
#     """
#     result = buggy_function(lst)
#     assert result >= 0  # Esta aserción fallará con listas que contengan 0


# =============================================================================
# EJEMPLO 9: Decorador @example - Casos Específicos Combinados
# =============================================================================

def divide_safe(a: int, b: int) -> float:
    """División segura que retorna 0 si b es 0."""
    if b == 0:
        return 0.0
    return a / b


@given(st.integers(), st.integers())
@example(10, 2)  # Caso específico: división exacta
@example(10, 0)  # Caso específico: división por cero
@example(-10, 2)  # Caso específico: división con negativo
def test_divide_safe_with_examples(a, b):
    """
    Combina property-based testing con casos específicos.
    Hypothesis genera muchos casos Y también prueba los @example explícitos.
    """
    result = divide_safe(a, b)
    
    # Propiedades:
    if b == 0:
        assert result == 0.0
    else:
        assert result == a / b
        # Propiedad inversa: multiplicar el resultado por b da aproximadamente a
        if b != 0:
            assert abs((result * b) - a) < 1e-10


# =============================================================================
# EJEMPLO 10: Composición de Estrategias - one_of, sampled_from
# =============================================================================

@given(st.one_of(st.integers(), st.text()))
def test_one_of_strategy(value):
    """
    st.one_of: genera valores de UNO de los tipos dados.
    Propiedad: el valor es o int o string.
    """
    assert isinstance(value, (int, str))


@given(st.sampled_from(['red', 'green', 'blue']))
def test_sampled_from_strategy(color):
    """
    st.sampled_from: genera valores de una lista específica.
    Propiedad: el color es uno de los permitidos.
    """
    assert color in ['red', 'green', 'blue']


@given(st.lists(st.sampled_from(['a', 'b', 'c']), min_size=1, max_size=5))
def test_list_of_sampled(items):
    """
    Combina lists con sampled_from.
    Propiedad: todos los elementos están en el conjunto permitido.
    """
    assert all(item in ['a', 'b', 'c'] for item in items)


# =============================================================================
# EJEMPLO 11: Estrategia Personalizada con @composite
# =============================================================================

@composite
def email_strategy(draw):
    """
    Estrategia personalizada para generar emails.
    draw() se usa para obtener valores de otras estrategias.
    """
    username = draw(st.text(alphabet=st.characters(min_codepoint=97, max_codepoint=122), 
                            min_size=1, max_size=10))
    domain = draw(st.sampled_from(['gmail.com', 'yahoo.com', 'outlook.com']))
    return f"{username}@{domain}"


@given(email_strategy())
def test_email_format(email):
    """
    Usa estrategia personalizada.
    Propiedad: el email tiene formato correcto.
    """
    assert '@' in email
    username, domain = email.split('@')
    assert len(username) >= 1
    assert domain in ['gmail.com', 'yahoo.com', 'outlook.com']


# =============================================================================
# EJEMPLO 12: assume() - Filtrado Condicional
# =============================================================================

@given(st.integers(), st.integers())
def test_division_with_assume(a, b):
    """
    assume() filtra casos que no queremos probar.
    Hypothesis descartará casos donde b == 0.
    """
    assume(b != 0)  # Solo prueba casos donde b != 0
    
    result = a / b
    # Propiedad: multiplicar resultado por b da a (aproximadamente)
    assert abs((result * b) - a) < 1e-10


@given(st.lists(st.integers()))
def test_list_operations_non_empty(lst):
    """
    assume() para filtrar listas vacías.
    """
    assume(len(lst) > 0)  # Solo listas no-vacías
    
    # Ahora podemos usar max() sin preocuparnos por ValueError
    maximum = max(lst)
    assert maximum in lst
    assert all(x <= maximum for x in lst)


# =============================================================================
# EJEMPLO 13: settings() - Configuración de Pruebas
# =============================================================================

@settings(max_examples=500)  # Genera 500 casos en lugar de 100 predeterminados
@given(st.lists(st.integers()))
def test_with_more_examples(lst):
    """
    @settings permite configurar el comportamiento de Hypothesis.
    max_examples: cantidad de casos a generar (default 100).
    """
    sorted_list = sorted(lst)
    # Propiedad: lista ordenada está ordenada :)
    for i in range(len(sorted_list) - 1):
        assert sorted_list[i] <= sorted_list[i + 1]


@settings(deadline=None)  # Sin límite de tiempo por test
@given(st.lists(st.integers(), min_size=100, max_size=1000))
def test_with_no_deadline(lst):
    """
    deadline=None: sin límite de tiempo (útil para operaciones lentas).
    Default: cada caso debe completarse en 200ms.
    """
    # Operación potencialmente lenta
    sorted_list = sorted(lst)
    assert len(sorted_list) == len(lst)


# =============================================================================
# EJEMPLO 14: Ejemplo Real - Testing Parser JSON
# =============================================================================

def safe_json_dumps(obj):
    """Serializa objeto a JSON string."""
    return json.dumps(obj, sort_keys=True)


def safe_json_loads(json_str):
    """Deserializa JSON string a objeto."""
    return json.loads(json_str)


@given(st.dictionaries(
    keys=st.text(alphabet=st.characters(min_codepoint=97, max_codepoint=122), min_size=1),
    values=st.one_of(st.integers(), st.text(), st.booleans(), st.none())
))
def test_json_roundtrip(obj):
    """
    Propiedad de ROUNDTRIP: parse(serialize(obj)) == obj
    Test crítico para parsers, codecs, serializers.
    """
    json_str = safe_json_dumps(obj)
    parsed = safe_json_loads(json_str)
    
    assert parsed == obj


# =============================================================================
# EJEMPLO 15: Ejemplo Real - Testing Función de Validación
# =============================================================================

def validate_password(password: str) -> bool:
    """
    Valida contraseña:
    - Mínimo 8 caracteres
    - Al menos una mayúscula
    - Al menos un dígito
    """
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True


@given(st.text(min_size=8))
def test_password_length_required(password):
    """
    Propiedad: si la contraseña no tiene mayúsculas o dígitos, falla.
    """
    if not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
        assert validate_password(password) is False


@given(st.text(alphabet=st.characters(min_codepoint=65, max_codepoint=90), min_size=1),  # Mayúsculas
       st.text(alphabet=st.characters(min_codepoint=48, max_codepoint=57), min_size=1),  # Dígitos
       st.text(min_size=6))  # Resto
def test_password_valid_when_requirements_met(upper, digit, rest):
    """
    Propiedad: si construimos contraseña con mayúscula + dígito + longitud suficiente,
    debería ser válida.
    """
    password = upper + digit + rest
    if len(password) >= 8:
        assert validate_password(password) is True


# =============================================================================
# RESUMEN DE CONCEPTOS
# =============================================================================

"""
ESTRATEGIAS BÁSICAS:
- st.integers(min_value=X, max_value=Y)
- st.floats(allow_nan=False, allow_infinity=False)
- st.text(alphabet=..., min_size=..., max_size=...)
- st.booleans()

ESTRATEGIAS DE COLECCIONES:
- st.lists(strategy, min_size=..., max_size=...)
- st.tuples(strategy1, strategy2, ...)
- st.dictionaries(keys=..., values=...)
- st.sets(strategy, min_size=..., max_size=...)

COMPOSICIÓN:
- st.one_of(strategy1, strategy2, ...)
- st.sampled_from([value1, value2, ...])
- @composite para estrategias personalizadas

PROPIEDADES COMUNES:
1. Idempotencia: f(f(x)) == f(x)
   Ejemplos: sorted, upper, normalize

2. Operaciones Inversas: decode(encode(x)) == x
   Ejemplos: encode/decode, serialize/deserialize, compress/decompress

3. Invariantes: propiedades que no cambian
   Ejemplos: len(reverse(x)) == len(x), max(x) in x

4. Conmutatividad: f(a, b) == f(b, a)
   Ejemplos: addition, multiplication, set union

5. Asociatividad: f(f(a, b), c) == f(a, f(b, c))
   Ejemplos: addition, string concatenation

DECORADORES:
- @given(strategy): define property test
- @example(value): añade caso específico
- @settings(max_examples=N, deadline=T): configura ejecución
- @composite: define estrategia personalizada

UTILIDADES:
- assume(condition): filtra casos
- draw(strategy): obtiene valor en @composite

SHRINKING:
Hypothesis minimiza automáticamente casos de fallo.
Ejemplo: [1, 2, 0, 3, 4] → [0]

COMANDOS ÚTILES:
pytest test_file.py -v                    # Ejecutar tests
pytest test_file.py --hypothesis-show-statistics  # Ver estadísticas
pytest test_file.py -k test_name          # Ejecutar test específico

BEST PRACTICES:
✅ DO: Pensar en propiedades, no en casos específicos
✅ DO: Combinar @given con @example para regressions
✅ DO: Usar assume() para filtrar casos inválidos
✅ DO: Definir estrategias personalizadas para dominios complejos
❌ DON'T: Asumir que Hypothesis probará TODO (usa max_examples alto para críticos)
❌ DON'T: Usar lógica compleja en tests de propiedades (duplica bugs)
❌ DON'T: Ignorar shrinking (el caso mínimo es tu mejor pista)
"""
