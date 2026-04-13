"""
Módulo 7.4: Timeouts, Reintentos y Resiliencia

Técnicas esenciales para construir clientes HTTP robustos que manejan
fallas de red, timeouts y errores temporales de forma elegante.

Instalación:
    pip install requests httpx tenacity backoff

Documentación:
    - urllib3 Retry: https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#urllib3.util.Retry
    - tenacity: https://tenacity.readthedocs.io/
    - backoff: https://github.com/litl/backoff
"""

import requests
import httpx
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    after_log
)
import backoff
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# Ejemplo 1: Timeouts Básicos
# =============================================================================

def ejemplo_timeouts_basicos():
    """Entender diferentes tipos de timeouts."""
    print("\n" + "="*60)
    print("Ejemplo 1: Timeouts Básicos")
    print("="*60)
    
    # SIN timeout = MAL (puede colgar indefinidamente)
    # response = requests.get(url)  # ❌ NUNCA hagas esto
    
    # CON timeout = BIEN
    try:
        response = requests.get(
            'https://httpbin.org/delay/2',
            timeout=5  # 5 segundos timeout total
        )
        print(f"✓ Request exitoso: {response.status_code}")
    except requests.exceptions.Timeout:
        print("✗ Timeout alcanzado")
    
    # Timeout granular (connect, read)
    try:
        response = requests.get(
            'https://httpbin.org/delay/1',
            timeout=(3.0, 10.0)  # (connect_timeout, read_timeout)
        )
        print(f"✓ Request con timeout granular: {response.status_code}")
    except requests.exceptions.Timeout as e:
        print(f"✗ Timeout: {e}")


# =============================================================================
# Ejemplo 2: Reintentos con urllib3.Retry
# =============================================================================

def ejemplo_urllib3_retry():
    """Reintentos automáticos con urllib3.Retry."""
    print("\n" + "="*60)
    print("Ejemplo 2: Reintentos con urllib3.Retry")
    print("="*60)
    
    # Configurar estrategia de reintentos
    retry_strategy = Retry(
        total=3,  # Total de reintentos
        backoff_factor=1,  # 1s, 2s, 4s entre reintentos
        status_forcelist=[429, 500, 502, 503, 504],  # Reintentar estos códigos
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],  # Métodos seguros
        raise_on_status=False  # No lanzar excepción, retornar response
    )
    
    # Aplicar a sesión
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    try:
        # Este endpoint falla 50% de las veces
        print("Intentando request (puede reintentar)...")
        response = session.get(
            'https://httpbin.org/status/200,500,503',
            timeout=5
        )
        print(f"✓ Exitoso: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Falló después de {retry_strategy.total} reintentos: {e}")
    
    finally:
        session.close()


# =============================================================================
# Ejemplo 3: Backoff Exponencial Manual
# =============================================================================

def fetch_with_exponential_backoff(url, max_retries=5):
    """Implementar backoff exponencial manualmente."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response
        
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                # Backoff exponencial: 1s, 2s, 4s, 8s, 16s
                wait_time = 2 ** attempt
                print(f"  Intento {attempt + 1} falló: {e}")
                print(f"  Reintentando en {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"  Falló después de {max_retries} intentos")
                raise
    
    raise Exception("No se pudo completar request")


def ejemplo_backoff_exponencial():
    """Backoff exponencial manual."""
    print("\n" + "="*60)
    print("Ejemplo 3: Backoff Exponencial Manual")
    print("="*60)
    
    try:
        response = fetch_with_exponential_backoff(
            'https://httpbin.org/status/200,500,503',
            max_retries=3
        )
        print(f"✓ Exitoso: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")


# =============================================================================
# Ejemplo 4: Backoff Exponencial con Jitter
# =============================================================================

def fetch_with_jitter(url, max_retries=5):
    """Backoff exponencial con jitter para evitar thundering herd."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response
        
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                # Backoff exponencial con jitter aleatorio
                base_wait = 2 ** attempt
                jitter = random.uniform(0, 1)
                wait_time = base_wait + jitter
                
                print(f"  Intento {attempt + 1} falló")
                print(f"  Esperando {wait_time:.2f}s (base: {base_wait}s + jitter: {jitter:.2f}s)")
                time.sleep(wait_time)
            else:
                raise


