# 📘 Módulo 9 - APIs Web con FastAPI

## 🎯 Objetivos del Módulo

Al finalizar este módulo, serás capaz de:

✅ Crear APIs REST modernas con FastAPI  
✅ Estructurar proyectos con routers, dependencias y capas  
✅ Validar datos con Pydantic y generar documentación OpenAPI automática  
✅ Implementar autenticación JWT y gestionar permisos  
✅ Configurar middlewares y CORS  
✅ Probar endpoints con pytest y httpx  
✅ Integrar APIs con bases de datos usando SQLAlchemy  
✅ Desplegar APIs en producción con Uvicorn/Gunicorn  

---

## 📚 Contenido del Módulo

### 1. **FastAPI Básico** (`01_fastapi_basico.py`)
- ¿Qué es FastAPI? Ventajas vs Flask/Django
- Primera aplicación: Hello World API
- Path parameters, query parameters, request body
- Response models y status codes
- Documentación automática (Swagger UI, ReDoc)
- Async/await en endpoints

### 2. **Routers y Dependencias** (`02_routers_dependencias.py`)
- APIRouter para modularizar endpoints
- Dependency Injection system
- Compartir sesiones de base de datos
- Dependencias anidadas y reutilizables
- Background tasks
- Lifespans y eventos de startup/shutdown

### 3. **Pydantic y Validación** (`03_pydantic_validacion.py`)
- Schemas con Pydantic BaseModel
- Tipos de datos y validaciones
- Field validators y model validators
- Response models y serialización
- Config settings con pydantic-settings
- Manejo de errores y excepciones personalizadas

### 4. **Autenticación JWT** (`04_autenticacion_jwt.py`)
- Conceptos de JWT (JSON Web Tokens)
- Implementar login y registro
- Hash de passwords con passlib
- OAuth2 con Password Bearer
- Proteger endpoints con dependencias
- Refresh tokens y expiración
- Roles y permisos

### 5. **Testing de Endpoints** (`05_testing_endpoints.py`)
- TestClient de FastAPI
- Fixtures de pytest para API
- Testing con base de datos temporal
- Mocking de dependencias
- Testing de autenticación
- Coverage y best practices

### 6. **Laboratorio** (`LABORATORIO.md`)
- Sistema completo de gestión de pedidos
- CRUD de Orders con validación Pydantic
- Sistema de autenticación JWT
- Tests de integración con SQLite en memoria
- Documentación OpenAPI completa

### 7. **Ejercicios Adicionales** (`EJERCICIOS.md`)
- 10 ejercicios prácticos progresivos
- Desde APIs básicas hasta sistemas complejos
- Integración con servicios externos
- WebSockets y eventos en tiempo real
- Rate limiting y caching

---

## 🚀 ¿Por Qué FastAPI?

### Comparación con Otros Frameworks

| Característica | FastAPI | Flask | Django REST |
|----------------|---------|-------|-------------|
| **Performance** | ⭐⭐⭐⭐⭐ (Starlette) | ⭐⭐⭐ | ⭐⭐⭐ |
| **Async nativo** | ✅ | ❌ (extensión) | ❌ (extensión) |
| **Validación automática** | ✅ Pydantic | ❌ Manual | ✅ Serializers |
| **Documentación OpenAPI** | ✅ Automática | ❌ Manual | ❌ drf-yasg |
| **Type hints** | ✅ Completo | ❌ | ⚠️ Parcial |
| **Aprendizaje** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Ecosistema** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### Ventajas Clave

✅ **Rápido de desarrollar**: Type hints + Pydantic = menos código  
✅ **Alto rendimiento**: Comparable a NodeJS y Go  
✅ **Validación automática**: Errores claros sin código extra  
✅ **Documentación interactiva**: Swagger UI out-of-the-box  
✅ **Estándares modernos**: OpenAPI 3.0, JSON Schema  
✅ **Async/await nativo**: Perfecto para I/O-bound tasks  

---

## 📦 Instalación y Configuración

### Dependencias Principales

```bash
pip install fastapi[all]
```

El paquete `[all]` incluye:
- `fastapi` - Framework core
- `uvicorn[standard]` - ASGI server para producción
- `pydantic[email]` - Validación de datos
- `python-multipart` - Para formularios y archivos

### Dependencias Adicionales

```bash
# Base de datos
pip install sqlalchemy alembic psycopg2-binary

# Autenticación
pip install python-jose[cryptography] passlib[bcrypt]

# Testing
pip install pytest pytest-asyncio httpx

# Variables de entorno
pip install python-dotenv

# CORS
pip install fastapi-cors  # Ya incluido en fastapi
```

