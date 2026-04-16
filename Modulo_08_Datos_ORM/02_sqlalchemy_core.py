"""
Módulo 8.2 - SQLAlchemy Core (Expression Language)

SQLAlchemy Core proporciona un SQL Expression Language que permite construir
queries SQL de forma programática, con type checking y abstracción de diferentes
dialectos SQL.

Temas:
- Engine y conexiones
- MetaData y Table definition
- Insert, Select, Update, Delete
- Joins y subqueries
- Transactions
- Connection pooling
"""

from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Float, DateTime, ForeignKey, Text,
    select, insert, update, delete, func, and_, or_, not_
)
from sqlalchemy.pool import StaticPool
from datetime import datetime
from typing import List, Dict, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Ejemplo 1: Crear Engine y Conexión
# =============================================================================

def ejemplo_01_engine():
    """Crear engine de SQLAlchemy."""
    print("=== Ejemplo 1: Engine y Conexión ===\n")
    
    # Engine para SQLite en memoria
    engine = create_engine(
        'sqlite:///:memory:',
        echo=True,  # Mostrar SQL generado
        poolclass=StaticPool  # Pool para in-memory
    )
    
    print(f"✓ Engine creado: {engine.url}")
    print(f"  Dialect: {engine.dialect.name}")
    print(f"  Driver: {engine.driver}")
    
    # Obtener conexión
    with engine.connect() as conn:
        result = conn.execute(select(func.now()))  # type: ignore
        print(f"  Timestamp: {result.scalar()}")
    
    return engine


# =============================================================================
# Ejemplo 2: Definir Tablas con MetaData
# =============================================================================

def ejemplo_02_metadata():
    """Definir schema con MetaData y Table."""
    print("\n=== Ejemplo 2: MetaData y Tables ===\n")
    
    # MetaData contenedor de schema
    metadata = MetaData()
    
    # Definir tabla users
    users = Table(
        'users',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(50), nullable=False),
        Column('email', String(100), unique=True, nullable=False),
        Column('age', Integer),
        Column('created_at', DateTime, default=datetime.now)
    )
    
    # Definir tabla orders
    orders = Table(
        'orders',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
        Column('total', Float, nullable=False),
        Column('status', String(20), default='pending'),
        Column('created_at', DateTime, default=datetime.now)
    )
    
    print(f"✓ Tablas definidas: {list(metadata.tables.keys())}")
    
    return metadata, users, orders


# =============================================================================
# Ejemplo 3: Crear Tablas
# =============================================================================

def ejemplo_03_crear_tablas(engine, metadata):
    """Crear tablas en la base de datos."""
    print("\n=== Ejemplo 3: Crear Tablas ===\n")
    
    # Crear todas las tablas
    metadata.create_all(engine)
    
    print("✓ Tablas creadas en la base de datos")
    
    # Verificar tablas existentes
    with engine.connect() as conn:
        result = conn.execute(select(func.count()).select_from(metadata.tables['users']))  # type: ignore
        print(f"  Registros en users: {result.scalar()}")


# =============================================================================
# Ejemplo 4: INSERT - Insertar Datos
# =============================================================================

def ejemplo_04_insert(engine, users):
    """Insertar datos en tabla."""
    print("\n=== Ejemplo 4: INSERT ===\n")
    
    with engine.connect() as conn:
        # Insertar un registro
        stmt = insert(users).values(
            name='Alice Johnson',
            email='alice@example.com',
            age=30
        )
        
        result = conn.execute(stmt)
        conn.commit()
        
        print(f"✓ Usuario insertado con ID: {result.inserted_primary_key[0]}")
        
        # Insertar múltiples registros
        stmt = insert(users)
        users_data = [
            {'name': 'Bob Smith', 'email': 'bob@example.com', 'age': 25},
            {'name': 'Carol White', 'email': 'carol@example.com', 'age': 35},
            {'name': 'David Brown', 'email': 'david@example.com', 'age': 28}
        ]
        
        result = conn.execute(stmt, users_data)
        conn.commit()
        
        print(f"✓ {result.rowcount} usuarios insertados")


# =============================================================================
# Ejemplo 5: SELECT - Consultar Datos
# =============================================================================

