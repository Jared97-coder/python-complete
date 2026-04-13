# Laboratorio: Cliente HTTP Robusto con Streaming

## Objetivos
- Construir cliente HTTP robusto con httpx
- Implementar reintentos automáticos y timeouts configurables
- Descargar archivos grandes usando streaming
- Validar integridad con checksums
- Manejar errores de forma resiliente

---

## Escenario

Debes crear un sistema de descarga robusto que:
1. Use httpx para requests HTTP con HTTP/2
2. Implemente reintentos con backoff exponencial
3. Configure timeouts apropiados
4. Descargue archivos grandes usando streaming (sin cargar todo en memoria)
5. Verifique integridad con SHA-256
6. Registre todo el proceso con logging

---

## Ejercicio 1: Cliente HTTP Básico con httpx ⭐⭐

### Descripción
Crear cliente HTTP básico con configuración robusta.

### Tareas

**Parte A: Configurar Cliente Base**

```python
import httpx
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HTTPClient:
    """Cliente HTTP robusto con httpx."""
    
    def __init__(
        self,
        base_url: str = "",
        timeout: float = 30.0,
        max_retries: int = 3,
        http2: bool = True
    ):
        """
        Inicializa cliente HTTP.
        
        Args:
            base_url: URL base para requests relativos
            timeout: Timeout en segundos
            max_retries: Máximo número de reintentos
            http2: Habilitar HTTP/2
        """
        self.base_url = base_url
        self.max_retries = max_retries
        
        # Configurar timeout granular
        self.timeout = httpx.Timeout(
            connect=5.0,  # Tiempo para conectar
            read=timeout,  # Tiempo para leer
            write=5.0,  # Tiempo para escribir
            pool=10.0  # Timeout del pool
        )
        
        # Configurar límites de conexión
        self.limits = httpx.Limits(
            max_keepalive_connections=20,
            max_connections=100
        )
        
        # Crear cliente
        self.client = httpx.Client(
            base_url=base_url,
            timeout=self.timeout,
            limits=self.limits,
            http2=http2,
            follow_redirects=True
        )
        
        logger.info(f"Cliente HTTP inicializado (HTTP/2: {http2})")
    
    def get(self, endpoint: str, **kwargs) -> httpx.Response:
        """
        GET request con reintentos.
        
        Args:
            endpoint: Endpoint relativo o URL completa
            **kwargs: Argumentos adicionales para request
        
        Returns:
            httpx.Response
        
        Raises:
            httpx.HTTPError: Si falla después de reintentos
        """
        # TODO: Implementar lógica de reintentos
        pass
    
    def close(self):
        """Cerrar cliente."""
        self.client.close()
        logger.info("Cliente HTTP cerrado")
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
```

**Parte B: Implementar GET con Reintentos**

```python
import time
from typing import Callable

def get(self, endpoint: str, **kwargs) -> httpx.Response:
    """GET request con reintentos y backoff exponencial."""
    url = endpoint if endpoint.startswith('http') else f"{self.base_url}/{endpoint}"
    
    for attempt in range(self.max_retries):
        try:
            logger.debug(f"Intento {attempt + 1}/{self.max_retries}: GET {url}")
            
            response = self.client.get(endpoint, **kwargs)
            response.raise_for_status()
            
            logger.info(f"✓ GET {url}: {response.status_code}")
            return response
        
        except httpx.HTTPStatusError as e:
            # Errores 4xx no se reintentan (error del cliente)
            if 400 <= e.response.status_code < 500:
                logger.error(f"Error del cliente {e.response.status_code}: {url}")
                raise
            
            # Errores 5xx se reintentan
            if attempt < self.max_retries - 1:
                wait_time = 2 ** attempt  # Backoff exponencial: 1s, 2s, 4s
                logger.warning(
                    f"Error {e.response.status_code} en intento {attempt + 1}. "
                    f"Reintentando en {wait_time}s..."
                )
                time.sleep(wait_time)
            else:
                logger.error(f"✗ Falló después de {self.max_retries} intentos")
                raise
        
        except (httpx.TimeoutException, httpx.ConnectError) as e:
            if attempt < self.max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"{type(e).__name__} en intento {attempt + 1}. Reintentando en {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"✗ {type(e).__name__} después de {self.max_retries} intentos")
                raise
```

