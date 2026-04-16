"""
Módulo 8.1 - SQLite y Fundamentos de Bases de Datos

SQLite es una base de datos embebida que no requiere servidor.
Es ideal para desarrollo, testing, aplicaciones móviles y casos de uso ligeros.

Temas:
- Conexiones y cursores
- CRUD operations
- Transacciones y rollback
- Context managers
- Tipos de datos SQLite
- Índices y optimización
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import contextmanager


# =============================================================================
# Ejemplo 1: Conexión Básica y Creación de Tabla
# =============================================================================

def ejemplo_01_conexion_basica():
    """Conectar a SQLite y crear tabla."""
    print("=== Ejemplo 1: Conexión y Creación de Tabla ===\n")
    
    # Conectar (crea archivo si no existe)
    conn = sqlite3.connect('ejemplo.db')
    
    # Crear cursor para ejecutar SQL
    cursor = conn.cursor()
    
    # Crear tabla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Confirmar cambios
    conn.commit()
    
    print("✓ Tabla 'users' creada")
    
    # Cerrar conexión
    conn.close()


# =============================================================================
# Ejemplo 2: Insertar Datos (INSERT)
# =============================================================================

def ejemplo_02_insert():
    """Insertar registros en la base de datos."""
    print("\n=== Ejemplo 2: Insertar Datos ===\n")
    
    conn = sqlite3.connect('ejemplo.db')
    cursor = conn.cursor()
    
    # Insertar un registro
    cursor.execute('''
        INSERT INTO users (name, email, age)
        VALUES (?, ?, ?)
    ''', ('Alice Johnson', 'alice@example.com', 30))
    
    print(f"✓ Usuario insertado con ID: {cursor.lastrowid}")
    
    # Insertar múltiples registros
    users_data = [
        ('Bob Smith', 'bob@example.com', 25),
        ('Carol White', 'carol@example.com', 35),
        ('David Brown', 'david@example.com', 28)
    ]
    
    cursor.executemany('''
        INSERT INTO users (name, email, age)
        VALUES (?, ?, ?)
    ''', users_data)
    
    print(f"✓ {cursor.rowcount} usuarios insertados")
    
    conn.commit()
    conn.close()


# =============================================================================
# Ejemplo 3: Consultar Datos (SELECT)
# =============================================================================

def ejemplo_03_select():
    """Consultar registros."""
    print("\n=== Ejemplo 3: Consultar Datos ===\n")
    
    conn = sqlite3.connect('ejemplo.db')
    
    # Row factory para acceder por nombre de columna
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Seleccionar todos los usuarios
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    
    print("Todos los usuarios:")
    for user in users:
        print(f"  {user['id']}: {user['name']} ({user['email']}), {user['age']} años")
    
    # Seleccionar con WHERE
    cursor.execute('SELECT * FROM users WHERE age > ?', (28,))
    older_users = cursor.fetchall()
    
    print(f"\nUsuarios mayores de 28 años: {len(older_users)}")
    for user in older_users:
        print(f"  - {user['name']}: {user['age']} años")
    
    # Seleccionar un solo registro
    cursor.execute('SELECT * FROM users WHERE email = ?', ('alice@example.com',))
    alice = cursor.fetchone()
    
    if alice:
        print(f"\nUsuario encontrado: {alice['name']}")
    
    conn.close()


# =============================================================================
# Ejemplo 4: Actualizar Datos (UPDATE)
# =============================================================================

def ejemplo_04_update():
    """Actualizar registros existentes."""
    print("\n=== Ejemplo 4: Actualizar Datos ===\n")
    
    conn = sqlite3.connect('ejemplo.db')
    cursor = conn.cursor()
    
    # Actualizar un usuario
    cursor.execute('''
        UPDATE users
        SET age = ?, email = ?
        WHERE name = ?
    ''', (31, 'alice.johnson@example.com', 'Alice Johnson'))
    
    print(f"✓ {cursor.rowcount} registro(s) actualizado(s)")
    
    # Actualizar múltiples usuarios
    cursor.execute('''
        UPDATE users
        SET age = age + 1
        WHERE age < 30
    ''')
    
    print(f"✓ {cursor.rowcount} usuario(s) cumplieron años")
    
    conn.commit()
    conn.close()


# =============================================================================
# Ejemplo 5: Eliminar Datos (DELETE)
# =============================================================================

def ejemplo_05_delete():
    """Eliminar registros."""
    print("\n=== Ejemplo 5: Eliminar Datos ===\n")
    
    conn = sqlite3.connect('ejemplo.db')
    cursor = conn.cursor()
    
    # Contar registros antes
    cursor.execute('SELECT COUNT(*) FROM users')
    count_before = cursor.fetchone()[0]
    print(f"Usuarios antes: {count_before}")
    
    # Eliminar usuario específico
    cursor.execute('DELETE FROM users WHERE name = ?', ('David Brown',))
    print(f"✓ {cursor.rowcount} usuario(s) eliminado(s)")
    
    # Contar registros después
    cursor.execute('SELECT COUNT(*) FROM users')
    count_after = cursor.fetchone()[0]
    print(f"Usuarios después: {count_after}")
    
    conn.commit()
    conn.close()


# =============================================================================
# Ejemplo 6: Transacciones y Rollback
# =============================================================================

def ejemplo_06_transacciones():
    """Manejo de transacciones."""
    print("\n=== Ejemplo 6: Transacciones ===\n")
    
    conn = sqlite3.connect('ejemplo.db')
    cursor = conn.cursor()
    
    try:
        # Iniciar transacción (implícita)
        cursor.execute('''
            INSERT INTO users (name, email, age)
            VALUES (?, ?, ?)
        ''', ('Eve Martinez', 'eve@example.com', 27))
        
        print("✓ Usuario Eve insertado")
        
        # Simular error
        cursor.execute('''
            INSERT INTO users (name, email, age)
            VALUES (?, ?, ?)
        ''', ('Frank Wilson', 'alice@example.com', 29))  # Email duplicado!
        
        # Si llegamos aquí, confirmar
        conn.commit()
        print("✓ Transacción confirmada")
    
    except sqlite3.IntegrityError as e:
        # Revertir si hay error
        conn.rollback()
        print(f"✗ Error de integridad: {e}")
        print("✓ Transacción revertida (rollback)")
    
    finally:
        conn.close()


# =============================================================================
# Ejemplo 7: Context Manager (Automático)
# =============================================================================

def ejemplo_07_context_manager():
    """Usar context manager para gestión automática."""
    print("\n=== Ejemplo 7: Context Manager ===\n")
    
    # Context manager gestiona commit/rollback automáticamente
    with sqlite3.connect('ejemplo.db') as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (name, email, age)
                VALUES (?, ?, ?)
            ''', ('Grace Lee', 'grace@example.com', 32))
            
            print("✓ Usuario Grace insertado")
            # Commit automático al salir del with si no hay excepciones
        
        except sqlite3.IntegrityError as e:
            print(f"✗ Error: {e}")
            # Rollback automático si hay excepción


# =============================================================================
# Ejemplo 8: Custom Context Manager
# =============================================================================

@contextmanager
def get_db_connection(db_path: str = 'ejemplo.db'):
    """Context manager personalizado para conexiones."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def ejemplo_08_custom_context():
    """Usar context manager personalizado."""
    print("\n=== Ejemplo 8: Context Manager Personalizado ===\n")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM users')
        result = cursor.fetchone()
        print(f"Total de usuarios: {result['count']}")


