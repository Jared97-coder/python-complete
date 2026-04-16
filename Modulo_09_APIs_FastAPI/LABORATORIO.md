# 🔬 LABORATORIO - Módulo 9: APIs con FastAPI

## 📋 Objetivo

Construir una **API REST completa** para gestión de pedidos (Orders) con:
- ✅ Autenticación JWT (registro, login)
- ✅ CRUD completo de pedidos con validación
- ✅ Autorización (usuarios solo ven sus pedidos, admin ve todos)
- ✅ Tests de integración con base de datos temporal

---

## 🎯 Especificaciones del Proyecto

### **Sistema de Gestión de Pedidos (Orders API)**

Implementar una API que permita:

1. **Autenticación de usuarios**
   - Registro de nuevos usuarios (POST `/auth/register`)
   - Login con JWT (POST `/auth/login`)
   - Endpoint protegido para obtener perfil (GET `/users/me`)

2. **CRUD de Pedidos (Orders)**
   - Crear pedido (POST `/orders`)
   - Listar pedidos del usuario (GET `/orders`)
   - Obtener pedido específico (GET `/orders/{id}`)
   - Actualizar pedido (PUT `/orders/{id}`)
   - Eliminar pedido (DELETE `/orders/{id}`)
   - Agregar items a pedido (POST `/orders/{id}/items`)

3. **Autorización**
   - Usuarios solo pueden ver/modificar sus propios pedidos
   - Admin puede ver todos los pedidos
   - Verificar propiedad de recursos

4. **Validación con Pydantic**
   - Validar datos de entrada (campos obligatorios, tipos, rangos)
   - Precios > 0
   - Cantidades > 0
   - Email válido
   - Contraseña mínimo 6 caracteres

5. **Tests de Integración**
   - Base de datos SQLite en memoria (`:memory:`)
   - Tests de registro y login
   - Tests de CRUD completo
   - Tests de autorización
   - Tests de validación

---

## 📁 Estructura del Proyecto

```
orders_api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación FastAPI
│   ├── database.py             # Configuración DB
│   ├── dependencies.py         # Dependencias (get_db, get_current_user)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py            # Modelo User (SQLAlchemy)
│   │   └── order.py           # Modelos Order, OrderItem (SQLAlchemy)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py            # Schemas User (Pydantic)
│   │   └── order.py           # Schemas Order (Pydantic)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py            # Endpoints /auth/*
│   │   └── orders.py          # Endpoints /orders/*
│   └── utils/
│       ├── __init__.py
│       └── security.py        # JWT y password hashing
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Fixtures globales
│   ├── test_auth.py           # Tests de autenticación
│   └── test_orders.py         # Tests de orders
├── requirements.txt
└── README.md
```

---

## 🛠️ Paso 1: Configuración Inicial

### 1.1. Instalar Dependencias

```bash
pip install fastapi uvicorn sqlalchemy pydantic python-jose[cryptography] passlib[bcrypt] pytest pytest-asyncio httpx
```

### 1.2. Crear `requirements.txt`

```text
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.25
pydantic>=2.5.0
pydantic[email]
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
pytest>=7.4.3
pytest-asyncio>=0.21.1
httpx>=0.26.0
```

---

## 💾 Paso 2: Modelos de Base de Datos (SQLAlchemy)

### 2.1. `app/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite en memoria para testing, PostgreSQL para producción
SQLALCHEMY_DATABASE_URL = "sqlite:///./orders.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:pass@localhost/orders_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Solo para SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependencia: Obtener sesión de DB."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 2.2. `app/models/user.py`

```python
from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
```

### 2.3. `app/models/order.py`

```python
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="pending")  # pending, completed, cancelled
    total = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relaciones
    user = relationship("User", backref="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    
    # Relaciones
    order = relationship("Order", back_populates="items")
```

---

## 📋 Paso 3: Schemas Pydantic

### 3.1. `app/schemas/user.py`

```python
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_admin: bool
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

### 3.2. `app/schemas/order.py`

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_name: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)


class OrderItemResponse(OrderItemCreate):
    id: int
    
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(..., min_items=1)


class OrderUpdate(BaseModel):
    status: Literal["pending", "completed", "cancelled"]


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    total: float
    created_at: datetime
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True
```

---

## 🔐 Paso 4: Utilidades de Seguridad

### 4.1. `app/utils/security.py`

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Configuración JWT
SECRET_KEY = "tu-clave-secreta-super-segura-cambiar-en-produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hashear contraseña."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Crear token JWT."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """Decodificar token JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

---

## 🔑 Paso 5: Dependencias

