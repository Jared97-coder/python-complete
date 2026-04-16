# 📝 EJERCICIOS PRÁCTICOS - Módulo 9: APIs con FastAPI

## 🎯 Objetivo

Practicar conceptos avanzados de FastAPI mediante ejercicios progresivos que cubren:
- Diseño de APIs RESTful
- Autenticación y autorización
- Validación compleja
- Testing
- Integración con servicios externos
- Deployment

---

## 📊 Nivel de Dificultad

- 🟢 **Básico**: Conceptos fundamentales de FastAPI
- 🟡 **Intermedio**: Autenticación, validación, testing
- 🔴 **Avanzado**: WebSockets, GraphQL, microservicios

---

## 🟢 Ejercicio 1: API de Libros (Básico)

### Descripción
Crear una API REST para gestionar una biblioteca de libros con CRUD completo.

### Requisitos

**Endpoints:**
- `GET /books` - Listar todos los libros (paginación: skip, limit)
- `GET /books/{id}` - Obtener libro por ID
- `POST /books` - Crear libro nuevo
- `PUT /books/{id}` - Actualizar libro
- `DELETE /books/{id}` - Eliminar libro
- `GET /books/search?q={query}` - Buscar libros por título o autor

**Modelo:**
```python
class Book:
    id: int
    title: str (min_length=1, max_length=200)
    author: str (min_length=1, max_length=100)
    isbn: str (pattern=r'^\d{3}-\d{10}$')  # Formato: XXX-XXXXXXXXXX
    published_year: int (ge=1000, le=2024)
    pages: int (gt=0)
    price: float (gt=0)
    genre: Literal["Fiction", "Non-Fiction", "Science", "History", "Biography"]
    in_stock: bool = True
```

**Validaciones:**
- ISBN único
- Año no futuro
- Precio positivo

### Criterios de Éxito
- [ ] CRUD completo funcionando
- [ ] Validación con Pydantic
- [ ] Paginación implementada
- [ ] Búsqueda funcional
- [ ] Manejo de errores 404, 422
- [ ] Tests con pytest (coverage > 70%)

---

## 🟡 Ejercicio 2: API de Blog con Comentarios (Intermedio)

### Descripción
Sistema de blog multi-usuario con posts, comentarios y relaciones Many-to-Many (tags).

### Requisitos

**Modelos:**
```python
# User (del módulo anterior)
class User:
    id, username, email, hashed_password, is_active

# Post
class Post:
    id: int
    title: str
    content: str
    author_id: int  # FK a User
    published: bool = False
    created_at: datetime
    tags: List[Tag]  # Many-to-Many

# Comment
class Comment:
    id: int
    content: str
    post_id: int  # FK a Post
    author_id: int  # FK a User
    created_at: datetime

# Tag
class Tag:
    id: int
    name: str (unique)
```

**Endpoints:**

*Posts:*
- `POST /posts` - Crear post (auth required)
- `GET /posts` - Listar posts (filtrar por published, author, tag)
- `GET /posts/{id}` - Ver post con comentarios
- `PUT /posts/{id}` - Actualizar post (solo autor)
- `DELETE /posts/{id}` - Eliminar post (solo autor)
- `PATCH /posts/{id}/publish` - Publicar post (solo autor)

*Comentarios:*
- `POST /posts/{id}/comments` - Agregar comentario (auth required)
- `GET /posts/{id}/comments` - Listar comentarios del post
- `DELETE /comments/{id}` - Eliminar comentario (autor o admin)

*Tags:*
- `GET /tags` - Listar todos los tags
- `GET /tags/{name}/posts` - Posts por tag

### Criterios de Éxito
- [ ] Autenticación JWT
- [ ] Autorización (autor vs admin)
- [ ] Relaciones Many-to-Many (post_tags)
- [ ] Filtrado y búsqueda avanzada
- [ ] Tests de integración
- [ ] Documentación OpenAPI clara

---