### Estructura de Proyecto Recomendada

```
fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación principal
│   ├── config.py            # Configuración (settings)
│   ├── database.py          # Conexión DB
│   ├── dependencies.py      # Dependencias compartidas
│   │
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── order.py
│   │
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── order.py
│   │
│   ├── routers/             # Endpoints organizados
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── orders.py
│   │
│   ├── services/            # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── order_service.py
│   │
│   └── utils/               # Utilidades
│       ├── __init__.py
│       ├── security.py
│       └── exceptions.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures pytest
│   ├── test_auth.py
│   └── test_orders.py
│
├── alembic/                 # Migraciones DB
├── .env                     # Variables de entorno
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🔧 Conceptos Fundamentales

### 1. Request Lifecycle

```
Cliente HTTP Request
    ↓
Middlewares (CORS, Auth, etc.)
    ↓
Path Operation (endpoint function)
    ↓
Dependency Injection
    ↓
Request Validation (Pydantic)
    ↓
Business Logic
    ↓
Response Model Serialization
    ↓
Middlewares (response)
    ↓
Cliente HTTP Response
```

### 2. Dependency Injection

FastAPI usa DI para compartir recursos (DB sessions, auth, config):

```python
from fastapi import Depends
from sqlalchemy.orm import Session

# Dependencia: obtener sesión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Usar en endpoint
@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()
```

### 3. Path Operations

```python
@app.get("/items")           # Listar recursos
@app.post("/items")          # Crear recurso
@app.get("/items/{id}")      # Obtener recurso específico
@app.put("/items/{id}")      # Actualizar completo
@app.patch("/items/{id}")    # Actualizar parcial
@app.delete("/items/{id}")   # Eliminar recurso
```

### 4. Request Components

```python
from fastapi import Path, Query, Body, Header, Cookie

@app.get("/items/{item_id}")
async def read_item(
    # Path parameter (obligatorio)
    item_id: int = Path(..., gt=0, description="Item ID"),
    
    # Query parameter (opcional)
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    
    # Header
    user_agent: str = Header(None),
    
    # Cookie
    session_id: str = Cookie(None)
):
    ...
```

### 5. Response Models

```python
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    id: int
    name: str
    price: float

@app.get("/items", response_model=List[Item])
async def list_items():
    return [
        {"id": 1, "name": "Item 1", "price": 10.0, "secret": "no visible"},
        {"id": 2, "name": "Item 2", "price": 20.0, "secret": "no visible"}
    ]
    # response_model filtra solo campos definidos
```

---

## 🔐 Autenticación y Seguridad

### Flujo de Autenticación JWT

```
1. Usuario envía credentials (username/password)
   POST /auth/login
   
2. Servidor valida y genera JWT
   → Hash password con bcrypt
   → Crear token con python-jose
   → Devolver access_token
   
3. Cliente guarda token
   → LocalStorage o Cookie HttpOnly
   
4. Requests posteriores incluyen token
   Authorization: Bearer <token>
   
5. Servidor valida token en cada request
   → Decodificar JWT
   → Verificar firma y expiración
   → Extraer user_id y permisos
```

### Ejemplo de Protección de Endpoint

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependencia: obtener usuario actual del token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    
    return user

# Usar en endpoint protegido
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

---

## 🧪 Testing con Pytest

### TestClient de FastAPI

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Test Item", "price": 10.0}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert "id" in data
```

### Testing con Base de Datos Temporal

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.dependencies import get_db

# Engine de test (SQLite en memoria)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def db():
    """Fixture: DB temporal."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    """Fixture: TestClient con DB temporal."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_create_user(client):
    response = client.post("/users/", json={"email": "test@example.com", "name": "Test"})
    assert response.status_code == 201
```

---

## 🌐 CORS y Middlewares

### Configurar CORS

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://myapp.com"],  # Orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Authorization, Content-Type, etc.
)
```

### Middleware Personalizado

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Agregar header con tiempo de procesamiento."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

---

## 📖 Documentación Automática

FastAPI genera documentación interactiva automáticamente:

### Swagger UI (OpenAPI)
```
http://localhost:8000/docs
```
- Interfaz interactiva para probar endpoints
- Formularios de autenticación
- Ejemplos de request/response

### ReDoc
```
http://localhost:8000/redoc
```
- Documentación alternativa más limpia
- Mejor para lectura que para testing

### OpenAPI JSON
```
http://localhost:8000/openapi.json
```
- Schema completo en JSON
- Útil para generar clientes (SDKs)

