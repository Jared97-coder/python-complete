"""
Módulo 8.3 - SQLAlchemy ORM

El ORM de SQLAlchemy permite trabajar con bases de datos usando objetos Python,
con mapeo automático entre tablas y clases.

Temas:
- Declarative Base y modelos
- Relaciones: One-to-Many, Many-to-Many, One-to-One
- Session management
- Query API (select)
- Lazy loading vs Eager loading (joinedload, selectinload)
- Backref y back_populates
- Cascade operations
- Repository pattern
"""

from sqlalchemy import (
    create_engine, select, func, and_, or_,
    String, Integer, Float, DateTime, ForeignKey, Table, Column, Text
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship,
    Session, sessionmaker, scoped_session,
    joinedload, selectinload, subqueryload
)
from sqlalchemy.pool import StaticPool
from datetime import datetime
from typing import List, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Declarative Base (SQLAlchemy 2.0)
# =============================================================================

class Base(DeclarativeBase):
    """Base class para todos los modelos."""
    pass


# =============================================================================
# Ejemplo 1: Modelo Básico
# =============================================================================

class User(Base):
    """Modelo de usuario."""
    
    __tablename__ = 'users'
    
    # Columnas con type hints (SQLAlchemy 2.0)
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    age: Mapped[Optional[int]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"


def ejemplo_01_modelo_basico():
    """Crear engine y tablas."""
    print("=== Ejemplo 1: Modelo Básico ===\n")
    
    # Engine
    engine = create_engine('sqlite:///:memory:', poolclass=StaticPool)
    
    # Crear tablas
    Base.metadata.create_all(engine)
    
    print(f"✓ Tablas creadas: {list(Base.metadata.tables.keys())}")
    
    return engine


# =============================================================================
# Ejemplo 2: CRUD Básico con Session
# =============================================================================

def ejemplo_02_crud_basico(engine):
    """Operaciones CRUD básicas."""
    print("\n=== Ejemplo 2: CRUD Básico ===\n")
    
    # Crear session
    with Session(engine) as session:
        # CREATE
        user = User(name='Alice Johnson', email='alice@example.com', age=30)
        session.add(user)
        session.commit()
        
        print(f"✓ Usuario creado: {user}")
        print(f"  ID asignado: {user.id}")
        
        # READ
        stmt = select(User).where(User.email == 'alice@example.com')
        alice = session.scalar(stmt)
        print(f"\n✓ Usuario encontrado: {alice}")
        
        # UPDATE
        alice.age = 31
        session.commit()
        print(f"✓ Usuario actualizado: edad = {alice.age}")
        
        # DELETE (comentado para mantener datos)
        # session.delete(alice)
        # session.commit()
        # print("✓ Usuario eliminado")


# =============================================================================
# Ejemplo 3: Insertar Múltiples Registros
# =============================================================================

def ejemplo_03_bulk_insert(engine):
    """Insertar múltiples registros."""
    print("\n=== Ejemplo 3: Bulk Insert ===\n")
    
    with Session(engine) as session:
        users = [
            User(name='Bob Smith', email='bob@example.com', age=25),
            User(name='Carol White', email='carol@example.com', age=35),
            User(name='David Brown', email='david@example.com', age=28)
        ]
        
        session.add_all(users)
        session.commit()
        
        print(f"✓ {len(users)} usuarios insertados")
        
        # Verificar
        count = session.scalar(select(func.count()).select_from(User))
        print(f"  Total usuarios: {count}")


# =============================================================================
# Ejemplo 4: Query API (Select)
# =============================================================================

def ejemplo_04_query_api(engine):
    """Usar Query API para consultas."""
    print("\n=== Ejemplo 4: Query API ===\n")
    
    with Session(engine) as session:
        # SELECT all
        stmt = select(User)
        users = session.scalars(stmt).all()
        
        print(f"Todos los usuarios ({len(users)}):")
        for user in users:
            print(f"  {user.name}: {user.age} años")
        
        # WHERE
        stmt = select(User).where(User.age > 28)
        older_users = session.scalars(stmt).all()
        
        print(f"\nUsuarios > 28 años: {len(older_users)}")
        
        # ORDER BY
        stmt = select(User).order_by(User.age.desc())
        users = session.scalars(stmt).all()
        
        print("\nUsuarios por edad (desc):")
        for user in users:
            print(f"  {user.name}: {user.age}")
        
        # LIMIT
        stmt = select(User).limit(2)
        users = session.scalars(stmt).all()
        
        print(f"\nPrimeros 2 usuarios: {[u.name for u in users]}")


# =============================================================================
# Ejemplo 5: Relación One-to-Many
# =============================================================================

class Order(Base):
    """Modelo de orden."""
    
    __tablename__ = 'orders'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    total: Mapped[float]
    status: Mapped[str] = mapped_column(String(20), default='pending')
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    # Relación Many-to-One
    user: Mapped["User"] = relationship(back_populates='orders')
    
    def __repr__(self):
        return f"Order(id={self.id}, user_id={self.user_id}, total={self.total})"


# Actualizar User con relación One-to-Many
User.orders = relationship('Order', back_populates='user', cascade='all, delete-orphan')


def ejemplo_05_one_to_many(engine):
    """Relación One-to-Many."""
    print("\n=== Ejemplo 5: One-to-Many ===\n")
    
    # Recrear tablas con nuevo modelo
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    with Session(engine) as session:
        # Crear usuario
        user = User(name='Alice Johnson', email='alice@example.com', age=30)
        session.add(user)
        session.flush()  # Asignar ID sin commit
        
        # Crear órdenes
        order1 = Order(user_id=user.id, total=99.99, status='completed')
        order2 = Order(user_id=user.id, total=50.00, status='pending')
        
        session.add_all([order1, order2])
        session.commit()
        
        print(f"✓ Usuario con {len(user.orders)} órdenes creado")
        
        # Acceder a relación
        stmt = select(User).where(User.email == 'alice@example.com')
        alice = session.scalar(stmt)
        
        print(f"\nÓrdenes de {alice.name}:")
        for order in alice.orders:
            print(f"  Orden #{order.id}: ${order.total} ({order.status})")


# =============================================================================
# Ejemplo 6: Lazy Loading vs Eager Loading
# =============================================================================

def ejemplo_06_loading_strategies(engine):
    """Comparar lazy y eager loading."""
    print("\n=== Ejemplo 6: Loading Strategies ===\n")
    
    with Session(engine) as session:
        # Insertar más datos
        users = [
            User(name='Bob Smith', email='bob@example.com', age=25),
            User(name='Carol White', email='carol@example.com', age=35)
        ]
        session.add_all(users)
        session.flush()
        
        for user in users:
            orders = [
                Order(user_id=user.id, total=10.0 * i, status='completed')
                for i in range(3)
            ]
            session.add_all(orders)
        
        session.commit()
    
    # LAZY LOADING (default) - N+1 problem
    print("1. Lazy Loading (N+1 queries):")
    with Session(engine) as session:
        stmt = select(User)
        users = session.scalars(stmt).all()  # 1 query
        
        for user in users:
            # Cada acceso a .orders hace una query adicional (N queries)
            print(f"  {user.name}: {len(user.orders)} órdenes")
    
    # EAGER LOADING con joinedload - 1 query con JOIN
    print("\n2. Eager Loading con joinedload (1 query):")
    with Session(engine) as session:
        stmt = select(User).options(joinedload(User.orders))
        users = session.scalars(stmt).unique().all()  # 1 query con JOIN
        
        for user in users:
            print(f"  {user.name}: {len(user.orders)} órdenes")  # Sin queries adicionales
    
    # EAGER LOADING con selectinload - 2 queries
    print("\n3. Eager Loading con selectinload (2 queries):")
    with Session(engine) as session:
        stmt = select(User).options(selectinload(User.orders))
        users = session.scalars(stmt).all()  # 1 query + 1 query para orders
        
        for user in users:
            print(f"  {user.name}: {len(user.orders)} órdenes")


# =============================================================================
# Ejemplo 7: Many-to-Many Relationship
# =============================================================================

# Tabla de asociación
student_course = Table(
    'student_course',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)


class Student(Base):
    """Modelo de estudiante."""
    
    __tablename__ = 'students'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    
    # Relación Many-to-Many
    courses: Mapped[List["Course"]] = relationship(
        secondary=student_course,
        back_populates='students'
    )
    
    def __repr__(self):
        return f"Student(id={self.id}, name='{self.name}')"


class Course(Base):
    """Modelo de curso."""
    
    __tablename__ = 'courses'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    
    # Relación Many-to-Many
    students: Mapped[List["Student"]] = relationship(
        secondary=student_course,
        back_populates='courses'
    )
    
    def __repr__(self):
        return f"Course(id={self.id}, name='{self.name}')"


def ejemplo_07_many_to_many(engine):
    """Relación Many-to-Many."""
    print("\n=== Ejemplo 7: Many-to-Many ===\n")
    
    # Crear tablas
    Base.metadata.create_all(engine)
    
    with Session(engine) as session:
        # Crear estudiantes
        alice = Student(name='Alice')
        bob = Student(name='Bob')
        
        # Crear cursos
        python = Course(name='Python Programming')
        data_science = Course(name='Data Science')
        web_dev = Course(name='Web Development')
        
        # Asociar estudiantes y cursos
        alice.courses.extend([python, data_science])
        bob.courses.extend([python, web_dev])
        
        session.add_all([alice, bob, python, data_science, web_dev])
        session.commit()
        
        print("✓ Estudiantes y cursos creados")
        
        # Consultar relaciones
        stmt = select(Student).options(selectinload(Student.courses))
        students = session.scalars(stmt).all()
        
        print("\nEstudiantes y sus cursos:")
        for student in students:
            courses = ', '.join([c.name for c in student.courses])
            print(f"  {student.name}: {courses}")
        
        # Inversa
        stmt = select(Course).options(selectinload(Course.students))
        courses = session.scalars(stmt).all()
        
        print("\nCursos y sus estudiantes:")
        for course in courses:
            students = ', '.join([s.name for s in course.students])
            print(f"  {course.name}: {students}")


# =============================================================================
# Ejemplo 8: One-to-One Relationship
# =============================================================================

class Profile(Base):
    """Modelo de perfil de usuario."""
    
    __tablename__ = 'profiles'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    website: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Relación One-to-One
    user: Mapped["User"] = relationship(back_populates='profile')
    
    def __repr__(self):
        return f"Profile(user_id={self.user_id}, website='{self.website}')"


# Actualizar User
User.profile = relationship('Profile', back_populates='user', uselist=False)


def ejemplo_08_one_to_one(engine):
    """Relación One-to-One."""
    print("\n=== Ejemplo 8: One-to-One ===\n")
    
    # Recrear tablas
    Base.metadata.create_all(engine)
    
    with Session(engine) as session:
        # Buscar usuario existente
        stmt = select(User).where(User.email == 'alice@example.com')
        alice = session.scalar(stmt)
        
        if alice:
            # Crear perfil
            profile = Profile(
                user_id=alice.id,
                bio='Python developer',
                website='https://alice.dev'
            )
            session.add(profile)
            session.commit()
            
            print(f"✓ Perfil creado para {alice.name}")
            
            # Acceder a relación
            print(f"  Website: {alice.profile.website}")
            print(f"  Bio: {alice.profile.bio}")


# =============================================================================
# Ejemplo 9: Cascade Operations
# =============================================================================

def ejemplo_09_cascade(engine):
    """Operaciones en cascada."""
    print("\n=== Ejemplo 9: Cascade Operations ===\n")
    
    with Session(engine) as session:
        # Crear usuario con órdenes
        user = User(name='TestUser', email='test@example.com', age=25)
        user.orders = [
            Order(total=10.0, status='pending'),
            Order(total=20.0, status='completed')
        ]
        
        session.add(user)
        session.commit()
        
        user_id = user.id
        print(f"✓ Usuario creado con {len(user.orders)} órdenes")
    
    # Eliminar usuario (cascade='all, delete-orphan' eliminará órdenes)
    with Session(engine) as session:
        stmt = select(User).where(User.id == user_id)
        user = session.scalar(stmt)
        
        if user:
            orders_count = len(user.orders)
            session.delete(user)
            session.commit()
            
            print(f"✓ Usuario eliminado (cascade eliminó {orders_count} órdenes)")


# =============================================================================
# Ejemplo 10: Filtering y Operators
# =============================================================================

def ejemplo_10_filtering(engine):
    """Operadores de filtrado."""
    print("\n=== Ejemplo 10: Filtering ===\n")
    
    with Session(engine) as session:
        # Operadores básicos
        stmt = select(User).where(User.age >= 30)
        users = session.scalars(stmt).all()
        print(f"Usuarios >= 30 años: {[u.name for u in users]}")
        
        # LIKE
        stmt = select(User).where(User.name.like('A%'))
        users = session.scalars(stmt).all()
        print(f"Nombres que empiezan con A: {[u.name for u in users]}")
        
        # IN
        stmt = select(User).where(User.name.in_(['Alice Johnson', 'Bob Smith']))
        users = session.scalars(stmt).all()
        print(f"Usuarios específicos: {[u.name for u in users]}")
        
        # AND / OR
        stmt = select(User).where(
            and_(User.age >= 25, User.age <= 35)
        )
        users = session.scalars(stmt).all()
        print(f"Usuarios entre 25 y 35: {[u.name for u in users]}")
        
        # NOT NULL
        stmt = select(User).where(User.age.isnot(None))
        users = session.scalars(stmt).all()
        print(f"Usuarios con edad: {[u.name for u in users]}")


# =============================================================================
# Ejemplo 11: Joins en ORM
# =============================================================================

def ejemplo_11_joins_orm(engine):
    """JOINs con ORM."""
    print("\n=== Ejemplo 11: Joins en ORM ===\n")
    
    with Session(engine) as session:
        # JOIN implícito
        stmt = select(User, Order).join(Order.user)
        results = session.execute(stmt).all()
        
        print("Usuarios y órdenes (JOIN):")
        for user, order in results[:5]:  # Primeros 5
            print(f"  {user.name} - Orden #{order.id}: ${order.total}")
        
        # JOIN con WHERE
        stmt = select(User).join(User.orders).where(Order.total > 50)
        users = session.scalars(stmt).unique().all()
        
        print(f"\nUsuarios con órdenes > $50: {[u.name for u in users]}")


# =============================================================================
# Ejemplo 12: Aggregations en ORM
# =============================================================================

def ejemplo_12_aggregations_orm(engine):
    """Agregaciones en ORM."""
    print("\n=== Ejemplo 12: Agregaciones ===\n")
    
    with Session(engine) as session:
        # COUNT
        count = session.scalar(select(func.count()).select_from(User))
        print(f"Total usuarios: {count}")
        
        # SUM
        total_revenue = session.scalar(
            select(func.sum(Order.total)).where(Order.status == 'completed')
        )
        print(f"Revenue total: ${total_revenue:.2f}")
        
        # AVG
        avg_order = session.scalar(select(func.avg(Order.total)))
        print(f"Promedio de órdenes: ${avg_order:.2f}")
        
        # GROUP BY
        stmt = select(
            User.name,
            func.count(Order.id).label('order_count')
        ).join(User.orders).group_by(User.id).order_by(func.count(Order.id).desc())
        
        results = session.execute(stmt).all()
        
        print("\nÓrdenes por usuario:")
        for name, count in results[:5]:
            print(f"  {name}: {count} órdenes")


# =============================================================================
# Ejemplo 13: Session Scopes y Factories
# =============================================================================

def ejemplo_13_session_factory(engine):
    """Session factory y scoped session."""
    print("\n=== Ejemplo 13: Session Factory ===\n")
    
    # Session factory
    SessionFactory = sessionmaker(bind=engine)
    
    # Usar factory
    with SessionFactory() as session:
        count = session.scalar(select(func.count()).select_from(User))
        print(f"✓ Session factory: {count} usuarios")
    
    # Scoped session (thread-local)
    ScopedSession = scoped_session(SessionFactory)
    
    try:
        count = ScopedSession.execute(select(func.count()).select_from(User)).scalar()
        print(f"✓ Scoped session: {count} usuarios")
    finally:
        ScopedSession.remove()  # Limpiar session


# =============================================================================
# Ejemplo 14: Repository Pattern
# =============================================================================

class UserRepository:
    """Repository pattern para User."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene usuario por ID."""
        return self.session.get(User, user_id)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene usuario por email."""
        stmt = select(User).where(User.email == email)
        return self.session.scalar(stmt)
    
    def get_all(self) -> List[User]:
        """Obtiene todos los usuarios."""
        stmt = select(User).order_by(User.name)
        return list(self.session.scalars(stmt))
    
    def save(self, user: User) -> User:
        """Guarda usuario."""
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def delete(self, user: User):
        """Elimina usuario."""
        self.session.delete(user)
        self.session.commit()


def ejemplo_14_repository(engine):
    """Usar Repository pattern."""
    print("\n=== Ejemplo 14: Repository Pattern ===\n")
    
    with Session(engine) as session:
        repo = UserRepository(session)
        
        # Obtener todos
        users = repo.get_all()
        print(f"Total usuarios: {len(users)}")
        
        # Obtener por email
        alice = repo.get_by_email('alice@example.com')
        if alice:
            print(f"Usuario encontrado: {alice.name}")
        
        # Crear usuario
        new_user = User(name='Repository Test', email='repo@test.com', age=40)
        saved_user = repo.save(new_user)
        print(f"✓ Usuario guardado con ID: {saved_user.id}")


# =============================================================================
# Ejemplo 15: Refresh y Expire
# =============================================================================

def ejemplo_15_refresh_expire(engine):
    """Refresh y expire de objetos."""
    print("\n=== Ejemplo 15: Refresh y Expire ===\n")
    
    with Session(engine) as session:
        # Crear usuario
        user = User(name='RefreshUser', email='refresh@test.com', age=25)
        session.add(user)
        session.commit()
        
        print(f"Usuario creado: edad={user.age}")
        
        # Modificar directamente en DB (simulado con otra session)
        with Session(engine) as other_session:
            stmt = select(User).where(User.email == 'refresh@test.com')
            other_user = other_session.scalar(stmt)
            if other_user:
                other_user.age = 26
                other_session.commit()
        
        # user todavía tiene edad=25 (cacheado)
        print(f"Usuario antes de refresh: edad={user.age}")
        
        # Refresh para obtener cambios de DB
        session.refresh(user)
        print(f"Usuario después de refresh: edad={user.age}")


# =============================================================================
# Función Principal
# =============================================================================

def main():
    """Ejecuta todos los ejemplos."""
    print("=" * 70)
    print("SQLAlchemy ORM - Object-Relational Mapping")
    print("=" * 70)
    
    # Crear engine
    engine = ejemplo_01_modelo_basico()
    
    # CRUD básico
    ejemplo_02_crud_basico(engine)
    ejemplo_03_bulk_insert(engine)
    ejemplo_04_query_api(engine)
    
    # Relaciones
    ejemplo_05_one_to_many(engine)
    ejemplo_06_loading_strategies(engine)
    ejemplo_07_many_to_many(engine)
    ejemplo_08_one_to_one(engine)
    ejemplo_09_cascade(engine)
    
    # Queries avanzadas
    ejemplo_10_filtering(engine)
    ejemplo_11_joins_orm(engine)
    ejemplo_12_aggregations_orm(engine)
    
    # Patrones
    ejemplo_13_session_factory(engine)
    ejemplo_14_repository(engine)
    ejemplo_15_refresh_expire(engine)
    
    # Cleanup
    engine.dispose()
    
    print("\n" + "=" * 70)
    print("✓ Todos los ejemplos completados")
    print("=" * 70)


if __name__ == "__main__":
    main()
