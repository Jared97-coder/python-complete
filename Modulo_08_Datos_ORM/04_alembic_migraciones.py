"""
Módulo 8.4 - Alembic (Migraciones de Base de Datos)

Alembic es el sistema de migraciones oficial de SQLAlchemy, permite gestionar
cambios en el schema de la base de datos de forma versionada y reversible.

Temas:
- Inicialización de proyecto Alembic
- Auto-generación de migraciones
- Upgrade y downgrade
- Migraciones de datos
- Branching y merging
- Best practices

Nota: Este archivo es educativo. Para usar Alembic en un proyecto real,
      se ejecutan comandos CLI (alembic init, revision, upgrade, etc.)
"""

from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from pathlib import Path
import sys


# =============================================================================
# Ejemplo 1: Estructura de Proyecto Alembic
# =============================================================================

def ejemplo_01_estructura_alembic():
    """Explicar estructura de proyecto Alembic."""
    print("=== Ejemplo 1: Estructura de Proyecto Alembic ===\n")
    
    estructura = '''
proyecto/
├── alembic/                    # Directorio de Alembic
│   ├── versions/               # Migraciones (archivos de revisión)
│   │   ├── 001_create_users.py
│   │   ├── 002_add_orders.py
│   │   └── 003_add_profile_table.py
│   ├── env.py                  # Configuración del entorno
│   ├── script.py.mako          # Template para nuevas migraciones
│   └── README
├── alembic.ini                 # Configuración de Alembic
├── models.py                   # Modelos de SQLAlchemy
└── main.py                     # Aplicación
'''
    
    print(estructura)
    
    print("\nArchivos clave:")
    print("  - alembic.ini: Configuración (connection string, rutas)")
    print("  - env.py: Importa modelos y configura MetaData")
    print("  - versions/: Archivos de migración versionados")


# =============================================================================
# Ejemplo 2: Comandos CLI de Alembic
# =============================================================================

def ejemplo_02_comandos_cli():
    """Comandos esenciales de Alembic."""
    print("\n=== Ejemplo 2: Comandos CLI ===\n")
    
    comandos = {
        "Inicialización": [
            ("alembic init alembic", "Inicializar Alembic en proyecto"),
        ],
        "Crear Migraciones": [
            ("alembic revision -m 'descripción'", "Crear migración vacía manual"),
            ("alembic revision --autogenerate -m 'descripción'", "Auto-generar migración"),
        ],
        "Aplicar Migraciones": [
            ("alembic upgrade head", "Aplicar todas las migraciones"),
            ("alembic upgrade +1", "Aplicar siguiente migración"),
            ("alembic upgrade abc123", "Aplicar hasta revisión específica"),
        ],
        "Revertir Migraciones": [
            ("alembic downgrade -1", "Revertir última migración"),
            ("alembic downgrade base", "Revertir todas las migraciones"),
            ("alembic downgrade abc123", "Revertir hasta revisión específica"),
        ],
        "Información": [
            ("alembic current", "Mostrar revisión actual"),
            ("alembic history", "Mostrar historial de migraciones"),
            ("alembic show abc123", "Mostrar detalles de revisión"),
        ],
        "Avanzado": [
            ("alembic upgrade head --sql", "Generar SQL sin ejecutar"),
            ("alembic stamp head", "Marcar DB como actualizada sin ejecutar"),
        ]
    }
    
    for categoria, cmds in comandos.items():
        print(f"\n{categoria}:")
        for cmd, desc in cmds:
            print(f"  $ {cmd}")
            print(f"    → {desc}")


# =============================================================================
# Ejemplo 3: alembic.ini - Configuración
# =============================================================================

def ejemplo_03_alembic_ini():
    """Contenido de alembic.ini."""
    print("\n=== Ejemplo 3: alembic.ini ===\n")
    
    config = '''
# alembic.ini

[alembic]
# Path al directorio de Alembic
script_location = alembic

# Connection string de la base de datos
# SQLite
sqlalchemy.url = sqlite:///database.db

# PostgreSQL
# sqlalchemy.url = postgresql://user:pass@localhost/dbname

# SQL Server
# sqlalchemy.url = mssql+pyodbc://user:pass@server/db?driver=ODBC+Driver+17

# MySQL
# sqlalchemy.url = mysql+pymysql://user:pass@localhost/dbname


# Logging
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
'''
    
    print(config)
    
    print("\n💡 Tip: Puedes usar variables de entorno:")
    print("   sqlalchemy.url = ${DATABASE_URL}")


# =============================================================================
# Ejemplo 4: env.py - Configuración del Entorno
# =============================================================================

