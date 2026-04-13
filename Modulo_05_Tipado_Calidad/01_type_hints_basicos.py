"""
Módulo 5.1: Type Hints Básicos
==============================

Conceptos:
- Anotaciones de tipos para variables y funciones
- Tipos básicos: int, str, float, bool, None
- Tipos compuestos: List, Dict, Set, Tuple
- Optional y Union
- Type aliases
- Beneficios del tipado gradual
"""

from typing import List, Dict, Set, Tuple, Optional, Union


# ============================================================================
# 1. ANOTACIONES BÁSICAS DE VARIABLES
# ============================================================================

# Variables simples
nombre: str = "Juan"
edad: int = 30
altura: float = 1.75
activo: bool = True

# Python 3.9+ permite usar tipos built-in directamente
# En lugar de List[int], puedes usar list[int]
# numeros: list[int] = [1, 2, 3]  # Python 3.9+

# Variables sin inicialización (solo tipo)
contador: int
mensaje: str


# ============================================================================
# 2. FUNCIONES CON TYPE HINTS
# ============================================================================

def saludar(nombre: str) -> str:
    """Función simple con tipos anotados."""
    return f"Hola, {nombre}!"


def sumar(a: int, b: int) -> int:
    """Suma dos números enteros."""
    return a + b


def calcular_promedio(numeros: List[float]) -> float:
    """Calcula el promedio de una lista de números."""
    if not numeros:
        return 0.0
    return sum(numeros) / len(numeros)


def sin_retorno(mensaje: str) -> None:
    """Función que no retorna nada (None)."""
    print(mensaje)


# ============================================================================
# 3. TIPOS COMPUESTOS
# ============================================================================

def procesar_lista(items: List[str]) -> int:
    """Trabaja con lista de strings."""
    return len(items)


def contar_palabras(texto: str) -> Dict[str, int]:
    """Retorna un diccionario con conteo de palabras."""
    palabras = texto.lower().split()
    conteo: Dict[str, int] = {}
    for palabra in palabras:
        conteo[palabra] = conteo.get(palabra, 0) + 1
    return conteo


def obtener_unicos(items: List[int]) -> Set[int]:
    """Retorna conjunto de elementos únicos."""
    return set(items)


def obtener_coordenadas() -> Tuple[float, float]:
    """Retorna tupla de coordenadas (latitud, longitud)."""
    return 19.4326, -99.1332


def obtener_datos_usuario() -> Tuple[str, int, str]:
    """Retorna tupla con datos del usuario (nombre, edad, email)."""
    return "Ana", 25, "ana@example.com"


# ============================================================================
# 4. OPTIONAL Y UNION
# ============================================================================

def buscar_usuario(user_id: int) -> Optional[str]:
    """
    Busca un usuario por ID.
    Retorna el nombre si existe, None si no existe.
    """
    usuarios = {1: "Juan", 2: "Ana", 3: "Carlos"}
    return usuarios.get(user_id)


def dividir(a: float, b: float) -> Optional[float]:
    """División segura que retorna None si b es cero."""
    if b == 0:
        return None
    return a / b


# Union para múltiples tipos posibles
def procesar_id(id_valor: Union[int, str]) -> str:
    """
    Acepta ID como int o str.
    Union[int, str] significa "int O str".
    """
    if isinstance(id_valor, int):
        return f"ID-{id_valor:04d}"
    return id_valor


# Python 3.10+ permite usar | en lugar de Union
# def procesar_id(id_valor: int | str) -> str:
#     ...


def obtener_configuracion(clave: str) -> Union[str, int, bool, None]:
    """Puede retornar diferentes tipos según la clave."""
    configs = {
        "host": "localhost",
        "puerto": 8080,
        "debug": True,
        "api_key": None
    }
    return configs.get(clave)


# ============================================================================
# 5. PARÁMETROS CON VALORES POR DEFECTO
# ============================================================================

def conectar_db(
    host: str = "localhost",
    puerto: int = 5432,
    timeout: float = 30.0,
    ssl: bool = False
) -> str:
    """Parámetros opcionales con tipo y valor por defecto."""
    return f"Conectado a {host}:{puerto} (SSL: {ssl})"


def crear_usuario(
    nombre: str,
    email: str,
    edad: Optional[int] = None,
    direccion: Optional[str] = None
) -> Dict[str, Union[str, int, None]]:
    """Algunos parámetros pueden ser None."""
    return {
        "nombre": nombre,
        "email": email,
        "edad": edad,
        "direccion": direccion
    }


# ============================================================================
# 6. TYPE ALIASES
# ============================================================================

# Aliases para tipos complejos (mejora legibilidad)
Usuario = Dict[str, Union[str, int]]
ListaUsuarios = List[Usuario]
Coordenadas = Tuple[float, float]
ResultadoBusqueda = Optional[Usuario]


def crear_usuario_alias(nombre: str, edad: int) -> Usuario:
    """Usa alias Usuario en lugar de Dict[str, Union[str, int]]."""
    return {"nombre": nombre, "edad": edad}


def buscar_usuarios_por_edad(edad: int) -> ListaUsuarios:
    """Retorna lista de usuarios."""
    return [
        {"nombre": "Ana", "edad": 25},
        {"nombre": "Carlos", "edad": 25}
    ]


def obtener_ubicacion() -> Coordenadas:
    """Usa alias Coordenadas."""
    return 19.4326, -99.1332


# ============================================================================
# 7. CLASES CON TYPE HINTS
# ============================================================================