## 🟡 Ejercicio 3: E-commerce API (Intermedio)

### Descripción
API de tienda online con productos, carrito de compras y checkout.

### Requisitos

**Modelos:**
```python
# Product
class Product:
    id, name, description, price, stock, category, image_url

# Cart
class Cart:
    id: int
    user_id: int
    items: List[CartItem]
    total: float

# CartItem
class CartItem:
    product_id: int
    quantity: int
    price: float  # Precio al agregar (snapshot)

# Order (del laboratorio)
class Order:
    id, user_id, items, total, status, created_at
```

**Endpoints:**

*Productos:*
- `GET /products` - Listar con filtros (category, min_price, max_price)
- `GET /products/{id}` - Detalle de producto
- `POST /products` - Crear producto (admin only)

*Carrito:*
- `GET /cart` - Ver carrito actual (auth)
- `POST /cart/items` - Agregar producto (auth)
- `PUT /cart/items/{product_id}` - Actualizar cantidad (auth)
- `DELETE /cart/items/{product_id}` - Remover del carrito (auth)
- `DELETE /cart` - Vaciar carrito (auth)

*Checkout:*
- `POST /checkout` - Convertir carrito en orden (auth)
- `GET /orders` - Ver mis órdenes (auth)

### Validaciones Especiales
- Stock disponible al agregar al carrito
- Stock se reserva al hacer checkout
- Precio snapshot (guardar precio al agregar, no calcular dinámicamente)

### Criterios de Éxito
- [ ] Manejo de stock transaccional
- [ ] Carrito persistente (DB, no memoria)
- [ ] Checkout atómico (todo o nada)
- [ ] Tests de race conditions (stock)
- [ ] Background task para enviar email de confirmación

---

## 🔴 Ejercicio 4: WebSockets - Chat en Tiempo Real (Avanzado)

### Descripción
Sistema de chat en tiempo real usando WebSockets de FastAPI.

### Requisitos

**Endpoints:**
```python
# REST
POST /auth/login  # Obtener token
GET /rooms  # Listar salas de chat

# WebSocket
WS /ws/{room_id}?token={jwt_token}  # Conectar a sala
```

**Funcionalidades:**
- Autenticación por JWT en WebSocket
- Múltiples salas de chat
- Broadcast de mensajes a todos en la sala
- Notificación de usuario conectado/desconectado
- Historial de mensajes recientes

**Ejemplo de mensajes:**
```json
// Cliente envía
{"type": "message", "content": "Hola!"}

// Servidor broadcast
{
  "type": "message",
  "username": "user123",
  "content": "Hola!",
  "timestamp": "2024-01-15T10:30:00Z"
}

// Sistema notifica
{"type": "user_joined", "username": "newuser"}
```

### Criterios de Éxito
- [ ] WebSocket con autenticación JWT
- [ ] Múltiples conexiones concurrentes
- [ ] Broadcast eficiente
- [ ] Manejo de desconexiones
- [ ] Tests con WebSocketTestSession

---

## 🔴 Ejercicio 5: GraphQL con Strawberry (Avanzado)

### Descripción
Implementar GraphQL sobre FastAPI usando Strawberry para consultas flexibles.

### Requisitos

**Instalar:**
```bash
pip install strawberry-graphql[fastapi]
```

**Schema:**
```graphql
type User {
  id: ID!
  username: String!
  email: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  comments: [Comment!]!
}

type Query {
  users: [User!]!
  user(id: ID!): User
  posts(limit: Int = 10): [Post!]!
  post(id: ID!): Post
}

type Mutation {
  createPost(title: String!, content: String!): Post!
  deletePost(id: ID!): Boolean!
}
```

**Endpoint:**
- `/graphql` - GraphQL endpoint con GraphiQL

### Criterios de Éxito
- [ ] Queries anidadas funcionando
- [ ] Resolvers eficientes (N+1 query problem)
- [ ] Mutations con autenticación
- [ ] DataLoader para optimización
- [ ] Tests de GraphQL queries

