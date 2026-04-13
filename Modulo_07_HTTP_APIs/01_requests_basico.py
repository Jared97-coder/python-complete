"""
Módulo 7.1: Requests - Biblioteca HTTP Estándar

La biblioteca 'requests' es el estándar de facto para HTTP en Python.
Simple, elegante y perfecta para la mayoría de casos de uso.

Instalación:
    pip install requests

Documentación:
    https://requests.readthedocs.io/
"""

import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json
from pathlib import Path
from typing import Dict, Any, Optional


# =============================================================================
# Ejemplo 1: Requests GET Básicos
# =============================================================================

def ejemplo_get_basico():
    """GET simple a una API pública."""
    print("\n" + "="*60)
    print("Ejemplo 1: GET Básico")
    print("="*60)
    
    # GET simple
    response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"\nRespuesta JSON:")
    print(json.dumps(response.json(), indent=2))
    
    # Acceder a propiedades comunes
    print(f"\nTitulo: {response.json()['title']}")
    print(f"Encoding: {response.encoding}")
    print(f"Content-Type: {response.headers.get('content-type')}")


# =============================================================================
# Ejemplo 2: Parámetros de Query
# =============================================================================

def ejemplo_parametros_query():
    """Enviar parámetros en la URL."""
    print("\n" + "="*60)
    print("Ejemplo 2: Parámetros de Query")
    print("="*60)
    
    # Parámetros como diccionario
    params = {
        'userId': 1,
        'completed': False
    }
    
    response = requests.get(
        'https://jsonplaceholder.typicode.com/todos',
        params=params
    )
    
    print(f"URL completa: {response.url}")
    print(f"Resultados encontrados: {len(response.json())}")
    
    # Mostrar primeros 3 resultados
    for todo in response.json()[:3]:
        print(f"  - {todo['title']} (Completado: {todo['completed']})")


# =============================================================================
# Ejemplo 3: Headers Personalizados
# =============================================================================

def ejemplo_headers():
    """Enviar headers personalizados."""
    print("\n" + "="*60)
    print("Ejemplo 3: Headers Personalizados")
    print("="*60)
    
    headers = {
        'User-Agent': 'MiAplicacion/1.0',
        'Accept': 'application/json',
        'Accept-Language': 'es-MX',
        'X-Custom-Header': 'valor-personalizado'
    }
    
    response = requests.get(
        'https://httpbin.org/headers',
        headers=headers
    )
    
    print("Headers enviados (según servidor):")
    headers_recibidos = response.json()['headers']
    for key, value in headers_recibidos.items():
        print(f"  {key}: {value}")


# =============================================================================
# Ejemplo 4: POST con JSON
# =============================================================================

def ejemplo_post_json():
    """Enviar datos JSON en POST."""
    print("\n" + "="*60)
    print("Ejemplo 4: POST con JSON")
    print("="*60)
    
    # Datos a enviar
    nuevo_post = {
        'title': 'Mi Nuevo Post',
        'body': 'Este es el contenido del post',
        'userId': 1
    }
    
    response = requests.post(
        'https://jsonplaceholder.typicode.com/posts',
        json=nuevo_post  # Automáticamente serializa y pone Content-Type
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"\nRespuesta del servidor:")
    print(json.dumps(response.json(), indent=2))


# =============================================================================
# Ejemplo 5: POST con Form Data
# =============================================================================

def ejemplo_post_form():
    """Enviar form data (application/x-www-form-urlencoded)."""
    print("\n" + "="*60)
    print("Ejemplo 5: POST con Form Data")
    print("="*60)
    
    # Datos de formulario
    form_data = {
        'nombre': 'Juan Pérez',
        'email': 'juan@example.com',
        'mensaje': 'Hola desde Python!'
    }
    
    response = requests.post(
        'https://httpbin.org/post',
        data=form_data  # Se envía como form-urlencoded
    )
    
    print("Datos enviados:")
    print(json.dumps(response.json()['form'], indent=2))


# =============================================================================
# Ejemplo 6: PUT y PATCH
# =============================================================================

def ejemplo_put_patch():
    """Actualizar recursos con PUT y PATCH."""
    print("\n" + "="*60)
    print("Ejemplo 6: PUT y PATCH")
    print("="*60)
    
    # PUT - Reemplaza el recurso completo
    datos_completos = {
        'id': 1,
        'title': 'Título Actualizado',
        'body': 'Contenido completamente nuevo',
        'userId': 1
    }
    
    put_response = requests.put(
        'https://jsonplaceholder.typicode.com/posts/1',
        json=datos_completos
    )
    
    print("PUT Response:")
    print(json.dumps(put_response.json(), indent=2))
    
    # PATCH - Actualiza solo campos específicos
    datos_parciales = {
        'title': 'Solo actualizo el título'
    }
    
    patch_response = requests.patch(
        'https://jsonplaceholder.typicode.com/posts/1',
        json=datos_parciales
    )
    
    print("\nPATCH Response:")
    print(json.dumps(patch_response.json(), indent=2))


