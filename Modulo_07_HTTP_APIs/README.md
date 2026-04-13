# Módulo 7: HTTP y Consumo de APIs

## Descripción General

Este módulo cubre el consumo profesional de APIs HTTP en Python, desde clientes básicos hasta implementaciones robustas y eficientes. Aprenderás a trabajar con las principales bibliotecas HTTP, manejar errores, implementar reintentos inteligentes y trabajar con streaming para optimizar memoria.

---

## Objetivos de Aprendizaje

Al completar este módulo serás capaz de:

- ✅ Consumir APIs REST con `requests`, `aiohttp` y `httpx`
- ✅ Implementar clientes HTTP robustos con manejo de errores
- ✅ Configurar timeouts, reintentos y backoff exponencial
- ✅ Usar streaming para descargas eficientes en memoria
- ✅ Trabajar con APIs asíncronas de forma concurrente
- ✅ Implementar autenticación (Basic, Bearer, OAuth)
- ✅ Testear clientes HTTP con mocks (Smocker)

---

## Contenidos

### 1. Requests - El Estándar de Facto
**Archivo:** `01_requests_basico.py`

La biblioteca más popular para HTTP en Python. Simple, elegante y suficiente para la mayoría de casos.

**Temas cubiertos:**
- GET, POST, PUT, PATCH, DELETE
- Parámetros de query y headers
- JSON automático
- Autenticación (Basic, Bearer, API Keys)
- Sesiones y cookies
- Verificación SSL
- Subida de archivos (multipart)

**Cuándo usar:**
- APIs simples
- Scripts y automatización
- Prototipos rápidos
- No necesitas HTTP/2 o async

### 2. aiohttp - HTTP Asíncrono
**Archivo:** `02_aiohttp_async.py`

Cliente y servidor HTTP asíncrono para alto rendimiento con asyncio.

**Temas cubiertos:**
- ClientSession para conexiones persistentes
- Operaciones concurrentes con `asyncio.gather()`
- Context managers asíncronos
- Streaming de respuestas
- Manejo de errores asíncronos
- Connection pooling

**Cuándo usar:**
- Necesitas hacer múltiples requests concurrentes
- APIs lentas donde puedes paralelizar
- Aplicaciones con mucho I/O
- Web scraping a escala

### 3. httpx - HTTP Moderno y Versátil
**Archivo:** `03_httpx_moderno.py`

El sucesor moderno de requests con soporte HTTP/2 y API síncrona/asíncrona unificada.

**Temas cubiertos:**
- API compatible con requests
- HTTP/2 y multiplexing
- Cliente síncrono y asíncrono
- Timeouts granulares
- Límites de conexión
- Event hooks
- Testing con mocks

**Cuándo usar:**
- Necesitas HTTP/2
- Quieres flexibilidad sync/async
- API moderna y mantenida
- Testing con transports personalizados

### 4. Timeouts, Reintentos y Resiliencia
**Archivo:** `04_timeouts_reintentos.py`

Técnicas para construir clientes HTTP robustos que manejan fallas de red.

**Temas cubiertos:**
- Tipos de timeouts (connect, read, total)
- Estrategias de reintentos (fijo, exponencial, jitter)
- Circuit breaker pattern
- Retry con urllib3 y tenacity
- Manejo de errores HTTP (4xx, 5xx)
- Rate limiting

**Cuándo usar:**
- APIs inestables o lentas
- Producción (siempre)
- Redes no confiables
- Microservicios

### 5. Streaming y Eficiencia de Memoria
**Archivo:** `05_streaming_eficiencia.py`

Técnicas para manejar respuestas grandes sin consumir memoria excesiva.

**Temas cubiertos:**
- Streaming de respuestas por chunks
- Descarga de archivos grandes
- Upload con streaming
- Procesamiento incremental (JSON lines)
- Iteradores y generadores
- Progress bars con tqdm

**Cuándo usar:**
- Archivos grandes (>100MB)
- APIs que retornan mucha data
- Memoria limitada
- Procesamiento en tiempo real

---

## Comparación de Bibliotecas

| Característica | requests | aiohttp | httpx |
|---------------|----------|---------|-------|
| **Facilidad** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **HTTP/2** | ❌ | ❌ | ✅ |
| **Async** | ❌ | ✅ | ✅ |
| **Sync** | ✅ | ❌ | ✅ |
| **Streaming** | ✅ | ✅ | ✅ |
| **Mantenimiento** | ⚠️ Bajo | ✅ Activo | ✅ Activo |
| **Ecosistema** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

**Recomendación:**
- **Proyectos nuevos:** httpx (versátil y moderno)
- **Scripts simples:** requests (más fácil)
- **Alto concurrencia:** aiohttp (más maduro en async)

