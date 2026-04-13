"""
Módulo 6.1: pathlib y Manejo de Archivos
==========================================

Aprende a manipular archivos y rutas de forma segura y multiplataforma
usando pathlib en lugar de os.path.

Temas:
- pathlib.Path vs os.path
- Operaciones con rutas
- Lectura y escritura de archivos
- Context managers
- Globbing y búsqueda
- Archivos temporales
"""

from pathlib import Path
from typing import Iterator, List
import shutil
import tempfile
from contextlib import contextmanager


# =============================================================================
# 1. Introducción a pathlib.Path
# =============================================================================

def ejemplo_path_basico():
    """Ejemplos básicos de uso de Path."""
    print("=== Path Básico ===\n")
    
    # Crear Path desde string
    archivo = Path("datos/usuarios.json")
    print(f"Path: {archivo}")
    print(f"Tipo: {type(archivo)}")
    
    # Path del archivo actual
    archivo_actual = Path(__file__)
    print(f"\nArchivo actual: {archivo_actual}")
    print(f"Absoluto: {archivo_actual.absolute()}")
    
    # Directorio del archivo actual
    directorio_actual = Path(__file__).parent
    print(f"Directorio: {directorio_actual}")
    
    # Path del directorio de trabajo
    cwd = Path.cwd()
    print(f"Working directory: {cwd}")
    
    # Home directory del usuario
    home = Path.home()
    print(f"Home: {home}")


def ejemplo_operaciones_path():
    """Operaciones comunes con paths."""
    print("\n=== Operaciones con Path ===\n")
    
    # Construir rutas con /
    base = Path("proyecto")
    carpeta_datos = base / "datos"
    archivo = carpeta_datos / "usuarios.json"
    
    print(f"Ruta construida: {archivo}")
    
    # Componentes de una ruta
    ruta = Path("/home/usuario/proyectos/app/datos/config.json")
    print(f"\nRuta completa: {ruta}")
    print(f"Partes: {ruta.parts}")
    print(f"Parent: {ruta.parent}")
    print(f"Nombre: {ruta.name}")
    print(f"Stem (sin extensión): {ruta.stem}")
    print(f"Extensión: {ruta.suffix}")
    
    # Múltiples extensiones
    archivo_tar = Path("backup.tar.gz")
    print(f"\nArchivo: {archivo_tar}")
    print(f"Extensión: {archivo_tar.suffix}")
    print(f"Extensiones: {archivo_tar.suffixes}")
    
    # Cambiar extensión
    nuevo_archivo = archivo_tar.with_suffix(".zip")
    print(f"Con nueva extensión: {nuevo_archivo}")
    
    # Cambiar nombre
    otro_archivo = archivo_tar.with_name("restore.tar.gz")
    print(f"Con nuevo nombre: {otro_archivo}")


def ejemplo_verificacion_archivos():
    """Verificar existencia y tipo de archivos."""
    print("\n=== Verificación de Archivos ===\n")
    
    archivo = Path(__file__)
    
    print(f"Archivo: {archivo}")
    print(f"¿Existe?: {archivo.exists()}")
    print(f"¿Es archivo?: {archivo.is_file()}")
    print(f"¿Es directorio?: {archivo.is_dir()}")
    print(f"¿Es absoluto?: {archivo.is_absolute()}")
    
    # Información del archivo
    stat = archivo.stat()
    print(f"\nTamaño: {stat.st_size} bytes")
    print(f"Tamaño (KB): {stat.st_size / 1024:.2f} KB")
    print(f"Modificado: {stat.st_mtime}")
    
    # Resolver path (absoluto y normalizado)
    relativo = Path("../datos")
    print(f"\nPath relativo: {relativo}")
    print(f"Path resuelto: {relativo.resolve()}")


# =============================================================================
# 2. Lectura y Escritura de Archivos
# =============================================================================

def ejemplo_leer_escribir_texto():
    """Lectura y escritura de archivos de texto."""
    print("\n=== Archivos de Texto ===\n")
    
    archivo = Path("ejemplo_texto.txt")
    
    # Escribir texto
    contenido = """Línea 1
Línea 2
Línea 3"""
    
    archivo.write_text(contenido, encoding="utf-8")
    print(f"Archivo escrito: {archivo}")
    
    # Leer todo el texto
    texto_leido = archivo.read_text(encoding="utf-8")
    print(f"\nContenido leído:\n{texto_leido}")
    
    # Limpiar
    archivo.unlink()
    print(f"\nArchivo eliminado: {archivo}")


