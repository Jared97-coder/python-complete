"""
Módulo 9.5 - Testing de Endpoints con Pytest

Testing completo de APIs FastAPI con pytest, TestClient,
fixtures, mocking de dependencias, y testing de autenticación.

Para ejecutar tests:
    pytest 05_testing_endpoints.py -v
    pytest 05_testing_endpoints.py -v -s  # Con stdout
    pytest 05_testing_endpoints.py --cov # Con coverage
"""

import pytest
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# =============================================================================
# Aplicación de Ejemplo para Testing
# =============================================================================

app = FastAPI(title="Testing API")

# Base de datos simulada
items_db = {}
users_db = {}

# OAuth2 scheme simulado
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Schemas
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool
    created_at: datetime


class User(BaseModel):
    username: str
    email: str


# Dependencia simulada
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependencia: obtener usuario actual."""
    if token == "invalid":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": "testuser", "email": "test@example.com"}


# Endpoints
@app.get("/")
async def root():
    return {"message": "API for testing"}


@app.get("/items", response_model=list[ItemResponse])
async def list_items():
    """Listar items."""
    return list(items_db.values())


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """Obtener item por ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    """Crear item."""
    item_id = len(items_db) + 1
    item_data = ItemResponse(
        id=item_id,
        **item.model_dump(),
        created_at=datetime.now()
    )
    items_db[item_id] = item_data
    return item_data


@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: Item):
    """Actualizar item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    items_db[item_id].name = item.name
    items_db[item_id].price = item.price
    items_db[item_id].in_stock = item.in_stock
    
    return items_db[item_id]


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """Eliminar item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    del items_db[item_id]
    return None


@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """Endpoint protegido."""
    return current_user


@app.get("/search")
async def search_items(q: Optional[str] = None, skip: int = 0, limit: int = 10):
    """Buscar items con query parameters."""
    return {
        "query": q,
        "skip": skip,
        "limit": limit,
        "results": []
    }


# =============================================================================
# TESTS CON PYTEST
# =============================================================================

# =============================================================================
# Ejemplo 1: Fixtures Básicos
# =============================================================================