**Parte C: Probar Cliente**

```python
def main():
    """Prueba el cliente HTTP."""
    
    # Crear cliente
    with HTTPClient(timeout=10.0, max_retries=3) as client:
        try:
            # GET exitoso
            response = client.get('https://jsonplaceholder.typicode.com/posts/1')
            print(f"✓ Status: {response.status_code}")
            print(f"  Data: {response.json()['title']}")
            
            # GET que puede fallar (para probar reintentos)
            response = client.get('https://httpbin.org/status/200,503,500')
            print(f"✓ Status después de posibles reintentos: {response.status_code}")
        
        except httpx.HTTPError as e:
            print(f"✗ Error: {e}")


if __name__ == "__main__":
    main()
```

---

## Ejercicio 2: Descarga con Streaming ⭐⭐⭐⭐

### Descripción
Implementar descarga de archivos usando streaming para eficiencia de memoria.

### Tareas

**Parte A: Downloader con Streaming**

```python
import hashlib
from tqdm import tqdm

class FileDownloader:
    """Descarga archivos usando streaming."""
    
    def __init__(self, client: HTTPClient, chunk_size: int = 8192):
        """
        Inicializa downloader.
        
        Args:
            client: Cliente HTTP a usar
            chunk_size: Tamaño de chunks para streaming
        """
        self.client = client
        self.chunk_size = chunk_size
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def download(
        self,
        url: str,
        output_file: Path,
        verify_hash: Optional[str] = None,
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        Descarga archivo usando streaming.
        
        Args:
            url: URL del archivo a descargar
            output_file: Ruta donde guardar archivo
            verify_hash: Hash SHA-256 esperado (opcional)
            show_progress: Mostrar barra de progreso
        
        Returns:
            Dict con metadata de descarga
        
        Raises:
            ValueError: Si hash no coincide
        """
        self.logger.info(f"Descargando {url} -> {output_file}")
        
        # Hacer request con streaming
        with self.client.client.stream('GET', url) as response:
            response.raise_for_status()
            
            # Obtener tamaño total
            total_size = int(response.headers.get('content-length', 0))
            self.logger.info(f"Tamaño total: {total_size:,} bytes")
            
            # Preparar hash si es necesario
            sha256 = hashlib.sha256() if verify_hash else None
            
            # Barra de progreso
            pbar = None
            if show_progress and total_size > 0:
                pbar = tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    desc=output_file.name
                )
            
            downloaded = 0
            
            try:
                # Crear directorio si no existe
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Descargar en chunks
                with output_file.open('wb') as f:
                    for chunk in response.iter_bytes(chunk_size=self.chunk_size):
                        # Escribir chunk
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Actualizar hash
                        if sha256:
                            sha256.update(chunk)
                        
                        # Actualizar progress bar
                        if pbar:
                            pbar.update(len(chunk))
            
            finally:
                if pbar:
                    pbar.close()
            
            # Verificar hash si se proporcionó
            if verify_hash and sha256:
                calculated_hash = sha256.hexdigest()
                if calculated_hash != verify_hash:
                    self.logger.error(f"Hash no coincide!")
                    self.logger.error(f"  Esperado: {verify_hash}")
                    self.logger.error(f"  Calculado: {calculated_hash}")
                    output_file.unlink()  # Eliminar archivo corrupto
                    raise ValueError("Hash verification failed")
                
                self.logger.info(f"✓ Hash verificado: {calculated_hash}")
            
            # Resultado
            result = {
                'url': url,
                'output_file': str(output_file),
                'size': downloaded,
                'hash': sha256.hexdigest() if sha256 else None,
                'content_type': response.headers.get('content-type')
            }
            
            self.logger.info(f"✓ Descarga completada: {downloaded:,} bytes")
            return result
```

