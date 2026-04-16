# Módulo 8: Acceso a Datos y ORM

## Descripción

Este módulo cubre técnicas profesionales para trabajar con bases de datos relacionales y NoSQL en Python, utilizando tanto SQL directo como ORMs modernos.

## Objetivos de Aprendizaje

- Trabajar con SQLite y drivers para PostgreSQL/SQL Server
- Dominar SQLAlchemy Core (SQL expression language) y ORM
- Modelar entidades con relaciones (One-to-Many, Many-to-Many)
- Gestionar migraciones de base de datos con Alembic
- Realizar operaciones CRUD robustas con transacciones
- Introducción a MongoDB y Motor (driver async)

## Contenidos

### 1. SQLite y Drivers de Bases de Datos
- **sqlite3**: Base de datos embebida
- **psycopg2**: Driver PostgreSQL
- **pyodbc/pymssql**: Drivers SQL Server
- Connection pooling y context managers
- Transacciones y rollback

### 2. SQLAlchemy Core
- SQL Expression Language
- Tables, columns, constraints
- Select, insert, update, delete
- Joins y subqueries
- Transactions y engine configuration

### 3. SQLAlchemy ORM
- Declarative base y modelos
- Relaciones: One-to-Many, Many-to-Many
- Lazy loading vs Eager loading
- Session management
- Query API avanzado

### 4. Migraciones con Alembic
- Inicialización de proyecto
- Auto-generación de migraciones
- Upgrade y downgrade
- Branching y merging
- Migraciones de datos

### 5. MongoDB con Motor
- Conceptos NoSQL vs SQL
- Motor (async MongoDB driver)
- CRUD operations
- Índices y agregaciones
- Validación de esquemas

## Estructura del Módulo

```
Modulo_08_Datos_ORM/
├── README.md                      # Este archivo
├── requirements.txt               # Dependencias
├── 01_sqlite3_basico.py          # SQLite fundamentals
├── 02_sqlalchemy_core.py         # SQLAlchemy Core
├── 03_sqlalchemy_orm.py          # SQLAlchemy ORM
├── 04_alembic_migraciones.py     # Migraciones
├── 05_mongodb_motor.py           # MongoDB async
├── LABORATORIO.md                # Proyecto guiado
└── EJERCICIOS.md                 # Ejercicios adicionales
```

## Tecnologías

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **SQLite** | Built-in | Base de datos embebida |
| **SQLAlchemy** | 2.0+ | ORM y SQL toolkit |
| **Alembic** | 1.13+ | Migraciones de BD |
| **psycopg2-binary** | 2.9+ | Driver PostgreSQL |
| **pymongo** | 4.6+ | Driver MongoDB |
| **motor** | 3.3+ | Async MongoDB driver |

## Comparación: SQLAlchemy Core vs ORM

### SQLAlchemy Core (Expression Language)

**Ventajas:**
- Más cercano a SQL real
- Mayor control sobre queries
- Mejor rendimiento en queries complejas
- Ideal para scripts y transformaciones

**Cuándo usar:**
- Necesitas control fino sobre SQL
- Queries muy complejas o optimizadas
- Batch processing
- Reporting y analytics

**Ejemplo:**
```python
from sqlalchemy import select, insert

# Core - SQL Expression Language
stmt = select(users.c.name, users.c.email).where(users.c.age > 18)
result = conn.execute(stmt)
```

### SQLAlchemy ORM

**Ventajas:**
- Abstracción orientada a objetos
- Relaciones automáticas (lazy/eager)
- Session management
- Validación de modelos
- Ideal para aplicaciones

**Cuándo usar:**
- Aplicaciones con muchas entidades
- Necesitas relaciones complejas
- Domain-driven design
- APIs REST/GraphQL

**Ejemplo:**
```python
from sqlalchemy.orm import Session

# ORM - Objetos Python
session = Session(engine)
users = session.query(User).filter(User.age > 18).all()
```

## Drivers de Bases de Datos

### SQLite (Built-in)
```python
import sqlite3

# No requiere instalación adicional
conn = sqlite3.connect('database.db')
```

