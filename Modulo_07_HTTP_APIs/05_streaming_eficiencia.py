"""
Módulo 7.5: Streaming y Eficiencia de Memoria

Técnicas para manejar respuestas HTTP grandes sin consumir
memoria excesiva usando streaming y procesamiento incremental.

Instalación:
    pip install requests httpx aiohttp tqdm

Documentación:
    - requests streaming: https://requests.readthedocs.io/en/latest/user/advanced/#streaming-requests
    - httpx streaming: https://www.python-httpx.org/quickstart/#streaming-responses
"""

import requests
import httpx
import aiohttp
import asyncio
import json
import hashlib
from pathlib import Path
from tqdm import tqdm
from typing import Iterator, Dict, Any
import gzip
import io


# =============================================================================
# Ejemplo 1: Problema - Cargar Todo en Memoria (MAL)
# =============================================================================

def ejemplo_problema_memoria():
    """Ejemplo de lo que NO hacer con archivos grandes."""
    print("\n" + "="*60)
    print("Ejemplo 1: Problema - Cargar Todo en Memoria")
    print("="*60)
    
    # ❌ MAL: Carga todo el archivo en memoria
    # Si el archivo es 1GB, usa 1GB de RAM
    url = 'https://httpbin.org/image/png'
    
    print("Método incorrecto (carga todo en memoria):")
    response = requests.get(url)
    contenido = response.content  # TODO el contenido en memoria
    
    print(f"  Bytes en memoria: {len(contenido):,}")
    print("  ❌ Con archivos grandes esto es ineficiente")


# =============================================================================
# Ejemplo 2: Solución - Streaming por Chunks
# =============================================================================

def ejemplo_streaming_chunks():
    """Descargar archivo usando streaming."""
    print("\n" + "="*60)
    print("Ejemplo 2: Streaming por Chunks")
    print("="*60)
    
    url = 'https://httpbin.org/image/png'
    output_file = Path("streaming_download.png")
    
    # ✅ BIEN: Stream=True para no cargar todo en memoria
    response = requests.get(url, stream=True)
    
    chunk_size = 8192  # 8KB por chunk
    chunks_procesados = 0
    
    with output_file.open('wb') as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:  # Filtrar keep-alive chunks
                f.write(chunk)
                chunks_procesados += 1
    
    print(f"✓ Archivo descargado: {output_file}")
    print(f"  Tamaño: {output_file.stat().st_size:,} bytes")
    print(f"  Chunks procesados: {chunks_procesados}")
    print(f"  Memoria usada por chunk: {chunk_size:,} bytes")
    
    # Limpiar
    output_file.unlink()


# =============================================================================
# Ejemplo 3: Progress Bar con tqdm
# =============================================================================