@pytest.fixture
def client():
    """
    Fixture: TestClient de FastAPI.
    
    TestClient se usa igual que requests:
    - client.get("/endpoint")
    - client.post("/endpoint", json={...})
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def clear_db():
    """
    Fixture: Limpiar DB antes de cada test.
    
    autouse=True → se ejecuta automáticamente en todos los tests.
    """
    items_db.clear()
    users_db.clear()
    yield  # Test se ejecuta aquí
    # Cleanup después del test


print("=== Ejemplo 1: Fixtures ===")
print("client: TestClient de FastAPI")
print("clear_db: Limpia DB automáticamente\n")


# =============================================================================
# Ejemplo 2: Tests de GET Endpoints
# =============================================================================

def test_read_root(client):
    """Test endpoint raíz."""
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "API for testing"}


def test_list_items_empty(client):
    """Test listar items (vacío)."""
    response = client.get("/items")
    
    assert response.status_code == 200
    assert response.json() == []


def test_get_item_not_found(client):
    """Test obtener item no existente."""
    response = client.get("/items/999")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


print("=== Ejemplo 2: Tests de GET ===")
print("test_read_root: Test endpoint básico")
print("test_list_items_empty: Test lista vacía")
print("test_get_item_not_found: Test 404\n")


# =============================================================================
# Ejemplo 3: Tests de POST Endpoints
# =============================================================================

def test_create_item(client):
    """Test crear item."""
    item_data = {
        "name": "Laptop",
        "price": 999.99,
        "in_stock": True
    }
    
    response = client.post("/items", json=item_data)
    
    # Verificar status code
    assert response.status_code == 201
    
    # Verificar response body
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 999.99
    assert data["in_stock"] is True
    assert "id" in data
    assert "created_at" in data


def test_create_item_validation_error(client):
    """Test crear item con datos inválidos."""
    invalid_data = {
        "name": "Item",
        # Falta "price" (obligatorio)
    }
    
    response = client.post("/items", json=invalid_data)
    
    assert response.status_code == 422  # Validation error


print("=== Ejemplo 3: Tests de POST ===")
print("test_create_item: Test creación exitosa")
print("test_create_item_validation_error: Test validación\n")


# =============================================================================
# Ejemplo 4: Tests de PUT/PATCH y DELETE
# =============================================================================

def test_update_item(client):
    """Test actualizar item."""
    # Crear item primero
    create_response = client.post("/items", json={
        "name": "Original",
        "price": 10.0
    })
    item_id = create_response.json()["id"]
    
    # Actualizar
    update_data = {
        "name": "Updated",
        "price": 20.0,
        "in_stock": False
    }
    response = client.put(f"/items/{item_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"
    assert data["price"] == 20.0
    assert data["in_stock"] is False


def test_delete_item(client):
    """Test eliminar item."""
    # Crear item
    create_response = client.post("/items", json={
        "name": "To Delete",
        "price": 5.0
    })
    item_id = create_response.json()["id"]
    
    # Eliminar
    response = client.delete(f"/items/{item_id}")
    
    assert response.status_code == 204
    
    # Verificar que no existe
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404


print("=== Ejemplo 4: Tests de PUT/DELETE ===")
print("test_update_item: Test actualización")
print("test_delete_item: Test eliminación\n")


# =============================================================================
# Ejemplo 5: Tests con Query Parameters
# =============================================================================

def test_search_with_query_params(client):
    """Test endpoint con query parameters."""
    response = client.get("/search?q=laptop&skip=0&limit=10")
    
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "laptop"
    assert data["skip"] == 0
    assert data["limit"] == 10


def test_search_with_default_params(client):
    """Test query parameters con defaults."""
    response = client.get("/search")
    
    assert response.status_code == 200
    data = response.json()
    assert data["query"] is None
    assert data["skip"] == 0
    assert data["limit"] == 10


print("=== Ejemplo 5: Tests con Query Parameters ===")
print("test_search_with_query_params: Test con parámetros")
print("test_search_with_default_params: Test con defaults\n")


# =============================================================================
# Ejemplo 6: Tests con Headers y Cookies
# =============================================================================

def test_with_custom_headers(client):
    """Test con headers personalizados."""
    headers = {
        "X-Custom-Header": "test-value",
        "User-Agent": "test-agent"
    }
    
    response = client.get("/", headers=headers)
    
    assert response.status_code == 200


def test_with_cookies(client):
    """Test con cookies."""
    cookies = {"session_id": "abc123"}
    
    response = client.get("/", cookies=cookies)
    
    assert response.status_code == 200


print("=== Ejemplo 6: Tests con Headers/Cookies ===")
print("test_with_custom_headers: Test headers")
print("test_with_cookies: Test cookies\n")


# =============================================================================
# Ejemplo 7: Fixture con Datos Iniciales
# =============================================================================

@pytest.fixture
def sample_items(client):
    """Fixture: Crear items de ejemplo."""
    items = [
        {"name": "Item 1", "price": 10.0},
        {"name": "Item 2", "price": 20.0},
        {"name": "Item 3", "price": 30.0}
    ]
    
    created_items = []
    for item in items:
        response = client.post("/items", json=item)
        created_items.append(response.json())
    
    return created_items


def test_list_items_with_data(client, sample_items):
    """Test listar items con datos iniciales."""
    response = client.get("/items")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["name"] == "Item 1"


print("=== Ejemplo 7: Fixture con Datos ===")
print("sample_items: Crea 3 items de ejemplo")
print("test_list_items_with_data: Usa fixture\n")


# =============================================================================
# Ejemplo 8: Testing de Autenticación (Mock Dependencies)
# =============================================================================

def test_protected_endpoint_with_token(client):
    """Test endpoint protegido con token válido."""
    headers = {"Authorization": "Bearer valid-token"}
    
    response = client.get("/users/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


def test_protected_endpoint_without_token(client):
    """Test endpoint protegido sin token."""
    response = client.get("/users/me")
    
    assert response.status_code == 403  # FastAPI devuelve 403 sin token


def test_protected_endpoint_with_invalid_token(client):
    """Test endpoint protegido con token inválido."""
    headers = {"Authorization": "Bearer invalid"}
    
    response = client.get("/users/me", headers=headers)
    
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


print("=== Ejemplo 8: Testing de Autenticación ===")
print("test_protected_endpoint_with_token: Token válido")
print("test_protected_endpoint_without_token: Sin token")
print("test_protected_endpoint_with_invalid_token: Token inválido\n")


# =============================================================================
# Ejemplo 9: Mocking de Dependencias
# =============================================================================

@pytest.fixture
def client_with_mocked_user():
    """Fixture: Client con usuario mock."""
    
    # Mock de la dependencia
    async def mock_get_current_user():
        return {"username": "mockuser", "email": "mock@example.com"}
    
    # Override dependency
    app.dependency_overrides[get_current_user] = mock_get_current_user
    
    with TestClient(app) as c:
        yield c
    
    # Limpiar override
    app.dependency_overrides.clear()


def test_with_mocked_dependency(client_with_mocked_user):
    """Test con dependencia mockeada."""
    headers = {"Authorization": "Bearer any-token"}
    
    response = client_with_mocked_user.get("/users/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "mockuser"


print("=== Ejemplo 9: Mocking de Dependencias ===")
print("client_with_mocked_user: Mock de get_current_user")
print("test_with_mocked_dependency: Test con mock\n")


# =============================================================================
# Ejemplo 10: Parametrize Tests
# =============================================================================

@pytest.mark.parametrize("item_name,price,expected_status", [
    ("Valid Item", 10.0, 201),
    ("Another Item", 99.99, 201),
])
def test_create_items_parametrized(client, item_name, price, expected_status):
    """Test parametrizado con múltiples casos."""
    response = client.post("/items", json={
        "name": item_name,
        "price": price
    })
    
    assert response.status_code == expected_status


print("=== Ejemplo 10: Parametrize Tests ===")
print("test_create_items_parametrized: Multiple test cases\n")


# =============================================================================
# Ejemplo 11: Testing de Errores y Excepciones
# =============================================================================

def test_handle_404(client):
    """Test manejo de 404."""
    response = client.get("/non-existent-endpoint")
    
    assert response.status_code == 404


def test_handle_422_validation(client):
    """Test manejo de errores de validación."""
    # Data inválida (price debe ser número)
    response = client.post("/items", json={
        "name": "Item",
        "price": "not-a-number"
    })
    
    assert response.status_code == 422
    assert "detail" in response.json()


print("=== Ejemplo 11: Testing de Errores ===")
print("test_handle_404: Test 404")
print("test_handle_422_validation: Test validación\n")


# =============================================================================
# Ejemplo 12: Testing Async Endpoints
# =============================================================================

@pytest.mark.asyncio
async def test_async_endpoint():
    """
    Test de endpoint async usando pytest-asyncio.
    
    Nota: TestClient ya maneja async automáticamente,
    este es un ejemplo de testing async explícito.
    """
    async with TestClient(app) as client:
        response = await client.get("/")
        assert response.status_code == 200


print("=== Ejemplo 12: Testing Async ===")
print("test_async_endpoint: Test explícito async\n")


# =============================================================================
# Ejemplo 13: Fixtures con Scope
# =============================================================================

@pytest.fixture(scope="module")
def module_client():
    """
    Fixture con scope=module.
    
    Se crea una vez por módulo (archivo), no por cada test.
    Útil para fixtures costosos.
    """
    print("  → Creating module-scoped client")
    with TestClient(app) as c:
        yield c
    print("  → Tearing down module-scoped client")


def test_with_module_fixture(module_client):
    """Test usando fixture de módulo."""
    response = module_client.get("/")
    assert response.status_code == 200


print("=== Ejemplo 13: Fixture Scopes ===")
print("module_client: Fixture scope=module\n")


# =============================================================================
# Ejemplo 14: Testing Response Headers
# =============================================================================

def test_response_headers(client):
    """Test headers de respuesta."""
    response = client.get("/")
    
    # Verificar headers
    assert "content-type" in response.headers
    assert response.headers["content-type"] == "application/json"


print("=== Ejemplo 14: Testing Response Headers ===")
print("test_response_headers: Verify response headers\n")


# =============================================================================
# Ejemplo 15: Integration Test (Flujo Completo)
# =============================================================================

def test_complete_crud_flow(client):
    """
    Test de integración: flujo CRUD completo.
    
    1. Crear item
    2. Leerlo
    3. Actualizarlo
    4. Eliminarlo
    """
    # 1. CREATE
    create_response = client.post("/items", json={
        "name": "Test Item",
        "price": 50.0
    })
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]
    
    # 2. READ
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test Item"
    
    # 3. UPDATE
    update_response = client.put(f"/items/{item_id}", json={
        "name": "Updated Item",
        "price": 100.0,
        "in_stock": False
    })
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Item"
    
    # 4. DELETE
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 204
    
    # 5. Verificar que no existe
    final_get = client.get(f"/items/{item_id}")
    assert final_get.status_code == 404


print("=== Ejemplo 15: Integration Test ===")
print("test_complete_crud_flow: Test CRUD completo\n")


# =============================================================================
# Instrucciones de Ejecución
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("TESTING DE ENDPOINTS con PYTEST - MÓDULO 9.5")
    print("=" * 70)
    print("\nPara ejecutar tests:")
    print("  pytest 05_testing_endpoints.py -v")
    print("  pytest 05_testing_endpoints.py -v -s  # Con stdout")
    print("  pytest 05_testing_endpoints.py -k test_create  # Solo tests con 'create'")
    print("  pytest 05_testing_endpoints.py --cov  # Con coverage")
    print("\nTests incluidos:")
    print("  ✓ Tests de GET, POST, PUT, DELETE")
    print("  ✓ Tests con query parameters")
    print("  ✓ Tests de autenticación (mocked)")
    print("  ✓ Tests de validación y errores")
    print("  ✓ Tests parametrizados")
    print("  ✓ Tests de integración (CRUD completo)")
    print("\nFixtures:")
    print("  ✓ client: TestClient de FastAPI")
    print("  ✓ clear_db: Limpiar DB automáticamente")
    print("  ✓ sample_items: Datos de ejemplo")
    print("  ✓ client_with_mocked_user: Mock de dependencia")
    print("\n" + "=" * 70)
    print("💡 Ejecuta pytest para ver todos los tests en acción")
    print("=" * 70 + "\n")
    
    # Ejecutar pytest programáticamente (opcional)
    # pytest.main([__file__, "-v"])
