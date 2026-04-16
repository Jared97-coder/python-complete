"""
Módulo 10.2 - Fixtures y Parametrización Avanzadas

Conceptos avanzados de pytest:
- Fixtures con diferentes scopes
- Fixtures con setup/teardown
- Fixture factories
- Parametrización de tests
- Parametrización de fixtures
- Markers personalizados

Para ejecutar:
    pytest 02_fixtures_avanzados.py -v
    pytest 02_fixtures_avanzados.py -v -s  # Con stdout
"""

import pytest
import tempfile
import os
from pathlib import Path

# =============================================================================
# CÓDIGO A TESTEAR
# =============================================================================

class Database:
    """Simulación de base de datos."""
    
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.users = {}
        self.connected = False
    
    def connect(self):
        """Conectar a la base de datos."""
        print(f"  → Connecting to {self.connection_string}")
        self.connected = True
    
    def disconnect(self):
        """Desconectar de la base de datos."""
        print(f"  → Disconnecting from {self.connection_string}")
        self.connected = False
        self.users.clear()
    
    def add_user(self, username, email):
        """Agregar usuario."""
        if not self.connected:
            raise RuntimeError("Database not connected")
        
        user_id = len(self.users) + 1
        self.users[user_id] = {'id': user_id, 'username': username, 'email': email}
        return user_id
    
    def get_user(self, user_id):
        """Obtener usuario."""
        return self.users.get(user_id)
    
    def get_all_users(self):
        """Obtener todos los usuarios."""
        return list(self.users.values())


class FileStorage:
    """Simulación de almacenamiento de archivos."""
    
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
    
    def save_file(self, filename, content):
        """Guardar archivo."""
        file_path = self.base_path / filename
        file_path.write_text(content)
        return file_path
    
    def read_file(self, filename):
        """Leer archivo."""
        file_path = self.base_path / filename
        return file_path.read_text()
    
    def delete_file(self, filename):
        """Eliminar archivo."""
        file_path = self.base_path / filename
        file_path.unlink()
    
    def cleanup(self):
        """Limpiar todos los archivos."""
        for file in self.base_path.glob("*"):
            file.unlink()
        self.base_path.rmdir()


# =============================================================================
# Ejemplo 1: Fixture Simple (Scope Function)
# =============================================================================

@pytest.fixture
def sample_data():
    """
    Fixture simple que retorna datos.
    
    Scope por defecto: function
    → Nueva instancia por cada test
    """
    print("\n  → Creating sample_data")
    return {"name": "Alice", "age": 30, "email": "alice@example.com"}


def test_use_sample_data(sample_data):
    """Test que usa fixture simple."""
    assert sample_data["name"] == "Alice"
    assert sample_data["age"] == 30


def test_modify_sample_data(sample_data):
    """Test que modifica fixture (no afecta otros tests)."""
    sample_data["age"] = 31  # Modificar copia local
    assert sample_data["age"] == 31


print("=== Ejemplo 1: Fixture Simple ===")
print("@pytest.fixture sin scope → nueva instancia por test\n")


# =============================================================================
# Ejemplo 2: Fixture con Setup/Teardown
# =============================================================================

@pytest.fixture
def database():
    """
    Fixture con setup/teardown.
    
    - Código antes de yield: Setup
    - yield: Retorna objeto al test
    - Código después de yield: Teardown (siempre se ejecuta)
    """
    # SETUP
    print("\n  → Setup: Creating database")
    db = Database("test_db.sqlite")
    db.connect()
    
    yield db  # Test usa db aquí
    
    # TEARDOWN (siempre se ejecuta, incluso si test falla)
    print("  → Teardown: Closing database")
    db.disconnect()


def test_database_add_user(database):
    """Test que usa fixture con setup/teardown."""
    user_id = database.add_user("bob", "bob@example.com")
    
    assert user_id == 1
    assert database.get_user(user_id)["username"] == "bob"


def test_database_multiple_users(database):
    """Test independiente (nueva instancia de database)."""
    database.add_user("alice", "alice@example.com")
    database.add_user("charlie", "charlie@example.com")
    
    users = database.get_all_users()
    assert len(users) == 2


print("=== Ejemplo 2: Fixture con Setup/Teardown ===")
print("yield: Divide setup y teardown\n")


