"""
Módulo 8.5 - MongoDB con Motor (Async Driver)

MongoDB es una base de datos NoSQL orientada a documentos. Motor es el driver
oficial asyncio para acceder a MongoDB desde Python.

Temas:
- Conceptos NoSQL vs SQL
- Conexión a MongoDB
- CRUD operations async
- Consultas y filtros
- Agregaciones
- Índices
- Validación de esquemas

Nota: Requiere MongoDB corriendo localmente o MongoDB Atlas (cloud)
      Docker: docker run -d -p 27017:27017 mongo
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any, Optional
from datetime import datetime
from pprint import pprint
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Ejemplo 1: Conceptos NoSQL vs SQL
# =============================================================================

def ejemplo_01_conceptos():
    """Conceptos fundamentales de MongoDB."""
    print("=== Ejemplo 1: MongoDB Concepts ===\n")
    
    comparacion = '''
SQL (Relacional)          MongoDB (NoSQL)
──────────────────────────────────────────────────
Database                  Database
Table                     Collection
Row                       Document (BSON/JSON)
Column                    Field
Primary Key               _id (automático)
Foreign Key               Referencia o embedding
JOIN                      $lookup o datos embebidos
Schema fijo               Schema flexible

Ejemplo documento MongoDB:
{
    "_id": ObjectId("507f1f77bcf86cd799439011"),
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "age": 30,
    "address": {                    # ← Documento embebido
        "street": "123 Main St",
        "city": "NYC"
    },
    "orders": [                     # ← Array de documentos
        {"id": 1, "total": 99.99},
        {"id": 2, "total": 50.00}
    ],
    "created_at": ISODate("2024-04-16T10:00:00Z")
}

Ventajas MongoDB:
  ✓ Schema flexible (campos variables por documento)
  ✓ Escalabilidad horizontal (sharding)
  ✓ Documentos nested (sin JOINs)
  ✓ Arrays nativos
  ✓ Performance en reads

Desventajas:
  ✗ No ACID completo multi-documento (hasta v4.0)
  ✗ Duplicación de datos común
  ✗ Queries complejos menos expresivos que SQL
  ✗ Mayor uso de espacio
'''
    
    print(comparacion)


# =============================================================================
# Ejemplo 2: Conexión async con Motor
# =============================================================================

async def get_database():
    """Obtener conexión a MongoDB."""
    # Connection string
    MONGO_URL = "mongodb://localhost:27017"
    
    # Cliente async
    client = AsyncIOMotorClient(MONGO_URL)
    
    # Seleccionar database
    db = client.test_database
    
    logger.info("✓ Conectado a MongoDB")
    
    return client, db


async def ejemplo_02_conexion():
    """Conectar a MongoDB."""
    print("\n=== Ejemplo 2: Conexión ===\n")
    
    try:
        client, db = await get_database()
        
        # Verificar conexión
        await client.admin.command('ping')
        print("✓ Conexión exitosa a MongoDB")
        
        # Listar bases de datos
        db_list = await client.list_database_names()
        print(f"Bases de datos: {db_list}")
        
        # Listar colecciones
        collections = await db.list_collection_names()
        print(f"Colecciones en test_database: {collections}")
        
        return client, db
    
    except Exception as e:
        print(f"✗ Error de conexión: {e}")
        print("\n💡 Asegúrate de que MongoDB está corriendo:")
        print("   Docker: docker run -d -p 27017:27017 mongo")
        print("   macOS: brew services start mongodb-community")
        print("   Linux: sudo systemctl start mongod")
        return None, None


# =============================================================================
# Ejemplo 3: INSERT - Insertar Documentos
# =============================================================================

async def ejemplo_03_insert(db):
    """Insertar documentos."""
    print("\n=== Ejemplo 3: INSERT ===\n")
    
    if not db:
        return
    
    collection = db.users
    
    # Insertar un documento
    user = {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "age": 30,
        "created_at": datetime.now()
    }
    
    result = await collection.insert_one(user)
    print(f"✓ Usuario insertado, _id: {result.inserted_id}")
    
    # Insertar múltiples documentos
    users = [
        {"name": "Bob Smith", "email": "bob@example.com", "age": 25},
        {"name": "Carol White", "email": "carol@example.com", "age": 35},
        {"name": "David Brown", "email": "david@example.com", "age": 28}
    ]
    
    result = await collection.insert_many(users)
    print(f"✓ {len(result.inserted_ids)} usuarios insertados")
    print(f"  IDs: {result.inserted_ids}")


# =============================================================================
# Ejemplo 4: FIND - Consultar Documentos
# =============================================================================

async def ejemplo_04_find(db):
    """Consultar documentos."""
    print("\n=== Ejemplo 4: FIND ===\n")
    
    if not db:
        return
    
    collection = db.users
    
    # Find all
    print("Todos los usuarios:")
    cursor = collection.find()
    async for user in cursor:
        print(f"  {user['name']}: {user.get('age', 'N/A')} años")
    
    # Find with filter
    print("\nUsuarios mayores de 28:")
    cursor = collection.find({"age": {"$gt": 28}})
    async for user in cursor:
        print(f"  {user['name']}: {user['age']} años")
    
    # Find one
    user = await collection.find_one({"email": "alice@example.com"})
    print(f"\nUsuario encontrado: {user['name']}")
    
    # Find with projection (select columns)
    print("\nSolo nombres y emails:")
    cursor = collection.find({}, {"name": 1, "email": 1, "_id": 0})
    async for user in cursor:
        print(f"  {user['name']}: {user['email']}")
    
    # Find with sort and limit
    print("\nTop 2 usuarios más viejos:")
    cursor = collection.find().sort("age", -1).limit(2)
    async for user in cursor:
        print(f"  {user['name']}: {user['age']} años")


# =============================================================================
# Ejemplo 5: Operadores de Consulta
# =============================================================================

async def ejemplo_05_query_operators(db):
    """Operadores de consulta MongoDB."""
    print("\n=== Ejemplo 5: Query Operators ===\n")
    
    if not db:
        return
    
    collection = db.users
    
    # $gt, $gte, $lt, $lte, $ne
    count = await collection.count_documents({"age": {"$gte": 25, "$lt": 35}})
    print(f"Usuarios entre 25 y 34 años: {count}")
    
    # $in
    cursor = collection.find({"name": {"$in": ["Alice Johnson", "Bob Smith"]}})
    print("\nUsuarios específicos:")
    async for user in cursor:
        print(f"  {user['name']}")
    
    # $regex (pattern matching)
    cursor = collection.find({"name": {"$regex": "^A", "$options": "i"}})
    print("\nNombres que empiezan con A:")
    async for user in cursor:
        print(f"  {user['name']}")
    
    # $and, $or
    cursor = collection.find({
        "$and": [
            {"age": {"$gte": 25}},
            {"name": {"$regex": "Smith|White"}}
        ]
    })
    print("\nUsuarios >= 25 y apellido Smith/White:")
    async for user in cursor:
        print(f"  {user['name']}: {user['age']}")
    
    # $exists
    count = await collection.count_documents({"age": {"$exists": True}})
    print(f"\nUsuarios con campo 'age': {count}")


# =============================================================================
# Ejemplo 6: UPDATE - Actualizar Documentos
# =============================================================================

async def ejemplo_06_update(db):
    """Actualizar documentos."""
    print("\n=== Ejemplo 6: UPDATE ===\n")
    
    if not db:
        return
    
    collection = db.users
    
    # Update one
    result = await collection.update_one(
        {"email": "alice@example.com"},  # Filter
        {"$set": {"age": 31}}             # Update
    )
    print(f"✓ {result.modified_count} documento actualizado")
    
    # Update many
    result = await collection.update_many(
        {"age": {"$lt": 30}},
        {"$inc": {"age": 1}}  # Incrementar edad
    )
    print(f"✓ {result.modified_count} documentos actualizados")
    
    # Replace one
    result = await collection.replace_one(
        {"email": "bob@example.com"},
        {
            "name": "Robert Smith",
            "email": "bob@example.com",
            "age": 26,
            "updated": True
        }
    )
    print(f"✓ {result.modified_count} documento reemplazado")
    
    # Upsert (insert si no existe)
    result = await collection.update_one(
        {"email": "new@example.com"},
        {"$set": {"name": "New User", "age": 20}},
        upsert=True
    )
    if result.upserted_id:
        print(f"✓ Nuevo documento insertado (upsert): {result.upserted_id}")


# =============================================================================
# Ejemplo 7: Operadores de Update
# =============================================================================

async def ejemplo_07_update_operators(db):
    """Operadores de actualización."""
    print("\n=== Ejemplo 7: Update Operators ===\n")
    
    if not db:
        return
    
    collection = db.users
    
    # $set - establecer campo
    await collection.update_one(
        {"email": "alice@example.com"},
        {"$set": {"website": "https://alice.dev"}}
    )
    print("✓ $set: Campo agregado/actualizado")
    
    # $unset - eliminar campo
    await collection.update_one(
        {"email": "alice@example.com"},
        {"$unset": {"website": ""}}
    )
    print("✓ $unset: Campo eliminado")
    
    # $inc - incrementar
    await collection.update_one(
        {"email": "alice@example.com"},
        {"$inc": {"age": 1}}
    )
    print("✓ $inc: Edad incrementada")
    
    # $push - agregar a array
    await collection.update_one(
        {"email": "alice@example.com"},
        {"$push": {"orders": {"id": 1, "total": 99.99}}}
    )
    print("✓ $push: Elemento agregado a array")
    
    # $pull - remover de array
    await collection.update_one(
        {"email": "alice@example.com"},
        {"$pull": {"orders": {"id": 1}}}
    )
    print("✓ $pull: Elemento removido de array")
    
    # $addToSet - agregar único a array
    await collection.update_one(
        {"email": "alice@example.com"},
        {"$addToSet": {"tags": "python"}}
    )
    print("✓ $addToSet: Tag agregado (solo si no existe)")


# =============================================================================
# Ejemplo 8: DELETE - Eliminar Documentos
# =============================================================================

async def ejemplo_08_delete(db):
    """Eliminar documentos."""
    print("\n=== Ejemplo 8: DELETE ===\n")
    
    if not db:
        return
    
    collection = db.users
    
    # Count before
    count_before = await collection.count_documents({})
    print(f"Documentos antes: {count_before}")
    
    # Delete one
    result = await collection.delete_one({"email": "new@example.com"})
    print(f"✓ {result.deleted_count} documento eliminado")
    
    # Delete many
    result = await collection.delete_many({"age": {"$lt": 25}})
    print(f"✓ {result.deleted_count} documentos eliminados")
    
    # Count after
    count_after = await collection.count_documents({})
    print(f"Documentos después: {count_after}")


# =============================================================================
# Ejemplo 9: Documentos Embebidos
# =============================================================================

async def ejemplo_09_embedded(db):
    """Documentos embebidos."""
    print("\n=== Ejemplo 9: Documentos Embebidos ===\n")
    
    if not db:
        return
    
    collection = db.users
    
    # Insertar con documento embebido
    user = {
        "name": "Eve Martinez",
        "email": "eve@example.com",
        "address": {
            "street": "123 Main St",
            "city": "NYC",
            "zip": "10001"
        },
        "orders": [
            {"id": 1, "total": 99.99, "status": "completed"},
            {"id": 2, "total": 50.00, "status": "pending"}
        ]
    }
    
    await collection.insert_one(user)
    print("✓ Usuario con documentos embebidos insertado")
    
    # Consultar por campo embebido (dot notation)
    eve = await collection.find_one({"address.city": "NYC"})
    print(f"\nUsuario en NYC: {eve['name']}")
    print(f"  Dirección: {eve['address']['street']}, {eve['address']['city']}")
    
    # Actualizar campo embebido
    await collection.update_one(
        {"email": "eve@example.com"},
        {"$set": {"address.zip": "10002"}}
    )
    print("✓ Código postal actualizado")
    
    # Consultar array
    user = await collection.find_one({"orders.status": "pending"})
    if user:
        print(f"\nUsuario con órdenes pendientes: {user['name']}")


# =============================================================================
# Ejemplo 10: Agregaciones
# =============================================================================

async def ejemplo_10_aggregation(db):
    """Pipeline de agregación."""
    print("\n=== Ejemplo 10: Agregaciones ===\n")
    
    if not db:
        return
    
    collection = db.users
    
    # Agregación simple: contar por edad
    pipeline = [
        {"$group": {
            "_id": "$age",
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    
    print("Usuarios por edad:")
    async for result in collection.aggregate(pipeline):
        print(f"  Edad {result['_id']}: {result['count']} usuarios")
    
    # Agregación con match y project
    pipeline = [
        {"$match": {"age": {"$gte": 30}}},
        {"$project": {
            "name": 1,
            "email": 1,
            "age": 1,
            "_id": 0
        }},
        {"$sort": {"age": -1}}
    ]
    
    print("\nUsuarios >= 30 años:")
    async for user in collection.aggregate(pipeline):
        print(f"  {user['name']}: {user['age']} años")
    
    # Estadísticas
    pipeline = [
        {"$group": {
            "_id": None,
            "avg_age": {"$avg": "$age"},
            "min_age": {"$min": "$age"},
            "max_age": {"$max": "$age"},
            "total": {"$sum": 1}
        }}
    ]
    
    async for stats in collection.aggregate(pipeline):
        print(f"\nEstadísticas:")
        print(f"  Total usuarios: {stats['total']}")
        print(f"  Edad promedio: {stats['avg_age']:.1f}")
        print(f"  Edad mínima: {stats['min_age']}")
        print(f"  Edad máxima: {stats['max_age']}")


# =============================================================================
# Ejemplo 11: Índices
# =============================================================================

async def ejemplo_11_indices(db):
    """Crear y usar índices."""
    print("\n=== Ejemplo 11: Índices ===\n")
    
    if not db:
        return
    
    collection = db.users
    
    # Crear índice simple
    await collection.create_index("email", unique=True)
    print("✓ Índice creado en 'email' (unique)")
    
    # Crear índice compuesto
    await collection.create_index([("age", 1), ("name", 1)])
    print("✓ Índice compuesto creado en 'age' + 'name'")
    
    # Listar índices
    indices = await collection.list_indexes().to_list()
    print("\nÍndices en colección:")
    for index in indices:
        print(f"  {index['name']}: {index['key']}")
    
    # Crear índice de texto (para búsqueda full-text)
    await collection.create_index([("name", "text")])
    print("\n✓ Índice de texto creado en 'name'")
    
    # Buscar con índice de texto
    cursor = collection.find({"$text": {"$search": "Alice"}})
    print("\nBúsqueda de texto 'Alice':")
    async for user in cursor:
        print(f"  {user['name']}")


# =============================================================================
# Ejemplo 12: Validación de Schema
# =============================================================================

async def ejemplo_12_validation(db):
    """Validación de schema."""
    print("\n=== Ejemplo 12: Schema Validation ===\n")
    
    if not db:
        return
    
    # Crear colección con validación
    try:
        await db.create_collection("products", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["name", "price"],
                "properties": {
                    "name": {
                        "bsonType": "string",
                        "description": "Debe ser string y es obligatorio"
                    },
                    "price": {
                        "bsonType": "double",
                        "minimum": 0,
                        "description": "Debe ser número >= 0"
                    },
                    "category": {
                        "enum": ["electronics", "clothing", "food"],
                        "description": "Debe ser una categoría válida"
                    }
                }
            }
        })
        
        print("✓ Colección 'products' creada con validación")
        
        collection = db.products
        
        # Insertar válido
        await collection.insert_one({
            "name": "Laptop",
            "price": 999.99,
            "category": "electronics"
        })
        print("✓ Producto válido insertado")
        
        # Intentar insertar inválido
        try:
            await collection.insert_one({
                "name": "Invalid Product",
                "price": -10  # Precio negativo!
            })
        except Exception as e:
            print(f"✗ Validación falló: Document failed validation")
    
    except Exception as e:
        if "already exists" in str(e):
            print("⚠️  Colección 'products' ya existe")


# =============================================================================
# Ejemplo 13: Transacciones (MongoDB 4.0+)
# =============================================================================

async def ejemplo_13_transacciones(client, db):
    """Transacciones multi-documento."""
    print("\n=== Ejemplo 13: Transacciones ===\n")
    
    if not client:
        return
    
    try:
        # Iniciar sesión
        async with await client.start_session() as session:
            # Iniciar transacción
            async with session.start_transaction():
                collection = db.accounts
                
                # Operación 1: Debitar cuenta A
                await collection.update_one(
                    {"account": "A"},
                    {"$inc": {"balance": -100}},
                    session=session
                )
                
                # Operación 2: Acreditar cuenta B
                await collection.update_one(
                    {"account": "B"},
                    {"$inc": {"balance": 100}},
                    session=session
                )
                
                # Commit automático al salir del with
                print("✓ Transacción completada")
    
    except Exception as e:
        print(f"✗ Error en transacción: {e}")
        print("  (Transacciones requieren replica set)")


# =============================================================================
# Función Principal
# =============================================================================

async def main():
    """Ejecuta todos los ejemplos."""
    print("=" * 70)
    print("MongoDB con Motor - Async Driver")
    print("=" * 70)
    
    # Explicar conceptos
    ejemplo_01_conceptos()
    
    # Conectar
    client, db = await ejemplo_02_conexion()
    
    if db:
        # Limpiar colección
        await db.users.drop()
        
        # CRUD
        await ejemplo_03_insert(db)
        await ejemplo_04_find(db)
        await ejemplo_05_query_operators(db)
        await ejemplo_06_update(db)
        await ejemplo_07_update_operators(db)
        await ejemplo_08_delete(db)
        
        # Avanzado
        await ejemplo_09_embedded(db)
        await ejemplo_10_aggregation(db)
        await ejemplo_11_indices(db)
        await ejemplo_12_validation(db)
        await ejemplo_13_transacciones(client, db)
        
        # Cerrar conexión
        client.close()
        print("\n✓ Conexión cerrada")
    
    print("\n" + "=" * 70)
    print("✓ Ejemplos completados")
    print("\n💡 Para más información:")
    print("   - MongoDB Docs: https://docs.mongodb.com/")
    print("   - Motor Docs: https://motor.readthedocs.io/")
    print("=" * 70)


if __name__ == "__main__":
    # Ejecutar async main
    asyncio.run(main())