def ejemplo_context_manager():
    """Uso de context managers para manejo seguro de archivos."""
    print("\n=== Context Managers ===\n")
    
    archivo = Path("ejemplo_context.txt")
    
    # Escribir con context manager
    with archivo.open("w", encoding="utf-8") as f:
        f.write("Primera línea\n")
        f.write("Segunda línea\n")
        f.write("Tercera línea\n")
    # El archivo se cierra automáticamente aquí
    
    print(f"Archivo escrito: {archivo}")
    
    # Leer línea por línea (eficiente para archivos grandes)
    print("\nLeyendo línea por línea:")
    with archivo.open("r", encoding="utf-8") as f:
        for i, linea in enumerate(f, 1):
            print(f"  {i}: {linea.rstrip()}")
    
    # Limpiar
    archivo.unlink()


def ejemplo_escribir_lineas():
    """Escribir múltiples líneas eficientemente."""
    print("\n=== Escribir Líneas ===\n")
    
    archivo = Path("ejemplo_lineas.txt")
    
    # Lista de líneas
    lineas = [
        "Usuario: Ana\n",
        "Email: ana@ejemplo.com\n",
        "Edad: 28\n",
    ]
    
    # Escribir todas las líneas de una vez
    archivo.write_text("".join(lineas), encoding="utf-8")
    
    # O usando writelines con context manager
    with archivo.open("w", encoding="utf-8") as f:
        f.writelines(lineas)
    
    # Leer líneas
    lineas_leidas = archivo.read_text(encoding="utf-8").splitlines()
    print("Líneas leídas:")
    for linea in lineas_leidas:
        print(f"  - {linea}")
    
    # Limpiar
    archivo.unlink()


def ejemplo_archivos_binarios():
    """Trabajo con archivos binarios."""
    print("\n=== Archivos Binarios ===\n")
    
    archivo = Path("ejemplo_binario.bin")
    
    # Escribir bytes
    datos = bytes([0x48, 0x65, 0x6C, 0x6C, 0x6F])  # "Hello" en ASCII
    archivo.write_bytes(datos)
    
    print(f"Bytes escritos: {datos}")
    print(f"Como texto: {datos.decode('ascii')}")
    
    # Leer bytes
    datos_leidos = archivo.read_bytes()
    print(f"\nBytes leídos: {datos_leidos}")
    print(f"Como texto: {datos_leidos.decode('ascii')}")
    
    # Limpiar
    archivo.unlink()


# =============================================================================
# 3. Operaciones con Directorios
# =============================================================================

def ejemplo_crear_directorios():
    """Crear directorios y estructuras de carpetas."""
    print("\n=== Crear Directorios ===\n")
    
    # Crear un directorio
    carpeta = Path("temp_ejemplo")
    carpeta.mkdir(exist_ok=True)
    print(f"Directorio creado: {carpeta}")
    
    # Crear estructura de directorios
    estructura = Path("temp_ejemplo/datos/usuarios/reportes")
    estructura.mkdir(parents=True, exist_ok=True)
    print(f"Estructura creada: {estructura}")
    
    # Listar contenido de directorio
    print(f"\nContenido de {carpeta}:")
    for item in carpeta.iterdir():
        tipo = "📁" if item.is_dir() else "📄"
        print(f"  {tipo} {item.name}")
    
    # Limpiar
    shutil.rmtree(carpeta)
    print(f"\nDirectorio eliminado: {carpeta}")


def ejemplo_listar_archivos():
    """Listar archivos en un directorio."""
    print("\n=== Listar Archivos ===\n")
    
    # Directorio actual
    directorio = Path(".")
    
    # Listar todo
    print("Todos los archivos:")
    for item in directorio.iterdir():
        if item.is_file():
            print(f"  📄 {item.name}")
    
    # Listar solo archivos .py
    print("\nArchivos Python:")
    for archivo in directorio.glob("*.py"):
        print(f"  🐍 {archivo.name}")
    
    # Buscar recursivamente
    print("\nArchivos .md (recursivo):")
    for archivo in directorio.rglob("*.md"):
        print(f"  📝 {archivo}")


def ejemplo_globbing():
    """Patrones de búsqueda con glob."""
    print("\n=== Globbing ===\n")
    
    directorio = Path(".")
    
    # Patrones básicos
    print("Archivos .py:")
    for f in directorio.glob("*.py"):
        print(f"  - {f.name}")
    
    # Recursivo con rglob
    print("\nTodos los .md (recursivo):")
    for f in directorio.rglob("*.md"):
        print(f"  - {f}")
    
    # Patrones complejos
    print("\nArchivos que empiezan con '0':")
    for f in directorio.glob("0*.py"):
        print(f"  - {f.name}")


# =============================================================================
# 4. Operaciones de Copia y Movimiento
# =============================================================================

