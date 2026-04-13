"""
Módulo 6.2: CSV, JSON y YAML
==============================

Aprende a trabajar con los formatos de datos más comunes:
CSV, JSON y YAML para intercambio y almacenamiento de información.

Temas:
- Lectura y escritura de CSV
- DictReader y DictWriter
- JSON: parseo y serialización
- Custom JSON encoders
- YAML para configuraciones
- Streaming de archivos grandes
"""

import csv
import json
import yaml
from pathlib import Path
from typing import List, Dict, Any, Iterator
from datetime import datetime, date
from decimal import Decimal
from dataclasses import dataclass, asdict
from pydantic import BaseModel


# =============================================================================
# 1. Trabajo con CSV
# =============================================================================

def ejemplo_csv_basico():
    """Lectura y escritura básica de CSV."""
    print("=== CSV Básico ===\n")
    
    archivo_csv = Path("ejemplo.csv")
    
    # Escribir CSV
    with archivo_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "Edad", "Ciudad"])
        writer.writerow(["Ana", 28, "Madrid"])
        writer.writerow(["Juan", 35, "Barcelona"])
        writer.writerow(["María", 22, "Valencia"])
    
    print(f"CSV creado: {archivo_csv}")
    
    # Leer CSV
    print("\nLeyendo CSV:")
    with archivo_csv.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, fila in enumerate(reader):
            print(f"  Fila {i}: {fila}")
    
    # Limpiar
    archivo_csv.unlink()


def ejemplo_csv_dict():
    """Usar DictReader y DictWriter para trabajar con diccionarios."""
    print("\n=== CSV con Diccionarios ===\n")
    
    archivo_csv = Path("usuarios.csv")
    
    # Datos a escribir
    usuarios = [
        {"nombre": "Ana", "email": "ana@ejemplo.com", "edad": 28},
        {"nombre": "Juan", "email": "juan@ejemplo.com", "edad": 35},
        {"nombre": "María", "email": "maria@ejemplo.com", "edad": 22},
    ]
    
    # Escribir con DictWriter
    with archivo_csv.open("w", newline="", encoding="utf-8") as f:
        campos = ["nombre", "email", "edad"]
        writer = csv.DictWriter(f, fieldnames=campos)
        
        writer.writeheader()  # Escribir encabezados
        writer.writerows(usuarios)  # Escribir todas las filas
    
    print(f"CSV escrito: {archivo_csv}")
    
    # Leer con DictReader
    print("\nLeyendo con DictReader:")
    with archivo_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for usuario in reader:
            print(f"  {usuario['nombre']}: {usuario['email']} ({usuario['edad']} años)")
    
    # Limpiar
    archivo_csv.unlink()