def ejemplo_jitter():
    """Backoff con jitter."""
    print("\n" + "="*60)
    print("Ejemplo 4: Backoff con Jitter")
    print("="*60)
    
    try:
        response = fetch_with_jitter(
            'https://httpbin.org/status/200,503',
            max_retries=3
        )
        print(f"✓ Exitoso: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")


# =============================================================================
# Ejemplo 5: Tenacity - Librería de Reintentos
# =============================================================================

@retry(
    stop=stop_after_attempt(3),  # Máximo 3 intentos
    wait=wait_exponential(multiplier=1, min=1, max=10),  # 1s, 2s, 4s
    retry=retry_if_exception_type(requests.exceptions.RequestException),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.INFO)
)
def fetch_with_tenacity(url):
    """Request con reintentos usando tenacity."""
    logger.info(f"Intentando {url}")
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response


def ejemplo_tenacity():
    """Reintentos con tenacity."""
    print("\n" + "="*60)
    print("Ejemplo 5: Tenacity - Reintentos Elegantes")
    print("="*60)
    
    try:
        response = fetch_with_tenacity('https://httpbin.org/status/200,500,503')
        print(f"✓ Exitoso: {response.status_code}")
    except Exception as e:
        print(f"✗ Falló después de reintentos: {type(e).__name__}")


# =============================================================================
# Ejemplo 6: Backoff - Decoradores Simples
# =============================================================================

@backoff.on_exception(
    backoff.expo,  # Backoff exponencial
    requests.exceptions.RequestException,  # Excepciones a capturar
    max_tries=5,  # Máximo de intentos
    jitter=backoff.full_jitter  # Jitter completo
)
def fetch_with_backoff_decorator(url):
    """Request con backoff usando decorador."""
    logger.info(f"Fetching {url}")
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response


def ejemplo_backoff_decorator():
    """Reintentos con decorador backoff."""
    print("\n" + "="*60)
    print("Ejemplo 6: Backoff - Decoradores")
    print("="*60)
    
    try:
        response = fetch_with_backoff_decorator('https://httpbin.org/status/200,503')
        print(f"✓ Exitoso: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}")


# =============================================================================
# Ejemplo 7: Circuit Breaker Pattern
# =============================================================================

class CircuitBreaker:
    """Implementación simple de Circuit Breaker."""
    
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        """Ejecuta función a través del circuit breaker."""
        # Si está OPEN, verificar si debe pasar a HALF_OPEN
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time >= self.timeout:
                self.state = 'HALF_OPEN'
                logger.info("Circuit Breaker: OPEN → HALF_OPEN")
            else:
                raise Exception("Circuit Breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            
            # Éxito: resetear si estaba en HALF_OPEN
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failures = 0
                logger.info("Circuit Breaker: HALF_OPEN → CLOSED")
            
            return result
        
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            
            # Si excede threshold, abrir circuito
            if self.failures >= self.failure_threshold:
                self.state = 'OPEN'
                logger.warning(f"Circuit Breaker: {self.state} (failures: {self.failures})")
            
            raise


def ejemplo_circuit_breaker():
    """Circuit Breaker para prevenir requests a servicio caído."""
    print("\n" + "="*60)
    print("Ejemplo 7: Circuit Breaker Pattern")
    print("="*60)
    
    cb = CircuitBreaker(failure_threshold=3, timeout=5)
    
    def fetch_data():
        response = requests.get('https://httpbin.org/status/500', timeout=2)
        response.raise_for_status()
        return response
    
    # Simular múltiples requests fallidos
    for i in range(5):
        try:
            print(f"\nIntento {i+1}:")
            cb.call(fetch_data)
            print("✓ Exitoso")
        except Exception as e:
            print(f"✗ Falló: {type(e).__name__}")
            print(f"  Circuit state: {cb.state}, Failures: {cb.failures}")


# =============================================================================
# Ejemplo 8: Timeout con httpx
# =============================================================================

def ejemplo_httpx_timeouts():
    """Timeouts granulares con httpx."""
    print("\n" + "="*60)
    print("Ejemplo 8: Timeouts con httpx")
    print("="*60)
    
    # Timeout completo
    timeout = httpx.Timeout(
        connect=3.0,  # Tiempo para establecer conexión
        read=5.0,  # Tiempo para leer respuesta
        write=5.0,  # Tiempo para enviar datos
        pool=10.0  # Tiempo esperando conexión del pool
    )
    
    with httpx.Client(timeout=timeout) as client:
        try:
            response = client.get('https://httpbin.org/delay/2')
            print(f"✓ Request exitoso: {response.status_code}")
        except httpx.TimeoutException as e:
            print(f"✗ Timeout: {e}")
    
    # Timeout infinito para ciertas operaciones
    timeout_custom = httpx.Timeout(
        connect=5.0,
        read=None,  # Sin límite de lectura
        write=5.0
    )
    
    print("✓ Timeout configurado con lectura ilimitada")


# =============================================================================
# Ejemplo 9: Reintentos Condicionales
# =============================================================================

def should_retry(exception):
    """Decide si debe reintentar basado en la excepción."""
    # Reintentar solo en errores de red y 5xx
    if isinstance(exception, requests.exceptions.ConnectionError):
        return True
    if isinstance(exception, requests.exceptions.Timeout):
        return True
    if isinstance(exception, requests.exceptions.HTTPError):
        if exception.response.status_code >= 500:
            return True
    return False


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=should_retry
)
def fetch_smart_retry(url):
    """Reintentos inteligentes basados en tipo de error."""
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response