---

## 🟡 Ejercicio 6: Rate Limiting y Seguridad (Intermedio)

### Descripción
Implementar límites de tasa, CORS y headers de seguridad.

### Requisitos

**Instalar:**
```bash
pip install slowapi
```

**Implementar:**

1. **Rate Limiting:**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/data")
@limiter.limit("5/minute")  # 5 requests por minuto
async def get_data(request: Request):
    return {"data": "..."}
```

2. **CORS:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. **Security Headers:**
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"]
)
```

### Criterios de Éxito
- [ ] Rate limiting funcionando (429 Too Many Requests)
- [ ] CORS configurado correctamente
- [ ] Helmet-like security headers
- [ ] Logger de requests
- [ ] Tests de rate limiting

---

## 🟢 Ejercicio 7: File Upload y Storage (Básico)

### Descripción
API para subir archivos con validación y almacenamiento.

### Requisitos

**Endpoints:**
```python
POST /upload  # Subir archivo
GET /files/{filename}  # Descargar archivo
DELETE /files/{filename}  # Eliminar archivo (auth)
GET /files  # Listar archivos del usuario (auth)
```

**Validaciones:**
- Tipos permitidos: `.jpg`, `.png`, `.pdf`, `.txt`
- Tamaño máximo: 5 MB
- Renombrar archivo con UUID para evitar colisiones

**Implementación:**
```python
from fastapi import UploadFile, File
import shutil
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validar extensión
    ext = Path(file.filename).suffix
    if ext not in [".jpg", ".png", ".pdf", ".txt"]:
        raise HTTPException(400, "Invalid file type")
    
    # Validar tamaño (5MB)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(400, "File too large")
    
    # Guardar con UUID
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    return {"filename": unique_filename}
```

### Criterios de Éxito
- [ ] Validación de tipo y tamaño
- [ ] Almacenamiento seguro (sanitizar nombres)
- [ ] Servir archivos con FileResponse
- [ ] Tests de upload/download

---

## 🔴 Ejercicio 8: Microservicios con API Gateway (Avanzado)

### Descripción
Dividir aplicación en microservicios independientes con un API Gateway.

### Arquitectura

```
API Gateway (FastAPI)
    ├── Auth Service (localhost:8001)
    ├── Products Service (localhost:8002)
    └── Orders Service (localhost:8003)
```

### Requisitos

**1. Auth Service (puerto 8001):**
```python
# auth_service/main.py
app = FastAPI()

@app.post("/login")
def login(...): ...

@app.post("/register")
def register(...): ...
```

**2. Products Service (puerto 8002):**
```python
# products_service/main.py
app = FastAPI()

@app.get("/products")
def list_products(): ...
```

**3. Orders Service (puerto 8003):**
```python
# orders_service/main.py
app = FastAPI()

@app.post("/orders")
def create_order(): ...
```

**4. API Gateway (puerto 8000):**
```python
# gateway/main.py
import httpx

app = FastAPI()

@app.post("/api/auth/login")
async def gateway_login(credentials: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/login",
            json=credentials
        )
        return response.json()

@app.get("/api/products")
async def gateway_products():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8002/products")
        return response.json()
```

### Criterios de Éxito
- [ ] 3+ microservicios independientes
- [ ] API Gateway rutando correctamente
- [ ] Headers JWT propagados entre servicios
- [ ] Circuit breaker (retry, fallback)
- [ ] Tests end-to-end

---

## 🟡 Ejercicio 9: API Versioning (Intermedio)

### Descripción
Implementar versionado de API para mantener compatibilidad con clientes antiguos.

### Estrategias

**1. Path Versioning (Recomendado):**
```python
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

@v1_router.get("/users")
def get_users_v1():
    return {"version": "1.0", "users": [...]}

@v2_router.get("/users")
def get_users_v2():
    return {
        "version": "2.0",
        "users": [...],
        "metadata": {"total": 10}  # Nueva info
    }

app.include_router(v1_router)
app.include_router(v2_router)
```