# =============================================================================
# Ejemplo 3: Fixture Scopes
# =============================================================================

@pytest.fixture(scope="function")
def function_scope():
    """Fixture con scope=function (default)."""
    print("\n  → Creating function_scope fixture")
    return "function"


@pytest.fixture(scope="class")
def class_scope():
    """
    Fixture con scope=class.
    
    Se crea una vez por clase de tests.
    """
    print("\n  → Creating class_scope fixture (expensive operation)")
    return "class"


@pytest.fixture(scope="module")
def module_scope():
    """
    Fixture con scope=module.
    
    Se crea una vez por archivo de tests.
    """
    print("\n  → Creating module_scope fixture (very expensive operation)")
    return "module"


@pytest.fixture(scope="session")
def session_scope():
    """
    Fixture con scope=session.
    
    Se crea una vez por toda la sesión de pytest.
    Útil para recursos muy costosos.
    """
    print("\n  → Creating session_scope fixture (extremely expensive operation)")
    return "session"


class TestScopes:
    """Clase de tests para demostrar scopes."""
    
    def test_scopes_1(self, function_scope, class_scope, module_scope, session_scope):
        """Primer test de la clase."""
        assert function_scope == "function"
        assert class_scope == "class"
    
    def test_scopes_2(self, function_scope, class_scope, module_scope, session_scope):
        """Segundo test de la clase (class_scope no se recrea)."""
        assert function_scope == "function"
        assert class_scope == "class"


def test_scopes_outside_class(function_scope, module_scope):
    """Test fuera de clase."""
    assert function_scope == "function"
    assert module_scope == "module"


print("=== Ejemplo 3: Fixture Scopes ===")
print("function < class < module < session")
print("Usar scope alto para recursos costosos\n")


# =============================================================================
# Ejemplo 4: Fixture Factories
# =============================================================================

@pytest.fixture
def make_database():
    """
    Factory fixture: Retorna función para crear múltiples instancias.
    
    Útil cuando necesitas crear varios objetos en un test.
    """
    databases = []
    
    def _make_database(name):
        print(f"\n  → Creating database: {name}")
        db = Database(name)
        db.connect()
        databases.append(db)
        return db
    
    yield _make_database
    
    # Cleanup: Cerrar todas las databases creadas
    print("\n  → Cleanup: Closing all databases")
    for db in databases:
        db.disconnect()


def test_multiple_databases(make_database):
    """Test que crea múltiples databases."""
    db1 = make_database("db1.sqlite")
    db2 = make_database("db2.sqlite")
    
    db1.add_user("alice", "alice@example.com")
    db2.add_user("bob", "bob@example.com")
    
    assert len(db1.get_all_users()) == 1
    assert len(db2.get_all_users()) == 1


print("=== Ejemplo 4: Fixture Factories ===")
print("Factory fixture: Crear múltiples instancias en un test\n")


# =============================================================================
# Ejemplo 5: Fixture con Tempdir
# =============================================================================

@pytest.fixture
def temp_storage():
    """Fixture que crea almacenamiento temporal."""
    # Crear directorio temporal
    temp_dir = tempfile.mkdtemp()
    print(f"\n  → Created temp dir: {temp_dir}")
    
    storage = FileStorage(temp_dir)
    
    yield storage
    
    # Cleanup
    print(f"  → Cleaning up temp dir: {temp_dir}")
    storage.cleanup()


def test_file_storage_save(temp_storage):
    """Test de guardar archivo."""
    file_path = temp_storage.save_file("test.txt", "Hello World")
    
    assert file_path.exists()
    assert temp_storage.read_file("test.txt") == "Hello World"


def test_file_storage_delete(temp_storage):
    """Test de eliminar archivo."""
    temp_storage.save_file("delete_me.txt", "Content")
    temp_storage.delete_file("delete_me.txt")
    
    # Verificar que no existe
    with pytest.raises(FileNotFoundError):
        temp_storage.read_file("delete_me.txt")


print("=== Ejemplo 5: Fixture con Tempdir ===")
print("tempfile.mkdtemp() para tests de archivos\n")


# =============================================================================
# Ejemplo 6: pytest tmpdir Fixture (Builtin)
# =============================================================================