### Personalizar Documentación

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API completa de gestión de pedidos",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Soporte API",
        "url": "http://example.com/contact/",
        "email": "api@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

@app.get("/items", tags=["items"], summary="List all items")
async def list_items():
    """
    Retrieve a list of all items.
    
    - **skip**: Number of items to skip (pagination)
    - **limit**: Maximum number of items to return
    
    Returns a list of item objects.
    """
    ...
```

---

## ⚡ Performance y Optimización

### 1. Async/Await para I/O

```python
import httpx

@app.get("/external")
async def call_external_api():
    """Async para llamadas externas."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```

### 2. Background Tasks

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    """Tarea pesada."""
    # Enviar email...
    pass

@app.post("/send-notification")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    """Devolver respuesta inmediata y procesar en background."""
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Notification sent"}
```

### 3. Caching con Redis

```python
import redis.asyncio as redis
from fastapi import FastAPI

app = FastAPI()
redis_client = None

@app.on_event("startup")
async def startup():
    global redis_client
    redis_client = redis.from_url("redis://localhost")

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    # Check cache
    cached = await redis_client.get(f"item:{item_id}")
    if cached:
        return json.loads(cached)
    
    # Query DB
    item = db.query(Item).filter(Item.id == item_id).first()
    
    # Set cache
    await redis_client.setex(f"item:{item_id}", 3600, json.dumps(item))
    
    return item
```

### 4. Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Engine con pool
engine = create_engine(
    DATABASE_URL,
    pool_size=10,          # Conexiones en pool
    max_overflow=20,       # Conexiones adicionales
    pool_pre_ping=True,    # Verificar conexión antes de usar
    pool_recycle=3600      # Reciclar cada hora
)

SessionLocal = sessionmaker(bind=engine)
```

---

## 🚀 Despliegue

### Desarrollo Local

```bash
# Con Uvicorn (desarrollo)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Producción

```bash
# Con Gunicorn + Uvicorn workers
gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile - \
    --error-logfile -
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - SECRET_KEY=your-secret-key
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 📊 Best Practices

### ✅ DO

1. **Usar async/await** para operaciones I/O
2. **Validar con Pydantic** en todos los endpoints
3. **Separar concerns**: routers, services, repositories
4. **Documentar endpoints** con docstrings
5. **Implementar paginación** en listados
6. **Manejar errores** con HTTPException
7. **Usar variables de entorno** para configuración
8. **Escribir tests** para todos los endpoints
9. **Versionar API** (`/api/v1/...`)
10. **Rate limiting** en producción

### ❌ DON'T

1. **No bloquear event loop** con operaciones síncronas pesadas
2. **No exponer secretos** en código
3. **No devolver errores detallados** en producción
4. **No omitir validación** de entrada
5. **No crear sesiones DB** sin cerrarlas
6. **No hardcodear valores** de configuración
7. **No mezclar lógica de negocio** en endpoints
8. **No olvidar CORS** en frontend-backend
9. **No usar password plano** (siempre hashear)
10. **No desplegar sin HTTPS** en producción

---

## 🔗 Recursos Adicionales

### Documentación Oficial
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Uvicorn Docs](https://www.uvicorn.org/)

### Tutoriales
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Real Python - FastAPI](https://realpython.com/fastapi-python-web-apis/)
- [TestDriven.io - FastAPI](https://testdriven.io/blog/fastapi-crud/)

### Herramientas
- [Postman](https://www.postman.com/) - Testing de APIs
- [Insomnia](https://insomnia.rest/) - Cliente REST
- [httpx](https://www.python-httpx.org/) - Cliente HTTP async

### Extensiones Útiles
- [fastapi-users](https://github.com/fastapi-users/fastapi-users) - Sistema de usuarios completo
- [fastapi-cache](https://github.com/long2ice/fastapi-cache) - Caching integrado
- [fastapi-limiter](https://github.com/long2ice/fastapi-limiter) - Rate limiting
- [fastapi-pagination](https://github.com/uriyyo/fastapi-pagination) - Paginación automática

---

## 📖 Siguientes Pasos

Después de completar este módulo:

1. ✅ **Módulo 10**: WebSockets y eventos en tiempo real
2. ✅ **Módulo 11**: Microservicios y mensajería (Celery, RabbitMQ)
3. ✅ **Módulo 12**: Despliegue en cloud (AWS, Azure, Docker)
4. ✅ **Módulo 13**: GraphQL con Strawberry
5. ✅ **Módulo 14**: Observabilidad (logging, monitoring, tracing)

---

**¡Comencemos a construir APIs modernas con FastAPI!** 🚀
