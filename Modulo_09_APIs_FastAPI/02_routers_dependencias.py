"""
Módulo 9.2 - Routers y Dependencias

Organizar aplicaciones con APIRouter, Dependency Injection,
shared dependencies, background tasks y lifecycle events.

Para ejecutar:
    uvicorn 02_routers_dependencias:app --reload
"""

from fastapi import FastAPI, APIRouter, Depends, HTTPException, BackgroundTasks, status
from pydantic import BaseModel
from typing import Optional, List, Annotated
from datetime import datetime
import time

# =============================================================================
# Ejemplo 1: APIRouter para Modularizar
# =============================================================================

# Router para usuarios
users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "User not found"}}
)

# Router para productos
products_router = APIRouter(
    prefix="/products",
    tags=["products"]
)


# Schemas
class User(BaseModel):
    id: int
    name: str
    email: str


class Product(BaseModel):
    id: int
    name: str
    price: float


# Base de datos simulada
users_db = [
    User(id=1, name="Alice", email="alice@example.com"),
    User(id=2, name="Bob", email="bob@example.com")
]

products_db = [
    Product(id=1, name="Laptop", price=999.99),
    Product(id=2, name="Mouse", price=29.99)
]


@users_router.get("/", response_model=List[User])
async def list_users():
    """Listar todos los usuarios."""
    return users_db


