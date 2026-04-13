"""
Módulo 7.2: aiohttp - Cliente HTTP Asíncrono

aiohttp es la biblioteca líder para HTTP asíncrono en Python.
Permite hacer múltiples requests concurrentes de forma eficiente.

Instalación:
    pip install aiohttp

Documentación:
    https://docs.aiohttp.org/
"""

import asyncio
import aiohttp
import time
import json
from typing import List, Dict, Any
from pathlib import Path


# =============================================================================
# Ejemplo 1: Request GET Asíncrono Básico
# =============================================================================

async def ejemplo_get_async_basico():
    """GET asíncrono simple."""
    print("\n" + "="*60)
    print("Ejemplo 1: GET Asíncrono Básico")
    print("="*60)
    
    # ClientSession maneja conexiones y cookies
    async with aiohttp.ClientSession() as session:
        url = 'https://jsonplaceholder.typicode.com/posts/1'
        
        async with session.get(url) as response:
            print(f"Status: {response.status}")
            print(f"Content-Type: {response.headers['content-type']}")
            
            # Leer respuesta JSON
            data = await response.json()
            print(f"\nTítulo: {data['title']}")
            print(f"Body: {data['body'][:50]}...")


# =============================================================================
# Ejemplo 2: Múltiples Requests Concurrentes
# =============================================================================

async def fetch_post(session: aiohttp.ClientSession, post_id: int) -> Dict:
    """Obtiene un post específico."""
    url = f'https://jsonplaceholder.typicode.com/posts/{post_id}'
    
    async with session.get(url) as response:
        return await response.json()


async def ejemplo_requests_concurrentes():
    """Hacer múltiples requests en paralelo."""
    print("\n" + "="*60)
    print("Ejemplo 2: Requests Concurrentes")
    print("="*60)
    
    # Medir tiempo
    inicio = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Crear tareas para 10 posts
        tasks = [fetch_post(session, i) for i in range(1, 11)]
        
        # Ejecutar todas concurrentemente
        posts = await asyncio.gather(*tasks)
    
    duracion = time.time() - inicio
    
    print(f"✓ {len(posts)} posts obtenidos en {duracion:.2f} segundos")
    print("\nPrimeros 3:")
    for post in posts[:3]:
        print(f"  - Post {post['id']}: {post['title'][:40]}...")


# =============================================================================
# Ejemplo 3: POST con JSON
# =============================================================================

async def ejemplo_post_async():
    """Enviar datos con POST."""
    print("\n" + "="*60)
    print("Ejemplo 3: POST Asíncrono")
    print("="*60)
    
    nuevo_post = {
        'title': 'Async Post',
        'body': 'Creado con aiohttp',
        'userId': 1
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'https://jsonplaceholder.typicode.com/posts',
            json=nuevo_post
        ) as response:
            print(f"Status: {response.status}")
            
            data = await response.json()
            print(f"Post creado - ID: {data['id']}")
            print(f"Título: {data['title']}")


# =============================================================================
# Ejemplo 4: Headers y Parámetros
# =============================================================================

