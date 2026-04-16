# 🧪 Laboratorio Módulo 8 - Sistema de Gestión de Pedidos

## 📋 Objetivo

Construir un sistema completo de gestión de usuarios y pedidos implementando:
- ✅ Modelos con SQLAlchemy ORM (User, Order, OrderItem, Product)
- ✅ Relaciones entre entidades (One-to-Many, Many-to-One)
- ✅ CRUD operations completo
- ✅ Migraciones con Alembic
- ✅ Tests con SQLite en memoria
- ✅ Repository pattern

---

## 🎯 Parte 1: Configuración del Proyecto

### 1.1 Estructura de Directorios

```
ecommerce_lab/
├── alembic/                  # Configuración de Alembic
│   └── versions/             # Archivos de migración
├── models/
│   ├── __init__.py
│   ├── base.py              # DeclarativeBase
│   ├── user.py              # Modelo User
│   ├── product.py           # Modelo Product
│   ├── order.py             # Modelo Order
│   └── order_item.py        # Modelo OrderItem
├── repositories/
│   ├── __init__.py
│   ├── base.py              # BaseRepository
│   ├── user_repository.py
│   └── order_repository.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures de pytest
│   ├── test_models.py       # Tests de modelos
│   ├── test_repositories.py # Tests de repositorios
│   └── test_integration.py  # Tests de integración
├── alembic.ini              # Configuración Alembic
├── database.py              # Configuración DB
├── main.py                  # Punto de entrada
└── requirements.txt
```

### 1.2 Crear `requirements.txt`

```txt
sqlalchemy>=2.0.25
alembic>=1.13.1
pytest>=7.4.3
pytest-asyncio>=0.21.1
```

### 1.3 Instalar dependencias

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🎯 Parte 2: Definir Modelos con SQLAlchemy ORM

### 2.1 `models/base.py` - Base declarativa

```python
"""Base declarativa para todos los modelos."""
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

# Estrategia de naming para constraints
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)


class Base(DeclarativeBase):
    """Clase base para todos los modelos."""
    metadata = metadata
```

### 2.2 `models/user.py` - Modelo User

```python
"""Modelo de usuario."""
from datetime import datetime
from typing import List
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class User(Base):
    """Modelo de usuario."""
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    
    # Relación con Orders (One-to-Many)
    orders: Mapped[List["Order"]] = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
```

### 2.3 `models/product.py` - Modelo Product

```python
"""Modelo de producto."""
from decimal import Decimal
from typing import List
from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Product(Base):
    """Modelo de producto."""
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock: Mapped[int] = mapped_column(default=0)
    
    # Relación con OrderItems
    order_items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="product"
    )
    
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"
```

### 2.4 `models/order.py` - Modelo Order

```python
"""Modelo de pedido."""
from datetime import datetime
from decimal import Decimal
from typing import List
from sqlalchemy import String, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Order(Base):
    """Modelo de pedido."""
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(
        String(20),
        default="pending"
    )  # pending, completed, cancelled
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    
    # Relación con User (Many-to-One)
    user: Mapped["User"] = relationship("User", back_populates="orders")
    
    # Relación con OrderItems (One-to-Many)
    items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Order(id={self.id}, user_id={self.user_id}, status={self.status}, total={self.total})>"
    
    def calculate_total(self) -> Decimal:
        """Calcular total del pedido."""
        return sum(item.subtotal for item in self.items)
```

### 2.5 `models/order_item.py` - Modelo OrderItem

```python
"""Modelo de item de pedido."""
from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class OrderItem(Base):
    """Modelo de item de pedido (relación Order-Product)."""
    __tablename__ = "order_items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(default=1)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))  # Precio al momento de compra
    
    # Relación con Order (Many-to-One)
    order: Mapped["Order"] = relationship("Order", back_populates="items")
    
    # Relación con Product (Many-to-One)
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")
    
    @property
    def subtotal(self) -> Decimal:
        """Calcular subtotal del item."""
        return self.price * self.quantity
    
    def __repr__(self) -> str:
        return f"<OrderItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity}, subtotal={self.subtotal})>"
```

### 2.6 `models/__init__.py` - Exportar modelos

```python
"""Exportar todos los modelos."""
from .base import Base
from .user import User
from .product import Product
from .order import Order
from .order_item import OrderItem

__all__ = ["Base", "User", "Product", "Order", "OrderItem"]
```

---

## 🎯 Parte 3: Configurar Database y Session

### 3.1 `database.py`