def ejemplo_05_select(engine, users):
    """Consultar datos con SELECT."""
    print("\n=== Ejemplo 5: SELECT ===\n")
    
    with engine.connect() as conn:
        # SELECT simple
        stmt = select(users)
        result = conn.execute(stmt)
        
        print("Todos los usuarios:")
        for row in result:
            print(f"  {row.id}: {row.name} ({row.email}), {row.age} años")
        
        # SELECT con WHERE
        stmt = select(users).where(users.c.age > 28)
        result = conn.execute(stmt)
        
        print("\nUsuarios mayores de 28:")
        for row in result:
            print(f"  {row.name}: {row.age} años")
        
        # SELECT con ORDER BY y LIMIT
        stmt = select(users).order_by(users.c.age.desc()).limit(2)
        result = conn.execute(stmt)
        
        print("\nTop 2 usuarios más viejos:")
        for row in result:
            print(f"  {row.name}: {row.age} años")


# =============================================================================
# Ejemplo 6: Operadores WHERE Avanzados
# =============================================================================

def ejemplo_06_where_operators(engine, users):
    """Operadores para cláusulas WHERE."""
    print("\n=== Ejemplo 6: WHERE Operators ===\n")
    
    with engine.connect() as conn:
        # AND
        stmt = select(users).where(
            and_(
                users.c.age >= 25,
                users.c.age <= 30
            )
        )
        result = conn.execute(stmt)
        print("Usuarios entre 25 y 30 años:")
        for row in result:
            print(f"  {row.name}: {row.age}")
        
        # OR
        stmt = select(users).where(
            or_(
                users.c.name.like('A%'),
                users.c.name.like('D%')
            )
        )
        result = conn.execute(stmt)
        print("\nUsuarios que empiezan con A o D:")
        for row in result:
            print(f"  {row.name}")
        
        # IN
        stmt = select(users).where(users.c.name.in_(['Alice Johnson', 'Bob Smith']))
        result = conn.execute(stmt)
        print("\nUsuarios específicos:")
        for row in result:
            print(f"  {row.name}")
        
        # NOT
        stmt = select(users).where(not_(users.c.age > 30))
        result = conn.execute(stmt)
        print("\nUsuarios <= 30 años:")
        for row in result:
            print(f"  {row.name}: {row.age}")


# =============================================================================
# Ejemplo 7: UPDATE - Actualizar Datos
# =============================================================================

def ejemplo_07_update(engine, users):
    """Actualizar registros."""
    print("\n=== Ejemplo 7: UPDATE ===\n")
    
    with engine.connect() as conn:
        # UPDATE simple
        stmt = update(users).where(
            users.c.name == 'Alice Johnson'
        ).values(age=31, email='alice.johnson@example.com')
        
        result = conn.execute(stmt)
        conn.commit()
        
        print(f"✓ {result.rowcount} registro(s) actualizado(s)")
        
        # UPDATE con expresión
        stmt = update(users).where(
            users.c.age < 30
        ).values(age=users.c.age + 1)
        
        result = conn.execute(stmt)
        conn.commit()
        
        print(f"✓ {result.rowcount} usuario(s) cumplieron años")
        
        # Verificar cambios
        stmt = select(users).where(users.c.name == 'Alice Johnson')
        result = conn.execute(stmt)
        alice = result.first()
        print(f"\nAlice ahora: {alice.age} años, {alice.email}")


# =============================================================================
# Ejemplo 8: DELETE - Eliminar Datos
# =============================================================================

def ejemplo_08_delete(engine, users):
    """Eliminar registros."""
    print("\n=== Ejemplo 8: DELETE ===\n")
    
    with engine.connect() as conn:
        # Contar antes
        stmt = select(func.count()).select_from(users)
        count_before = conn.execute(stmt).scalar()
        print(f"Usuarios antes: {count_before}")
        
        # DELETE
        stmt = delete(users).where(users.c.name == 'David Brown')
        result = conn.execute(stmt)
        conn.commit()
        
        print(f"✓ {result.rowcount} usuario(s) eliminado(s)")
        
        # Contar después
        count_after = conn.execute(select(func.count()).select_from(users)).scalar()
        print(f"Usuarios después: {count_after}")


# =============================================================================
# Ejemplo 9: SELECT con Columnas Específicas
# =============================================================================