async def ejemplo_headers_params():
    """Enviar headers y parámetros."""
    print("\n" + "="*60)
    print("Ejemplo 4: Headers y Parámetros")
    print("="*60)
    
    headers = {
        'User-Agent': 'aiohttp-client/1.0',
        'Accept': 'application/json'
    }
    
    params = {
        'userId': 1,
        '_limit': 5
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(
            'https://jsonplaceholder.typicode.com/posts',
            params=params
        ) as response:
            posts = await response.json()
            
            print(f"Obtenidos {len(posts)} posts del usuario 1")
            for post in posts:
                print(f"  - {post['title'][:40]}...")


# =============================================================================
# Ejemplo 5: Timeouts
# =============================================================================

async def ejemplo_timeouts_async():
    """Configurar timeouts."""
    print("\n" + "="*60)
    print("Ejemplo 5: Timeouts")
    print("="*60)
    
    # Timeout de 5 segundos
    timeout = aiohttp.ClientTimeout(total=5)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            # Este endpoint se demora 3 segundos
            async with session.get('https://httpbin.org/delay/3') as response:
                data = await response.json()
                print(f"✓ Request completado: {response.status}")
        
        except asyncio.TimeoutError:
            print("✗ Timeout alcanzado")
    
    # Timeout granular
    timeout_granular = aiohttp.ClientTimeout(
        total=10,  # Timeout total
        connect=3,  # Timeout de conexión
        sock_read=5  # Timeout de lectura
    )
    
    async with aiohttp.ClientSession(timeout=timeout_granular) as session:
        try:
            async with session.get('https://httpbin.org/delay/1') as response:
                print(f"✓ Request con timeout granular: {response.status}")
        except asyncio.TimeoutError:
            print("✗ Timeout alcanzado")


# =============================================================================
# Ejemplo 6: Manejo de Errores
# =============================================================================

async def ejemplo_manejo_errores_async():
    """Manejar errores en requests asíncronos."""
    print("\n" + "="*60)
    print("Ejemplo 6: Manejo de Errores")
    print("="*60)
    
    async with aiohttp.ClientSession() as session:
        # Error 404
        try:
            async with session.get(
                'https://jsonplaceholder.typicode.com/posts/99999'
            ) as response:
                if response.status == 404:
                    print("✗ Recurso no encontrado (404)")
                else:
                    response.raise_for_status()
                    data = await response.json()
                    print(f"✓ Datos: {data}")
        
        except aiohttp.ClientError as e:
            print(f"✗ Error del cliente: {e}")
        
        except asyncio.TimeoutError:
            print("✗ Timeout")
        
        # Error de red (dominio inválido)
        try:
            async with session.get('https://sitio-que-no-existe-12345.com') as response:
                pass
        except aiohttp.ClientConnectorError:
            print("✗ Error de conexión - dominio no válido")


# =============================================================================
# Ejemplo 7: Streaming de Respuestas
# =============================================================================

async def ejemplo_streaming_async():
    """Procesar respuestas en streaming."""
    print("\n" + "="*60)
    print("Ejemplo 7: Streaming de Respuestas")
    print("="*60)
    
    async with aiohttp.ClientSession() as session:
        async with session.get('https://httpbin.org/stream/5') as response:
            print("Procesando respuesta en streaming:")
            
            # Leer línea por línea
            async for line in response.content:
                if line:
                    try:
                        data = json.loads(line)
                        print(f"  - URL: {data['url']}")
                    except json.JSONDecodeError:
                        pass


# =============================================================================
# Ejemplo 8: Descargar Archivo con Streaming
# =============================================================================

async def ejemplo_download_streaming():
    """Descargar archivo sin cargarlo completamente en memoria."""
    print("\n" + "="*60)
    print("Ejemplo 8: Download con Streaming")
    print("="*60)
    
    url = 'https://httpbin.org/image/png'
    output_file = Path("async_download.png")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"Descargando... (Content-Length: {response.headers.get('content-length')} bytes)")
            
            # Escribir en chunks
            with output_file.open('wb') as f:
                async for chunk in response.content.iter_chunked(8192):
                    f.write(chunk)
    
    print(f"✓ Archivo descargado: {output_file}")
    print(f"  Tamaño: {output_file.stat().st_size} bytes")
    
    # Limpiar
    if output_file.exists():
        output_file.unlink()


# =============================================================================
# Ejemplo 9: Sesión con Configuración Personalizada
# =============================================================================

async def ejemplo_sesion_personalizada():
    """Crear sesión con configuración avanzada."""
    print("\n" + "="*60)
    print("Ejemplo 9: Sesión Personalizada")
    print("="*60)
    
    # Configurar timeout
    timeout = aiohttp.ClientTimeout(total=10)
    
    # Configurar headers
    headers = {
        'User-Agent': 'MiApp/1.0',
        'Accept': 'application/json'
    }
    
    # Crear sesión con configuración
    connector = aiohttp.TCPConnector(
        limit=100,  # Máximo de conexiones totales
        limit_per_host=10,  # Máximo por host
        ttl_dns_cache=300  # Cache DNS por 5 minutos
    )
    
    async with aiohttp.ClientSession(
        timeout=timeout,
        headers=headers,
        connector=connector
    ) as session:
        async with session.get('https://httpbin.org/headers') as response:
            data = await response.json()
            print("Headers enviados:")
            for key, value in data['headers'].items():
                print(f"  {key}: {value}")


# =============================================================================
# Ejemplo 10: Autenticación Basic
# =============================================================================

async def ejemplo_auth_basic_async():
    """Autenticación HTTP Basic."""
    print("\n" + "="*60)
    print("Ejemplo 10: Autenticación Basic")
    print("="*60)
    
    auth = aiohttp.BasicAuth('usuario', 'password123')
    
    async with aiohttp.ClientSession() as session:
        async with session.get(
            'https://httpbin.org/basic-auth/usuario/password123',
            auth=auth
        ) as response:
            print(f"Status: {response.status}")
            data = await response.json()
            print(f"Autenticado: {data['authenticated']}")


# =============================================================================
# Ejemplo 11: Reintentos Manuales
# =============================================================================