def test_with_tmpdir(tmp_path):
    """
    Test usando tmp_path (fixture builtin de pytest).
    
    tmp_path es un Path object que apunta a directorio temporal.
    Se limpia automáticamente después del test.
    """
    # Crear archivo en directorio temporal
    file = tmp_path / "test.txt"
    file.write_text("content")
    
    # Verificar
    assert file.read_text() == "content"
    assert file.exists()


def test_with_tmpdir_factory(tmp_path):
    """Test con múltiples archivos temporales."""
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    
    file1.write_text("content1")
    file2.write_text("content2")
    
    assert file1.read_text() == "content1"
    assert file2.read_text() == "content2"


print("=== Ejemplo 6: pytest tmp_path Fixture ===")
print("tmp_path: Fixture builtin para directorios temporales\n")


# =============================================================================
# Ejemplo 7: Parametrización Básica
# =============================================================================

@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
    (-2, 4),
    (0, 0),
])
def test_square_parametrized(input, expected):
    """
    Test parametrizado: Ejecuta 5 veces con diferentes valores.
    
    pytest genera: test_square_parametrized[2-4], test_square_parametrized[3-9], etc.
    """
    assert input ** 2 == expected


print("=== Ejemplo 7: Parametrización Básica ===")
print("@pytest.mark.parametrize: Múltiples casos de test\n")


# =============================================================================
# Ejemplo 8: Parametrización con IDs Personalizados
# =============================================================================

@pytest.mark.parametrize("input,expected", [
    (10, 2),
    (100, 3),
    (1000, 4),
], ids=["ten", "hundred", "thousand"])
def test_count_digits(input, expected):
    """Test con IDs personalizados."""
    assert len(str(input)) == expected


print("=== Ejemplo 8: Parametrización con IDs ===")
print("ids=[...]: Nombres personalizados para cada caso\n")


# =============================================================================
# Ejemplo 9: Parametrización Múltiple
# =============================================================================

@pytest.mark.parametrize("base", [2, 3, 10])
@pytest.mark.parametrize("exponent", [2, 3])
def test_power_combinations(base, exponent):
    """
    Parametrización múltiple: Genera producto cartesiano.
    
    3 bases × 2 exponentes = 6 tests
    """
    result = base ** exponent
    assert result > 0


print("=== Ejemplo 9: Parametrización Múltiple ===")
print("Múltiples decoradores: Producto cartesiano de parámetros\n")


# =============================================================================
# Ejemplo 10: Parametrización con pytest.param
# =============================================================================

@pytest.mark.parametrize("input,expected", [
    pytest.param(2, 4, id="positive"),
    pytest.param(-2, 4, id="negative"),
    pytest.param(0, 0, id="zero"),
    pytest.param(100, 10000, id="large", marks=pytest.mark.slow),
])
def test_square_with_param(input, expected):
    """Test con pytest.param para más control."""
    assert input ** 2 == expected


print("=== Ejemplo 10: pytest.param ===")
print("pytest.param: ID y markers por caso individual\n")


# =============================================================================
# Ejemplo 11: Parametrización de Fixtures
# =============================================================================

@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def database_type(request):
    """
    Fixture parametrizada: Ejecuta tests con diferentes valores.
    
    Tests que usen esta fixture se ejecutarán 3 veces.
    """
    db_type = request.param  # Acceder al parámetro actual
    print(f"\n  → Creating {db_type} database")
    
    db = Database(f"test_{db_type}.db")
    db.connect()
    
    yield db
    
    print(f"  → Closing {db_type} database")
    db.disconnect()


def test_with_parametrized_fixture(database_type):
    """Test que se ejecuta con cada tipo de database."""
    database_type.add_user("test", "test@example.com")
    assert len(database_type.get_all_users()) == 1


print("=== Ejemplo 11: Fixture Parametrizada ===")
print("@pytest.fixture(params=[...]): Tests se ejecutan con cada parámetro\n")


# =============================================================================
# Ejemplo 12: Combinación de Fixtures
# =============================================================================

@pytest.fixture
def database_with_users(database):
    """Fixture que depende de otra fixture (database)."""
    # database fixture ya conectó y creó DB
    database.add_user("alice", "alice@example.com")
    database.add_user("bob", "bob@example.com")
    
    return database