```python
"""Configuración de base de datos."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator
from models import Base

# SQLite para desarrollo
DATABASE_URL = "sqlite:///./ecommerce.db"

# Crear engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Mostrar SQL queries
    connect_args={"check_same_thread": False}  # Solo para SQLite
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def create_tables():
    """Crear todas las tablas."""
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas")


def drop_tables():
    """Eliminar todas las tablas."""
    Base.metadata.drop_all(bind=engine)
    print("✓ Tablas eliminadas")


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Context manager para sesión de DB."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

---

## 🎯 Parte 4: Implementar Repository Pattern

### 4.1 `repositories/base.py` - BaseRepository

```python
"""Repositorio base con operaciones comunes."""
from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.base import Base

T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    """Repositorio base genérico."""
    
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session
    
    def create(self, **kwargs) -> T:
        """Crear una entidad."""
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.flush()
        return instance
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Obtener entidad por ID."""
        return self.session.get(self.model, id)
    
    def get_all(self) -> List[T]:
        """Obtener todas las entidades."""
        stmt = select(self.model)
        return list(self.session.scalars(stmt).all())
    
    def update(self, instance: T, **kwargs) -> T:
        """Actualizar entidad."""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        self.session.flush()
        return instance
    
    def delete(self, instance: T) -> None:
        """Eliminar entidad."""
        self.session.delete(instance)
        self.session.flush()
    
    def count(self) -> int:
        """Contar entidades."""
        stmt = select(self.model)
        return len(self.session.scalars(stmt).all())
```

### 4.2 `repositories/user_repository.py`

```python
"""Repositorio de usuarios."""
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repositorio para User."""
    
    def __init__(self, session: Session):
        super().__init__(User, session)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email."""
        stmt = select(User).where(User.email == email)
        return self.session.scalar(stmt)
    
    def exists_email(self, email: str) -> bool:
        """Verificar si existe email."""
        return self.get_by_email(email) is not None
```

### 4.3 `repositories/order_repository.py`

```python
"""Repositorio de pedidos."""
from typing import List
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from models import Order, OrderItem, Product
from .base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """Repositorio para Order."""
    
    def __init__(self, session: Session):
        super().__init__(Order, session)
    
    def get_by_user(self, user_id: int) -> List[Order]:
        """Obtener órdenes de un usuario."""
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items))
        )
        return list(self.session.scalars(stmt).all())
    
    def get_with_items(self, order_id: int) -> Order:
        """Obtener orden con items (eager loading)."""
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.items))
        )
        return self.session.scalar(stmt)
    
    def add_item(
        self,
        order: Order,
        product: Product,
        quantity: int
    ) -> OrderItem:
        """Agregar item a orden."""
        item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity,
            price=product.price
        )
        self.session.add(item)
        
        # Actualizar total
        order.total = order.calculate_total()
        
        self.session.flush()
        return item
```

---

## 🎯 Parte 5: Configurar Alembic para Migraciones

### 5.1 Inicializar Alembic

```bash
alembic init alembic
```

### 5.2 Configurar `alembic.ini`

Cambiar la línea de `sqlalchemy.url`:

```ini
# sqlalchemy.url = driver://user:pass@localhost/dbname
sqlalchemy.url = sqlite:///./ecommerce.db
```

### 5.3 Configurar `alembic/env.py`

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Importar metadata de los modelos
from models.base import Base
import models  # Importar todos los modelos

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata

# ... resto del código generado por alembic init
```

### 5.4 Crear migración inicial

```bash
# Crear migración automática
alembic revision --autogenerate -m "Initial migration: users, products, orders, order_items"

# Aplicar migración
alembic upgrade head

# Ver historial
alembic history

# Ver estado actual
alembic current
```

### 5.5 Crear migración manual (ejemplo: agregar campo)

```bash
alembic revision -m "Add phone to users"
```

Editar el archivo generado en `alembic/versions/`:

```python
"""Add phone to users

Revision ID: abc123
"""
from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone')
```

Aplicar:

```bash
alembic upgrade head
```

---

## 🎯 Parte 6: Tests con Pytest y SQLite en Memoria

### 6.1 `tests/conftest.py` - Fixtures

```python
"""Fixtures para tests."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User, Product, Order
from repositories import UserRepository, OrderRepository


