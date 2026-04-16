"""
Módulo 9.1 - FastAPI Básico

Introducción a FastAPI: primera aplicación, path parameters,
query parameters, request body, response models, y async/await.

Para ejecutar:
    uvicorn 01_fastapi_basico:app --reload
    
Ver documentación:
    http://localhost:8000/docs       # Swagger UI
    http://localhost:8000/redoc      # ReDoc
"""

from fastapi import FastAPI, Path, Query, Body, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum
import asyncio

# =============================================================================
# Ejemplo 1: Primera Aplicación FastAPI
# =============================================================================

app = FastAPI(
    title="FastAPI Básico - Módulo 9",
    description="API de ejemplo para aprender FastAPI",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Endpoint raíz."""
    return {"message": "¡Bienvenido a FastAPI!", "docs": "/docs"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


print("\n=== Ejemplo 1: Primera Aplicación ===")
print("FastAPI creada con éxito")
print("Ejecutar: uvicorn 01_fastapi_basico:app --reload")
print("Visitar: http://localhost:8000/docs\n")


# =============================================================================
# Ejemplo 2: Path Parameters
# =============================================================================

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """
    Obtener item por ID.
    
    Path parameter con validación automática de tipo.
    """
    return {"item_id": item_id, "name": f"Item {item_id}"}


@app.get("/users/{user_id}/orders/{order_id}")
async def read_user_order(user_id: int, order_id: int):
    """Múltiples path parameters."""
    return {
        "user_id": user_id,
        "order_id": order_id,
        "message": f"Order {order_id} for user {user_id}"
    }


# Path parameters con validación avanzada
@app.get("/products/{product_id}")
async def read_product(
    product_id: int = Path(
        ...,  # Obligatorio
        title="Product ID",
        description="El ID del producto debe ser mayor a 0",
        gt=0,  # Greater than
        le=1000  # Less than or equal
    )
):
    """Path parameter con validaciones personalizadas."""
    return {"product_id": product_id}


# =============================================================================
# Ejemplo 3: Query Parameters
# =============================================================================

@app.get("/search")
async def search_items(
    q: Optional[str] = None,  # Opcional
    skip: int = 0,  # Default 0
    limit: int = 10  # Default 10
):
    """
    Buscar items con query parameters.
    
    Ejemplos:
        /search
        /search?q=laptop
        /search?skip=10&limit=20
        /search?q=phone&skip=0&limit=5
    """
    return {
        "query": q,
        "skip": skip,
        "limit": limit,
        "results": [f"Item {i}" for i in range(skip, skip + limit)]
    }


# Query parameters con validación
@app.get("/items")
async def list_items(
    skip: int = Query(0, ge=0, description="Número de items a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Máximo de items"),
    sort: str = Query("asc", regex="^(asc|desc)$"),
    active: bool = Query(True)
):
    """Query parameters con validación avanzada."""
    return {
        "skip": skip,
        "limit": limit,
        "sort": sort,
        "active": active
    }


# =============================================================================
# Ejemplo 4: Request Body con Pydantic
# =============================================================================

class Item(BaseModel):
    """Schema de Item."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0, description="Precio debe ser mayor a 0")
    tax: Optional[float] = Field(None, ge=0)
    in_stock: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Laptop",
                "description": "High performance laptop",
                "price": 1299.99,
                "tax": 129.99,
                "in_stock": True
            }
        }


@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    """
    Crear nuevo item.
    
    Request body validado automáticamente con Pydantic.
    """
    item_dict = item.model_dump()
    
    # Simular cálculo de total
    if item.tax:
        item_dict["total"] = item.price + item.tax
    
    return {
        "message": "Item creado exitosamente",
        "item": item_dict
    }


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """
    Actualizar item existente.
    
    Combina path parameter y request body.
    """
    return {
        "message": "Item actualizado",
        "item_id": item_id,
        "item": item.model_dump()
    }


# =============================================================================
# Ejemplo 5: Response Models
# =============================================================================

class UserCreate(BaseModel):
    """Schema para crear usuario (con password)."""
    email: EmailStr
    name: str
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    """Schema de respuesta (sin password)."""
    id: int
    email: EmailStr
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True  # Para SQLAlchemy models


# Base de datos simulada
fake_users_db = []
user_id_counter = 1


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Crear usuario.
    
    Response model filtra el password automáticamente.
    """
    global user_id_counter
    
    # Simular creación
    user_dict = user.model_dump()
    user_dict["id"] = user_id_counter
    user_dict["created_at"] = datetime.now()
    
    fake_users_db.append(user_dict)
    user_id_counter += 1
    
    # FastAPI filtra solo campos de UserResponse
    return user_dict


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Obtener usuario por ID."""
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