@users_router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Obtener usuario por ID."""
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@products_router.get("/", response_model=List[Product])
async def list_products():
    """Listar todos los productos."""
    return products_db


@products_router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """Obtener producto por ID."""
    for product in products_db:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


print("=== Ejemplo 1: APIRouter ===")
print("Routers creados: /users, /products")


# =============================================================================
# Ejemplo 2: Dependency Injection - Básico
# =============================================================================

async def common_parameters(
    skip: int = 0,
    limit: int = 10,
    sort: str = "asc"
):
    """Dependencia: parámetros comunes de paginación."""
    return {"skip": skip, "limit": limit, "sort": sort}


@users_router.get("/paginated")
async def paginated_users(commons: dict = Depends(common_parameters)):
    """Endpoint que usa dependencia."""
    return {
        "users": users_db[commons["skip"]:commons["skip"] + commons["limit"]],
        "pagination": commons
    }


print("=== Ejemplo 2: Dependency Injection ===")
print("Dependencia common_parameters creada")


# =============================================================================
# Ejemplo 3: Dependencias con Clases
# =============================================================================

class PaginationParams:
    """Dependencia de paginación usando clase."""
    
    def __init__(
        self,
        skip: int = 0,
        limit: int = 10,
        max_limit: int = 100
    ):
        self.skip = skip
        self.limit = min(limit, max_limit)  # Limitar máximo


@products_router.get("/paginated")
async def paginated_products(pagination: PaginationParams = Depends()):
    """Usar dependencia de clase."""
    return {
        "products": products_db[pagination.skip:pagination.skip + pagination.limit],
        "skip": pagination.skip,
        "limit": pagination.limit
    }


print("=== Ejemplo 3: Dependencias con Clases ===")
print("PaginationParams creada")


# =============================================================================
# Ejemplo 4: Dependencias Anidadas (Sub-dependencies)
# =============================================================================

async def get_database_connection():
    """Dependencia nivel 1: Conexión a DB."""
    print("  → Abriendo conexión a DB...")
    return {"connection": "db_connection_object"}


async def get_current_user(db: dict = Depends(get_database_connection)):
    """Dependencia nivel 2: Usuario actual (depende de DB)."""
    print("  → Obteniendo usuario actual...")
    # Simular obtener usuario de DB
    return {"user_id": 1, "username": "alice"}


async def verify_permissions(current_user: dict = Depends(get_current_user)):
    """Dependencia nivel 3: Verificar permisos (depende de usuario)."""
    print("  → Verificando permisos...")
    if current_user["user_id"] != 1:
        raise HTTPException(status_code=403, detail="Forbidden")
    return True


admin_router = APIRouter(prefix="/admin", tags=["admin"])


@admin_router.get("/dashboard")
async def admin_dashboard(
    has_permission: bool = Depends(verify_permissions),
    current_user: dict = Depends(get_current_user)
):
    """
    Endpoint con dependencias anidadas.
    
    Cadena de dependencias:
    verify_permissions → get_current_user → get_database_connection
    """
    return {
        "message": "Admin dashboard",
        "user": current_user,
        "has_permission": has_permission
    }


print("=== Ejemplo 4: Dependencias Anidadas ===")
print("Cadena de dependencias: permisos → usuario → DB")


# =============================================================================
# Ejemplo 5: Dependencias a Nivel de Router
# =============================================================================

async def log_request():
    """Dependencia que se ejecuta en todos los endpoints del router."""
    print(f"  → Request recibido: {datetime.now()}")


# Router con dependencia global
logged_router = APIRouter(
    prefix="/logged",
    tags=["logged"],
    dependencies=[Depends(log_request)]  # Se aplica a TODOS los endpoints
)


@logged_router.get("/endpoint1")
async def logged_endpoint1():
    """Endpoint 1 (log automático)."""
    return {"message": "Endpoint 1"}


@logged_router.get("/endpoint2")
async def logged_endpoint2():
    """Endpoint 2 (log automático)."""
    return {"message": "Endpoint 2"}


print("=== Ejemplo 5: Router Dependencies ===")
print("Todos los endpoints en /logged ejecutan log_request")


# =============================================================================
# Ejemplo 6: Dependencias con yield (Cleanup)
# =============================================================================

from contextlib import asynccontextmanager


async def get_db_session():
    """
    Dependencia con cleanup (similar a context manager).
    
    yield separa setup (antes) de teardown (después).
    """
    print("  → Setup: Abriendo sesión DB")
    db_session = {"session": "active"}
    
    try:
        yield db_session  # Proveer recurso
    finally:
        print("  → Teardown: Cerrando sesión DB")
        # Cerrar conexión, rollback si hubo error, etc.


@users_router.get("/with-cleanup/{user_id}")
async def get_user_with_cleanup(
    user_id: int,
    db: dict = Depends(get_db_session)
):
    """
    Endpoint con dependencia que hace cleanup.
    
    La sesión DB se cierra automáticamente después del request.
    """
    return {"user_id": user_id, "db_status": db["session"]}


print("=== Ejemplo 6: Dependencies con yield ===")
print("get_db_session hace setup y cleanup automático")


# =============================================================================
# Ejemplo 7: Annotated Dependencies (Python 3.10+)
# =============================================================================

# Definir dependencia reutilizable con Annotated
DatabaseDep = Annotated[dict, Depends(get_db_session)]
UserDep = Annotated[dict, Depends(get_current_user)]


@users_router.get("/annotated/{user_id}")
async def annotated_endpoint(
    user_id: int,
    db: DatabaseDep,
    current_user: UserDep
):
    """
    Usar Annotated para dependencias más claras.
    
    Ventaja: Type hints + dependency en una línea.
    """
    return {
        "user_id": user_id,
        "db": db,
        "current_user": current_user
    }


print("=== Ejemplo 7: Annotated Dependencies ===")
print("DatabaseDep y UserDep definidos con Annotated")


# =============================================================================
# Ejemplo 8: Background Tasks
# =============================================================================

def send_email(email: str, message: str):
    """Tarea de background: enviar email."""
    print(f"  → Enviando email a {email}...")
    time.sleep(2)  # Simular operación lenta
    print(f"  ✓ Email enviado a {email}: {message}")


def log_action(action: str, user_id: int):
    """Tarea de background: log de acción."""
    print(f"  → Logging acción: {action} por usuario {user_id}")


tasks_router = APIRouter(prefix="/tasks", tags=["background-tasks"])


@tasks_router.post("/send-notification")
async def send_notification(
    email: str,
    message: str,
    background_tasks: BackgroundTasks
):
    """
    Endpoint con background task.
    
    Devuelve respuesta inmediata y procesa en background.
    """
    # Agregar tarea de background
    background_tasks.add_task(send_email, email, message)
    
    # Devolver respuesta inmediatamente
    return {
        "message": "Notification queued",
        "email": email
    }


@tasks_router.post("/create-user")
async def create_user_with_tasks(
    name: str,
    email: str,
    background_tasks: BackgroundTasks
):
    """Múltiples background tasks."""
    # Simular creación de usuario
    user_id = len(users_db) + 1
    
    # Agregar múltiples tareas
    background_tasks.add_task(send_email, email, f"Welcome {name}!")
    background_tasks.add_task(log_action, "user_created", user_id)
    
    return {
        "message": "User created",
        "user_id": user_id,
        "background_tasks": 2
    }


print("=== Ejemplo 8: Background Tasks ===")
print("Tareas en background: send_email, log_action")


# =============================================================================
# Ejemplo 9: Lifespan Events (Startup/Shutdown)
# =============================================================================

from contextlib import asynccontextmanager


# Estado global de la aplicación
app_state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager (FastAPI 0.93+).
    
    Reemplaza @app.on_event("startup") y @app.on_event("shutdown").
    """
    # Startup
    print("\n🚀 Iniciando aplicación...")
    app_state["start_time"] = datetime.now()
    app_state["requests_count"] = 0
    print("  ✓ Estado inicializado")
    
    # Simular conexión a DB
    app_state["db"] = "Database connection established"
    print("  ✓ Conexión a DB establecida")
    
    yield  # Aplicación corriendo
    
    # Shutdown
    print("\n🛑 Cerrando aplicación...")
    uptime = datetime.now() - app_state["start_time"]
    print(f"  → Uptime: {uptime}")
    print(f"  → Total requests: {app_state['requests_count']}")
    print("  ✓ Recursos liberados")