def ejemplo_09_select_columns(engine, users):
    """SELECT columnas específicas."""
    print("\n=== Ejemplo 9: SELECT Columnas Específicas ===\n")
    
    with engine.connect() as conn:
        # SELECT columnas específicas
        stmt = select(users.c.name, users.c.age)
        result = conn.execute(stmt)
        
        print("Nombres y edades:")
        for row in result:
            print(f"  {row.name}: {row.age} años")
        
        # SELECT con alias
        stmt = select(
            users.c.name.label('nombre'),
            users.c.email.label('correo')
        )
        result = conn.execute(stmt)
        
        print("\nCon alias:")
        for row in result:
            print(f"  {row.nombre} -> {row.correo}")


# =============================================================================
# Ejemplo 10: Funciones de Agregación
# =============================================================================

def ejemplo_10_agregaciones(engine, users, orders):
    """Funciones de agregación (COUNT, SUM, AVG, etc.)."""
    print("\n=== Ejemplo 10: Agregaciones ===\n")
    
    with engine.connect() as conn:
        # Insertar órdenes para demo
        orders_data = [
            {'user_id': 1, 'total': 99.99, 'status': 'completed'},
            {'user_id': 1, 'total': 50.00, 'status': 'completed'},
            {'user_id': 2, 'total': 75.50, 'status': 'completed'},
            {'user_id': 2, 'total': 30.00, 'status': 'pending'},
        ]
        conn.execute(insert(orders), orders_data)
        conn.commit()
        
        # Agregaciones
        stmt = select(
            func.count(orders.c.id).label('total_orders'),
            func.sum(orders.c.total).label('revenue'),
            func.avg(orders.c.total).label('avg_order'),
            func.min(orders.c.total).label('min_order'),
            func.max(orders.c.total).label('max_order')
        ).where(orders.c.status == 'completed')
        
        result = conn.execute(stmt).first()
        
        print("Estadísticas de órdenes completadas:")
        print(f"  Total órdenes: {result.total_orders}")
        print(f"  Revenue: ${result.revenue:.2f}")
        print(f"  Promedio: ${result.avg_order:.2f}")
        print(f"  Mínimo: ${result.min_order:.2f}")
        print(f"  Máximo: ${result.max_order:.2f}")


# =============================================================================
# Ejemplo 11: GROUP BY y HAVING
# =============================================================================

def ejemplo_11_group_by(engine, users, orders):
    """GROUP BY y HAVING."""
    print("\n=== Ejemplo 11: GROUP BY y HAVING ===\n")
    
    with engine.connect() as conn:
        # GROUP BY
        stmt = select(
            users.c.name,
            func.count(orders.c.id).label('order_count'),
            func.coalesce(func.sum(orders.c.total), 0).label('total_spent')
        ).select_from(
            users.join(orders, users.c.id == orders.c.user_id, isouter=True)
        ).group_by(users.c.id).order_by(func.sum(orders.c.total).desc())
        
        result = conn.execute(stmt)
        
        print("Gasto por usuario:")
        for row in result:
            print(f"  {row.name}: {row.order_count} órdenes, ${row.total_spent:.2f}")
        
        # HAVING
        stmt = select(
            users.c.name,
            func.count(orders.c.id).label('order_count')
        ).select_from(
            users.join(orders, users.c.id == orders.c.user_id)
        ).group_by(users.c.id).having(func.count(orders.c.id) > 1)
        
        result = conn.execute(stmt)
        
        print("\nUsuarios con más de 1 orden:")
        for row in result:
            print(f"  {row.name}: {row.order_count} órdenes")


# =============================================================================
# Ejemplo 12: JOINs
# =============================================================================

def ejemplo_12_joins(engine, users, orders):
    """Diferentes tipos de JOIN."""
    print("\n=== Ejemplo 12: JOINs ===\n")
    
    with engine.connect() as conn:
        # INNER JOIN
        stmt = select(
            users.c.name,
            orders.c.id.label('order_id'),
            orders.c.total,
            orders.c.status
        ).select_from(
            users.join(orders, users.c.id == orders.c.user_id)
        )
        
        result = conn.execute(stmt)
        
        print("INNER JOIN (usuarios con órdenes):")
        for row in result:
            print(f"  {row.name} - Orden #{row.order_id}: ${row.total} ({row.status})")
        
        # LEFT OUTER JOIN
        stmt = select(
            users.c.name,
            func.count(orders.c.id).label('order_count')
        ).select_from(
            users.join(orders, users.c.id == orders.c.user_id, isouter=True)
        ).group_by(users.c.id)
        
        result = conn.execute(stmt)
        
        print("\nLEFT JOIN (todos los usuarios):")
        for row in result:
            print(f"  {row.name}: {row.order_count} órdenes")