def ejemplo_reintentos_condicionales():
    """Reintentar solo bajo ciertas condiciones."""
    print("\n" + "="*60)
    print("Ejemplo 9: Reintentos Condicionales")
    print("="*60)
    
    # Error 404 - No debe reintentar
    try:
        fetch_smart_retry('https://httpbin.org/status/404')
    except requests.exceptions.HTTPError:
        print("✗ Error 404 - no reintentó (correcto)")
    
    # Error 503 - Debe reintentar
    try:
        fetch_smart_retry('https://httpbin.org/status/200,503')
        print("✓ Error 503 - reintentó y tuvo éxito")
    except Exception as e:
        print(f"✗ Error 503 - reintentó pero falló: {type(e).__name__}")


# =============================================================================
# Ejemplo 10: Rate Limiting
# =============================================================================

class RateLimiter:
    """Rate limiter simple usando token bucket."""
    
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            now = time.time()
            
            # Remover llamadas antiguas
            self.calls = [call for call in self.calls if now - call < self.period]
            
            # Verificar límite
            if len(self.calls) >= self.max_calls:
                sleep_time = self.period - (now - self.calls[0])
                logger.warning(f"Rate limit alcanzado, esperando {sleep_time:.2f}s")
                time.sleep(sleep_time)
                self.calls.pop(0)
            
            # Hacer llamada
            self.calls.append(time.time())
            return func(*args, **kwargs)
        
        return wrapper


@RateLimiter(max_calls=5, period=1.0)  # 5 calls por segundo
def fetch_rate_limited(url):
    """Request con rate limiting."""
    response = requests.get(url, timeout=5)
    return response


def ejemplo_rate_limiting():
    """Rate limiting para respetar límites de API."""
    print("\n" + "="*60)
    print("Ejemplo 10: Rate Limiting")
    print("="*60)
    
    inicio = time.time()
    
    # Intentar 10 requests (debería tomar ~2 segundos con límite de 5/s)
    print("Haciendo 10 requests (límite: 5/segundo)...")
    for i in range(10):
        response = fetch_rate_limited('https://httpbin.org/uuid')
        print(f"  Request {i+1}: {response.status_code}")
    
    duracion = time.time() - inicio
    print(f"\n✓ 10 requests completados en {duracion:.2f}s")


# =============================================================================
# Ejemplo 11: Timeout Adaptativo
# =============================================================================

class AdaptiveTimeout:
    """Timeout que se ajusta basado en latencia histórica."""
    
    def __init__(self, initial_timeout=5.0, percentile=95):
        self.timeout = initial_timeout
        self.latencies = []
        self.percentile = percentile
    
    def get_timeout(self):
        """Obtiene timeout actual."""
        if len(self.latencies) < 10:
            return self.timeout
        
        # Calcular percentil de latencias
        sorted_latencies = sorted(self.latencies)
        index = int(len(sorted_latencies) * self.percentile / 100)
        p_latency = sorted_latencies[index]
        
        # Timeout = percentil + buffer del 50%
        return p_latency * 1.5
    
    def record_latency(self, latency):
        """Registra latencia de request."""
        self.latencies.append(latency)
        # Mantener solo últimas 100 mediciones
        if len(self.latencies) > 100:
            self.latencies.pop(0)