def ejemplo_04_env_py():
    """Configuración de env.py."""
    print("\n=== Ejemplo 4: env.py (Configuración) ===\n")
    
    env_py = '''
# alembic/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Importar tus modelos aquí
from myapp.models import Base  # ← IMPORTANTE!

# Configuración de Alembic
config = context.config

# Configurar logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de tus modelos
target_metadata = Base.metadata  # ← Usar metadata de tus modelos


def run_migrations_offline():
    """Migraciones en modo 'offline' (generar SQL)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Migraciones en modo 'online' (conectar a DB)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''
    
    print(env_py)
    
    print("\n⚠️  IMPORTANTE: Debes importar tus modelos en env.py")
    print("   para que Alembic pueda detectar cambios automáticamente.")


# =============================================================================
# Ejemplo 5: Archivo de Migración - Estructura
# =============================================================================

def ejemplo_05_estructura_migracion():
    """Estructura de archivo de migración."""
    print("\n=== Ejemplo 5: Archivo de Migración ===\n")
    
    migracion = '''
# alembic/versions/001_create_users_table.py

"""create users table

Revision ID: abc123def456
Revises: 
Create Date: 2024-04-16 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# Identificadores de revisión
revision = 'abc123def456'       # ID de esta revisión (único)
down_revision = None            # Revisión anterior (None si es primera)
branch_labels = None
depends_on = None


def upgrade():
    """Aplicar cambios (migración hacia adelante)."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Crear índice
    op.create_index('ix_users_email', 'users', ['email'])


def downgrade():
    """Revertir cambios (migración hacia atrás)."""
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
'''
    
    print(migracion)
    
    print("\nOperaciones disponibles en op.*:")
    print("  - create_table() / drop_table()")
    print("  - add_column() / drop_column()")
    print("  - alter_column()")
    print("  - create_index() / drop_index()")
    print("  - create_foreign_key() / drop_constraint()")
    print("  - execute() - SQL arbitrario")


# =============================================================================
# Ejemplo 6: Operaciones Comunes en Migraciones
# =============================================================================

def ejemplo_06_operaciones_comunes():
    """Operaciones comunes en migraciones."""
    print("\n=== Ejemplo 6: Operaciones Comunes ===\n")
    
    operaciones = '''
=== AGREGAR COLUMNA ===

def upgrade():
    op.add_column('users', 
        sa.Column('phone', sa.String(20), nullable=True)
    )

def downgrade():
    op.drop_column('users', 'phone')


=== MODIFICAR COLUMNA ===

def upgrade():
    op.alter_column('users', 'email',
        existing_type=sa.String(100),
        type_=sa.String(200),  # Nuevo tipo
        nullable=False  # Cambiar a NOT NULL
    )

def downgrade():
    op.alter_column('users', 'email',
        existing_type=sa.String(200),
        type_=sa.String(100),
        nullable=True
    )


=== RENOMBRAR COLUMNA ===

def upgrade():
    op.alter_column('users', 'name',
        new_column_name='full_name'
    )

def downgrade():
    op.alter_column('users', 'full_name',
        new_column_name='name'
    )


=== AGREGAR FOREIGN KEY ===

def upgrade():
    op.create_foreign_key(
        'fk_orders_user_id',  # Nombre de FK
        'orders',             # Tabla origen
        'users',              # Tabla referenciada
        ['user_id'],          # Columna origen
        ['id']                # Columna referenciada
    )

def downgrade():
    op.drop_constraint('fk_orders_user_id', 'orders')


=== CREAR ÍNDICE ===

def upgrade():
    op.create_index('ix_users_age', 'users', ['age'])

def downgrade():
    op.drop_index('ix_users_age')


=== EJECUTAR SQL ARBITRARIO ===

def upgrade():
    op.execute("""
        UPDATE users
        SET status = 'active'
        WHERE created_at > '2024-01-01'
    """)

def downgrade():
    # Puede no ser reversible
    pass
'''
    
    print(operaciones)


# =============================================================================
# Ejemplo 7: Migración de Datos
# =============================================================================

def ejemplo_07_migracion_datos():
    """Migración de datos (no solo schema)."""
    print("\n=== Ejemplo 7: Migración de Datos ===\n")
    
    data_migration = '''