# =============================================================================
# Ejemplo 13: Subqueries
# =============================================================================

def ejemplo_13_subqueries(engine, users, orders):
    """Subqueries (subconsultas)."""
    print("\n=== Ejemplo 13: Subqueries ===\n")
    
    with engine.connect() as conn:
        # Subquery: usuarios con órdenes > 50
        subq = select(orders.c.user_id).where(
            orders.c.total > 50
        ).distinct().subquery()
        
        stmt = select(users).where(users.c.id.in_(select(subq)))
        
        result = conn.execute(stmt)
        
        print("Usuarios con órdenes > $50:")
        for row in result:
            print(f"  {row.name}")
        
        # Subquery con agregación
        avg_subq = select(
            func.avg(orders.c.total)
        ).scalar_subquery()
        
        stmt = select(
            users.c.name,
            orders.c.total
        ).select_from(
            users.join(orders, users.c.id == orders.c.user_id)
        ).where(orders.c.total > avg_subq)
        
        result = conn.execute(stmt)
        
        print("\nÓrdenes sobre el promedio:")
        for row in result:
            print(f"  {row.name}: ${row.total}")


# =============================================================================
# Ejemplo 14: Transacciones
# =============================================================================

def ejemplo_14_transacciones(engine, users):
    """Manejo de transacciones."""
    print("\n=== Ejemplo 14: Transacciones ===\n")
    
    # Transacción exitosa
    with engine.begin() as conn:
        stmt = insert(users).values(
            name='Eve Martinez',
            email='eve@example.com',
            age=27
        )
        result = conn.execute(stmt)
        print(f"✓ Usuario insertado (transacción auto-commit)")
    
    # Transacción con rollback
    try:
        with engine.begin() as conn:
            stmt = insert(users).values(
                name='Frank Wilson',
                email='frank@example.com',
                age=29
            )
            conn.execute(stmt)
            print("✓ Usuario Frank insertado")
            
            # Simular error (email duplicado)
            stmt = insert(users).values(
                name='Grace Lee',
                email='alice@example.com',  # Email duplicado!
                age=32
            )
            conn.execute(stmt)
    
    except Exception as e:
        print(f"✗ Error: {e}")
        print("✓ Transacción revertida (rollback automático)")


# =============================================================================
# Ejemplo 15: Connection vs Engine.begin()
# =============================================================================

def ejemplo_15_connection_patterns(engine, users):
    """Patrones de uso de conexiones."""
    print("\n=== Ejemplo 15: Connection Patterns ===\n")
    
    # Patrón 1: Connect + manual commit
    with engine.connect() as conn:
        conn.execute(insert(users).values(
            name='Helen Davis',
            email='helen@example.com',
            age=29
        ))
        conn.commit()  # Manual commit
        print("✓ Patrón 1: Manual commit")
    
    # Patrón 2: Begin + auto commit/rollback
    with engine.begin() as conn:
        conn.execute(insert(users).values(
            name='Ivan Garcia',
            email='ivan@example.com',
            age=33
        ))
        # Auto commit al salir del with
        print("✓ Patrón 2: Auto commit")


# =============================================================================
# Ejemplo 16: Batch Operations
# =============================================================================

def ejemplo_16_batch(engine, users):
    """Operaciones por lote (batch)."""
    print("\n=== Ejemplo 16: Batch Operations ===\n")
    
    import time
    
    # Preparar datos
    batch_data = [
        {'name': f'User{i}', 'email': f'user{i}@example.com', 'age': 20 + i}
        for i in range(100)
    ]
    
    with engine.begin() as conn:
        start = time.time()
        
        # Insertar en batch
        conn.execute(insert(users), batch_data)
        
        elapsed = time.time() - start
        
        print(f"✓ {len(batch_data)} usuarios insertados en {elapsed:.3f}s")
        
        # Verificar
        result = conn.execute(select(func.count()).select_from(users))
        total = result.scalar()
        print(f"  Total usuarios en DB: {total}")