**Características:**
- Embebido, sin servidor
- Ideal para desarrollo y testing
- Soporta la mayoría de SQL standard
- Limitaciones: sin usuarios, locks a nivel DB

### PostgreSQL (psycopg2)
```python
import psycopg2

# Instalar: pip install psycopg2-binary
conn = psycopg2.connect(
    dbname='mydb',
    user='user',
    password='pass',
    host='localhost',
    port=5432
)
```

**Características:**
- Base de datos más avanzada open-source
- ACID compliant
- JSON, arrays, tipos custom
- Extensiones (PostGIS, pgcrypto)

### SQL Server (pyodbc)
```python
import pyodbc

# Instalar: pip install pyodbc
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;DATABASE=mydb;UID=user;PWD=pass'
)
```

**Características:**
- Enterprise database de Microsoft
- Integración con ecosistema .NET
- T-SQL (Transact-SQL)
- Azure SQL Database compatible

## SQLAlchemy Connection Strings

```python
# SQLite
engine = create_engine('sqlite:///database.db')
engine = create_engine('sqlite:///:memory:')  # In-memory

# PostgreSQL
engine = create_engine('postgresql://user:pass@localhost:5432/mydb')
engine = create_engine('postgresql+psycopg2://user:pass@localhost/mydb')

# SQL Server
engine = create_engine('mssql+pyodbc://user:pass@localhost/mydb?driver=ODBC+Driver+17+for+SQL+Server')

# MySQL
engine = create_engine('mysql+pymysql://user:pass@localhost/mydb')
```

## Patrones de Diseño

### 1. Repository Pattern

```python
class UserRepository:
    """Abstracción de acceso a datos."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.query(User).get(user_id)
    
    def get_all(self) -> list[User]:
        return self.session.query(User).all()
    
    def save(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        return user
    
    def delete(self, user: User):
        self.session.delete(user)
        self.session.commit()
```

### 2. Unit of Work Pattern

```python
class UnitOfWork:
    """Gestiona transacciones."""
    
    def __init__(self, session_factory):
        self.session_factory = session_factory
    
    def __enter__(self):
        self.session = self.session_factory()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
    
    def commit(self):
        self.session.commit()
    
    def rollback(self):
        self.session.rollback()
```

### 3. Active Record Pattern (Simple)

```python
class User(Base):
    """Modelo con métodos de persistencia."""
    
    @classmethod
    def find_by_email(cls, session, email):
        return session.query(cls).filter_by(email=email).first()
    
    def save(self, session):
        session.add(self)
        session.commit()
    
    def delete(self, session):
        session.delete(self)
        session.commit()
```

## Mejores Prácticas

### 1. Session Management

```python
# ❌ MAL - Session compartida
session = Session(engine)  # Global

# ✅ BIEN - Context manager
with Session(engine) as session:
    user = session.query(User).first()
    # Session se cierra automáticamente

# ✅ MEJOR - Scoped session
from sqlalchemy.orm import scoped_session, sessionmaker

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# En aplicación web (por request)
@app.route('/users')
def users():
    session = Session()
    try:
        users = session.query(User).all()
        return jsonify([u.to_dict() for u in users])
    finally:
        Session.remove()  # Limpia session del thread
```

### 2. Eager Loading (N+1 Problem)

```python
# ❌ MAL - Lazy loading (N+1 queries)
users = session.query(User).all()
for user in users:  # 1 query
    print(user.orders)  # N queries adicionales

# ✅ BIEN - Eager loading (1 query)
from sqlalchemy.orm import joinedload

users = session.query(User).options(
    joinedload(User.orders)
).all()  # 1 query con JOIN

for user in users:
    print(user.orders)  # Sin queries adicionales
```

### 3. Transacciones

```python
# ✅ BIEN - Transacción explícita
with Session(engine) as session:
    try:
        user = User(name='Alice')
        session.add(user)
        
        order = Order(user_id=user.id, total=100)
        session.add(order)
        
        session.commit()
    except Exception as e:
        session.rollback()
        raise

# ✅ MEJOR - Context manager con rollback automático
with Session(engine, begin=True) as session:
    # begin=True inicia transacción
    user = User(name='Alice')
    session.add(user)
    # Commit automático si no hay excepciones
```