# =============================================================================
# Ejemplo 9: Tipos de Datos SQLite
# =============================================================================

def ejemplo_09_tipos_datos():
    """Tipos de datos en SQLite."""
    print("\n=== Ejemplo 9: Tipos de Datos ===\n")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Crear tabla con diferentes tipos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_types (
                id INTEGER PRIMARY KEY,
                text_col TEXT,
                integer_col INTEGER,
                real_col REAL,
                blob_col BLOB,
                null_col NULL
            )
        ''')
        
        # Insertar datos
        cursor.execute('''
            INSERT INTO data_types (text_col, integer_col, real_col, blob_col, null_col)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Hello', 42, 3.14, b'binary data', None))
        
        # Leer datos
        cursor.execute('SELECT * FROM data_types')
        row = cursor.fetchone()
        
        print("Tipos de datos SQLite:")
        print(f"  TEXT: {row['text_col']} (type: {type(row['text_col']).__name__})")
        print(f"  INTEGER: {row['integer_col']} (type: {type(row['integer_col']).__name__})")
        print(f"  REAL: {row['real_col']} (type: {type(row['real_col']).__name__})")
        print(f"  BLOB: {row['blob_col']} (type: {type(row['blob_col']).__name__})")
        print(f"  NULL: {row['null_col']} (type: {type(row['null_col']).__name__})")


