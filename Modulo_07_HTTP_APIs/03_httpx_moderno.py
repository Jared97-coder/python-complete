"""
Módulo 7.3: httpx - Cliente HTTP Moderno

httpx es el sucesor moderno de requests con soporte HTTP/2 y
API unificada para operaciones síncronas y asíncronas.

Instalación:
    pip install httpx
    pip install httpx[http2]  # Para soporte HTTP/2

Documentación:
    https://www.python-httpx.org/
"""

import httpx
import asyncio
import time
from typing import Dict, List
from pathlib import Path


# =============================================================================
# Ejemplo 1: API Compatible con Requests
# =============================================================================

def ejemplo_compatibilidad_requests():
    """httpx tiene API muy similar a requests."""
    print("\n" + "="*60)
    print("Ejemplo 1: Compatibilidad con Requests")
    print("="*60)
    
    # Muy similar a requests
    response = httpx.get('https://jsonplaceholder.typicode.com/posts/1')
    
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    
    data = response.json()
    print(f"\nPost: {data['title']}")


# =============================================================================
# Ejemplo 2: Cliente Síncrono vs Asíncrono
# =============================================================================

def ejemplo_sync():
    """Cliente síncrono."""
    print("\n" + "="*60)
    print("Ejemplo 2a: Cliente Síncrono")
    print("="*60)
    
    # Cliente síncrono
    with httpx.Client() as client:
        response = client.get('https://jsonplaceholder.typicode.com/posts/1')
        data = response.json()
        print(f"Sync - Post: {data['title']}")


async def ejemplo_async():
    """Cliente asíncrono."""
    print("\n" + "="*60)
    print("Ejemplo 2b: Cliente Asíncrono")
    print("="*60)
    
    # Cliente asíncrono
    async with httpx.AsyncClient() as client:
        response = await client.get('https://jsonplaceholder.typicode.com/posts/1')
        data = response.json()
        print(f"Async - Post: {data['title']}")


# =============================================================================
# Ejemplo 3: HTTP/2 Support
# =============================================================================

async def ejemplo_http2():
    """Usar HTTP/2 para mejor performance."""
    print("\n" + "="*60)
    print("Ejemplo 3: HTTP/2")
    print("="*60)
    
    # Habilitar HTTP/2
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get('https://www.google.com')
        
        print(f"HTTP Version: {response.http_version}")
        print(f"Status: {response.status_code}")
        
        # HTTP/2 permite multiplexing (múltiples requests en misma conexión)
        urls = [
            'https://jsonplaceholder.typicode.com/posts/1',
            'https://jsonplaceholder.typicode.com/posts/2',
            'https://jsonplaceholder.typicode.com/posts/3'
        ]
        
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        
        print(f"\n✓ {len(responses)} requests via HTTP/2 multiplexing")


# =============================================================================
# Ejemplo 4: Timeouts Granulares
# =============================================================================

def ejemplo_timeouts_granulares():
    """Configurar timeouts muy específicos."""
    print("\n" + "="*60)
    print("Ejemplo 4: Timeouts Granulares")
    print("="*60)
    
    # Timeout de 5 segundos total
    try:
        response = httpx.get(
            'https://httpbin.org/delay/2',
            timeout=5.0
        )
        print(f"✓ Request completado: {response.status_code}")
    except httpx.TimeoutException:
        print("✗ Timeout")
    
    # Timeouts granulares
    timeout = httpx.Timeout(
        connect=3.0,  # Tiempo para conectar
        read=5.0,  # Tiempo para leer respuesta
        write=5.0,  # Tiempo para enviar request
        pool=10.0  # Tiempo obteniendo conexión del pool
    )
    
    with httpx.Client(timeout=timeout) as client:
        response = client.get('https://httpbin.org/delay/1')
        print(f"✓ Request con timeout granular: {response.status_code}")


# =============================================================================
# Ejemplo 5: Límites de Conexión
# =============================================================================