async def fetch_with_retry(
    session: aiohttp.ClientSession,
    url: str,
    max_retries: int = 3
) -> Dict[str, Any]:
    """Hace request con reintentos."""
    for intento in range(max_retries):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status >= 500:
                    # Error del servidor, reintentar
                    if intento < max_retries - 1:
                        await asyncio.sleep(2 ** intento)  # Backoff exponencial
                        continue
                else:
                    # Error del cliente (4xx), no reintentar
                    response.raise_for_status()
        
        except aiohttp.ClientError as e:
            if intento < max_retries - 1:
                await asyncio.sleep(2 ** intento)
                continue
            raise
    
    raise Exception(f"Falló después de {max_retries} reintentos")


async def ejemplo_reintentos_async():
    """Implementar reintentos."""
    print("\n" + "="*60)
    print("Ejemplo 11: Reintentos")
    print("="*60)
    
    async with aiohttp.ClientSession() as session:
        try:
            # Este endpoint falla aleatoriamente
            data = await fetch_with_retry(
                session,
                'https://httpbin.org/status/200,500,503',
                max_retries=3
            )
            print("✓ Request exitoso después de posibles reintentos")
        except Exception as e:
            print(f"✗ Falló después de reintentos: {e}")


# =============================================================================
# Ejemplo 12: Rate Limiting
# =============================================================================

class RateLimiter:
    """Rate limiter simple para async."""
    
    def __init__(self, rate: int, per: float):
        """
        Args:
            rate: Número de requests permitidos
            per: Período de tiempo en segundos
        """
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = time.time()
    
    async def acquire(self):
        """Espera si se excede el rate limit."""
        current = time.time()
        time_passed = current - self.last_check
        self.last_check = current
        
        self.allowance += time_passed * (self.rate / self.per)
        
        if self.allowance > self.rate:
            self.allowance = self.rate
        
        if self.allowance < 1.0:
            sleep_time = (1.0 - self.allowance) * (self.per / self.rate)
            await asyncio.sleep(sleep_time)
            self.allowance = 0.0
        else:
            self.allowance -= 1.0


async def ejemplo_rate_limiting():
    """Rate limiting para evitar sobrecargar API."""
    print("\n" + "="*60)
    print("Ejemplo 12: Rate Limiting")
    print("="*60)
    
    # Máximo 5 requests por segundo
    limiter = RateLimiter(rate=5, per=1.0)
    
    async with aiohttp.ClientSession() as session:
        inicio = time.time()
        
        # Intentar hacer 10 requests
        for i in range(10):
            await limiter.acquire()
            
            async with session.get('https://httpbin.org/uuid') as response:
                data = await response.json()
                print(f"  Request {i+1}: {data['uuid']}")
        
        duracion = time.time() - inicio
        print(f"\n✓ 10 requests completados en {duracion:.2f}s (rate limited)")


# =============================================================================
# Ejemplo 13: Web Scraping Concurrente
# =============================================================================

async def scrape_url(session: aiohttp.ClientSession, url: str) -> Dict:
    """Scrapea una URL."""
    async with session.get(url) as response:
        data = await response.json()
        return {
            'id': data['id'],
            'title': data['title'],
            'url': url
        }


async def ejemplo_scraping_concurrente():
    """Scraping de múltiples URLs concurrentemente."""
    print("\n" + "="*60)
    print("Ejemplo 13: Web Scraping Concurrente")
    print("="*60)
    
    # URLs a scrapear
    urls = [f'https://jsonplaceholder.typicode.com/posts/{i}' for i in range(1, 21)]
    
    inicio = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Crear tareas para todas las URLs
        tasks = [scrape_url(session, url) for url in urls]
        
        # Ejecutar todas concurrentemente
        results = await asyncio.gather(*tasks)
    
    duracion = time.time() - inicio
    
    print(f"✓ {len(results)} páginas scrapeadas en {duracion:.2f}s")
    print("\nPrimeras 5:")
    for result in results[:5]:
        print(f"  - [{result['id']}] {result['title'][:40]}...")


# =============================================================================
# Ejemplo 14: Cliente API Asíncrono
# =============================================================================