# =============================================================================
# Ejemplo 17: Execute Many
# =============================================================================

def ejemplo_17_executemany(engine, orders):
    """executemany para múltiples inserts."""
    print("\n=== Ejemplo 17: Execute Many ===\n")
    
    with engine.begin() as conn:
        # Preparar datos
        orders_data = [
            {'user_id': i % 5 + 1, 'total': 10.0 * i, 'status': 'completed'}
            for i in range(1, 51)
        ]
        
        # Insert many
        result = conn.execute(insert(orders), orders_data)
        
        print(f"✓ {len(orders_data)} órdenes insertadas")
        print(f"  Filas afectadas: {result.rowcount}")


# =============================================================================
# Ejemplo 18: Text SQL (Raw SQL)
# =============================================================================

def ejemplo_18_text_sql(engine):
    """Ejecutar SQL raw con text()."""
    print("\n=== Ejemplo 18: Text SQL ===\n")
    
    from sqlalchemy import text
    
    with engine.connect() as conn:
        # SQL raw
        result = conn.execute(text(
            "SELECT name, age FROM users WHERE age > :age ORDER BY age DESC"
        ), {"age": 30})
        
        print("Usuarios mayores de 30 (raw SQL):")
        for row in result:
            print(f"  {row.name}: {row.age}")
        
        # Commit si es DML
        conn.execute(text(
            "UPDATE users SET age = :new_age WHERE name = :name"
        ), {"new_age": 34, "name": "Carol White"})
        conn.commit()
        
        print("✓ Usuario actualizado con raw SQL")


# =============================================================================
# Ejemplo 19: Inspecionar Engine
# =============================================================================

def ejemplo_19_inspect(engine, metadata):
    """Inspeccionar engine y schema."""
    print("\n=== Ejemplo 19: Inspect Engine ===\n")
    
    from sqlalchemy import inspect
    
    inspector = inspect(engine)
    
    # Listar tablas
    tables = inspector.get_table_names()
    print(f"Tablas: {tables}")
    
    # Inspeccionar columnas
    for table_name in tables:
        columns = inspector.get_columns(table_name)
        print(f"\n{table_name}:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']} {'NOT NULL' if not col['nullable'] else ''}")
    
    # Foreign keys
    fks = inspector.get_foreign_keys('orders')
    print(f"\nForeign keys en 'orders':")
    for fk in fks:
        print(f"  {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")


# =============================================================================
# Función Principal
# =============================================================================

def main():
    """Ejecuta todos los ejemplos."""
    print("=" * 70)
    print("SQLAlchemy Core - SQL Expression Language")
    print("=" * 70)
    
    # Crear engine (SQLite en memoria, pero sin echo para menos output)
    engine = create_engine('sqlite:///:memory:', poolclass=StaticPool)
    
    # Definir schema
    metadata, users, orders = ejemplo_02_metadata()
    
    # Crear tablas
    ejemplo_03_crear_tablas(engine, metadata)
    
    # Ejecutar ejemplos CRUD
    ejemplo_04_insert(engine, users)
    ejemplo_05_select(engine, users)
    ejemplo_06_where_operators(engine, users)
    ejemplo_07_update(engine, users)
    ejemplo_08_delete(engine, users)
    ejemplo_09_select_columns(engine, users)
    
    # Ejemplos avanzados
    ejemplo_10_agregaciones(engine, users, orders)
    ejemplo_11_group_by(engine, users, orders)
    ejemplo_12_joins(engine, users, orders)
    ejemplo_13_subqueries(engine, users, orders)
    
    # Transacciones y patrones
    ejemplo_14_transacciones(engine, users)
    ejemplo_15_connection_patterns(engine, users)
    
    # Performance
    ejemplo_16_batch(engine, users)
    ejemplo_17_executemany(engine, orders)
    
    # Utilidades
    ejemplo_18_text_sql(engine)
    ejemplo_19_inspect(engine, metadata)
    
    # Cerrar engine
    engine.dispose()
    
    print("\n" + "=" * 70)
    print("✓ Todos los ejemplos completados")
    print("=" * 70)


if __name__ == "__main__":
    main()