**2. Header Versioning:**
```python
from fastapi import Header

@app.get("/users")
def get_users(api_version: str = Header(default="1.0", alias="X-API-Version")):
    if api_version == "2.0":
        return {"version": "2.0", ...}
    return {"version": "1.0", ...}
```

### Cambios entre Versiones
- **v1**: Devolver lista simple
- **v2**: Agregar paginación y metadata
- **v2**: Cambiar formato de fechas (ISO 8601)

### Criterios de Éxito
- [ ] v1 y v2 coexisten
- [ ] Deprecation warnings en v1
- [ ] Tests separados por versión
- [ ] Documentación OpenAPI por versión

---

## 🔴 Ejercicio 10: Full Deployment (Avanzado)

### Descripción
Desplegar aplicación FastAPI en producción con Docker y CI/CD.

### Requisitos

**1. Dockerizar:**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**2. Docker Compose:**
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
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**3. CI/CD con GitHub Actions:**
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov
```

**4. Deploy en Railway/Render:**
- Conectar repositorio
- Configurar variables de entorno
- Deploy automático

### Criterios de Éxito
- [ ] Dockerfile multi-stage optimizado
- [ ] Docker Compose funcionando localmente
- [ ] CI/CD con tests automáticos
- [ ] Deploy en producción
- [ ] Health check endpoint (`/health`)
- [ ] Logs estructurados

---

## 🎁 Ejercicios Bonus

### Bonus 1: Caching con Redis
Implementar cache para endpoints frecuentes usando Redis.

```python
import aioredis
from fastapi import Depends

redis = aioredis.from_url("redis://localhost")

async def get_cached_or_fetch(key: str, fetch_func):
    # Buscar en cache
    cached = await redis.get(key)
    if cached:
        return json.loads(cached)
    
    # Fetch y guardar en cache
    data = await fetch_func()
    await redis.setex(key, 300, json.dumps(data))  # 5 min TTL
    return data
```

### Bonus 2: Background Jobs con Celery
Procesar tareas pesadas en background con Celery.

```python
from celery import Celery

celery_app = Celery('tasks', broker='redis://localhost:6379')

@celery_app.task
def send_confirmation_email(email: str, order_id: int):
    # Enviar email...
    pass

@app.post("/orders")
def create_order(...):
    # Crear orden
    order = ...
    
    # Enviar email en background
    send_confirmation_email.delay(user.email, order.id)
    
    return order
```

### Bonus 3: Logging Estructurado
Implementar logging JSON para observabilidad.

```python
import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        })

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logging.basicConfig(handlers=[handler], level=logging.INFO)
```

---

## 📚 Recursos Adicionales

### Documentación Oficial
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)

### Tutoriales
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [Real World FastAPI](https://github.com/gothinkster/realworld)

### Testing
- [pytest Documentation](https://docs.pytest.org/)
- [TestClient Examples](https://fastapi.tiangolo.com/tutorial/testing/)

### Deployment
- [FastAPI in Containers](https://fastapi.tiangolo.com/deployment/docker/)
- [Railway Deployment](https://railway.app/)
- [Render Deployment](https://render.com/)

---

## 💡 Tips Generales

1. **Estructura clara**: Separa lógica en routers, schemas, models, utils
2. **Tests desde el inicio**: TDD ayuda a diseñar mejor API
3. **Documentación automática**: Usa docstrings para mejorar /docs
4. **Validación robusta**: Pydantic es tu amigo, úsalo intensivamente
5. **Manejo de errores**: HTTPException con mensajes claros
6. **Logging**: Log requests, errores y eventos importantes
7. **Performance**: Usa async/await, caching, connection pooling
8. **Seguridad**: JWT, rate limiting, CORS, input validation

---

**¡Feliz coding!** 🚀