class AsyncJSONPlaceholderAPI:
    """Cliente asíncrono para JSONPlaceholder API."""
    
    BASE_URL = 'https://jsonplaceholder.typicode.com'
    
    def __init__(self):
        timeout = aiohttp.ClientTimeout(total=10)
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            headers={'User-Agent': 'AsyncClient/1.0'}
        )
    
    async def close(self):
        """Cerrar sesión."""
        await self.session.close()
    
    async def _get(self, endpoint: str, params: Dict = None) -> Any:
        """Helper para GET."""
        url = f"{self.BASE_URL}/{endpoint}"
        async with self.session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()
    
    async def _post(self, endpoint: str, data: Dict) -> Any:
        """Helper para POST."""
        url = f"{self.BASE_URL}/{endpoint}"
        async with self.session.post(url, json=data) as response:
            response.raise_for_status()
            return await response.json()
    
    async def get_posts(self, user_id: int = None) -> List[Dict]:
        """Obtener posts."""
        params = {'userId': user_id} if user_id else None
        return await self._get('posts', params=params)
    
    async def get_post(self, post_id: int) -> Dict:
        """Obtener post específico."""
        return await self._get(f'posts/{post_id}')
    
    async def create_post(self, title: str, body: str, user_id: int) -> Dict:
        """Crear nuevo post."""
        data = {'title': title, 'body': body, 'userId': user_id}
        return await self._post('posts', data)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.close()


async def ejemplo_cliente_api_async():
    """Usar cliente API asíncrono."""
    print("\n" + "="*60)
    print("Ejemplo 14: Cliente API Asíncrono")
    print("="*60)
    
    async with AsyncJSONPlaceholderAPI() as api:
        # Obtener posts
        posts = await api.get_posts(user_id=1)
        print(f"Posts del usuario 1: {len(posts)}")
        
        # Obtener post específico
        post = await api.get_post(1)
        print(f"\nPost #1: {post['title']}")
        
        # Crear nuevo post
        nuevo = await api.create_post(
            title='Async Post',
            body='Creado con cliente asíncrono',
            user_id=1
        )
        print(f"\nPost creado - ID: {nuevo['id']}")


# =============================================================================
# Ejemplo 15: Comparación Síncrono vs Asíncrono
# =============================================================================

async def fetch_one_by_one():
    """Requests secuenciales (uno por uno)."""
    async with aiohttp.ClientSession() as session:
        for i in range(1, 11):
            url = f'https://jsonplaceholder.typicode.com/posts/{i}'
            async with session.get(url) as response:
                await response.json()


async def fetch_concurrently():
    """Requests concurrentes."""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 11):
            url = f'https://jsonplaceholder.typicode.com/posts/{i}'
            task = session.get(url)
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        for response in responses:
            await response.json()
            response.close()


async def ejemplo_comparacion_performance():
    """Comparar performance secuencial vs concurrente."""
    print("\n" + "="*60)
    print("Ejemplo 15: Síncrono vs Asíncrono")
    print("="*60)
    
    # Secuencial
    inicio = time.time()
    await fetch_one_by_one()
    tiempo_secuencial = time.time() - inicio
    
    # Concurrente
    inicio = time.time()
    await fetch_concurrently()
    tiempo_concurrente = time.time() - inicio
    
    print(f"Secuencial (uno por uno): {tiempo_secuencial:.2f}s")
    print(f"Concurrente (paralelo):   {tiempo_concurrente:.2f}s")
    print(f"\n⚡ Speedup: {tiempo_secuencial/tiempo_concurrente:.1f}x más rápido")


# =============================================================================
# Main: Ejecutar Ejemplos
# =============================================================================

async def main():
    """Ejecuta todos los ejemplos."""
    print("\n" + "="*60)
    print("MÓDULO 7.2: AIOHTTP - CLIENTE HTTP ASÍNCRONO")
    print("="*60)
    
    ejemplos = [
        ("GET Asíncrono Básico", ejemplo_get_async_basico),
        ("Requests Concurrentes", ejemplo_requests_concurrentes),
        ("POST Asíncrono", ejemplo_post_async),
        ("Headers y Parámetros", ejemplo_headers_params),
        ("Timeouts", ejemplo_timeouts_async),
        ("Manejo de Errores", ejemplo_manejo_errores_async),
        ("Streaming", ejemplo_streaming_async),
        ("Download Streaming", ejemplo_download_streaming),
        ("Sesión Personalizada", ejemplo_sesion_personalizada),
        ("Auth Basic", ejemplo_auth_basic_async),
        ("Reintentos", ejemplo_reintentos_async),
        ("Rate Limiting", ejemplo_rate_limiting),
        ("Scraping Concurrente", ejemplo_scraping_concurrente),
        ("Cliente API", ejemplo_cliente_api_async),
        ("Comparación Performance", ejemplo_comparacion_performance),
    ]
    
    for nombre, funcion in ejemplos:
        try:
            await funcion()
        except Exception as e:
            print(f"\n✗ Error en '{nombre}': {e}")
    
    print("\n" + "="*60)
    print("✓ Ejemplos completados")
    print("="*60)


if __name__ == "__main__":
    # Ejecutar loop asíncrono
    asyncio.run(main())