### 4. Bulk Operations

```python
# ❌ MAL - Loop con commits individuales
for data in large_dataset:
    user = User(**data)
    session.add(user)
    session.commit()  # Lento!

# ✅ BIEN - Bulk insert
session.bulk_insert_mappings(User, large_dataset)
session.commit()  # 1 commit

# ✅ MEJOR - Batch processing
batch_size = 1000
for i in range(0, len(large_dataset), batch_size):
    batch = large_dataset[i:i+batch_size]
    session.bulk_insert_mappings(User, batch)
    session.commit()
```

### 5. Connection Pooling

```python
# ✅ Configurar pool apropiadamente
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:pass@localhost/mydb',
    poolclass=QueuePool,
    pool_size=10,        # Número de conexiones permanentes
    max_overflow=20,     # Conexiones adicionales temporales
    pool_timeout=30,     # Timeout para obtener conexión
    pool_recycle=3600,   # Reciclar conexiones cada hora
)
```

## Relaciones en SQLAlchemy

### One-to-Many

```python
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    orders = relationship('Order', back_populates='user')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='orders')
```

### Many-to-Many

```python
# Tabla de asociación
student_course = Table('student_course', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    courses = relationship('Course', secondary=student_course, back_populates='students')

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    students = relationship('Student', secondary=student_course, back_populates='courses')
```

### One-to-One

```python
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    profile = relationship('Profile', uselist=False, back_populates='user')

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    user = relationship('User', back_populates='profile')
```

## Migraciones con Alembic

### Flujo de Trabajo

```bash
# 1. Inicializar Alembic
alembic init alembic

# 2. Configurar alembic.ini (connection string)
sqlalchemy.url = postgresql://user:pass@localhost/mydb

# 3. Editar env.py (importar modelos)
from myapp.models import Base
target_metadata = Base.metadata

# 4. Crear migración automática
alembic revision --autogenerate -m "Create users table"

# 5. Revisar archivo de migración
# alembic/versions/xxxx_create_users_table.py

# 6. Aplicar migración
alembic upgrade head

# 7. Rollback si es necesario
alembic downgrade -1
```

### Comandos Útiles

```bash
# Ver estado actual
alembic current

# Ver historial
alembic history

# Upgrade a revisión específica
alembic upgrade abc123

# Downgrade a revisión específica
alembic downgrade abc123

# Mostrar SQL sin ejecutar
alembic upgrade head --sql

# Crear migración vacía (manual)
alembic revision -m "Add custom index"
```

## MongoDB vs SQL

| Aspecto | SQL (Relacional) | MongoDB (NoSQL) |
|---------|------------------|-----------------|
| **Estructura** | Tablas con schemas fijos | Colecciones con documentos JSON |
| **Relaciones** | Foreign keys, JOINs | Referencias o documentos embebidos |
| **Schema** | Estricto, definido | Flexible, dinámico |
| **Transacciones** | ACID completo | ACID desde v4.0 (multi-documento) |
| **Escalabilidad** | Vertical (más potente) | Horizontal (más servidores) |
| **Consultas** | SQL | Query language de MongoDB |
| **Cuándo usar** | Datos estructurados, transaccionales | Datos semi-estructurados, escalabilidad |

## Motor (Async MongoDB)

```python
import motor.motor_asyncio

# Cliente async
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db = client.mydatabase
collection = db.users

# CRUD async
async def create_user(name, email):
    result = await collection.insert_one({'name': name, 'email': email})
    return result.inserted_id

async def find_users():
    cursor = collection.find({'age': {'$gt': 18}})
    users = await cursor.to_list(length=100)
    return users
```

## Testing con SQLite In-Memory

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

@pytest.fixture
def db_session():
    """Session de prueba en memoria."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session
    
    engine.dispose()

def test_create_user(db_session):
    user = User(name='Test User', email='test@example.com')
    db_session.add(user)
    db_session.commit()
    
    assert user.id is not None
    assert db_session.query(User).count() == 1
```

## Recursos Adicionales

### Documentación Oficial
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Motor Documentation](https://motor.readthedocs.io/)
- [MongoDB Manual](https://docs.mongodb.com/manual/)