### 5.1. `app/dependencies.py`

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
from app.models.user import User
from app.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Obtener usuario actual desde JWT."""
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verificar que el usuario esté activo."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user


# Type hints con Annotated
CurrentUser = Annotated[User, Depends(get_current_active_user)]
```

---

## 🛣️ Paso 6: Routers

### 6.1. `app/routers/auth.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserResponse, Token
from app.utils.security import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Registrar nuevo usuario."""
    
    # Verificar username único
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Verificar email único
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Crear usuario
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login y obtener token JWT."""
    
    # Buscar usuario
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token
    access_token = create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}
```

### 6.2. `app/routers/orders.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.dependencies import CurrentUser
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate, OrderItemCreate

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """Crear nuevo pedido."""
    
    # Calcular total
    total = sum(item.price * item.quantity for item in order_data.items)
    
    # Crear order
    new_order = Order(
        user_id=current_user.id,
        total=total
    )
    
    db.add(new_order)
    db.flush()  # Obtener ID sin commit
    
    # Crear items
    for item_data in order_data.items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_name=item_data.product_name,
            quantity=item_data.quantity,
            price=item_data.price
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(new_order)
    
    return new_order


@router.get("", response_model=List[OrderResponse])
def list_orders(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    """Listar pedidos del usuario."""
    
    if current_user.is_admin:
        # Admin ve todos los pedidos
        orders = db.query(Order).offset(skip).limit(limit).all()
    else:
        # Usuario ve solo sus pedidos
        orders = db.query(Order).filter(
            Order.user_id == current_user.id
        ).offset(skip).limit(limit).all()
    
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """Obtener pedido específico."""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Verificar autorización
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to access this order")
    
    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """Actualizar pedido."""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Verificar autorización
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this order")
    
    # Actualizar
    order.status = order_data.status
    db.commit()
    db.refresh(order)
    
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """Eliminar pedido."""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Verificar autorización
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this order")
    
    db.delete(order)
    db.commit()
    
    return None


@router.post("/{order_id}/items", response_model=OrderResponse)
def add_order_items(
    order_id: int,
    items: List[OrderItemCreate],
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """Agregar items a pedido existente."""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Verificar autorización
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Agregar items
    for item_data in items:
        order_item = OrderItem(
            order_id=order.id,
            product_name=item_data.product_name,
            quantity=item_data.quantity,
            price=item_data.price
        )
        db.add(order_item)
    
    # Recalcular total
    order.total = sum(item.price * item.quantity for item in order.items)
    
    db.commit()
    db.refresh(order)
    
    return order
```

---

## 🚀 Paso 7: Aplicación Principal

### 7.1. `app/main.py`

```python
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import auth, orders
from app.dependencies import CurrentUser


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events: startup y shutdown."""
    # Startup
    print("🚀 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Shutdown
    print("🛑 Shutting down...")


# Crear aplicación
app = FastAPI(
    title="Orders API",
    description="API de gestión de pedidos con autenticación JWT",
    version="1.0.0",
    lifespan=lifespan
)

# Incluir routers
app.include_router(auth.router)
app.include_router(orders.router)


@app.get("/")
def root():
    """Endpoint raíz."""
    return {"message": "Orders API - Use /docs for documentation"}


@app.get("/users/me")
def read_users_me(current_user: CurrentUser):
    """Obtener perfil del usuario actual."""
    return current_user


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

---

## 🧪 Paso 8: Tests de Integración

### 8.1. `tests/conftest.py`

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.utils.security import get_password_hash

# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Fixture: Sesión de DB para tests."""
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Fixture: TestClient con DB de prueba."""
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Fixture: Usuario de prueba."""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpass123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return user


@pytest.fixture
def admin_user(db_session):
    """Fixture: Usuario admin."""
    admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("adminpass123"),
        is_admin=True
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    
    return admin


@pytest.fixture
def auth_headers(client, test_user):
    """Fixture: Headers de autenticación."""
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}
```

### 8.2. `tests/test_auth.py`

```python
from fastapi import status


def test_register_user(client):
    """Test: Registrar usuario."""
    response = client.post("/auth/register", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123"
    })
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "id" in data