def ejemplo_download_con_progress():
    """Descargar con barra de progreso."""
    print("\n" + "="*60)
    print("Ejemplo 3: Download con Progress Bar")
    print("="*60)
    
    url = 'https://httpbin.org/image/png'
    output_file = Path("download_progress.png")
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    # Barra de progreso
    with output_file.open('wb') as f:
        with tqdm(
            total=total_size,
            unit='B',
            unit_scale=True,
            desc='Descargando'
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                pbar.update(len(chunk))
    
    print(f"\n✓ Descargado: {output_file} ({total_size:,} bytes)")
    output_file.unlink()


# =============================================================================
# Ejemplo 4: Verificar Integridad con Hash
# =============================================================================

def ejemplo_download_con_hash():
    """Descargar y verificar integridad con hash."""
    print("\n" + "="*60)
    print("Ejemplo 4: Download con Verificación de Hash")
    print("="*60)
    
    url = 'https://httpbin.org/bytes/10000'
    output_file = Path("download_hash.bin")
    
    # Calcular hash mientras descargamos
    sha256 = hashlib.sha256()
    
    response = requests.get(url, stream=True)
    
    with output_file.open('wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            sha256.update(chunk)  # Actualizar hash
    
    hash_calculado = sha256.hexdigest()
    
    print(f"✓ Archivo descargado: {output_file}")
    print(f"  SHA-256: {hash_calculado}")
    print("  ✓ Hash calculado durante descarga (sin recargar archivo)")
    
    output_file.unlink()


# =============================================================================
# Ejemplo 5: Streaming de JSON Lines
# =============================================================================

def ejemplo_json_lines_streaming():
    """Procesar JSON Lines sin cargar todo en memoria."""
    print("\n" + "="*60)
    print("Ejemplo 5: Streaming de JSON Lines")
    print("="*60)
    
    url = 'https://httpbin.org/stream/10'
    
    response = requests.get(url, stream=True)
    
    print("Procesando líneas de JSON:")
    for i, line in enumerate(response.iter_lines(), 1):
        if line:
            try:
                data = json.loads(line)
                print(f"  Línea {i}: ID={data['id']}, URL={data['url']}")
            except json.JSONDecodeError:
                pass
    
    print("✓ JSON Lines procesado sin cargar todo en memoria")


# =============================================================================
# Ejemplo 6: Generador para Procesar Líneas
# =============================================================================

def stream_json_lines(url: str) -> Iterator[Dict[str, Any]]:
    """Generador que yield cada línea JSON."""
    response = requests.get(url, stream=True)
    
    for line in response.iter_lines():
        if line:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def ejemplo_generador_json():
    """Usar generador para procesamiento eficiente."""
    print("\n" + "="*60)
    print("Ejemplo 6: Generador para JSON Lines")
    print("="*60)
    
    # Procesar solo primeras 5 líneas
    url = 'https://httpbin.org/stream/100'
    
    print("Procesando con generador (lazy evaluation):")
    for i, item in enumerate(stream_json_lines(url), 1):
        print(f"  Item {i}: {item['url']}")
        if i >= 5:
            break  # Podemos parar cuando queramos
    
    print("✓ Solo procesamos lo necesario (no todo el stream)")


# =============================================================================
# Ejemplo 7: Upload con Streaming
# =============================================================================

def ejemplo_upload_streaming():
    """Subir archivo usando streaming."""
    print("\n" + "="*60)
    print("Ejemplo 7: Upload con Streaming")
    print("="*60)
    
    # Crear archivo grande (simulado con generador)
    def file_generator():
        """Genera contenido sin almacenarlo todo en memoria."""
        for i in range(1000):
            yield f"Línea {i}: Datos de prueba\n".encode()
    
    # Upload con streaming
    response = requests.post(
        'https://httpbin.org/post',
        data=file_generator(),  # Generador en lugar de bytes completos
        headers={'Content-Type': 'text/plain'}
    )
    
    print(f"✓ Upload exitoso: {response.status_code}")
    print("  Memoria usada: Solo chunk actual (no todo el archivo)")


# =============================================================================
# Ejemplo 8: httpx Streaming
# =============================================================================

def ejemplo_httpx_streaming():
    """Streaming con httpx."""
    print("\n" + "="*60)
    print("Ejemplo 8: httpx Streaming")
    print("="*60)
    
    url = 'https://httpbin.org/stream/5'
    
    # Usar context manager para streaming
    with httpx.stream('GET', url) as response:
        print("Procesando con httpx:")
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                print(f"  - {data['id']}: {data['url']}")
    
    print("✓ httpx streaming completado")


# =============================================================================
# Ejemplo 9: aiohttp Streaming Asíncrono
# =============================================================================

async def ejemplo_aiohttp_streaming():
    """Streaming asíncrono con aiohttp."""
    print("\n" + "="*60)
    print("Ejemplo 9: aiohttp Streaming Asíncrono")
    print("="*60)
    
    url = 'https://httpbin.org/stream/5'
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print("Procesando async streaming:")
            async for line in response.content:
                if line:
                    try:
                        data = json.loads(line)
                        print(f"  - Async: {data['url']}")
                    except json.JSONDecodeError:
                        pass
    
    print("✓ Async streaming completado")


# =============================================================================
# Ejemplo 10: Descarga Concurrente de Múltiples Archivos
# =============================================================================

async def download_async(session: aiohttp.ClientSession, url: str, filename: str):
    """Descarga un archivo asíncronamente."""
    async with session.get(url) as response:
        with Path(filename).open('wb') as f:
            async for chunk in response.content.iter_chunked(8192):
                f.write(chunk)
    
    return filename


async def ejemplo_descarga_concurrente():
    """Descargar múltiples archivos concurrentemente."""
    print("\n" + "="*60)
    print("Ejemplo 10: Descarga Concurrente")
    print("="*60)
    
    # Simular descarga de 5 archivos
    urls = [
        ('https://httpbin.org/image/png', 'async_img1.png'),
        ('https://httpbin.org/image/jpeg', 'async_img2.jpg'),
        ('https://httpbin.org/image/webp', 'async_img3.webp'),
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [download_async(session, url, filename) for url, filename in urls]
        archivos = await asyncio.gather(*tasks)
    
    print(f"✓ {len(archivos)} archivos descargados concurrentemente")
    
    # Limpiar
    for _, filename in urls:
        Path(filename).unlink(missing_ok=True)


# =============================================================================
# Ejemplo 11: Procesamiento Incremental de CSV
# =============================================================================

def ejemplo_csv_streaming():
    """Procesar CSV grande linea por linea."""
    print("\n" + "="*60)
    print("Ejemplo 11: CSV Streaming")
    print("="*60)
    
    # Simular CSV stream
    csv_url = 'https://httpbin.org/stream/5'  # Simulado
    
    response = requests.get(csv_url, stream=True)
    
    print("Procesando CSV línea por línea:")
    line_count = 0
    
    for line in response.iter_lines(decode_unicode=True):
        if line:
            line_count += 1
            # Procesar cada línea sin acumular en memoria
            print(f"  Línea {line_count} procesada")
            
            if line_count >= 5:
                break
    
    print(f"✓ {line_count} líneas procesadas (memoria constante)")


# =============================================================================
# Ejemplo 12: Comprimir Durante Descarga
# =============================================================================

def ejemplo_download_comprimido():
    """Descargar y comprimir al mismo tiempo."""
    print("\n" + "="*60)
    print("Ejemplo 12: Download y Compresión Streaming")
    print("="*60)
    
    url = 'https://httpbin.org/bytes/50000'
    output_file = Path("download.gz")
    
    response = requests.get(url, stream=True)
    
    # Comprimir mientras descargamos
    with gzip.open(output_file, 'wb') as f_out:
        for chunk in response.iter_content(chunk_size=8192):
            f_out.write(chunk)
    
    original_size = int(response.headers.get('content-length', 0))
    compressed_size = output_file.stat().st_size
    ratio = (1 - compressed_size / original_size) * 100
    
    print(f"✓ Descargado y comprimido:")
    print(f"  Original: {original_size:,} bytes")
    print(f"  Comprimido: {compressed_size:,} bytes")
    print(f"  Ratio: {ratio:.1f}% de ahorro")
    
    output_file.unlink()


# =============================================================================
# Ejemplo 13: Downloader Class Reutilizable
# =============================================================================

class StreamingDownloader:
    """Downloader eficiente con streaming."""
    
    def __init__(self, chunk_size=8192):
        self.chunk_size = chunk_size
    
    def download(
        self,
        url: str,
        output_file: Path,
        show_progress: bool = True,
        verify_hash: bool = False
    ) -> Dict[str, Any]:
        """
        Descarga archivo con streaming.
        
        Returns:
            Dict con metadata de descarga
        """
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        downloaded = 0
        sha256 = hashlib.sha256() if verify_hash else None
        
        pbar = None
        if show_progress and total_size > 0:
            pbar = tqdm(total=total_size, unit='B', unit_scale=True)
        
        try:
            with output_file.open('wb') as f:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if sha256:
                            sha256.update(chunk)
                        
                        if pbar:
                            pbar.update(len(chunk))
        finally:
            if pbar:
                pbar.close()
        
        return {
            'url': url,
            'file': str(output_file),
            'size': downloaded,
            'hash': sha256.hexdigest() if sha256 else None
        }


def ejemplo_downloader_class():
    """Usar downloader class."""
    print("\n" + "="*60)
    print("Ejemplo 13: Downloader Class Reutilizable")
    print("="*60)
    
    downloader = StreamingDownloader()
    
    result = downloader.download(
        url='https://httpbin.org/image/png',
        output_file=Path('downloader_test.png'),
        show_progress=True,
        verify_hash=True
    )
    
    print(f"\n✓ Descarga completada:")
    print(f"  Archivo: {result['file']}")
    print(f"  Tamaño: {result['size']:,} bytes")
    print(f"  SHA-256: {result['hash']}")
    
    Path(result['file']).unlink()


# =============================================================================
# Ejemplo 14: Procesamiento Pipeline
# =============================================================================

def download_stream(url: str) -> Iterator[bytes]:
    """Generador que descarga en chunks."""
    response = requests.get(url, stream=True)
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            yield chunk


def process_stream(stream: Iterator[bytes]) -> Iterator[bytes]:
    """Procesa stream (ej: reemplazar bytes)."""
    for chunk in stream:
        # Ejemplo: convertir a mayúsculas si es texto
        yield chunk.upper() if chunk.isascii() else chunk


def save_stream(stream: Iterator[bytes], output_file: Path):
    """Guarda stream a archivo."""
    with output_file.open('wb') as f:
        for chunk in stream:
            f.write(chunk)


def ejemplo_pipeline():
    """Pipeline de procesamiento streaming."""
    print("\n" + "="*60)
    print("Ejemplo 14: Pipeline de Procesamiento")
    print("="*60)
    
    url = 'https://httpbin.org/bytes/10000'
    output = Path('pipeline_output.bin')
    
    # Pipeline: download -> process -> save
    # Todo en streaming, sin cargar archivo completo
    stream = download_stream(url)
    processed = process_stream(stream)
    save_stream(processed, output)
    
    print(f"✓ Pipeline completado:")
    print(f"  Descarga -> Procesamiento -> Guardado")
    print(f"  Archivo: {output} ({output.stat().st_size:,} bytes)")
    print("  Memoria usada: Solo chunk actual")
    
    output.unlink()


# =============================================================================
# Ejemplo 15: Resumable Downloads
# =============================================================================

class ResumableDownloader:
    """Downloader que puede resumir descargas interrumpidas."""
    
    def download(self, url: str, output_file: Path):
        """Descarga con capacidad de resumir."""
        # Verificar si ya existe archivo parcial
        start_byte = 0
        if output_file.exists():
            start_byte = output_file.stat().st_size
            print(f"Resumiendo descarga desde byte {start_byte:,}")
        
        # Request con Range header
        headers = {}
        if start_byte > 0:
            headers['Range'] = f'bytes={start_byte}-'
        
        response = requests.get(url, headers=headers, stream=True)
        
        # 206 = Partial Content (resume exitoso)
        # 200 = OK (descarga completa)
        if response.status_code not in (200, 206):
            raise Exception(f"Error: {response.status_code}")
        
        total_size = int(response.headers.get('content-length', 0))
        mode = 'ab' if start_byte > 0 else 'wb'
        
        with output_file.open(mode) as f:
            with tqdm(
                total=total_size,
                initial=start_byte,
                unit='B',
                unit_scale=True
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    pbar.update(len(chunk))
        
        print(f"✓ Descarga completada: {output_file}")


def ejemplo_resumable_download():
    """Descarga que puede resumirse."""
    print("\n" + "="*60)
    print("Ejemplo 15: Resumable Downloads")
    print("="*60)
    
    downloader = ResumableDownloader()
    output = Path('resumable.bin')
    
    try:
        # Nota: httpbin no soporta Range, pero el código está preparado
        downloader.download('https://httpbin.org/bytes/50000', output)
        print("✓ Descarga completada (o resumida si existía)")
    except Exception as e:
        print(f"Nota: {e}")
    finally:
        output.unlink(missing_ok=True)


# =============================================================================
# Main: Ejecutar Ejemplos
# =============================================================================

async def main_async():
    """Ejecuta ejemplos asíncronos."""
    await ejemplo_aiohttp_streaming()
    await ejemplo_descarga_concurrente()


def main():
    """Ejecuta todos los ejemplos."""
    print("\n" + "="*60)
    print("MÓDULO 7.5: STREAMING Y EFICIENCIA DE MEMORIA")
    print("="*60)
    
    ejemplos = [
        ("Problema - Memoria", ejemplo_problema_memoria),
        ("Streaming Chunks", ejemplo_streaming_chunks),
        ("Progress Bar", ejemplo_download_con_progress),
        ("Download con Hash", ejemplo_download_con_hash),
        ("JSON Lines", ejemplo_json_lines_streaming),
        ("Generador JSON", ejemplo_generador_json),
        ("Upload Streaming", ejemplo_upload_streaming),
        ("httpx Streaming", ejemplo_httpx_streaming),
        ("CSV Streaming", ejemplo_csv_streaming),
        ("Download Comprimido", ejemplo_download_comprimido),
        ("Downloader Class", ejemplo_downloader_class),
        ("Pipeline", ejemplo_pipeline),
        ("Resumable Download", ejemplo_resumable_download),
    ]
    
    for nombre, funcion in ejemplos:
        try:
            funcion()
        except Exception as e:
            print(f"\n✗ Error en '{nombre}': {e}")
    
    # Ejemplos asíncronos
    asyncio.run(main_async())
    
    print("\n" + "="*60)
    print("✓ Ejemplos completados")
    print("="*60)


if __name__ == "__main__":
    main()