async def ejemplo_limites_conexion():
    """Controlar límites de conexiones concurrentes."""
    print("\n" + "="*60)
    print("Ejemplo 5: Límites de Conexión")
    print("="*60)
    
    # Configurar límites
    limits = httpx.Limits(
        max_keepalive_connections=20,  # Máximo de conexiones keep-alive
        max_connections=100,  # Máximo total de conexiones
        keepalive_expiry=30.0  # Tiempo antes de cerrar conexión inactiva
    )
    
    async with httpx.AsyncClient(limits=limits) as client:
        # Hacer múltiples requests
        urls = [f'https://jsonplaceholder.typicode.com/posts/{i}' for i in range(1, 11)]
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        
        print(f"✓ {len(responses)} requests con límites de conexión configurados")


# =============================================================================
# Ejemplo 6: Event Hooks
# =============================================================================

def log_request(request):
    """Hook que se ejecuta antes de enviar request."""
    print(f"  → {request.method} {request.url}")


def log_response(response):
    """Hook que se ejecuta después de recibir response."""
    request = response.request
    print(f"  ← {response.status_code} {request.url}")


def ejemplo_event_hooks():
    """Usar hooks para logging y debugging."""
    print("\n" + "="*60)
    print("Ejemplo 6: Event Hooks")
    print("="*60)
    
    # Crear cliente con hooks
    client = httpx.Client(
        event_hooks={
            'request': [log_request],
            'response': [log_response]
        }
    )
    
    with client:
        print("Haciendo requests (con logging automático):")
        client.get('https://jsonplaceholder.typicode.com/posts/1')
        client.get('https://jsonplaceholder.typicode.com/users/1')


# =============================================================================
# Ejemplo 7: Custom Transport (Testing)
# =============================================================================

class MockTransport(httpx.BaseTransport):
    """Transport personalizado para testing."""
    
    def handle_request(self, request):
        """Maneja request sin hacer llamada real."""
        return httpx.Response(
            200,
            json={'mocked': True, 'url': str(request.url)},
            request=request
        )


def ejemplo_custom_transport():
    """Usar transport personalizado para testing."""
    print("\n" + "="*60)
    print("Ejemplo 7: Custom Transport (Testing)")
    print("="*60)
    
    # Cliente con transport mockeado
    client = httpx.Client(transport=MockTransport())
    
    response = client.get('https://api.example.com/data')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("✓ Request mockeado (sin llamada HTTP real)")


# =============================================================================
# Ejemplo 8: Streaming de Respuestas
# =============================================================================

def ejemplo_streaming_response():
    """Procesar respuesta en streaming."""
    print("\n" + "="*60)
    print("Ejemplo 8: Streaming de Respuestas")
    print("="*60)
    
    with httpx.stream('GET', 'https://httpbin.org/stream/5') as response:
        print("Procesando líneas en streaming:")
        for line in response.iter_lines():
            if line:
                import json
                data = json.loads(line)
                print(f"  - {data['url']}")


# =============================================================================
# Ejemplo 9: Descargar Archivo con Progress
# =============================================================================