def test_register_duplicate_username(client, test_user):
    """Test: Registrar username duplicado."""
    response = client.post("/auth/register", json={
        "username": "testuser",  # Ya existe
        "email": "other@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_success(client, test_user):
    """Test: Login exitoso."""
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, test_user):
    """Test: Login con credenciales inválidas."""
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401


def test_get_current_user(client, auth_headers):
    """Test: Obtener usuario actual."""
    response = client.get("/users/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
```

### 8.3. `tests/test_orders.py`

```python
from fastapi import status


def test_create_order(client, auth_headers):
    """Test: Crear pedido."""
    response = client.post("/orders", headers=auth_headers, json={
        "items": [
            {"product_name": "Laptop", "quantity": 1, "price": 999.99},
            {"product_name": "Mouse", "quantity": 2, "price": 25.50}
        ]
    })
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["status"] == "pending"
    assert data["total"] == 1050.99  # 999.99 + (25.50 * 2)
    assert len(data["items"]) == 2


def test_create_order_without_auth(client):
    """Test: Crear pedido sin autenticación."""
    response = client.post("/orders", json={
        "items": [{"product_name": "Item", "quantity": 1, "price": 10.0}]
    })
    
    assert response.status_code == 403  # Forbidden


def test_list_orders(client, auth_headers, db_session, test_user):
    """Test: Listar pedidos del usuario."""
    # Crear pedido
    client.post("/orders", headers=auth_headers, json={
        "items": [{"product_name": "Item", "quantity": 1, "price": 10.0}]
    })
    
    # Listar
    response = client.get("/orders", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == test_user.id


def test_get_order(client, auth_headers):
    """Test: Obtener pedido específico."""
    # Crear
    create_response = client.post("/orders", headers=auth_headers, json={
        "items": [{"product_name": "Item", "quantity": 1, "price": 10.0}]
    })
    order_id = create_response.json()["id"]
    
    # Obtener
    response = client.get(f"/orders/{order_id}", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id


def test_get_order_unauthorized(client, auth_headers, db_session):
    """Test: Intentar acceder pedido de otro usuario."""
    # Crear otro usuario y su pedido
    from app.models.user import User
    from app.models.order import Order
    from app.utils.security import get_password_hash
    
    other_user = User(
        username="otheruser",
        email="other@example.com",
        hashed_password=get_password_hash("pass123")
    )
    db_session.add(other_user)
    db_session.commit()
    
    other_order = Order(user_id=other_user.id, total=100.0)
    db_session.add(other_order)
    db_session.commit()
    
    # Intentar acceder con testuser
    response = client.get(f"/orders/{other_order.id}", headers=auth_headers)
    
    assert response.status_code == 403  # Forbidden


def test_update_order(client, auth_headers):
    """Test: Actualizar pedido."""
    # Crear
    create_response = client.post("/orders", headers=auth_headers, json={
        "items": [{"product_name": "Item", "quantity": 1, "price": 10.0}]
    })
    order_id = create_response.json()["id"]
    
    # Actualizar
    response = client.put(f"/orders/{order_id}", headers=auth_headers, json={
        "status": "completed"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"


def test_delete_order(client, auth_headers):
    """Test: Eliminar pedido."""
    # Crear
    create_response = client.post("/orders", headers=auth_headers, json={
        "items": [{"product_name": "Item", "quantity": 1, "price": 10.0}]
    })
    order_id = create_response.json()["id"]
    
    # Eliminar
    response = client.delete(f"/orders/{order_id}", headers=auth_headers)
    
    assert response.status_code == 204
    
    # Verificar que no existe
    get_response = client.get(f"/orders/{order_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_add_items_to_order(client, auth_headers):
    """Test: Agregar items a pedido."""
    # Crear pedido
    create_response = client.post("/orders", headers=auth_headers, json={
        "items": [{"product_name": "Item 1", "quantity": 1, "price": 10.0}]
    })
    order_id = create_response.json()["id"]
    
    # Agregar más items
    response = client.post(f"/orders/{order_id}/items", headers=auth_headers, json=[
        {"product_name": "Item 2", "quantity": 2, "price": 20.0}
    ])
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 50.0  # 10 + (20*2)


def test_validation_price_positive(client, auth_headers):
    """Test: Validación de precio positivo."""
    response = client.post("/orders", headers=auth_headers, json={
        "items": [{"product_name": "Item", "quantity": 1, "price": -10.0}]
    })
    
    assert response.status_code == 422  # Validation error


def test_validation_quantity_positive(client, auth_headers):
    """Test: Validación de cantidad positiva."""
    response = client.post("/orders", headers=auth_headers, json={
        "items": [{"product_name": "Item", "quantity": 0, "price": 10.0}]
    })
    
    assert response.status_code == 422


def test_admin_sees_all_orders(client, db_session, admin_user, test_user):
    """Test: Admin ve todos los pedidos."""
    # Login como admin
    login_response = client.post("/auth/login", data={
        "username": "admin",
        "password": "adminpass123"
    })
    admin_token = login_response.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Crear pedido con testuser
    from app.models.order import Order
    user_order = Order(user_id=test_user.id, total=50.0)
    db_session.add(user_order)
    db_session.commit()
    
    # Admin lista todos
    response = client.get("/orders", headers=admin_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1  # Ve el pedido del testuser
```

---

## ▶️ Paso 9: Ejecutar el Proyecto

### 9.1. Iniciar Servidor

```bash
# Desde la raíz del proyecto
uvicorn app.main:app --reload
```

### 9.2. Probar en Swagger UI

Abrir en navegador: http://localhost:8000/docs

### 9.3. Ejecutar Tests

```bash
# Todos los tests
pytest

# Con verbose
pytest -v

# Con coverage
pytest --cov=app

# Tests específicos
pytest tests/test_auth.py
pytest tests/test_orders.py
```


---

## 📚 Recursos

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Validation](https://docs.pydantic.dev/latest/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/)
- [pytest Documentation](https://docs.pytest.org/)
- [JWT Introduction](https://jwt.io/introduction)