@pytest.fixture(scope="function")
def engine():
    """Engine de SQLite en memoria."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def session(engine) -> Session:
    """Sesión de DB para tests."""
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def user_repo(session) -> UserRepository:
    """Fixture de UserRepository."""
    return UserRepository(session)


@pytest.fixture
def order_repo(session) -> OrderRepository:
    """Fixture de OrderRepository."""
    return OrderRepository(session)


@pytest.fixture
def sample_user(user_repo) -> User:
    """Usuario de ejemplo."""
    user = user_repo.create(
        email="test@example.com",
        name="Test User"
    )
    user_repo.session.commit()
    return user


@pytest.fixture
def sample_product(session) -> Product:
    """Producto de ejemplo."""
    product = Product(
        name="Test Product",
        description="A test product",
        price=99.99,
        stock=10
    )
    session.add(product)
    session.commit()
    return product
```

### 6.2 `tests/test_models.py` - Tests de Modelos

```python
"""Tests de modelos."""
from decimal import Decimal
from models import User, Product, Order, OrderItem


def test_user_creation(session):
    """Test crear usuario."""
    user = User(email="alice@example.com", name="Alice")
    session.add(user)
    session.commit()
    
    assert user.id is not None
    assert user.email == "alice@example.com"
    assert user.name == "Alice"
    assert user.created_at is not None


def test_product_creation(session):
    """Test crear producto."""
    product = Product(
        name="Laptop",
        description="Gaming Laptop",
        price=Decimal("1499.99"),
        stock=5
    )
    session.add(product)
    session.commit()
    
    assert product.id is not None
    assert product.name == "Laptop"
    assert product.price == Decimal("1499.99")


def test_order_with_items(session):
    """Test orden con items."""
    # Crear user y product
    user = User(email="bob@example.com", name="Bob")
    product = Product(name="Mouse", price=Decimal("29.99"), stock=10)
    session.add_all([user, product])
    session.commit()
    
    # Crear orden
    order = Order(user_id=user.id, status="pending")
    session.add(order)
    session.commit()
    
    # Agregar items
    item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        quantity=2,
        price=product.price
    )
    session.add(item)
    session.commit()
    
    # Actualizar total
    order.total = order.calculate_total()
    session.commit()
    
    # Verificar
    assert order.id is not None
    assert len(order.items) == 1
    assert order.items[0].quantity == 2
    assert order.items[0].subtotal == Decimal("59.98")
    assert order.total == Decimal("59.98")


def test_user_orders_relationship(session):
    """Test relación User -> Orders."""
    user = User(email="carol@example.com", name="Carol")
    session.add(user)
    session.commit()
    
    # Crear 2 órdenes
    order1 = Order(user_id=user.id, status="pending")
    order2 = Order(user_id=user.id, status="completed")
    session.add_all([order1, order2])
    session.commit()
    
    # Verificar relación
    assert len(user.orders) == 2
    assert user.orders[0].user == user
    assert user.orders[1].user == user


def test_cascade_delete(session):
    """Test cascade delete."""
    user = User(email="dave@example.com", name="Dave")
    session.add(user)
    session.commit()
    
    order = Order(user_id=user.id, status="pending")
    session.add(order)
    session.commit()
    
    # Eliminar usuario (debe eliminar órdenes)
    session.delete(user)
    session.commit()
    
    # Verificar que orden fue eliminada
    assert session.get(Order, order.id) is None
```

### 6.3 `tests/test_repositories.py` - Tests de Repositorios

```python
"""Tests de repositorios."""
from models import User, Order


def test_user_repo_create(user_repo):
    """Test crear usuario con repositorio."""
    user = user_repo.create(email="alice@example.com", name="Alice")
    user_repo.session.commit()
    
    assert user.id is not None
    assert user.email == "alice@example.com"


def test_user_repo_get_by_id(user_repo, sample_user):
    """Test obtener usuario por ID."""
    user = user_repo.get_by_id(sample_user.id)
    
    assert user is not None
    assert user.id == sample_user.id
    assert user.email == sample_user.email


def test_user_repo_get_by_email(user_repo, sample_user):
    """Test obtener usuario por email."""
    user = user_repo.get_by_email("test@example.com")
    
    assert user is not None
    assert user.email == "test@example.com"


def test_user_repo_update(user_repo, sample_user):
    """Test actualizar usuario."""
    updated = user_repo.update(sample_user, name="Updated Name")
    user_repo.session.commit()
    
    assert updated.name == "Updated Name"
    
    # Verificar en DB
    user = user_repo.get_by_id(sample_user.id)
    assert user.name == "Updated Name"


def test_user_repo_delete(user_repo, sample_user):
    """Test eliminar usuario."""
    user_id = sample_user.id
    user_repo.delete(sample_user)
    user_repo.session.commit()
    
    # Verificar que no existe
    user = user_repo.get_by_id(user_id)
    assert user is None


def test_order_repo_get_by_user(order_repo, user_repo, sample_user):
    """Test obtener órdenes de usuario."""
    # Crear órdenes
    order1 = order_repo.create(user_id=sample_user.id, status="pending")
    order2 = order_repo.create(user_id=sample_user.id, status="completed")
    order_repo.session.commit()
    
    # Obtener órdenes
    orders = order_repo.get_by_user(sample_user.id)
    
    assert len(orders) == 2


def test_order_repo_add_item(order_repo, sample_user, sample_product, session):
    """Test agregar item a orden."""
    # Crear orden
    order = order_repo.create(user_id=sample_user.id, status="pending")
    session.commit()
    
    # Agregar item
    item = order_repo.add_item(order, sample_product, quantity=2)
    session.commit()
    
    # Verificar
    assert item.id is not None
    assert item.quantity == 2
    assert item.subtotal == sample_product.price * 2
    assert order.total == item.subtotal
```

### 6.4 `tests/test_integration.py` - Tests de Integración

```python
"""Tests de integración."""
from decimal import Decimal
from models import User, Product, Order, OrderItem


def test_complete_order_flow(session):
    """Test flujo completo de orden."""
    # 1. Crear usuario
    user = User(email="integration@example.com", name="Integration User")
    session.add(user)
    session.commit()
    
    # 2. Crear productos
    product1 = Product(name="Product 1", price=Decimal("50.00"), stock=10)
    product2 = Product(name="Product 2", price=Decimal("30.00"), stock=20)
    session.add_all([product1, product2])
    session.commit()
    
    # 3. Crear orden
    order = Order(user_id=user.id, status="pending")
    session.add(order)
    session.commit()
    
    # 4. Agregar items
    item1 = OrderItem(
        order_id=order.id,
        product_id=product1.id,
        quantity=2,
        price=product1.price
    )
    item2 = OrderItem(
        order_id=order.id,
        product_id=product2.id,
        quantity=3,
        price=product2.price
    )
    session.add_all([item1, item2])
    session.commit()
    
    # 5. Calcular total
    order.total = order.calculate_total()
    session.commit()
    
    # 6. Verificar
    assert len(order.items) == 2
    assert order.total == Decimal("190.00")  # (50*2) + (30*3)
    assert order.status == "pending"
    
    # 7. Completar orden
    order.status = "completed"
    session.commit()
    
    assert order.status == "completed"


def test_multiple_users_with_orders(session):
    """Test múltiples usuarios con órdenes."""
    # Crear usuarios
    users = [
        User(email=f"user{i}@example.com", name=f"User {i}")
        for i in range(3)
    ]
    session.add_all(users)
    session.commit()
    
    # Crear orden para cada usuario
    for user in users:
        order = Order(user_id=user.id, status="pending")
        session.add(order)
    
    session.commit()
    
    # Verificar
    for user in users:
        assert len(user.orders) == 1
    
    # Contar todas las órdenes
    all_orders = session.query(Order).count()
    assert all_orders == 3
```

### 6.5 Ejecutar Tests

```bash
# Instalar pytest
pip install pytest pytest-cov

# Ejecutar tests
pytest

# Con cobertura
pytest --cov=models --cov=repositories --cov-report=html

# Ejecutar test específico
pytest tests/test_models.py::test_user_creation -v

# Ver output detallado
pytest -v -s
```

---

## 🎯 Parte 7: Main Application

### 7.1 `main.py`

```python
"""Aplicación principal."""
from decimal import Decimal
from database import create_tables, drop_tables, get_session
from repositories import UserRepository, OrderRepository
from models import Product


def seed_data():
    """Insertar datos de ejemplo."""
    with get_session() as session:
        user_repo = UserRepository(session)
        
        # Crear usuarios
        alice = user_repo.create(email="alice@example.com", name="Alice Johnson")
        bob = user_repo.create(email="bob@example.com", name="Bob Smith")
        
        # Crear productos
        products = [
            Product(name="Laptop", price=Decimal("1499.99"), stock=5),
            Product(name="Mouse", price=Decimal("29.99"), stock=50),
            Product(name="Keyboard", price=Decimal("79.99"), stock=30)
        ]
        session.add_all(products)
        session.flush()
        
        # Crear órdenes
        order_repo = OrderRepository(session)
        
        order1 = order_repo.create(user_id=alice.id, status="pending")
        order_repo.add_item(order1, products[0], quantity=1)
        order_repo.add_item(order1, products[1], quantity=2)
        
        order2 = order_repo.create(user_id=bob.id, status="completed")
        order_repo.add_item(order2, products[2], quantity=1)
        
        print("✓ Datos de ejemplo insertados")


def list_users():
    """Listar usuarios con sus órdenes."""
    with get_session() as session:
        user_repo = UserRepository(session)
        users = user_repo.get_all()
        
        print("\n" + "="*60)
        print("USUARIOS Y ÓRDENES")
        print("="*60 + "\n")
        
        for user in users:
            print(f"👤 {user.name} ({user.email})")
            print(f"   📧 Email: {user.email}")
            print(f"   📅 Creado: {user.created_at}")
            print(f"   🛒 Órdenes: {len(user.orders)}")
            
            for order in user.orders:
                print(f"      Order #{order.id}: ${order.total} - {order.status}")
                for item in order.items:
                    print(f"         • {item.product.name}: {item.quantity}x ${item.price} = ${item.subtotal}")
            
            print()


def main():
    """Función principal."""
    print("=" * 60)
    print("E-COMMERCE LAB - Sistema de Gestión de Pedidos")
    print("=" * 60 + "\n")
    
    # Crear tablas
    drop_tables()
    create_tables()
    
    # Insertar datos
    seed_data()
    
    # Listar datos
    list_users()
    
    print("=" * 60)
    print("✓ Aplicación completada")
    print("=" * 60)


if __name__ == "__main__":
    main()
```

---

## 🎯 Parte 8: Ejecución y Validación

### 8.1 Crear base de datos

```bash
# Con Alembic
alembic upgrade head

# O con Python
python -c "from database import create_tables; create_tables()"
```

### 8.2 Ejecutar aplicación

```bash
python main.py
```

**Salida esperada:**

```
============================================================
E-COMMERCE LAB - Sistema de Gestión de Pedidos
============================================================

✓ Tablas eliminadas
✓ Tablas creadas
✓ Datos de ejemplo insertados

============================================================
USUARIOS Y ÓRDENES
============================================================

👤 Alice Johnson (alice@example.com)
   📧 Email: alice@example.com
   📅 Creado: 2024-04-16 10:00:00
   🛒 Órdenes: 1
      Order #1: $1559.97 - pending
         • Laptop: 1x $1499.99 = $1499.99
         • Mouse: 2x $29.99 = $59.98

👤 Bob Smith (bob@example.com)
   📧 Email: bob@example.com
   📅 Creado: 2024-04-16 10:00:01
   🛒 Órdenes: 1
      Order #2: $79.99 - completed
         • Keyboard: 1x $79.99 = $79.99

============================================================
✓ Aplicación completada
============================================================
```

### 8.3 Ejecutar tests

```bash
pytest -v

# Salida esperada:
# tests/test_models.py::test_user_creation PASSED
# tests/test_models.py::test_product_creation PASSED
# tests/test_models.py::test_order_with_items PASSED
# tests/test_models.py::test_user_orders_relationship PASSED
# tests/test_models.py::test_cascade_delete PASSED
# tests/test_repositories.py::test_user_repo_create PASSED
# tests/test_repositories.py::test_user_repo_get_by_id PASSED
# tests/test_repositories.py::test_user_repo_get_by_email PASSED
# tests/test_repositories.py::test_user_repo_update PASSED
# tests/test_repositories.py::test_user_repo_delete PASSED
# tests/test_repositories.py::test_order_repo_get_by_user PASSED
# tests/test_repositories.py::test_order_repo_add_item PASSED
# tests/test_integration.py::test_complete_order_flow PASSED
# tests/test_integration.py::test_multiple_users_with_orders PASSED
#
# ====================== 14 passed in 0.52s ======================
```

---

## 📚 Comandos de Referencia Rápida

```bash
# Alembic
alembic init alembic
alembic revision --autogenerate -m "message"
alembic upgrade head
alembic downgrade -1
alembic history
alembic current

# Pytest
pytest                          # Ejecutar todos
pytest tests/test_models.py     # Archivo específico
pytest -v -s                    # Verbose + stdout
pytest --cov                    # Con cobertura
pytest -k "test_user"          # Tests que coincidan

# Python
python main.py                  # Ejecutar app
python -m pytest                # Ejecutar tests con módulo
```

---