**Parte B: Probar Downloader**

```python
def test_downloader():
    """Prueba el downloader."""
    with HTTPClient() as client:
        downloader = FileDownloader(client)
        
        # Descargar imagen
        result = downloader.download(
            url='https://httpbin.org/image/png',
            output_file=Path('downloads/test_image.png'),
            show_progress=True
        )
        
        print(f"\n✓ Descarga completada:")
        print(f"  Archivo: {result['output_file']}")
        print(f"  Tamaño: {result['size']:,} bytes")
        print(f"  Tipo: {result['content_type']}")
        print(f"  SHA-256: {result['hash']}")


if __name__ == "__main__":
    test_downloader()
```

---

## Ejercicio 3: Descargas Múltiples Async ⭐⭐⭐⭐⭐

### Descripción
Descargar múltiples archivos concurrentemente usando httpx async.

### Tareas

**Parte A: Cliente Asíncrono**

```python
import asyncio

class AsyncHTTPClient:
    """Cliente HTTP asíncrono con httpx."""
    
    def __init__(
        self,
        timeout: float = 30.0,
        max_retries: int = 3,
        http2: bool = True
    ):
        self.timeout = httpx.Timeout(connect=5.0, read=timeout, write=5.0, pool=10.0)
        self.limits = httpx.Limits(max_keepalive_connections=50, max_connections=200)
        self.max_retries = max_retries
        
        self.client = httpx.AsyncClient(
            timeout=self.timeout,
            limits=self.limits,
            http2=http2,
            follow_redirects=True
        )
    
    async def get(self, url: str, **kwargs) -> httpx.Response:
        """GET async con reintentos."""
        for attempt in range(self.max_retries):
            try:
                response = await self.client.get(url, **kwargs)
                response.raise_for_status()
                return response
            
            except (httpx.HTTPStatusError, httpx.TimeoutException) as e:
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Reintentando en {wait_time}s...")
                    await asyncio.sleep(wait_time)
                else:
                    raise
    
    async def download_file(
        self,
        url: str,
        output_file: Path,
        chunk_size: int = 8192
    ) -> Dict[str, Any]:
        """Descarga archivo async."""
        logger.info(f"Descargando async: {url}")
        
        async with self.client.stream('GET', url) as response:
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with output_file.open('wb') as f:
                async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                    f.write(chunk)
                    downloaded += len(chunk)
        
        return {
            'url': url,
            'file': str(output_file),
            'size': downloaded
        }
    
    async def close(self):
        """Cerrar cliente."""
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.close()
```

**Parte B: Descargar Múltiples Archivos**

```python
async def download_multiple(urls: list[tuple[str, Path]]):
    """Descarga múltiples archivos concurrentemente."""
    async with AsyncHTTPClient() as client:
        tasks = [
            client.download_file(url, output_file)
            for url, output_file in urls
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Procesar resultados
        exitosos = 0
        fallidos = 0
        
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"✗ Descarga falló: {result}")
                fallidos += 1
            else:
                logger.info(f"✓ {result['file']}: {result['size']:,} bytes")
                exitosos += 1
        
        print(f"\n✓ Completado: {exitosos} exitosos, {fallidos} fallidos")


async def test_async_downloads():
    """Prueba descargas async múltiples."""
    urls = [
        ('https://httpbin.org/image/png', Path('downloads/async_img1.png')),
        ('https://httpbin.org/image/jpeg', Path('downloads/async_img2.jpg')),
        ('https://httpbin.org/image/webp', Path('downloads/async_img3.webp')),
    ]
    
    await download_multiple(urls)


if __name__ == "__main__":
    asyncio.run(test_async_downloads())
```