def test_preloaded_database(database_with_users):
    """Test con database pre-cargada."""
    users = database_with_users.get_all_users()
    
    assert len(users) == 2
    assert users[0]["username"] == "alice"
    assert users[1]["username"] == "bob"


print("=== Ejemplo 12: Composición de Fixtures ===")
print("Fixtures pueden depender de otras fixtures\n")


# =============================================================================
# Ejemplo 13: Autouse Fixtures
# =============================================================================

@pytest.fixture(autouse=True)
def reset_environment():
    """
    Fixture con autouse=True: Se ejecuta automáticamente.
    
    Útil para setup/teardown global.
    """
    print("\n  → [autouse] Resetting environment")
    # Setup código aquí
    
    yield
    
    print("  → [autouse] Cleanup environment")
    # Teardown código aquí


def test_with_autouse():
    """Test que usa autouse fixture automáticamente."""
    assert True


def test_another_with_autouse():
    """Otro test (autouse se ejecuta igual)."""
    assert True


print("=== Ejemplo 13: Autouse Fixtures ===")
print("autouse=True: Se ejecuta sin necesidad de mencionarla\n")


# =============================================================================
# Ejemplo 14: Fixture Request Object
# =============================================================================

@pytest.fixture
def dynamic_fixture(request):
    """
    Fixture que accede a metadatos del test.
    
    request object contiene:
    - request.node: Nodo del test
    - request.function: Función del test
    - request.cls: Clase del test (si existe)
    - request.module: Módulo del test
    """
    print(f"\n  → Test name: {request.node.name}")
    print(f"  → Test function: {request.function.__name__}")
    
    return "dynamic"


def test_with_request(dynamic_fixture):
    """Test que usa fixture con request."""
    assert dynamic_fixture == "dynamic"


print("=== Ejemplo 14: Request Object ===")
print("request: Acceder a metadatos del test en fixtures\n")


# =============================================================================
# Ejemplo 15: Fixture con Finalizer
# =============================================================================

@pytest.fixture
def resource_with_finalizer(request):
    """
    Fixture con finalizer explícito.
    
    Alternativa a yield para cleanup.
    """
    print("\n  → Creating resource")
    resource = {"data": "important"}
    
    def cleanup():
        print("  → Finalizer: Cleaning resource")
        resource.clear()
    
    request.addfinalizer(cleanup)
    
    return resource


def test_with_finalizer(resource_with_finalizer):
    """Test con fixture usando finalizer."""
    assert resource_with_finalizer["data"] == "important"


print("=== Ejemplo 15: Finalizer ===")
print("request.addfinalizer(): Registrar cleanup explícitamente\n")


# =============================================================================
# INSTRUCCIONES DE EJECUCIÓN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("FIXTURES Y PARAMETRIZACIÓN - MÓDULO 10.2")
    print("=" * 70)
    print("\nComandos de ejecución:")
    print("\n1. Ejecutar todos los tests:")
    print("   pytest 02_fixtures_avanzados.py -v")
    print("\n2. Ver output de fixtures (setup/teardown):")
    print("   pytest 02_fixtures_avanzados.py -v -s")
    print("\n3. Ver fixture setup:")
    print("   pytest 02_fixtures_avanzados.py --setup-show")
    print("\n4. Ejecutar solo tests parametrizados:")
    print("   pytest 02_fixtures_avanzados.py -k 'parametrized' -v")
    print("\n5. Ver lista de fixtures disponibles:")
    print("   pytest 02_fixtures_avanzados.py --fixtures")
    print("\n6. Ejecutar tests sin slow:")
    print("   pytest 02_fixtures_avanzados.py -m 'not slow' -v")
    print("\n" + "=" * 70)
    print("Conceptos cubiertos:")
    print("  ✓ Fixtures con diferentes scopes")
    print("  ✓ Setup/Teardown con yield")
    print("  ✓ Fixture factories")
    print("  ✓ Parametrización de tests")
    print("  ✓ Parametrización de fixtures")
    print("  ✓ Autouse fixtures")
    print("  ✓ Request object y finalizers")
    print("  ✓ tmp_path builtin fixture")
    print("=" * 70 + "\n")