---

## Dependencias

```txt
# Core
requests>=2.31.0
httpx>=0.27.0
aiohttp>=3.9.0

# Resiliencia
tenacity>=8.2.0
urllib3>=2.0.0

# Utilidades
python-dotenv>=1.0.0
pydantic>=2.0.0
tqdm>=4.66.0

# Testing
responses>=0.24.0
aioresponses>=0.7.6
pytest>=8.0.0
pytest-asyncio>=0.23.0
```

---

## Conceptos Clave

### 1. Timeouts

```python
# ❌ Sin timeout = puede colgar indefinidamente
response = requests.get('https://api.example.com/slow')

# ✅ Con timeout
response = requests.get('https://api.example.com/slow', timeout=10)

# ✅ Timeouts granulares (connect, read)
response = requests.get(
    'https://api.example.com/slow',
    timeout=(3.0, 10.0)  # 3s connect, 10s read
)
```

### 2. Reintentos

```python
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# Configurar reintentos automáticos
retry_strategy = Retry(
    total=3,
    backoff_factor=1,  # 1s, 2s, 4s
    status_forcelist=[429, 500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)
```

### 3. Streaming

```python
# ❌ Carga todo en memoria
response = requests.get('https://example.com/large-file.zip')
with open('file.zip', 'wb') as f:
    f.write(response.content)  # 1GB en memoria

# ✅ Streaming por chunks
response = requests.get('https://example.com/large-file.zip', stream=True)
with open('file.zip', 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)  # Solo 8KB en memoria
```

### 4. Async Concurrente

```python
import asyncio
import aiohttp

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# 100 requests en paralelo
urls = [f'https://api.example.com/item/{i}' for i in range(100)]
results = asyncio.run(fetch_all(urls))
```

---

## Mejores Prácticas

### 1. Siempre Usa Timeouts

```python
# ❌ NUNCA hagas esto en producción
response = requests.get(url)

# ✅ SIEMPRE especifica timeout
response = requests.get(url, timeout=10)
```

### 2. Usa Sesiones para Múltiples Requests

```python
# ❌ Ineficiente - nueva conexión cada vez
for url in urls:
    requests.get(url)

# ✅ Eficiente - reutiliza conexión
with requests.Session() as session:
    for url in urls:
        session.get(url)
```

### 3. Maneja Errores Específicos

```python
import requests

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Lanza excepción para 4xx/5xx
    
except requests.exceptions.Timeout:
    print("Request timeout")
except requests.exceptions.ConnectionError:
    print("Network error")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
        print("Not found")
    elif e.response.status_code >= 500:
        print("Server error")
except requests.exceptions.RequestException as e:
    print(f"Error general: {e}")
```

### 4. Valida Respuestas con Pydantic

```python
from pydantic import BaseModel
import requests

class User(BaseModel):
    id: int
    name: str
    email: str

response = requests.get('https://api.example.com/users/1')
user = User(**response.json())  # Validación automática
```

### 5. Logging para Debugging

```python
import logging
import requests

# Habilitar logging de requests
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.DEBUG)

# Ahora verás todos los detalles HTTP
response = requests.get('https://api.example.com/data')
```

---

## Autenticación

### API Key en Header

```python
headers = {'X-API-Key': 'tu-api-key'}
response = requests.get(url, headers=headers)
```

### Bearer Token (OAuth 2.0)

```python
headers = {'Authorization': 'Bearer tu-token-jwt'}
response = requests.get(url, headers=headers)
```

### Basic Auth

```python
from requests.auth import HTTPBasicAuth

response = requests.get(
    url,
    auth=HTTPBasicAuth('usuario', 'password')
)
```

### OAuth 2.0 Completo

```python
from requests_oauthlib import OAuth2Session

client_id = 'tu-client-id'
oauth = OAuth2Session(client_id)
authorization_url, state = oauth.authorization_url(
    'https://provider.com/oauth/authorize'
)
```

---

## Testing con Smocker