def ejemplo_csv_dialectos():
    """Diferentes dialectos de CSV (delimitadores, quotes, etc)."""
    print("\n=== Dialectos CSV ===\n")
    
    # CSV con punto y coma (común en Excel español)
    archivo_csv = Path("datos_semicolon.csv")
    
    datos = [
        ["Producto", "Precio", "Stock"],
        ["Laptop", "1200.50", "15"],
        ["Mouse", "25.99", "50"],
        ["Teclado", "75.00", "30"],
    ]
    
    # Escribir con punto y coma
    with archivo_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerows(datos)
    
    print("CSV con punto y coma creado")
    print(archivo_csv.read_text(encoding="utf-8"))
    
    # Leer con punto y coma
    print("Leyendo:")
    with archivo_csv.open("r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        for fila in reader:
            print(f"  {fila}")
    
    # Limpiar
    archivo_csv.unlink()


def ejemplo_csv_con_validacion():
    """CSV con validación usando Pydantic."""
    print("\n=== CSV con Validación ===\n")
    
    class Usuario(BaseModel):
        """Modelo con validación."""
        nombre: str
        email: str
        edad: int
        
        class Config:
            str_strip_whitespace = True
    
    archivo_csv = Path("usuarios_validar.csv")
    
    # Crear CSV
    with archivo_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nombre", "email", "edad"])
        writer.writeheader()
        writer.writerow({"nombre": "Ana", "email": "ana@ejemplo.com", "edad": 28})
        writer.writerow({"nombre": " Juan ", "email": "juan@ejemplo.com", "edad": 35})
    
    # Leer y validar
    print("Leyendo y validando:")
    usuarios_validos: List[Usuario] = []
    
    with archivo_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                usuario = Usuario(**row)
                usuarios_validos.append(usuario)
                print(f"  ✅ {usuario.nombre}: {usuario.email}")
            except Exception as e:
                print(f"  ❌ Error en fila: {e}")
    
    print(f"\nUsuarios válidos: {len(usuarios_validos)}")
    
    # Limpiar
    archivo_csv.unlink()


# =============================================================================
# 2. Trabajo con JSON
# =============================================================================

def ejemplo_json_basico():
    """Operaciones básicas con JSON."""
    print("\n=== JSON Básico ===\n")
    
    # Datos Python
    datos = {
        "nombre": "Ana García",
        "edad": 28,
        "activo": True,
        "hobbies": ["lectura", "música", "viajes"],
        "direccion": {
            "calle": "Gran Vía 123",
            "ciudad": "Madrid",
            "cp": "28013"
        }
    }
    
    # Python → JSON string
    json_string = json.dumps(datos, indent=2, ensure_ascii=False)
    print("Python → JSON:")
    print(json_string)
    
    # JSON string → Python
    datos_parseados = json.loads(json_string)
    print("\nJSON → Python:")
    print(f"Nombre: {datos_parseados['nombre']}")
    print(f"Ciudad: {datos_parseados['direccion']['ciudad']}")


def ejemplo_json_archivo():
    """Leer y escribir archivos JSON."""
    print("\n=== Archivos JSON ===\n")
    
    archivo_json = Path("datos.json")
    
    # Datos a guardar
    configuracion = {
        "app_name": "Mi Aplicación",
        "version": "1.0.0",
        "debug": True,
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "mi_db"
        },
        "features": ["auth", "api", "admin"]
    }
    
    # Escribir JSON
    with archivo_json.open("w", encoding="utf-8") as f:
        json.dump(configuracion, f, indent=2, ensure_ascii=False)
    
    print(f"JSON escrito: {archivo_json}")
    
    # Leer JSON
    with archivo_json.open("r", encoding="utf-8") as f:
        config_leida = json.load(f)
    
    print("\nConfiguración leída:")
    print(f"  App: {config_leida['app_name']}")
    print(f"  DB: {config_leida['database']['host']}:{config_leida['database']['port']}")
    
    # Forma más simple con Path
    archivo_json.write_text(
        json.dumps(configuracion, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    
    config_leida = json.loads(archivo_json.read_text(encoding="utf-8"))
    
    # Limpiar
    archivo_json.unlink()


class CustomJSONEncoder(json.JSONEncoder):
    """Encoder personalizado para tipos no serializables por defecto."""
    
    def default(self, obj):
        """Serializa tipos personalizados."""
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, set):
            return list(obj)
        # Intenta serializar dataclasses y Pydantic models
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return super().default(obj)


def ejemplo_json_custom_encoder():
    """Serializar tipos personalizados a JSON."""
    print("\n=== JSON Custom Encoder ===\n")
    
    @dataclass
    class Producto:
        """Producto con tipos complejos."""
        id: int
        nombre: str
        precio: Decimal
        fecha_creacion: datetime
        tags: set
    
    # Crear producto
    producto = Producto(
        id=1,
        nombre="Laptop",
        precio=Decimal("1299.99"),
        fecha_creacion=datetime.now(),
        tags={"electrónica", "computadoras", "ofertas"}
    )
    
    # Serializar con encoder custom
    json_string = json.dumps(
        producto,
        cls=CustomJSONEncoder,
        indent=2,
        ensure_ascii=False
    )
    
    print("Producto serializado:")
    print(json_string)
    
    # Parsear de vuelta
    datos = json.loads(json_string)
    print(f"\nProducto parseado:")
    print(f"  Nombre: {datos['nombre']}")
    print(f"  Precio: ${datos['precio']}")
    print(f"  Tags: {datos['tags']}")


class Usuario(BaseModel):
    """Usuario con Pydantic para JSON automático."""
    id: int
    nombre: str
    email: str
    activo: bool = True
    fecha_registro: datetime


def ejemplo_json_pydantic():
    """Serialización/deserialización con Pydantic."""
    print("\n=== JSON con Pydantic ===\n")
    
    # Crear usuario
    usuario = Usuario(
        id=1,
        nombre="Ana García",
        email="ana@ejemplo.com",
        fecha_registro=datetime.now()
    )
    
    # Pydantic → JSON (model_dump_json)
    json_string = usuario.model_dump_json(indent=2)
    print("Usuario → JSON:")
    print(json_string)
    
    # JSON → Pydantic (model_validate_json)
    usuario_parseado = Usuario.model_validate_json(json_string)
    print(f"\nUsuario parseado: {usuario_parseado.nombre}")
    
    # Guardar en archivo
    archivo = Path("usuario.json")
    archivo.write_text(usuario.model_dump_json(indent=2), encoding="utf-8")
    
    # Leer desde archivo
    usuario_desde_archivo = Usuario.model_validate_json(
        archivo.read_text(encoding="utf-8")
    )
    print(f"Usuario desde archivo: {usuario_desde_archivo.email}")
    
    # Limpiar
    archivo.unlink()


# =============================================================================
# 3. Trabajo con YAML
# =============================================================================

def ejemplo_yaml_basico():
    """Operaciones básicas con YAML."""
    print("\n=== YAML Básico ===\n")
    
    # Datos Python
    configuracion = {
        "app": {
            "name": "Mi Aplicación",
            "version": "1.0.0",
            "debug": True
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "credentials": {
                "user": "admin",
                "password": "secreto"
            }
        },
        "features": ["auth", "api", "admin"]
    }
    
    # Python → YAML string
    yaml_string = yaml.dump(
        configuracion,
        default_flow_style=False,
        allow_unicode=True
    )
    
    print("Python → YAML:")
    print(yaml_string)
    
    # YAML string → Python
    datos = yaml.safe_load(yaml_string)
    print("YAML → Python:")
    print(f"App: {datos['app']['name']}")
    print(f"DB: {datos['database']['host']}")


def ejemplo_yaml_archivo():
    """Leer y escribir archivos YAML."""
    print("\n=== Archivos YAML ===\n")
    
    archivo_yaml = Path("config.yaml")
    
    # Configuración compleja
    config = {
        "server": {
            "host": "0.0.0.0",
            "port": 8000,
            "workers": 4
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "handlers": ["console", "file"]
        },
        "database": {
            "engine": "postgresql",
            "pool_size": 10,
            "url": "postgresql://user:pass@localhost/db"
        }
    }
    
    # Escribir YAML
    with archivo_yaml.open("w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    print(f"YAML escrito: {archivo_yaml}")
    print("\nContenido:")
    print(archivo_yaml.read_text(encoding="utf-8"))
    
    # Leer YAML
    with archivo_yaml.open("r", encoding="utf-8") as f:
        config_leida = yaml.safe_load(f)
    
    print("Configuración leída:")
    print(f"  Server: {config_leida['server']['host']}:{config_leida['server']['port']}")
    print(f"  Logging: {config_leida['logging']['level']}")
    
    # Limpiar
    archivo_yaml.unlink()


def ejemplo_yaml_multilinea():
    """YAML con strings multilinea."""
    print("\n=== YAML Multilinea ===\n")
    
    yaml_content = """
app:
  name: Mi Aplicación
  description: |
    Esta es una aplicación de ejemplo
    que demuestra el uso de YAML
    con strings multilinea.
  
  welcome_message: >
    Bienvenido a la aplicación.
    Este mensaje aparece en una sola línea
    aunque esté escrito en varias.
  
  features:
    - Autenticación
    - API REST
    - Panel de administración
"""
    
    # Parsear YAML
    config = yaml.safe_load(yaml_content)
    
    print("Descripción (multilinea con |):")
    print(config["app"]["description"])
    
    print("\nMensaje de bienvenida (multilinea con >):")
    print(config["app"]["welcome_message"])


# =============================================================================
# 4. Conversión entre Formatos
# =============================================================================

def convertir_csv_a_json(archivo_csv: Path, archivo_json: Path):
    """Convierte CSV a JSON."""
    # Leer CSV
    with archivo_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        datos = list(reader)
    
    # Escribir JSON
    with archivo_json.open("w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def ejemplo_csv_to_json():
    """Convertir CSV a JSON."""
    print("\n=== CSV → JSON ===\n")
    
    # Crear CSV
    csv_file = Path("productos.csv")
    with csv_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "nombre", "precio"])
        writer.writeheader()
        writer.writerows([
            {"id": "1", "nombre": "Laptop", "precio": "1200"},
            {"id": "2", "nombre": "Mouse", "precio": "25"},
            {"id": "3", "nombre": "Teclado", "precio": "75"},
        ])
    
    # Convertir a JSON
    json_file = Path("productos.json")
    convertir_csv_a_json(csv_file, json_file)
    
    print(f"CSV: {csv_file}")
    print(f"JSON: {json_file}")
    print("\nContenido JSON:")
    print(json_file.read_text(encoding="utf-8"))
    
    # Limpiar
    csv_file.unlink()
    json_file.unlink()


def convertir_json_a_yaml(archivo_json: Path, archivo_yaml: Path):
    """Convierte JSON a YAML."""
    # Leer JSON
    datos = json.loads(archivo_json.read_text(encoding="utf-8"))
    
    # Escribir YAML
    with archivo_yaml.open("w", encoding="utf-8") as f:
        yaml.dump(datos, f, default_flow_style=False, allow_unicode=True)


def ejemplo_json_to_yaml():
    """Convertir JSON a YAML."""
    print("\n=== JSON → YAML ===\n")
    
    # Crear JSON
    json_file = Path("config.json")
    config = {
        "database": {
            "host": "localhost",
            "port": 5432
        },
        "cache": {
            "enabled": True,
            "ttl": 300
        }
    }
    json_file.write_text(
        json.dumps(config, indent=2),
        encoding="utf-8"
    )
    
    # Convertir a YAML
    yaml_file = Path("config.yaml")
    convertir_json_a_yaml(json_file, yaml_file)
    
    print(f"JSON: {json_file}")
    print(f"YAML: {yaml_file}")
    print("\nContenido YAML:")
    print(yaml_file.read_text(encoding="utf-8"))
    
    # Limpiar
    json_file.unlink()
    yaml_file.unlink()


# =============================================================================
# 5. Streaming de Archivos Grandes
# =============================================================================

def leer_csv_por_chunks(
    archivo: Path,
    chunk_size: int = 1000
) -> Iterator[List[Dict[str, Any]]]:
    """Lee CSV en chunks para archivos grandes."""
    with archivo.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        chunk = []
        for row in reader:
            chunk.append(row)
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        
        # Yield último chunk si tiene datos
        if chunk:
            yield chunk


def ejemplo_streaming_csv():
    """Procesar archivos CSV grandes con streaming."""
    print("\n=== Streaming CSV ===\n")
    
    # Crear CSV grande
    csv_file = Path("datos_grandes.csv")
    with csv_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "valor"])
        writer.writeheader()
        for i in range(10000):
            writer.writerow({"id": i, "valor": i * 2})
    
    print(f"CSV creado: {csv_file} ({csv_file.stat().st_size} bytes)")
    
    # Procesar en chunks
    total_procesado = 0
    for i, chunk in enumerate(leer_csv_por_chunks(csv_file, chunk_size=2000)):
        total_procesado += len(chunk)
        print(f"  Chunk {i+1}: {len(chunk)} registros")
    
    print(f"\nTotal registros procesados: {total_procesado}")
    
    # Limpiar
    csv_file.unlink()