# =============================================================================
# Ejemplo 7: DELETE
# =============================================================================

def ejemplo_delete():
    """Eliminar un recurso."""
    print("\n" + "="*60)
    print("Ejemplo 7: DELETE")
    print("="*60)
    
    response = requests.delete(
        'https://jsonplaceholder.typicode.com/posts/1'
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    # 200 o 204 indican éxito
    if response.status_code in (200, 204):
        print("✓ Recurso eliminado exitosamente")


# =============================================================================
# Ejemplo 8: Manejo de Errores HTTP
# =============================================================================

def ejemplo_manejo_errores():
    """Manejar diferentes tipos de errores HTTP."""
    print("\n" + "="*60)
    print("Ejemplo 8: Manejo de Errores")
    print("="*60)
    
    # Intentar acceder a recurso que no existe
    try:
        response = requests.get(
            'https://jsonplaceholder.typicode.com/posts/9999999',
            timeout=5
        )
        
        # raise_for_status() lanza excepción para códigos 4xx y 5xx
        response.raise_for_status()
        
        print("Recurso encontrado:", response.json())
    
    except requests.exceptions.HTTPError as e:
        print(f"✗ Error HTTP: {e}")
        print(f"  Status Code: {e.response.status_code}")
        if e.response.status_code == 404:
            print("  El recurso no existe")
    
    except requests.exceptions.Timeout:
        print("✗ Timeout - El servidor tardó demasiado")
    
    except requests.exceptions.ConnectionError:
        print("✗ Error de Conexión - Verifica tu red")
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error general: {e}")


# =============================================================================
# Ejemplo 9: Autenticación Basic
# =============================================================================

def ejemplo_auth_basic():
    """Autenticación HTTP Basic."""
    print("\n" + "="*60)
    print("Ejemplo 9: Autenticación Basic")
    print("="*60)
    
    # Opción 1: Usando HTTPBasicAuth
    response = requests.get(
        'https://httpbin.org/basic-auth/usuario/password123',
        auth=HTTPBasicAuth('usuario', 'password123')
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Autenticado: {response.json()['authenticated']}")
    
    # Opción 2: Tupla (más simple)
    response2 = requests.get(
        'https://httpbin.org/basic-auth/usuario/password123',
        auth=('usuario', 'password123')
    )
    
    print(f"Respuesta: {response2.json()}")


# =============================================================================
# Ejemplo 10: Bearer Token (API Keys)
# =============================================================================

def ejemplo_bearer_token():
    """Autenticación con Bearer Token (común en APIs REST)."""
    print("\n" + "="*60)
    print("Ejemplo 10: Bearer Token")
    print("="*60)
    
    # Simular token (en producción vendría de OAuth2, etc.)
    api_token = "mi-super-token-secreto-12345"
    
    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    
    response = requests.get(
        'https://httpbin.org/bearer',
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Autenticado: {response.json()['authenticated']}")
    print(f"Token: {response.json()['token']}")


# =============================================================================
# Ejemplo 11: Sesiones - Reutilizar Conexiones
# =============================================================================

def ejemplo_sesiones():
    """Usar sesiones para múltiples requests."""
    print("\n" + "="*60)
    print("Ejemplo 11: Sesiones")
    print("="*60)
    
    # Crear sesión (mantiene conexión, cookies, headers)
    session = requests.Session()
    
    # Configurar headers comunes
    session.headers.update({
        'User-Agent': 'MiAplicacion/1.0',
        'Accept': 'application/json'
    })
    
    # Hacer múltiples requests (reutiliza conexión)
    urls = [
        'https://jsonplaceholder.typicode.com/posts/1',
        'https://jsonplaceholder.typicode.com/posts/2',
        'https://jsonplaceholder.typicode.com/posts/3'
    ]
    
    print("Haciendo 3 requests con sesión:")
    for url in urls:
        response = session.get(url)
        data = response.json()
        print(f"  - Post {data['id']}: {data['title'][:40]}...")
    
    # Cerrar sesión
    session.close()
    
    # Mejor: usar context manager
    print("\nUsando context manager:")
    with requests.Session() as s:
        for url in urls[:2]:
            response = s.get(url)
            data = response.json()
            print(f"  - Post {data['id']}: {data['title'][:40]}...")


# =============================================================================
# Ejemplo 12: Cookies
# =============================================================================

def ejemplo_cookies():
    """Trabajar con cookies."""
    print("\n" + "="*60)
    print("Ejemplo 12: Cookies")
    print("="*60)
    
    # Enviar cookies
    cookies = {
        'session_id': 'abc123',
        'user_pref': 'dark_mode'
    }
    
    response = requests.get(
        'https://httpbin.org/cookies',
        cookies=cookies
    )
    
    print("Cookies enviadas:")
    print(json.dumps(response.json()['cookies'], indent=2))
    
    # Leer cookies de la respuesta
    response2 = requests.get('https://httpbin.org/cookies/set?theme=dark&lang=es')
    print(f"\nCookies recibidas: {dict(response2.cookies)}")


# =============================================================================
# Ejemplo 13: Timeouts
# =============================================================================

def ejemplo_timeouts():
    """Configurar timeouts apropiados."""
    print("\n" + "="*60)
    print("Ejemplo 13: Timeouts")
    print("="*60)
    
    try:
        # Timeout simple (segundos)
        response = requests.get(
            'https://httpbin.org/delay/2',
            timeout=5
        )
        print(f"✓ Request completado: {response.status_code}")
    except requests.exceptions.Timeout:
        print("✗ Timeout alcanzado")
    
    # Timeout granular (connect_timeout, read_timeout)
    try:
        response = requests.get(
            'https://httpbin.org/delay/1',
            timeout=(3.0, 10.0)  # 3s para conectar, 10s para leer
        )
        print(f"✓ Request con timeout granular: {response.status_code}")
    except requests.exceptions.Timeout:
        print("✗ Timeout alcanzado")


# =============================================================================
# Ejemplo 14: Reintentos Automáticos
# =============================================================================

def ejemplo_reintentos():
    """Configurar reintentos automáticos."""
    print("\n" + "="*60)
    print("Ejemplo 14: Reintentos Automáticos")
    print("="*60)
    
    # Configurar estrategia de reintentos
    retry_strategy = Retry(
        total=3,  # Máximo 3 reintentos
        backoff_factor=1,  # 1s, 2s, 4s entre reintentos
        status_forcelist=[429, 500, 502, 503, 504],  # Reintentar estos códigos
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
    )
    
    # Crear adaptador con reintentos
    adapter = HTTPAdapter(max_retries=retry_strategy)
    
    # Aplicar a sesión
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    try:
        # Este endpoint a veces falla aleatoriamente
        response = session.get(
            'https://httpbin.org/status/200,500,502',
            timeout=5
        )
        print(f"✓ Request exitoso después de posibles reintentos: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Falló incluso después de reintentos: {e}")
    
    finally:
        session.close()


# =============================================================================
# Ejemplo 15: Subir Archivos (Multipart)
# =============================================================================

def ejemplo_upload_archivo():
    """Subir archivos con multipart/form-data."""
    print("\n" + "="*60)
    print("Ejemplo 15: Upload de Archivos")
    print("="*60)
    
    # Crear archivo temporal
    temp_file = Path("temp_upload.txt")
    temp_file.write_text("Contenido del archivo de prueba\n")
    
    try:
        # Subir archivo
        with temp_file.open('rb') as f:
            files = {
                'file': ('documento.txt', f, 'text/plain')
            }
            
            # También puedes enviar datos adicionales
            data = {
                'descripcion': 'Archivo de prueba',
                'categoria': 'documentos'
            }
            
            response = requests.post(
                'https://httpbin.org/post',
                files=files,
                data=data
            )
        
        print(f"Status Code: {response.status_code}")
        print("\nArchivo subido:")
        print(f"  Nombre: {response.json()['files']}")
        print(f"  Datos adicionales: {response.json()['form']}")
    
    finally:
        # Limpiar
        if temp_file.exists():
            temp_file.unlink()


# =============================================================================
# Ejemplo 16: Descargar Archivos
# =============================================================================

def ejemplo_download_archivo():
    """Descargar archivos binarios."""
    print("\n" + "="*60)
    print("Ejemplo 16: Download de Archivos")
    print("="*60)
    
    # Descargar imagen
    url = 'https://httpbin.org/image/png'
    response = requests.get(url)
    
    # Guardar contenido binario
    output_file = Path("imagen_descargada.png")
    output_file.write_bytes(response.content)
    
    print(f"✓ Archivo descargado: {output_file}")
    print(f"  Tamaño: {len(response.content)} bytes")
    print(f"  Content-Type: {response.headers['content-type']}")
    
    # Limpiar
    if output_file.exists():
        output_file.unlink()
        print(f"  (archivo temporal eliminado)")


# =============================================================================
# Ejemplo 17: Verificación SSL
# =============================================================================

def ejemplo_ssl():
    """Configurar verificación SSL."""
    print("\n" + "="*60)
    print("Ejemplo 17: Verificación SSL")
    print("="*60)
    
    # Por defecto, verifica SSL
    try:
        response = requests.get('https://httpbin.org/get', verify=True)
        print("✓ SSL verificado correctamente")
    except requests.exceptions.SSLError as e:
        print(f"✗ Error SSL: {e}")
    
    # ADVERTENCIA: Nunca usar verify=False en producción
    # Solo para desarrollo/debugging
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # response = requests.get('https://sitio-sin-ssl-valido.com', verify=False)
    # print("⚠️  SSL no verificado (INSEGURO)")


# =============================================================================
# Ejemplo 18: Response Streaming
# =============================================================================

def ejemplo_response_streaming():
    """Procesar respuestas en streaming."""
    print("\n" + "="*60)
    print("Ejemplo 18: Response Streaming")
    print("="*60)
    
    # Stream=True para no cargar todo en memoria
    response = requests.get(
        'https://httpbin.org/stream/5',
        stream=True
    )
    
    print("Procesando líneas en streaming:")
    for i, line in enumerate(response.iter_lines(), 1):
        if line:
            data = json.loads(line)
            print(f"  Línea {i}: {data['url']}")
    
    # Importante: cerrar la conexión
    response.close()


# =============================================================================
# Ejemplo 19: Cliente API Reutilizable
# =============================================================================

class JSONPlaceholderAPI:
    """Cliente para JSONPlaceholder API."""
    
    BASE_URL = 'https://jsonplaceholder.typicode.com'
    
    def __init__(self, timeout: int = 10):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JSONPlaceholder-Client/1.0',
            'Accept': 'application/json'
        })
        self.timeout = timeout
        
        # Configurar reintentos
        retry = Retry(total=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('https://', adapter)
    
    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET request helper."""
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def _post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """POST request helper."""
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.post(url, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def get_posts(self, user_id: Optional[int] = None):
        """Obtener posts, opcionalmente filtrados por usuario."""
        params = {'userId': user_id} if user_id else None
        return self._get('posts', params=params)
    
    def get_post(self, post_id: int):
        """Obtener un post específico."""
        return self._get(f'posts/{post_id}')
    
    def create_post(self, title: str, body: str, user_id: int):
        """Crear nuevo post."""
        data = {'title': title, 'body': body, 'userId': user_id}
        return self._post('posts', data)
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.session.close()


def ejemplo_cliente_api():
    """Usar cliente API personalizado."""
    print("\n" + "="*60)
    print("Ejemplo 19: Cliente API Reutilizable")
    print("="*60)
    
    # Usar con context manager
    with JSONPlaceholderAPI() as api:
        # Obtener posts del usuario 1
        posts = api.get_posts(user_id=1)
        print(f"Posts del usuario 1: {len(posts)}")
        
        # Obtener post específico
        post = api.get_post(1)
        print(f"\nPost #1: {post['title']}")
        
        # Crear nuevo post
        nuevo = api.create_post(
            title='Mi Nuevo Post',
            body='Contenido interesante',
            user_id=1
        )
        print(f"\nPost creado - ID: {nuevo['id']}")


# =============================================================================
# Main: Ejecutar Ejemplos
# =============================================================================

def main():
    """Ejecuta todos los ejemplos."""
    print("\n" + "="*60)
    print("MÓDULO 7.1: REQUESTS - BIBLIOTECA HTTP ESTÁNDAR")
    print("="*60)
    
    ejemplos = [
        ("GET Básico", ejemplo_get_basico),
        ("Parámetros Query", ejemplo_parametros_query),
        ("Headers Personalizados", ejemplo_headers),
        ("POST JSON", ejemplo_post_json),
        ("POST Form Data", ejemplo_post_form),
        ("PUT y PATCH", ejemplo_put_patch),
        ("DELETE", ejemplo_delete),
        ("Manejo de Errores", ejemplo_manejo_errores),
        ("Autenticación Basic", ejemplo_auth_basic),
        ("Bearer Token", ejemplo_bearer_token),
        ("Sesiones", ejemplo_sesiones),
        ("Cookies", ejemplo_cookies),
        ("Timeouts", ejemplo_timeouts),
        ("Reintentos", ejemplo_reintentos),
        ("Upload Archivo", ejemplo_upload_archivo),
        ("Download Archivo", ejemplo_download_archivo),
        ("SSL", ejemplo_ssl),
        ("Response Streaming", ejemplo_response_streaming),
        ("Cliente API", ejemplo_cliente_api),
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