# =============================================================================
# Ejemplo 10: Fechas y Timestamps
# =============================================================================

def ejemplo_10_fechas():
    """Trabajar con fechas y timestamps."""
    print("\n=== Ejemplo 10: Fechas y Timestamps ===\n")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # SQLite no tiene tipo DATE, usa TEXT/INTEGER/REAL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                name TEXT,
                event_date TEXT,  -- ISO 8601: 'YYYY-MM-DD HH:MM:SS'
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertar con fecha actual
        now = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO events (name, event_date)
            VALUES (?, ?)
        ''', ('Meeting', now))
        
        # Consultar con funciones de fecha
        cursor.execute('''
            SELECT 
                name,
                event_date,
                date(event_date) as date_only,
                time(event_date) as time_only,
                datetime(event_date, '+1 day') as tomorrow
            FROM events
        ''')
        
        event = cursor.fetchone()
        print(f"Evento: {event['name']}")
        print(f"  Fecha completa: {event['event_date']}")
        print(f"  Solo fecha: {event['date_only']}")
        print(f"  Solo hora: {event['time_only']}")
        print(f"  Mañana: {event['tomorrow']}")


# =============================================================================
# Ejemplo 11: Índices para Optimización
# =============================================================================

def ejemplo_11_indices():
    """Crear índices para mejorar rendimiento."""
    print("\n=== Ejemplo 11: Índices ===\n")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Crear índice en columna email
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_users_email
            ON users(email)
        ''')
        
        # Índice compuesto
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_users_age_name
            ON users(age, name)
        ''')
        
        print("✓ Índices creados")
        
        # Ver índices existentes
        cursor.execute('''
            SELECT name, sql
            FROM sqlite_master
            WHERE type = 'index' AND tbl_name = 'users'
        ''')
        
        print("\nÍndices en tabla 'users':")
        for index in cursor.fetchall():
            print(f"  - {index['name']}")


# =============================================================================
# Ejemplo 12: EXPLAIN QUERY PLAN
# =============================================================================

def ejemplo_12_explain():
    """Analizar plan de ejecución de queries."""
    print("\n=== Ejemplo 12: EXPLAIN QUERY PLAN ===\n")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Query sin índice
        cursor.execute('''
            EXPLAIN QUERY PLAN
            SELECT * FROM users WHERE age = 30
        ''')
        
        print("Plan para query sin índice (age):")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[3]}")
        
        # Query con índice
        cursor.execute('''
            EXPLAIN QUERY PLAN
            SELECT * FROM users WHERE email = 'alice@example.com'
        ''')
        
        print("\nPlan para query con índice (email):")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[3]}")


# =============================================================================
# Ejemplo 13: Foreign Keys
# =============================================================================

def ejemplo_13_foreign_keys():
    """Relaciones con foreign keys."""
    print("\n=== Ejemplo 13: Foreign Keys ===\n")
    
    with get_db_connection() as conn:
        # Habilitar foreign keys (deshabilitadas por defecto en SQLite)
        conn.execute('PRAGMA foreign_keys = ON')
        
        cursor = conn.cursor()
        
        # Crear tabla orders con FK
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                total REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users(id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )
        ''')
        
        # Insertar orden
        cursor.execute('''
            INSERT INTO orders (user_id, total, status)
            VALUES (?, ?, ?)
        ''', (1, 99.99, 'completed'))
        
        print("✓ Orden creada con foreign key")
        
        # Consultar con JOIN
        cursor.execute('''
            SELECT 
                users.name,
                orders.id as order_id,
                orders.total,
                orders.status
            FROM orders
            JOIN users ON orders.user_id = users.id
        ''')
        
        print("\nÓrdenes con usuarios:")
        for row in cursor.fetchall():
            print(f"  Orden #{row['order_id']}: {row['name']} - ${row['total']} ({row['status']})")


# =============================================================================
# Ejemplo 14: Agregaciones y GROUP BY
# =============================================================================