def ejemplo_copiar_mover():
    """Copiar, mover y renombrar archivos."""
    print("\n=== Copiar y Mover ===\n")
    
    # Crear archivo de prueba
    origen = Path("archivo_origen.txt")
    origen.write_text("Contenido de prueba", encoding="utf-8")
    print(f"Archivo creado: {origen}")
    
    # Copiar archivo
    destino = Path("archivo_copia.txt")
    shutil.copy2(origen, destino)
    print(f"Copiado a: {destino}")
    
    # Renombrar (mover en el mismo directorio)
    nuevo_nombre = Path("archivo_renombrado.txt")
    destino.rename(nuevo_nombre)
    print(f"Renombrado a: {nuevo_nombre}")
    
    # Mover a otro directorio
    carpeta = Path("temp_destino")
    carpeta.mkdir(exist_ok=True)
    nuevo_destino = carpeta / "archivo_movido.txt"
    shutil.move(str(nuevo_nombre), str(nuevo_destino))
    print(f"Movido a: {nuevo_destino}")
    
    # Limpiar
    origen.unlink()
    shutil.rmtree(carpeta)
    print("\nArchivos de prueba eliminados")


def ejemplo_copiar_directorio():
    """Copiar directorios completos."""
    print("\n=== Copiar Directorios ===\n")
    
    # Crear estructura de prueba
    origen = Path("temp_origen")
    origen.mkdir(exist_ok=True)
    (origen / "archivo1.txt").write_text("Contenido 1")
    (origen / "archivo2.txt").write_text("Contenido 2")
    (origen / "subcarpeta").mkdir(exist_ok=True)
    (origen / "subcarpeta" / "archivo3.txt").write_text("Contenido 3")
    
    print(f"Estructura creada en: {origen}")
    
    # Copiar todo el directorio
    destino = Path("temp_destino")
    shutil.copytree(origen, destino)
    print(f"Copiado a: {destino}")
    
    # Verificar
    print("\nContenido copiado:")
    for item in destino.rglob("*"):
        if item.is_file():
            print(f"  📄 {item.relative_to(destino)}")
    
    # Limpiar
    shutil.rmtree(origen)
    shutil.rmtree(destino)
    print("\nDirectorios eliminados")


# =============================================================================
# 5. Archivos Temporales
# =============================================================================

def ejemplo_archivos_temporales():
    """Trabajar con archivos temporales."""
    print("\n=== Archivos Temporales ===\n")
    
    # Archivo temporal que se elimina automáticamente
    with tempfile.NamedTemporaryFile(
        mode="w",
        delete=True,
        suffix=".txt",
        encoding="utf-8"
    ) as tmp:
        print(f"Archivo temporal: {tmp.name}")
        tmp.write("Contenido temporal\n")
        tmp.flush()
        
        # Leer el archivo
        tmp.seek(0)
        contenido = tmp.read()
        print(f"Contenido: {contenido}")
    # El archivo se elimina aquí
    
    print("Archivo temporal eliminado automáticamente")


def ejemplo_directorio_temporal():
    """Trabajar con directorios temporales."""
    print("\n=== Directorio Temporal ===\n")
    
    # Directorio temporal con context manager
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        print(f"Directorio temporal: {tmp_path}")
        
        # Crear archivos en el directorio temporal
        (tmp_path / "temp1.txt").write_text("Temporal 1")
        (tmp_path / "temp2.txt").write_text("Temporal 2")
        
        print("Archivos creados:")
        for archivo in tmp_path.iterdir():
            print(f"  - {archivo.name}")
    # El directorio y su contenido se eliminan aquí
    
    print("Directorio temporal eliminado automáticamente")


@contextmanager
def temporal_working_directory(path: Path):
    """Context manager para cambiar temporalmente el directorio de trabajo."""
    original_dir = Path.cwd()
    try:
        import os
        os.chdir(path)
        yield path
    finally:
        os.chdir(original_dir)


def ejemplo_cambiar_directorio():
    """Cambiar temporalmente el directorio de trabajo."""
    print("\n=== Cambiar Directorio ===\n")
    
    print(f"Directorio actual: {Path.cwd()}")
    
    # Crear directorio temporal
    temp_dir = Path("temp_working")
    temp_dir.mkdir(exist_ok=True)
    
    # Usar context manager personalizado
    with temporal_working_directory(temp_dir):
        print(f"Dentro del context: {Path.cwd()}")
        
        # Crear archivo en el directorio actual
        Path("archivo_temp.txt").write_text("Contenido")
    
    print(f"Fuera del context: {Path.cwd()}")
    
    # Limpiar
    shutil.rmtree(temp_dir)


# =============================================================================
# 6. Utilidades Avanzadas
# =============================================================================

def obtener_tamano_directorio(path: Path) -> int:
    """Calcula el tamaño total de un directorio."""
    total = 0
    for item in path.rglob("*"):
        if item.is_file():
            total += item.stat().st_size
    return total