[Smocker](https://smocker.dev/) es un servidor HTTP mock para testing.

### Instalación

```bash
# Con Docker
docker run -d -p 8080:8080 -p 8081:8081 thiht/smocker

# O con Docker Compose
# Crear docker-compose.yml con configuración Smocker
```

### Uso Básico

```python
import requests

# 1. Configurar mock en Smocker
mock_config = {
    "request": {
        "method": "GET",
        "path": "/api/users/1"
    },
    "response": {
        "status": 200,
        "headers": {"Content-Type": "application/json"},
        "body": '{"id": 1, "name": "Test User"}'
    }
}

requests.post('http://localhost:8081/mocks', json=mock_config)

# 2. Hacer request a la API mockeada
response = requests.get('http://localhost:8080/api/users/1')
assert response.json() == {"id": 1, "name": "Test User"}
```

### Ventajas de Smocker

- ✅ No requiere cambios en código
- ✅ Mocks configurables vía API
- ✅ Verificación de requests recibidos
- ✅ Delays y errores configurables
- ✅ UI web para inspección

---

## Patrones de Diseño

### 1. Cliente Base Reutilizable

```python
class APIClient:
    """Cliente base para APIs."""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'User-Agent': 'MiApp/1.0'
        })
        
        # Configurar reintentos
        retry = Retry(total=3, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('https://', adapter)
    
    def get(self, endpoint: str, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        return self.session.get(url, timeout=10, **kwargs)
    
    def post(self, endpoint: str, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        return self.session.post(url, timeout=10, **kwargs)
```

### 2. Rate Limiter

```python
import time
from functools import wraps

class RateLimiter:
    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
        self.timestamps = []
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            # Limpiar timestamps antiguos
            self.timestamps = [
                ts for ts in self.timestamps
                if now - ts < self.period
            ]
            
            # Esperar si excede límite
            if len(self.timestamps) >= self.calls:
                sleep_time = self.period - (now - self.timestamps[0])
                time.sleep(sleep_time)
                self.timestamps.pop(0)
            
            self.timestamps.append(time.time())
            return func(*args, **kwargs)
        
        return wrapper

# Uso: máximo 10 requests por minuto
@RateLimiter(calls=10, period=60)
def fetch_data(url):
    return requests.get(url)
```

### 3. Cache de Respuestas

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=128)
def fetch_cached(url: str, params_hash: str):
    """Cachea respuestas GET."""
    return requests.get(url).json()

def get_with_cache(url: str, params: dict = None):
    params_str = str(sorted((params or {}).items()))
    params_hash = hashlib.md5(params_str.encode()).hexdigest()
    return fetch_cached(url, params_hash)
```

---

## Casos de Uso Comunes

### 1. Consumir API REST

```python
class UserAPI:
    def __init__(self, base_url: str, api_key: str):
        self.client = APIClient(base_url, api_key)
    
    def get_user(self, user_id: int) -> dict:
        response = self.client.get(f'users/{user_id}')
        response.raise_for_status()
        return response.json()
    
    def create_user(self, user_data: dict) -> dict:
        response = self.client.post('users', json=user_data)
        response.raise_for_status()
        return response.json()
```

### 2. Web Scraping

```python
async def scrape_pages(urls: list[str]):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = scrape_page(session, url)
            tasks.append(task)
        
        return await asyncio.gather(*tasks)
```

### 3. Descargar Archivos con Progress

```python
from tqdm import tqdm

def download_file(url: str, destination: str):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(destination, 'wb') as f:
        with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                pbar.update(len(chunk))
```

---

## Troubleshooting

### Problema: SSL Certificate Verification Failed

```python
# Temporal (SOLO para desarrollo)
response = requests.get(url, verify=False)

# Mejor: especificar certificado
response = requests.get(url, verify='/path/to/certfile')
```

### Problema: Connection Pool Exhausted

```python
# Aumentar tamaño del pool
adapter = HTTPAdapter(
    pool_connections=100,
    pool_maxsize=100
)
session.mount('https://', adapter)
```

### Problema: Requests Lentos

```python
# 1. Usar sesiones
# 2. Habilitar HTTP/2 con httpx
# 3. Usar async para paralelizar
# 4. Verificar timeout no es muy alto
```

---

## Recursos Adicionales

### Documentación Oficial
- [Requests](https://requests.readthedocs.io/)
- [aiohttp](https://docs.aiohttp.org/)
- [httpx](https://www.python-httpx.org/)
- [Smocker](https://smocker.dev/)

### Herramientas Útiles
- [Postman](https://www.postman.com/) - Testing de APIs
- [httpie](https://httpie.io/) - Cliente HTTP CLI
- [curl](https://curl.se/) - Cliente HTTP clásico

### Bibliotecas Complementarias
- `tenacity` - Reintentos avanzados
- `backoff` - Estrategias de backoff
- `requests-cache` - Cache de requests
- `requests-mock` - Mocking para tests

---

## Laboratorio

El laboratorio de este módulo consiste en:

1. **Cliente HTTP Robusto con httpx:**
   - Implementar cliente con timeouts configurables
   - Sistema de reintentos con backoff exponencial
   - Manejo completo de errores

2. **Descarga por Streaming:**
   - Descargar archivos grandes sin cargar en memoria
   - Implementar progress bar
   - Validar integridad (checksums)

**Ver:** [LABORATORIO.md](LABORATORIO.md)

---