# =============================================================================
# Aplicación Principal
# =============================================================================

app = FastAPI(
    title="Routers y Dependencias",
    version="1.0.0",
    lifespan=lifespan  # Lifespan context manager
)


# Incluir todos los routers
app.include_router(users_router)
app.include_router(products_router)
app.include_router(admin_router)
app.include_router(logged_router)
app.include_router(tasks_router)


@app.get("/")
async def root():
    """Root endpoint con estado de la app."""
    return {
        "message": "API con Routers y Dependencias",
        "uptime": str(datetime.now() - app_state.get("start_time", datetime.now())),
        "requests": app_state.get("requests_count", 0)
    }


# Middleware para contar requests
@app.middleware("http")
async def count_requests(request, call_next):
    """Middleware: contar requests."""
    app_state["requests_count"] = app_state.get("requests_count", 0) + 1
    response = await call_next(request)
    return response


# =============================================================================
# Ejemplo 10: Dependencias Opcionales
# =============================================================================

async def get_optional_user(user_id: Optional[int] = None):
    """Dependencia opcional."""
    if user_id:
        return {"user_id": user_id, "name": f"User {user_id}"}
    return None


@app.get("/optional-dep")
async def optional_dependency(user: Optional[dict] = Depends(get_optional_user)):
    """Endpoint con dependencia opcional."""
    if user:
        return {"message": "User provided", "user": user}
    return {"message": "No user provided"}


# =============================================================================
# Ejemplo 11: Dependency Overrides (útil para testing)
# =============================================================================

async def get_real_db():
    """Dependencia real de DB (producción)."""
    return {"type": "real_db", "connection": "postgresql://..."}


async def get_fake_db():
    """Dependencia fake de DB (testing)."""
    return {"type": "fake_db", "connection": "sqlite:///:memory:"}


@app.get("/database-info")
async def database_info(db: dict = Depends(get_real_db)):
    """Endpoint que usa DB (puede ser overridden en tests)."""
    return {"database": db}


# En tests se puede hacer:
# app.dependency_overrides[get_real_db] = get_fake_db


# =============================================================================
# Ejemplo 12: Router con Prefix y Tags
# =============================================================================

api_v1_router = APIRouter(prefix="/api/v1")

# Sub-routers dentro de v1
api_v1_users = APIRouter(prefix="/users", tags=["v1-users"])
api_v1_products = APIRouter(prefix="/products", tags=["v1-products"])


@api_v1_users.get("/")
async def list_v1_users():
    """GET /api/v1/users"""
    return users_db


@api_v1_products.get("/")
async def list_v1_products():
    """GET /api/v1/products"""
    return products_db


# Incluir sub-routers en v1
api_v1_router.include_router(api_v1_users)
api_v1_router.include_router(api_v1_products)

# Incluir v1 en app
app.include_router(api_v1_router)


print("\n=== Routers Incluidos ===")
print("  → /users")
print("  → /products")
print("  → /admin")
print("  → /logged")
print("  → /tasks")
print("  → /api/v1/users")
print("  → /api/v1/products")


# =============================================================================
# Ejemplo 13: Dependencias con Settings/Config
# =============================================================================

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación."""
    app_name: str = "FastAPI App"
    admin_email: str = "admin@example.com"
    items_per_page: int = 10
    
    class Config:
        env_file = ".env"


# Dependencia: obtener settings
def get_settings():
    """Singleton de settings."""
    return Settings()


@app.get("/settings")
async def read_settings(settings: Settings = Depends(get_settings)):
    """Endpoint que usa settings."""
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_page": settings.items_per_page
    }


# =============================================================================
# Instrucciones de Ejecución
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("ROUTERS Y DEPENDENCIAS - MÓDULO 9.2")
    print("=" * 70)
    print("\nPara ejecutar:")
    print("  uvicorn 02_routers_dependencias:app --reload")
    print("\nDocumentación:")
    print("  http://localhost:8000/docs")
    print("\nEndpoints principales:")
    print("  GET  /users              - Listar usuarios")
    print("  GET  /products           - Listar productos")
    print("  GET  /admin/dashboard    - Admin con permisos")
    print("  POST /tasks/send-notification - Background task")
    print("  GET  /api/v1/users       - Versionado")
    print("\n" + "=" * 70)
    print("💡 Observa los logs para ver el flujo de dependencias")
    print("=" * 70 + "\n")