def ejemplo_timeout_adaptativo():
    """Timeout que se adapta a condiciones de red."""
    print("\n" + "="*60)
    print("Ejemplo 11: Timeout Adaptativo")
    print("="*60)
    
    adaptive = AdaptiveTimeout(initial_timeout=5.0)
    
    # Simular varios requests
    for i in range(15):
        timeout = adaptive.get_timeout()
        inicio = time.time()
        
        try:
            response = requests.get(
                f'https://httpbin.org/delay/{random.uniform(0.5, 2.0)}',
                timeout=timeout
            )
            latencia = time.time() - inicio
            adaptive.record_latency(latencia)
            
            print(f"Request {i+1}: {latencia:.2f}s (timeout: {timeout:.2f}s)")
        
        except requests.exceptions.Timeout:
            print(f"Request {i+1}: Timeout (timeout: {timeout:.2f}s)")
    
    print(f"\n✓ Timeout final adaptado: {adaptive.get_timeout():.2f}s")


# =============================================================================
# Ejemplo 12: Cliente Robusto Completo
# =============================================================================

class RobustHTTPClient:
    """Cliente HTTP robusto con todas las técnicas."""
    
    def __init__(self, base_url="", max_retries=3, timeout=10.0):
        self.base_url = base_url
        
        # Configurar reintentos
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        
        # Crear sesión
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        # Configurar timeout default
        self.timeout = timeout
        
        # Circuit breaker
        self.circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=30)
    
    def get(self, endpoint, **kwargs):
        """GET con todas las protecciones."""
        url = f"{self.base_url}/{endpoint}" if endpoint else self.base_url
        
        # Usar timeout si no se especifica
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        
        # Ejecutar a través de circuit breaker
        return self.circuit_breaker.call(self.session.get, url, **kwargs)
    
    def post(self, endpoint, **kwargs):
        """POST con todas las protecciones."""
        url = f"{self.base_url}/{endpoint}" if endpoint else self.base_url
        
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        
        return self.circuit_breaker.call(self.session.post, url, **kwargs)
    
    def close(self):
        """Cerrar sesión."""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()


def ejemplo_cliente_robusto():
    """Cliente HTTP completamente robusto."""
    print("\n" + "="*60)
    print("Ejemplo 12: Cliente Robusto Completo")
    print("="*60)
    
    with RobustHTTPClient(base_url='https://jsonplaceholder.typicode.com') as client:
        try:
            # GET
            response = client.get('posts/1')
            print(f"✓ GET exitoso: {response.status_code}")
            
            # POST
            response = client.post('posts', json={
                'title': 'Test',
                'body': 'Content',
                'userId': 1
            })
            print(f"✓ POST exitoso: {response.status_code}")
        
        except Exception as e:
            print(f"✗ Error: {e}")


# =============================================================================
# Main: Ejecutar Ejemplos
# =============================================================================

def main():
    """Ejecuta todos los ejemplos."""
    print("\n" + "="*60)
    print("MÓDULO 7.4: TIMEOUTS, REINTENTOS Y RESILIENCIA")
    print("="*60)
    
    ejemplos = [
        ("Timeouts Básicos", ejemplo_timeouts_basicos),
        ("urllib3.Retry", ejemplo_urllib3_retry),
        ("Backoff Exponencial", ejemplo_backoff_exponencial),
        ("Backoff con Jitter", ejemplo_jitter),
        ("Tenacity", ejemplo_tenacity),
        ("Backoff Decorator", ejemplo_backoff_decorator),
        ("Circuit Breaker", ejemplo_circuit_breaker),
        ("httpx Timeouts", ejemplo_httpx_timeouts),
        ("Reintentos Condicionales", ejemplo_reintentos_condicionales),
        ("Rate Limiting", ejemplo_rate_limiting),
        ("Timeout Adaptativo", ejemplo_timeout_adaptativo),
        ("Cliente Robusto", ejemplo_cliente_robusto),
    ]
    
    for nombre, funcion in ejemplos:
        try:
            funcion()
        except Exception as e:
            print(f"\n✗ Error en '{nombre}': {e}")
    
    print("\n" + "="*60)
    print("✓ Ejemplos completados")
    print("="*60)


if __name__ == "__main__":
    main()