def ejemplo_14_agregaciones():
    """Funciones de agregación."""
    print("\n=== Ejemplo 14: Agregaciones ===\n")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Insertar más órdenes para demo
        orders_data = [
            (1, 50.00, 'completed'),
            (2, 75.50, 'completed'),
            (2, 30.00, 'pending'),
            (3, 120.00, 'completed')
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO orders (user_id, total, status)
            VALUES (?, ?, ?)
        ''', orders_data)
        
        # Agregaciones
        cursor.execute('''
            SELECT 
                COUNT(*) as total_orders,
                SUM(total) as revenue,
                AVG(total) as avg_order,
                MIN(total) as min_order,
                MAX(total) as max_order
            FROM orders
            WHERE status = 'completed'
        ''')
        
        stats = cursor.fetchone()
        print("Estadísticas de órdenes completadas:")
        print(f"  Total órdenes: {stats['total_orders']}")
        print(f"  Revenue total: ${stats['revenue']:.2f}")
        print(f"  Promedio: ${stats['avg_order']:.2f}")
        print(f"  Mínimo: ${stats['min_order']:.2f}")
        print(f"  Máximo: ${stats['max_order']:.2f}")
        
        # GROUP BY
        cursor.execute('''
            SELECT 
                users.name,
                COUNT(orders.id) as order_count,
                COALESCE(SUM(orders.total), 0) as total_spent
            FROM users
            LEFT JOIN orders ON users.id = orders.user_id
            GROUP BY users.id
            HAVING order_count > 0
            ORDER BY total_spent DESC
        ''')
        
        print("\nGasto por usuario:")
        for row in cursor.fetchall():
            print(f"  {row['name']}: {row['order_count']} órdenes, ${row['total_spent']:.2f}")


# =============================================================================
# Ejemplo 15: Clase Database Helper
# =============================================================================

class Database:
    """Helper class para operaciones de base de datos."""
    
    def __init__(self, db_path: str = 'ejemplo.db'):
        self.db_path = db_path
    
    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        """Ejecuta SQL y retorna cursor."""
        with self.get_connection() as conn:
            return conn.execute(sql, params)
    
    def fetchall(self, sql: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Ejecuta query y retorna todos los resultados."""
        with self.get_connection() as conn:
            cursor = conn.execute(sql, params)
            return cursor.fetchall()
    
    def fetchone(self, sql: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """Ejecuta query y retorna un resultado."""
        with self.get_connection() as conn:
            cursor = conn.execute(sql, params)
            return cursor.fetchone()
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexiones."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


def ejemplo_15_database_class():
    """Usar clase helper Database."""
    print("\n=== Ejemplo 15: Database Helper Class ===\n")
    
    db = Database()
    
    # Obtener todos los usuarios
    users = db.fetchall('SELECT * FROM users ORDER BY name')
    print(f"Total usuarios: {len(users)}")
    
    # Obtener un usuario
    user = db.fetchone('SELECT * FROM users WHERE email = ?', ('alice.johnson@example.com',))
    if user:
        print(f"Usuario encontrado: {user['name']}")
    
    # Insertar y obtener ID
    with db.get_connection() as conn:
        cursor = conn.execute('''
            INSERT OR IGNORE INTO users (name, email, age)
            VALUES (?, ?, ?)
        ''', ('Helen Davis', 'helen@example.com', 29))
        print(f"✓ Nuevo usuario ID: {cursor.lastrowid}")


# =============================================================================
# Ejemplo 16: In-Memory Database (Testing)
# =============================================================================

def ejemplo_16_in_memory():
    """Base de datos en memoria para testing."""
    print("\n=== Ejemplo 16: In-Memory Database ===\n")
    
    # Usar :memory: para BD en memoria (muy rápido)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Crear schema
    cursor.execute('''
        CREATE TABLE test_users (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')
    
    # Insertar datos de prueba
    cursor.executemany(
        'INSERT INTO test_users (name) VALUES (?)',
        [('Test1',), ('Test2',), ('Test3',)]
    )
    
    # Consultar
    cursor.execute('SELECT COUNT(*) FROM test_users')
    count = cursor.fetchone()[0]
    
    print(f"✓ Base de datos en memoria creada con {count} registros")
    print("  (Ideal para unit tests)")
    
    conn.close()
    # BD se destruye al cerrar conexión


# =============================================================================
# Ejemplo 17: Backup de Base de Datos
# =============================================================================

def ejemplo_17_backup():
    """Crear backup de base de datos."""
    print("\n=== Ejemplo 17: Backup ===\n")
    
    source = sqlite3.connect('ejemplo.db')
    backup_path = 'ejemplo_backup.db'
    
    # Crear backup
    with sqlite3.connect(backup_path) as backup:
        source.backup(backup)
    
    source.close()
    
    print(f"✓ Backup creado: {backup_path}")
    
    # Verificar backup
    with sqlite3.connect(backup_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        print(f"  Usuarios en backup: {count}")


# =============================================================================
# Ejemplo 18: Pragma Commands
# =============================================================================

def ejemplo_18_pragma():
    """Comandos PRAGMA para configuración."""
    print("\n=== Ejemplo 18: PRAGMA Commands ===\n")
    
    with sqlite3.connect('ejemplo.db') as conn:
        cursor = conn.cursor()
        
        # Ver información de la base de datos
        cursor.execute('PRAGMA database_list')
        print("Bases de datos:")
        for db in cursor.fetchall():
            print(f"  {db[1]}: {db[2]}")
        
        # Ver tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        print("\nTablas:")
        for table in cursor.fetchall():
            print(f"  - {table[0]}")
        
        # Información de tabla
        cursor.execute('PRAGMA table_info(users)')
        print("\nEstructura de 'users':")
        for col in cursor.fetchall():
            print(f"  {col[1]} {col[2]} {'NOT NULL' if col[3] else ''} {'PK' if col[5] else ''}")
        
        # Configuración
        cursor.execute('PRAGMA foreign_keys')
        fk_enabled = cursor.fetchone()[0]
        print(f"\nForeign keys: {'ON' if fk_enabled else 'OFF'}")


# =============================================================================
# Ejemplo 19: Performance Tips
# =============================================================================

def ejemplo_19_performance():
    """Tips de rendimiento."""
    print("\n=== Ejemplo 19: Performance Tips ===\n")
    
    import time
    
    # 1. Sin transacción (muy lento)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE test (id INTEGER, value TEXT)')
    
    start = time.time()
    for i in range(100):
        cursor.execute('INSERT INTO test VALUES (?, ?)', (i, f'value_{i}'))
        conn.commit()  # Commit cada vez (lento!)
    slow_time = time.time() - start
    
    # 2. Con transacción (rápido)
    cursor.execute('DELETE FROM test')
    start = time.time()
    for i in range(100):
        cursor.execute('INSERT INTO test VALUES (?, ?)', (i, f'value_{i}'))
    conn.commit()  # Un solo commit
    fast_time = time.time() - start
    
    print(f"Sin transacción: {slow_time:.3f}s")
    print(f"Con transacción: {fast_time:.3f}s")
    print(f"Speedup: {slow_time/fast_time:.1f}x más rápido")
    
    conn.close()


# =============================================================================
# Función Principal
# =============================================================================

def main():
    """Ejecuta todos los ejemplos."""
    print("=" * 70)
    print("SQLite - Fundamentos de Bases de Datos")
    print("=" * 70)
    
    # Limpiar base de datos anterior
    db_files = ['ejemplo.db', 'ejemplo_backup.db']
    for db_file in db_files:
        if Path(db_file).exists():
            Path(db_file).unlink()
    
    # Ejecutar ejemplos
    ejemplo_01_conexion_basica()
    ejemplo_02_insert()
    ejemplo_03_select()
    ejemplo_04_update()
    ejemplo_05_delete()
    ejemplo_06_transacciones()
    ejemplo_07_context_manager()
    ejemplo_08_custom_context()
    ejemplo_09_tipos_datos()
    ejemplo_10_fechas()
    ejemplo_11_indices()
    ejemplo_12_explain()
    ejemplo_13_foreign_keys()
    ejemplo_14_agregaciones()
    ejemplo_15_database_class()
    ejemplo_16_in_memory()
    ejemplo_17_backup()
    ejemplo_18_pragma()
    ejemplo_19_performance()
    
    print("\n" + "=" * 70)
    print("✓ Todos los ejemplos completados")
    print("=" * 70)


if __name__ == "__main__":
    main()