class Persona:
    """Clase con atributos anotados."""
    
    nombre: str
    edad: int
    email: Optional[str]
    
    def __init__(self, nombre: str, edad: int, email: Optional[str] = None):
        self.nombre = nombre
        self.edad = edad
        self.email = email
    
    def saludar(self) -> str:
        """Método con tipo de retorno."""
        return f"Hola, soy {self.nombre}"
    
    def cumplir_años(self) -> None:
        """Método que modifica estado sin retornar."""
        self.edad += 1
    
    def obtener_info(self) -> Dict[str, Union[str, int, None]]:
        """Retorna diccionario con información."""
        return {
            "nombre": self.nombre,
            "edad": self.edad,
            "email": self.email
        }


class CuentaBancaria:
    """Ejemplo más completo."""
    
    titular: str
    saldo: float
    transacciones: List[str]
    
    def __init__(self, titular: str, saldo_inicial: float = 0.0):
        self.titular = titular
        self.saldo = saldo_inicial
        self.transacciones = []
    
    def depositar(self, cantidad: float) -> None:
        """Depositar dinero."""
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser positiva")
        self.saldo += cantidad
        self.transacciones.append(f"Depósito: +${cantidad:.2f}")
    
    def retirar(self, cantidad: float) -> bool:
        """Retira dinero. Retorna True si exitoso, False si fondos insuficientes."""
        if cantidad > self.saldo:
            return False
        self.saldo -= cantidad
        self.transacciones.append(f"Retiro: -${cantidad:.2f}")
        return True
    
    def obtener_saldo(self) -> float:
        """Retorna saldo actual."""
        return self.saldo
    
    def obtener_historial(self) -> List[str]:
        """Retorna historial de transacciones."""
        return self.transacciones.copy()


# ============================================================================
# 8. LISTAS HETEROGÉNEAS
# ============================================================================

def procesar_datos_mixtos(datos: List[Union[str, int, float]]) -> None:
    """Lista que puede contener diferentes tipos."""
    for dato in datos:
        if isinstance(dato, str):
            print(f"String: {dato}")
        elif isinstance(dato, int):
            print(f"Integer: {dato}")
        elif isinstance(dato, float):
            print(f"Float: {dato}")


# ============================================================================
# 9. BENEFICIOS DE TYPE HINTS
# ============================================================================

def ejemplo_sin_tipos(x, y):
    """Sin tipos: no sabemos qué espera ni qué retorna."""
    return x + y


def ejemplo_con_tipos(x: int, y: int) -> int:
    """Con tipos: queda claro qué acepta y retorna."""
    return x + y


# Los type hints ayudan a:
# 1. Documentación: Queda claro qué espera cada función
# 2. IDEs: Autocompletado y detección de errores
# 3. Refactoring: Cambios más seguros
# 4. Detección temprana: mypy/pyright encuentran errores antes de ejecutar


# ============================================================================
# 10. LIMITACIONES DEL TIPADO EN PYTHON
# ============================================================================

def ejemplo_limitaciones() -> None:
    """Python NO verifica tipos en runtime."""
    
    # Esto es válido en Python aunque los tipos no coincidan
    numero: int = "esto es una string"  # mypy lo detectará, Python no
    print(type(numero))  # <class 'str'>
    
    # Los type hints son hints (sugerencias), no restricciones
    resultado: str = sumar(5, 10)  # mypy error, Python OK
    print(type(resultado))  # <class 'int'>


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

def main() -> None:
    print("=" * 70)
    print("1. FUNCIONES BÁSICAS")
    print("=" * 70)
    
    saludo: str = saludar("Carlos")
    print(saludo)
    
    suma: int = sumar(10, 20)
    print(f"Suma: {suma}")
    
    numeros: List[float] = [10.5, 20.3, 15.7, 30.2]
    promedio: float = calcular_promedio(numeros)
    print(f"Promedio: {promedio:.2f}")
    
    print("\n" + "=" * 70)
    print("2. OPTIONAL Y UNION")
    print("=" * 70)
    
    usuario: Optional[str] = buscar_usuario(1)
    print(f"Usuario encontrado: {usuario}")
    
    usuario_inexistente: Optional[str] = buscar_usuario(99)
    print(f"Usuario no encontrado: {usuario_inexistente}")
    
    resultado_div: Optional[float] = dividir(10, 2)
    print(f"División: {resultado_div}")
    
    resultado_div_cero: Optional[float] = dividir(10, 0)
    print(f"División por cero: {resultado_div_cero}")
    
    print("\n" + "=" * 70)
    print("3. TYPE ALIASES")
    print("=" * 70)
    
    usuario_obj: Usuario = crear_usuario_alias("Ana", 25)
    print(f"Usuario: {usuario_obj}")
    
    usuarios: ListaUsuarios = buscar_usuarios_por_edad(25)
    print(f"Usuarios con 25 años: {len(usuarios)}")
    
    print("\n" + "=" * 70)
    print("4. CLASES")
    print("=" * 70)
    
    persona: Persona = Persona("Pedro", 30, "pedro@example.com")
    print(persona.saludar())
    persona.cumplir_años()
    print(f"Nueva edad: {persona.edad}")
    
    cuenta: CuentaBancaria = CuentaBancaria("María López", 1000.0)
    cuenta.depositar(500.0)
    exito: bool = cuenta.retirar(200.0)
    print(f"Retiro exitoso: {exito}")
    print(f"Saldo: ${cuenta.obtener_saldo():.2f}")
    
    historial: List[str] = cuenta.obtener_historial()
    print("Historial:")
    for transaccion in historial:
        print(f"  {transaccion}")
    
    print("\n" + "=" * 70)
    print("5. CONTAR PALABRAS")
    print("=" * 70)
    
    texto: str = "Python es genial Python es poderoso"
    conteo: Dict[str, int] = contar_palabras(texto)
    print("Conteo de palabras:")
    for palabra, cantidad in conteo.items():
        print(f"  {palabra}: {cantidad}")


if __name__ == "__main__":
    main()