def ejemplo_calcular_tamano():
    """Calcular tamaño de directorios."""
    print("\n=== Calcular Tamaño ===\n")
    
    # Crear estructura de prueba
    test_dir = Path("temp_size")
    test_dir.mkdir(exist_ok=True)
    
    # Crear archivos de diferentes tamaños
    (test_dir / "small.txt").write_text("x" * 100)
    (test_dir / "medium.txt").write_text("x" * 1000)
    (test_dir / "large.txt").write_text("x" * 10000)
    
    # Calcular tamaño
    tamano = obtener_tamano_directorio(test_dir)
    print(f"Directorio: {test_dir}")
    print(f"Tamaño total: {tamano} bytes")
    print(f"Tamaño en KB: {tamano / 1024:.2f} KB")
    
    # Limpiar
    shutil.rmtree(test_dir)


def buscar_archivos_por_extension(
    directorio: Path,
    extension: str
) -> List[Path]:
    """Busca todos los archivos con una extensión específica."""
    return list(directorio.rglob(f"*.{extension}"))


def ejemplo_buscar_archivos():
    """Buscar archivos por extensión."""
    print("\n=== Buscar Archivos ===\n")
    
    directorio = Path(".")
    
    # Buscar archivos Python
    archivos_py = buscar_archivos_por_extension(directorio, "py")
    print(f"Archivos .py encontrados: {len(archivos_py)}")
    for archivo in archivos_py[:5]:  # Mostrar solo los primeros 5
        print(f"  - {archivo}")


def backup_archivo(archivo: Path, carpeta_backup: Path) -> Path:
    """Crea un backup de un archivo con timestamp."""
    from datetime import datetime
    
    carpeta_backup.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_backup = f"{archivo.stem}_{timestamp}{archivo.suffix}"
    archivo_backup = carpeta_backup / nombre_backup
    
    shutil.copy2(archivo, archivo_backup)
    return archivo_backup


def ejemplo_backup():
    """Crear backup de archivos."""
    print("\n=== Backup de Archivos ===\n")
    
    # Crear archivo de prueba
    archivo = Path("importante.txt")
    archivo.write_text("Datos importantes", encoding="utf-8")
    
    # Crear backup
    carpeta_backup = Path("backups")
    archivo_backup = backup_archivo(archivo, carpeta_backup)
    
    print(f"Archivo original: {archivo}")
    print(f"Backup creado: {archivo_backup}")
    
    # Limpiar
    archivo.unlink()
    shutil.rmtree(carpeta_backup)


# =============================================================================
# 7. Comparación: pathlib vs os.path
# =============================================================================

def ejemplo_comparacion_apis():
    """Comparación entre pathlib y os.path."""
    print("\n=== pathlib vs os.path ===\n")
    
    import os
    
    # Con os.path (viejo estilo)
    print("Con os.path:")
    ruta_os = os.path.join("datos", "usuarios", "perfil.json")
    print(f"  Ruta: {ruta_os}")
    print(f"  Existe: {os.path.exists(ruta_os)}")
    print(f"  Nombre: {os.path.basename(ruta_os)}")
    print(f"  Directorio: {os.path.dirname(ruta_os)}")
    
    # Con pathlib (moderno)
    print("\nCon pathlib:")
    ruta_path = Path("datos") / "usuarios" / "perfil.json"
    print(f"  Ruta: {ruta_path}")
    print(f"  Existe: {ruta_path.exists()}")
    print(f"  Nombre: {ruta_path.name}")
    print(f"  Directorio: {ruta_path.parent}")
    
    print("\n✅ pathlib es más legible y orientado a objetos")


# =============================================================================
# Main
# =============================================================================

def main():
    """Ejecuta todos los ejemplos."""
    ejemplos = [
        ejemplo_path_basico,
        ejemplo_operaciones_path,
        ejemplo_verificacion_archivos,
        ejemplo_leer_escribir_texto,
        ejemplo_context_manager,
        ejemplo_escribir_lineas,
        ejemplo_archivos_binarios,
        ejemplo_crear_directorios,
        ejemplo_listar_archivos,
        ejemplo_globbing,
        ejemplo_copiar_mover,
        ejemplo_copiar_directorio,
        ejemplo_archivos_temporales,
        ejemplo_directorio_temporal,
        ejemplo_cambiar_directorio,
        ejemplo_calcular_tamano,
        ejemplo_buscar_archivos,
        ejemplo_backup,
        ejemplo_comparacion_apis,
    ]
    
    for ejemplo in ejemplos:
        try:
            ejemplo()
        except Exception as e:
            print(f"❌ Error en {ejemplo.__name__}: {e}")
        print("\n" + "="*70)


if __name__ == "__main__":
    main()