@app.get("/users", response_model=List[UserResponse])
async def list_users():
    """Listar todos los usuarios."""
    return fake_users_db


# =============================================================================
# Ejemplo 6: Enums para Validación
# =============================================================================

class OrderStatus(str, Enum):
    """Estados posibles de una orden."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(BaseModel):
    """Schema de Order con enum."""
    id: int
    customer_name: str
    status: OrderStatus  # Solo acepta valores del enum
    total: float


@app.post("/orders")
async def create_order(order: Order):
    """
    Crear orden con status validado por enum.
    
    Status solo acepta: pending, processing, completed, cancelled
    """
    return {
        "message": "Orden creada",
        "order": order.model_dump()
    }


@app.get("/orders/status/{status}")
async def get_orders_by_status(status: OrderStatus):
    """Filtrar órdenes por status (enum validation)."""
    return {
        "status": status,
        "orders": [
            {"id": 1, "customer": "Alice", "status": status},
            {"id": 2, "customer": "Bob", "status": status}
        ]
    }


# =============================================================================
# Ejemplo 7: Status Codes y HTTPException
# =============================================================================

items_db = {
    1: {"name": "Item 1", "price": 10.0},
    2: {"name": "Item 2", "price": 20.0},
    3: {"name": "Item 3", "price": 30.0}
}


@app.get("/items-db/{item_id}", status_code=status.HTTP_200_OK)
async def get_item_from_db(item_id: int):
    """Obtener item con manejo de errores."""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} no encontrado",
            headers={"X-Error": "ItemNotFound"}
        )
    
    return items_db[item_id]


@app.delete("/items-db/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """Eliminar item (204 No Content)."""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    
    del items_db[item_id]
    return None  # 204 no devuelve body


# =============================================================================
# Ejemplo 8: Async/Await
# =============================================================================

async def fetch_data_from_api(url: str):
    """Simular llamada a API externa (async)."""
    await asyncio.sleep(1)  # Simular latencia
    return {"data": f"Data from {url}"}


async def fetch_data_from_db(query: str):
    """Simular consulta a DB (async)."""
    await asyncio.sleep(0.5)
    return {"result": f"DB result for {query}"}


@app.get("/async-example")
async def async_example():
    """
    Ejemplo de operaciones async.
    
    Ejecuta múltiples operaciones I/O concurrentemente.
    """
    # Ejecutar en paralelo (concurrente)
    api_task = fetch_data_from_api("https://api.example.com")
    db_task = fetch_data_from_db("SELECT * FROM users")
    
    api_data = await api_task
    db_data = await db_task
    
    return {
        "api_data": api_data,
        "db_data": db_data,
        "message": "Operaciones completadas concurrentemente"
    }


# Comparación sync vs async
@app.get("/sync-slow")
def sync_slow():
    """Endpoint síncrono (bloqueante)."""
    import time
    time.sleep(2)  # Bloquea el event loop!
    return {"message": "Operación síncrona completada"}


@app.get("/async-fast")
async def async_fast():
    """Endpoint asíncrono (no bloqueante)."""
    await asyncio.sleep(2)  # No bloquea el event loop
    return {"message": "Operación asíncrona completada"}


# =============================================================================
# Ejemplo 9: Headers y Cookies
# =============================================================================

from fastapi import Header, Cookie


@app.get("/headers")
async def read_headers(
    user_agent: Optional[str] = Header(None),
    accept_language: Optional[str] = Header(None),
    x_request_id: Optional[str] = Header(None)
):
    """Leer headers del request."""
    return {
        "user_agent": user_agent,
        "accept_language": accept_language,
        "x_request_id": x_request_id
    }


@app.get("/cookies")
async def read_cookies(
    session_id: Optional[str] = Cookie(None),
    user_id: Optional[str] = Cookie(None)
):
    """Leer cookies del request."""
    return {
        "session_id": session_id,
        "user_id": user_id
    }


from fastapi import Response


@app.post("/set-cookie")
async def set_cookie(response: Response):
    """Establecer cookie en la respuesta."""
    response.set_cookie(
        key="session_id",
        value="abc123",
        max_age=3600,  # 1 hora
        httponly=True,  # No accesible desde JavaScript
        secure=True  # Solo HTTPS en producción
    )
    return {"message": "Cookie establecida"}


# =============================================================================
# Ejemplo 10: Multiple Body Parameters
# =============================================================================

class User(BaseModel):
    """Schema de User."""
    name: str
    email: EmailStr


class Product(BaseModel):
    """Schema de Product."""
    name: str
    price: float


@app.post("/purchase")
async def purchase(
    user: User,
    product: Product,
    quantity: int = Body(..., gt=0),
    notes: Optional[str] = Body(None)
):
    """
    Múltiples body parameters.
    
    Request body:
    {
        "user": {"name": "Alice", "email": "alice@example.com"},
        "product": {"name": "Laptop", "price": 999.99},
        "quantity": 2,
        "notes": "Entrega urgente"
    }
    """
    total = product.price * quantity
    
    return {
        "user": user.model_dump(),
        "product": product.model_dump(),
        "quantity": quantity,
        "total": total,
        "notes": notes
    }


# =============================================================================
# Ejemplo 11: Form Data
# =============================================================================

from fastapi import Form


@app.post("/login-form")
async def login_form(
    username: str = Form(...),
    password: str = Form(...)
):
    """
    Recibir datos de formulario (application/x-www-form-urlencoded).
    
    Útil para forms HTML tradicionales.
    """
    # En producción: validar credenciales
    return {
        "username": username,
        "message": "Login successful"
    }


# =============================================================================
# Ejemplo 12: File Upload
# =============================================================================

from fastapi import File, UploadFile


@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload de archivo.
    
    UploadFile es más eficiente que bytes para archivos grandes.
    """
    contents = await file.read()
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }


@app.post("/upload-multiple")
async def upload_multiple(files: List[UploadFile] = File(...)):
    """Upload de múltiples archivos."""
    return {
        "files": [
            {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(await file.read())
            }
            for file in files
        ]
    }


# =============================================================================
# Ejemplo 13: Custom Response
# =============================================================================

from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse


@app.get("/custom-json")
async def custom_json():
    """Respuesta JSON personalizada."""
    return JSONResponse(
        content={"message": "Custom JSON response"},
        status_code=200,
        headers={"X-Custom-Header": "Value"}
    )


@app.get("/html", response_class=HTMLResponse)
async def html_response():
    """Respuesta HTML."""
    html_content = """
    <html>
        <head><title>FastAPI HTML</title></head>
        <body>
            <h1>¡Hola desde FastAPI!</h1>
            <p>Esta es una respuesta HTML.</p>
        </body>
    </html>
    """
    return html_content


@app.get("/text", response_class=PlainTextResponse)
async def text_response():
    """Respuesta de texto plano."""
    return "Esta es una respuesta de texto plano"


# =============================================================================
# Ejemplo 14: Documentation Tags
# =============================================================================

@app.get("/tagged-endpoint", tags=["examples"])
async def tagged_endpoint():
    """Endpoint con tag para organizar en documentación."""
    return {"message": "Endpoint con tag"}


@app.post("/another-tagged", tags=["examples", "testing"])
async def another_tagged():
    """Endpoint con múltiples tags."""
    return {"message": "Múltiples tags"}


# =============================================================================
# Ejemplo 15: Metadata y Deprecation
# =============================================================================

@app.get(
    "/metadata",
    summary="Endpoint con metadata",
    description="Este endpoint tiene metadata completa para documentación",
    response_description="Respuesta exitosa con metadata"
)
async def metadata_endpoint():
    """Endpoint con metadata completa."""
    return {"message": "Metadata example"}


@app.get("/deprecated", deprecated=True)
async def deprecated_endpoint():
    """
    Endpoint marcado como deprecado.
    
    Aparece tachado en la documentación.
    """
    return {"message": "Este endpoint será removido pronto"}


# =============================================================================
# Instrucciones de Ejecución
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("FASTAPI BÁSICO - MÓDULO 9.1")
    print("=" * 70)
    print("\nPara ejecutar esta API:")
    print("  1. Instalar dependencias:")
    print("     pip install fastapi[all]")
    print("\n  2. Iniciar servidor:")
    print("     uvicorn 01_fastapi_basico:app --reload")
    print("\n  3. Ver documentación interactiva:")
    print("     Swagger UI: http://localhost:8000/docs")
    print("     ReDoc:      http://localhost:8000/redoc")
    print("\n  4. Endpoints disponibles:")
    print("     GET  /                   - Root endpoint")
    print("     GET  /health             - Health check")
    print("     GET  /items/{item_id}    - Path parameters")
    print("     GET  /search             - Query parameters")
    print("     POST /items              - Request body")
    print("     POST /users              - Response model")
    print("     GET  /async-example      - Async operations")
    print("     ... y más!")
    print("\n" + "=" * 70)
    print("💡 Consejo: Explora /docs para probar todos los endpoints")
    print("=" * 70 + "\n")