def ejemplo_streaming_json():
    """Procesar JSON grandes línea por línea (JSON Lines)."""
    print("\n=== Streaming JSON Lines ===\n")
    
    # Crear archivo JSONL (JSON Lines)
    jsonl_file = Path("datos.jsonl")
    
    # Escribir JSONL
    with jsonl_file.open("w", encoding="utf-8") as f:
        for i in range(5):
            registro = {"id": i, "nombre": f"Usuario {i}", "valor": i * 100}
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
    
    print(f"JSONL creado: {jsonl_file}")
    print("\nContenido:")
    print(jsonl_file.read_text(encoding="utf-8"))
    
    # Leer JSONL línea por línea
    print("Leyendo JSONL:")
    with jsonl_file.open("r", encoding="utf-8") as f:
        for linea in f:
            registro = json.loads(linea)
            print(f"  {registro}")
    
    # Limpiar
    jsonl_file.unlink()


# =============================================================================
# Main
# =============================================================================

def main():
    """Ejecuta todos los ejemplos."""
    ejemplos = [
        ejemplo_csv_basico,
        ejemplo_csv_dict,
        ejemplo_csv_dialectos,
        ejemplo_csv_con_validacion,
        ejemplo_json_basico,
        ejemplo_json_archivo,
        ejemplo_json_custom_encoder,
        ejemplo_json_pydantic,
        ejemplo_yaml_basico,
        ejemplo_yaml_archivo,
        ejemplo_yaml_multilinea,
        ejemplo_csv_to_json,
        ejemplo_json_to_yaml,
        ejemplo_streaming_csv,
        ejemplo_streaming_json,
    ]
    
    for ejemplo in ejemplos:
        try:
            ejemplo()
        except Exception as e:
            print(f"❌ Error en {ejemplo.__name__}: {e}")
        print("\n" + "="*70)


if __name__ == "__main__":
    main()