"""add default roles

Revision ID: 003_add_roles
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


def upgrade():
    # 1. Crear tabla roles
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 2. Insertar datos iniciales
    roles_table = table('roles',
        column('name', sa.String)
    )
    
    op.bulk_insert(roles_table, [
        {'name': 'admin'},
        {'name': 'user'},
        {'name': 'guest'}
    ])
    
    # 3. Agregar columna role_id a users
    op.add_column('users', 
        sa.Column('role_id', sa.Integer(), nullable=True)
    )
    
    # 4. Migrar datos: asignar role 'user' por defecto
    op.execute("""
        UPDATE users
        SET role_id = (SELECT id FROM roles WHERE name = 'user')
        WHERE role_id IS NULL
    """)
    
    # 5. Hacer columna NOT NULL ahora que tiene datos
    op.alter_column('users', 'role_id', nullable=False)
    
    # 6. Agregar FK
    op.create_foreign_key(
        'fk_users_role_id',
        'users', 'roles',
        ['role_id'], ['id']
    )


def downgrade():
    op.drop_constraint('fk_users_role_id', 'users')
    op.drop_column('users', 'role_id')
    op.drop_table('roles')
'''
    
    print(data_migration)
    
    print("\n💡 Tips para migraciones de datos:")
    print("   - Siempre llenar datos antes de hacer columnas NOT NULL")
    print("   - Usar op.execute() para UPDATE/DELETE complejos")
    print("   - Considerar batching para grandes volúmenes")


# =============================================================================
# Ejemplo 8: Autogenerate - Detectar Cambios
# =============================================================================

def ejemplo_08_autogenerate():
    """Cómo usar autogenerate."""
    print("\n=== Ejemplo 8: Autogenerate ===\n")
    
    print("Flujo de trabajo con autogenerate:\n")
    
    pasos = '''
1. Modificar tus modelos en models.py
   
   class User(Base):
       ...
       # Agregar nueva columna
       phone = Column(String(20))

2. Generar migración automáticamente
   
   $ alembic revision --autogenerate -m "add phone to users"
   
   Alembic detecta:
   - Nuevas tablas
   - Columnas agregadas/eliminadas
   - Cambios de tipo de datos
   - Índices nuevos
   
3. REVISAR archivo generado
   
   ⚠️  IMPORTANTE: siempre revisar el archivo generado
   Alembic puede NO detectar:
   - Cambios en nombres de columnas (las ve como drop + add)
   - Cambios en restricciones CHECK
   - Algunos cambios de tipos
   
4. Editar si es necesario
   
   def upgrade():
       # Alembic generó:
       # op.drop_column('users', 'name')
       # op.add_column('users', sa.Column('full_name', ...))
       
       # Mejor usar rename:
       op.alter_column('users', 'name', new_column_name='full_name')

5. Aplicar migración
   
   $ alembic upgrade head
'''
    
    print(pasos)


# =============================================================================
# Ejemplo 9: Branches y Merging
# =============================================================================

def ejemplo_09_branches():
    """Branches en migraciones."""
    print("\n=== Ejemplo 9: Branches y Merging ===\n")
    
    print("Escenario: Dos desarrolladores crean migraciones en paralelo\n")
    
    scenario = '''
Estado inicial:
  base -> 001 -> 002

Developer A crea:
  002 -> 003a (add column)

Developer B crea:
  002 -> 003b (add table)

Problema: Dos "heads" (003a y 003b)

Solución: Merge
  $ alembic merge -m "merge branches" 003a 003b
  
Resultado:
  003a \\
        -> 004 (merge)
  003b /

Aplicar merge:
  $ alembic upgrade head
'''
    
    print(scenario)
    
    print("\nComandos útiles:")
    print("  $ alembic heads          # Ver múltiples heads")
    print("  $ alembic merge 003a 003b  # Mergear branches")


# =============================================================================
# Ejemplo 10: Best Practices
# =============================================================================

def ejemplo_10_best_practices():
    """Best practices para Alembic."""
    print("\n=== Ejemplo 10: Best Practices ===\n")
    
    practices = '''
1. ✓ SIEMPRE revisar migraciones autogeneradas
   - Alembic puede generar código incorrecto
   - Verificar upgrade() y downgrade()

2. ✓ Escribir downgrade() completo
   - Debe revertir TODOS los cambios de upgrade()
   - Si no es reversible, documentarlo

3. ✓ Testear migraciones antes de aplicar
   $ alembic upgrade head --sql > migration.sql
   # Revisar SQL generado
   
4. ✓ Usar transacciones cuando sea posible
   - SQLite: transaccional por defecto
   - PostgreSQL: usar batch_alter_table para DDL transaccional

5. ✓ Nombres descriptivos para migraciones
   ✗ "changes"
   ✓ "add_user_profile_table"

6. ✓ No modificar migraciones ya aplicadas
   - Una vez en producción, NO editar
   - Crear nueva migración para correcciones

7. ✓ Mantener migraciones pequeñas y atómicas
   - Una migración = un cambio lógico
   - Más fácil de revertir y debuggear

8. ✓ Backup antes de migrar producción
   $ pg_dump mydb > backup.sql
   $ alembic upgrade head

9. ✓ Versionar alembic/ en git
   - Incluir alembic.ini (sin credenciales)
   - Incluir todas las versiones
   - No incluir __pycache__

10. ✓ Usar environment variables para connection strings
    sqlalchemy.url = ${DATABASE_URL}
    
    O programáticamente en env.py:
    config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))
'''
    
    print(practices)


# =============================================================================
# Ejemplo 11: Troubleshooting
# =============================================================================

def ejemplo_11_troubleshooting():
    """Resolución de problemas comunes."""
    print("\n=== Ejemplo 11: Troubleshooting ===\n")
    
    problemas = '''
=== PROBLEMA: "Target database is not up to date" ===
Causa: DB tiene migraciones que no están en código

Solución:
  $ alembic current  # Ver revisión en DB
  $ alembic history  # Ver todas las revisiones
  
  Si DB está adelantada:
  $ alembic downgrade <revision>
  
  Si código está adelantado:
  $ alembic upgrade head


=== PROBLEMA: "Can't locate revision identified by 'abc123'" ===
Causa: Falta archivo de migración o revision ID incorrecto

Solución:
  1. Verificar que archivo existe en alembic/versions/
  2. Verificar que revision ID coincide con nombre de archivo
  3. Si falta: recuperar de git o regenerar


=== PROBLEMA: Autogenerate no detecta cambios ===
Causa: Modelos no importados en env.py

Solución:
  # En alembic/env.py
  from myapp.models import Base  # ← Asegurarse de importar
  target_metadata = Base.metadata


=== PROBLEMA: Error en migración aplicada ===
Causa: Migración falló parcialmente

Solución:
  1. Revisar estado de DB (qué se aplicó)
  2. Corregir manualmente si es necesario
  3. Stamp a revisión correcta:
     $ alembic stamp <revision>
  4. Intentar upgrade nuevamente


=== PROBLEMA: Multiple heads ===
Causa: Desarrollo paralelo sin merge

Solución:
  $ alembic heads  # Ver heads
  $ alembic merge -m "merge" head1 head2
  $ alembic upgrade head
'''
    
    print(problemas)


# =============================================================================
# Ejemplo 12: Alembic Programático
# =============================================================================

def ejemplo_12_programatico():
    """Usar Alembic programáticamente."""
    print("\n=== Ejemplo 12: Uso Programático ===\n")
    
    code = '''
from alembic import command
from alembic.config import Config

# Configurar Alembic
alembic_cfg = Config("alembic.ini")

# Crear migración
command.revision(
    alembic_cfg,
    message="add new table",
    autogenerate=True
)

# Aplicar migraciones
command.upgrade(alembic_cfg, "head")

# Revertir
command.downgrade(alembic_cfg, "-1")

# Ver historial
from alembic.script import ScriptDirectory

script = ScriptDirectory.from_config(alembic_cfg)
for revision in script.walk_revisions():
    print(f"{revision.revision}: {revision.doc}")
'''
    
    print(code)


# =============================================================================
# Función Principal
# =============================================================================

def main():
    """Ejecuta todos los ejemplos."""
    print("=" * 70)
    print("Alembic - Sistema de Migraciones de SQLAlchemy")
    print("=" * 70)
    
    ejemplo_01_estructura_alembic()
    ejemplo_02_comandos_cli()
    ejemplo_03_alembic_ini()
    ejemplo_04_env_py()
    ejemplo_05_estructura_migracion()
    ejemplo_06_operaciones_comunes()
    ejemplo_07_migracion_datos()
    ejemplo_08_autogenerate()
    ejemplo_09_branches()
    ejemplo_10_best_practices()
    ejemplo_11_troubleshooting()
    ejemplo_12_programatico()
    
    print("\n" + "=" * 70)
    print("✓ Guía de Alembic completada")
    print("\nPróximos pasos:")
    print("  1. Inicializar Alembic en tu proyecto: alembic init alembic")
    print("  2. Configurar connection string en alembic.ini")
    print("  3. Importar modelos en alembic/env.py")
    print("  4. Crear primera migración: alembic revision --autogenerate -m 'initial'")
    print("  5. Aplicar: alembic upgrade head")
    print("=" * 70)


if __name__ == "__main__":
    main()