---

## Ejercicio 4: Sistema Completo ⭐⭐⭐⭐⭐

### Descripción
Integrar todo en un sistema de descarga production-ready.

### Tareas

**Sistema Integrado:**

```python
"""
Sistema de descarga robusto completo.

Características:
- Cliente HTTP con reintentos y timeouts
- Streaming de archivos grandes
- Verificación de integridad
- Descargas concurrentes
- Logging completo
- Manejo de errores
"""

import click
from datetime import datetime


class DownloadManager:
    """Gestor de descargas robusto."""
    
    def __init__(
        self,
        output_dir: Path = Path('downloads'),
        max_concurrent: int = 5
    ):
        self.output_dir = output_dir
        self.max_concurrent = max_concurrent
        self.client = HTTPClient(max_retries=3, timeout=60.0)
        self.downloader = FileDownloader(self.client)
        
        # Crear directorio de salida
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"DownloadManager inicializado: {output_dir}")
    
    def download(
        self,
        url: str,
        filename: Optional[str] = None,
        verify_hash: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Descarga un archivo.
        
        Args:
            url: URL a descargar
            filename: Nombre de archivo (opcional, se infiere de URL)
            verify_hash: SHA-256 esperado
        
        Returns:
            Metadata de descarga
        """
        # Determinar nombre de archivo
        if not filename:
            filename = Path(url).name or f"download_{int(time.time())}"
        
        output_file = self.output_dir / filename
        
        # Descargar
        result = self.downloader.download(
            url=url,
            output_file=output_file,
            verify_hash=verify_hash,
            show_progress=True
        )
        
        return result
    
    def download_list(self, downloads: list[dict]) -> list[Dict]:
        """
        Descarga lista de archivos.
        
        Args:
            downloads: Lista de dicts con {'url', 'filename', 'hash'}
        
        Returns:
            Lista de resultados
        """
        results = []
        
        for item in downloads:
            try:
                result = self.download(
                    url=item['url'],
                    filename=item.get('filename'),
                    verify_hash=item.get('hash')
                )
                results.append(result)
            
            except Exception as e:
                logger.error(f"Error descargando {item['url']}: {e}")
                results.append({
                    'url': item['url'],
                    'error': str(e)
                })
        
        return results
    
    def cleanup(self):
        """Cerrar recursos."""
        self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.cleanup()


# CLI con Click
@click.command()
@click.argument('url')
@click.option('--output', '-o', help='Archivo de salida')
@click.option('--hash', '-h', help='SHA-256 esperado')
@click.option('--dir', '-d', default='downloads', help='Directorio de salida')
def cli_download(url, output, hash, dir):
    """Descarga archivo con verificación."""
    with DownloadManager(output_dir=Path(dir)) as manager:
        result = manager.download(url, filename=output, verify_hash=hash)
        
        click.echo(f"\n✓ Descarga completada:")
        click.echo(f"  Archivo: {result['output_file']}")
        click.echo(f"  Tamaño: {result['size']:,} bytes")
        click.echo(f"  SHA-256: {result['hash']}")


if __name__ == "__main__":
    # Ejecutar CLI
    # cli_download()
    
    # O usar programáticamente
    with DownloadManager() as manager:
        # Descargar múltiples archivos
        downloads = [
            {
                'url': 'https://httpbin.org/image/png',
                'filename': 'test1.png'
            },
            {
                'url': 'https://httpbin.org/image/jpeg',
                'filename': 'test2.jpg'
            }
        ]
        
        results = manager.download_list(downloads)
        
        print(f"\n✓ Completado: {len(results)} archivos")
```

---

## Recursos

- [httpx Documentation](https://www.python-httpx.org/)
- [Tenacity Retry Library](https://tenacity.readthedocs.io/)
- [tqdm Progress Bars](https://tqdm.github.io/)
- [Click CLI Framework](https://click.palletsprojects.com/)