def ejemplo_download_con_progress():
    """Descargar archivo mostrando progreso."""
    print("\n" + "="*60)
    print("Ejemplo 9: Download con Progress")
    print("="*60)
    
    url = 'https://httpbin.org/image/png'
    output_file = Path("httpx_download.png")
    
    with httpx.stream('GET', url) as response:
        total = int(response.headers.get('content-length', 0))
        
        print(f"Descargando {total} bytes...")
        downloaded = 0
        
        with output_file.open('wb') as f:
            for chunk in response.iter_bytes(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                
                # Mostrar progreso
                percent = (downloaded / total) * 100 if total > 0 else 0
                print(f"  Progreso: {percent:.1f}%", end='\r')
        
        print(f"\n✓ Descargado: {output_file} ({downloaded} bytes)")
    
    # Limpiar
    if output_file.exists():
        output_file.unlink()


# =============================================================================
# Ejemplo 10: Reintentos Integrados
# =============================================================================

def ejemplo_reintentos():
    """httpx con reintentos usando httpx-retry."""
    print("\n" + "="*60)
    print("Ejemplo 10: Reintentos (manual)")
    print("="*60)
    
    def request_with_retry(url, max_retries=3):
        """Request con reintentos manuales."""
        for attempt in range(max_retries):
            try:
                response = httpx.get(url, timeout=5.0)
                response.raise_for_status()
                return response
            except (httpx.HTTPStatusError, httpx.TimeoutException) as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"  Reintento {attempt + 1} en {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise
    
    try:
        response = request_with_retry('https://httpbin.org/status/200,500,502')
        print(f"✓ Exitoso: {response.status_code}")
    except Exception as e:
        print(f"✗ Falló: {e}")


# =============================================================================
# Ejemplo 11: Manejo de Redirects
# =============================================================================

def ejemplo_redirects():
    """Manejar redirects."""
    print("\n" + "="*60)
    print("Ejemplo 11: Redirects")
    print("="*60)
    
    # Seguir redirects automáticamente (default)
    response = httpx.get('https://httpbin.org/redirect/3')
    print(f"URL final: {response.url}")
    print(f"Redirects: {len(response.history)}")
    
    # No seguir redirects
    response = httpx.get(
        'https://httpbin.org/redirect/3',
        follow_redirects=False
    )
    print(f"\nSin seguir redirects:")
    print(f"Status: {response.status_code}")
    print(f"Location: {response.headers.get('location')}")


# =============================================================================
# Ejemplo 12: Autenticación
# =============================================================================

def ejemplo_autenticacion():
    """Diferentes tipos de autenticación."""
    print("\n" + "="*60)
    print("Ejemplo 12: Autenticación")
    print("="*60)
    
    # Basic Auth
    response = httpx.get(
        'https://httpbin.org/basic-auth/user/pass',
        auth=('user', 'pass')
    )
    print(f"Basic Auth: {response.json()['authenticated']}")
    
    # Bearer Token
    headers = {'Authorization': 'Bearer mi-token'}
    response = httpx.get('https://httpbin.org/bearer', headers=headers)
    print(f"Bearer Auth: {response.json()['authenticated']}")
    
    # Custom Auth Class
    class APIKeyAuth(httpx.Auth):
        def __init__(self, api_key):
            self.api_key = api_key
        
        def auth_flow(self, request):
            request.headers['X-API-Key'] = self.api_key
            yield request
    
    client = httpx.Client(auth=APIKeyAuth('my-api-key-123'))
    response = client.get('https://httpbin.org/headers')
    print(f"API Key en headers: {'X-Api-Key' in response.json()['headers']}")


# =============================================================================
# Ejemplo 13: Request Files (Multipart)
# =============================================================================

def ejemplo_upload_files():
    """Subir archivos."""
    print("\n" + "="*60)
    print("Ejemplo 13: Upload de Archivos")
    print("="*60)
    
    # Crear archivo temporal
    temp_file = Path("httpx_upload.txt")
    temp_file.write_text("Contenido de prueba httpx")
    
    try:
        # Upload simple
        with temp_file.open('rb') as f:
            files = {'file': f}
            response = httpx.post('https://httpbin.org/post', files=files)
        
        print(f"Status: {response.status_code}")
        print(f"Archivo subido: {list(response.json()['files'].keys())}")
        
        # Upload con metadata
        with temp_file.open('rb') as f:
            files = {'file': ('documento.txt', f, 'text/plain')}
            data = {'descripcion': 'Mi archivo'}
            response = httpx.post(
                'https://httpbin.org/post',
                files=files,
                data=data
            )
        
        print(f"Con metadata: {response.json()['form']}")
    
    finally:
        if temp_file.exists():
            temp_file.unlink()


# =============================================================================
# Ejemplo 14: Cliente API Robusto
# =============================================================================

class HTTPXAPIClient:
    """Cliente API robusto con httpx."""
    
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url
        
        # Configuración avanzada
        timeout = httpx.Timeout(connect=5.0, read=10.0, write=5.0, pool=10.0)
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
        
        headers = {'User-Agent': 'HTTPXClient/1.0'}
        if api_key:
            headers['X-API-Key'] = api_key
        
        self.client = httpx.Client(
            base_url=base_url,
            headers=headers,
            timeout=timeout,
            limits=limits,
            follow_redirects=True
        )
    
    def get(self, endpoint: str, **kwargs):
        """GET request."""
        response = self.client.get(endpoint, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint: str, **kwargs):
        """POST request."""
        response = self.client.post(endpoint, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def close(self):
        """Cerrar cliente."""
        self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()


def ejemplo_cliente_robusto():
    """Usar cliente API robusto."""
    print("\n" + "="*60)
    print("Ejemplo 14: Cliente API Robusto")
    print("="*60)
    
    with HTTPXAPIClient('https://jsonplaceholder.typicode.com') as api:
        # GET
        post = api.get('/posts/1')
        print(f"Post obtenido: {post['title']}")
        
        # POST
        nuevo = api.post('/posts', json={
            'title': 'Nuevo Post',
            'body': 'Contenido',
            'userId': 1
        })
        print(f"Post creado: ID {nuevo['id']}")


# =============================================================================
# Ejemplo 15: Async Client Avanzado
# =============================================================================

async def ejemplo_async_avanzado():
    """Cliente asíncrono con configuración avanzada."""
    print("\n" + "="*60)
    print("Ejemplo 15: Cliente Async Avanzado")
    print("="*60)
    
    # Configuración completa
    timeout = httpx.Timeout(10.0)
    limits = httpx.Limits(max_keepalive_connections=50, max_connections=200)
    
    async with httpx.AsyncClient(
        timeout=timeout,
        limits=limits,
        http2=True,  # Habilitar HTTP/2
        follow_redirects=True
    ) as client:
        # Requests concurrentes
        urls = [f'https://jsonplaceholder.typicode.com/posts/{i}' for i in range(1, 11)]
        
        inicio = time.time()
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        duracion = time.time() - inicio
        
        print(f"✓ {len(responses)} requests en {duracion:.2f}s")
        
        # Procesar respuestas
        for i, response in enumerate(responses[:3], 1):
            data = response.json()
            print(f"  {i}. {data['title'][:40]}...")


# =============================================================================
# Ejemplo 16: Comparison: Sync vs Async
# =============================================================================

def fetch_sync():
    """Fetch síncrono."""
    with httpx.Client() as client:
        for i in range(1, 11):
            client.get(f'https://jsonplaceholder.typicode.com/posts/{i}')


async def fetch_async():
    """Fetch asíncrono."""
    async with httpx.AsyncClient() as client:
        tasks = [
            client.get(f'https://jsonplaceholder.typicode.com/posts/{i}')
            for i in range(1, 11)
        ]
        await asyncio.gather(*tasks)


async def ejemplo_comparacion():
    """Comparar sync vs async."""
    print("\n" + "="*60)
    print("Ejemplo 16: Sync vs Async Comparison")
    print("="*60)
    
    # Sync
    inicio = time.time()
    fetch_sync()
    tiempo_sync = time.time() - inicio
    
    # Async
    inicio = time.time()
    await fetch_async()
    tiempo_async = time.time() - inicio
    
    print(f"Sync:  {tiempo_sync:.2f}s")
    print(f"Async: {tiempo_async:.2f}s")
    print(f"⚡ Speedup: {tiempo_sync/tiempo_async:.1f}x")


# =============================================================================
# Main: Ejecutar Ejemplos
# =============================================================================

async def main_async():
    """Ejecuta ejemplos asíncronos."""
    await ejemplo_async()
    await ejemplo_http2()
    await ejemplo_limites_conexion()
    await ejemplo_async_avanzado()
    await ejemplo_comparacion()


def main():
    """Ejecuta todos los ejemplos."""
    print("\n" + "="*60)
    print("MÓDULO 7.3: HTTPX - CLIENTE HTTP MODERNO")
    print("="*60)
    
    # Ejemplos síncronos
    ejemplo_compatibilidad_requests()
    ejemplo_sync()
    ejemplo_timeouts_granulares()
    ejemplo_event_hooks()
    ejemplo_custom_transport()
    ejemplo_streaming_response()
    ejemplo_download_con_progress()
    ejemplo_reintentos()
    ejemplo_redirects()
    ejemplo_autenticacion()
    ejemplo_upload_files()
    ejemplo_cliente_robusto()
    
    # Ejemplos asíncronos
    asyncio.run(main_async())
    
    print("\n" + "="*60)
    print("✓ Ejemplos completados")
    print("="*60)


if __name__ == "__main__":
    main()
