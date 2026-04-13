"""
Módulo 5.2: Typing Avanzado
===========================

Conceptos:
- Union types y el operador |
- Literal para valores específicos
- TypedDict para diccionarios estructurados
- Protocol para duck typing estructurado
- Generic y TypeVar para tipos genéricos
- Callable para tipos de función
- overload para múltiples firmas
- NewType para tipos distintos semánticamente
- Any, cast y cuándo usarlos
"""

from typing import (
    Union, Literal, TypedDict, Protocol, Generic, TypeVar,
    Callable, Optional, List, Dict, Any, cast, overload
)
from typing import NewType
from datetime import datetime


# ============================================================================
# 1. UNION TYPES
# ============================================================================

# Union[X, Y] significa "X o Y"
def procesar_entrada(valor: Union[int, str, float]) -> str:
    """Acepta múltiples tipos."""
    if isinstance(valor, int):
        return f"Entero: {valor}"
    elif isinstance(valor, str):
        return f"String: {valor}"
    else:
        return f"Float: {valor:.2f}"


# Python 3.10+ permite usar | en lugar de Union
# def procesar_entrada_moderno(valor: int | str | float) -> str:
#     """Sintaxis moderna con |"""
#     ...


def buscar_por_id(id_valor: Union[int, str]) -> Optional[Dict[str, Any]]:
    """ID puede ser int o string."""
    # Normalizar a string para búsqueda
    id_str = str(id_valor)
    # Simulación de búsqueda
    return {"id": id_str, "nombre": "Usuario"}


# ============================================================================
# 2. LITERAL - VALORES ESPECÍFICOS
# ============================================================================

# Literal restringe a valores específicos (como un enum ligero)
Estado = Literal["activo", "inactivo", "suspendido"]
Modo = Literal["desarrollo", "producción", "prueba"]


def cambiar_estado(nuevo_estado: Estado) -> None:
    """Solo acepta valores específicos."""
    print(f"Estado cambiado a: {nuevo_estado}")


def configurar_app(modo: Modo, debug: Literal[True, False]) -> None:
    """Modo debe ser uno de los valores literales."""
    print(f"Configurando en modo: {modo}, debug: {debug}")


# Literal con números
def establecer_puerto(puerto: Literal[80, 443, 8080, 8443]) -> None:
    """Solo puertos específicos permitidos."""
    print(f"Puerto configurado: {puerto}")


# ============================================================================
# 3. TYPEDDICT - DICCIONARIOS ESTRUCTURADOS
# ============================================================================

# TypedDict define la estructura de un diccionario
class Usuario(TypedDict):
    """Estructura de diccionario para usuario."""
    id: int
    nombre: str
    email: str
    edad: int


class UsuarioOpcional(TypedDict, total=False):
    """Todos los campos son opcionales."""
    telefono: str
    direccion: str
    foto_url: str


class UsuarioCombinado(Usuario, UsuarioOpcional):
    """Combina campos requeridos y opcionales."""
    pass


def crear_usuario(nombre: str, email: str, edad: int) -> Usuario:
    """Retorna diccionario con estructura validada."""
    return {
        "id": 1,
        "nombre": nombre,
        "email": email,
        "edad": edad
    }


def procesar_usuario(usuario: Usuario) -> str:
    """Acepta diccionario con estructura específica."""
    return f"{usuario['nombre']} ({usuario['email']})"


# TypedDict con herencia
class Producto(TypedDict):
    id: str
    nombre: str
    precio: float


class ProductoExtendido(Producto):
    descripcion: str
    stock: int
    categorias: List[str]


# ============================================================================
# 4. PROTOCOL - DUCK TYPING ESTRUCTURADO
# ============================================================================

# Protocol define una "interfaz" sin herencia
class Drawable(Protocol):
    """Protocolo para objetos dibujables."""
    
    def draw(self) -> str:
        """Método que debe implementarse."""
        ...
    
    def get_color(self) -> str:
        """Otro método requerido."""
        ...


class Circulo:
    """Implementa Drawable implícitamente (duck typing)."""
    
    def __init__(self, radio: float, color: str):
        self.radio = radio
        self.color = color
    
    def draw(self) -> str:
        return f"Dibujando círculo de radio {self.radio}"
    
    def get_color(self) -> str:
        return self.color


class Rectangulo:
    """También implementa Drawable."""
    
    def __init__(self, ancho: float, alto: float, color: str):
        self.ancho = ancho
        self.alto = alto
        self.color = color
    
    def draw(self) -> str:
        return f"Dibujando rectángulo {self.ancho}x{self.alto}"
    
    def get_color(self) -> str:
        return self.color


def dibujar_forma(forma: Drawable) -> None:
    """Acepta cualquier objeto que implemente el protocolo."""
    print(forma.draw())
    print(f"Color: {forma.get_color()}")


# Protocol con runtime_checkable (permite isinstance)
from typing import runtime_checkable

@runtime_checkable
class Comparable(Protocol):
    """Protocolo para objetos comparables."""
    
    def __lt__(self, other: Any) -> bool:
        ...


# ============================================================================
# 5. GENERIC Y TYPEVAR - TIPOS GENÉRICOS
# ============================================================================

# TypeVar para crear tipos genéricos
T = TypeVar('T')  # Tipo genérico sin restricciones
N = TypeVar('N', int, float)  # Solo int o float


def primero(items: List[T]) -> Optional[T]:
    """Retorna el primer elemento o None."""
    return items[0] if items else None


def ultimo(items: List[T]) -> Optional[T]:
    """Retorna el último elemento o None."""
    return items[-1] if items else None


def maximo(a: N, b: N) -> N:
    """Máximo de dos números (int o float)."""
    return a if a > b else b


# Clase genérica
class Pila(Generic[T]):
    """Pila genérica (stack)."""
    
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        """Agregar elemento."""
        self._items.append(item)
    
    def pop(self) -> Optional[T]:
        """Remover y retornar último elemento."""
        return self._items.pop() if self._items else None
    
    def peek(self) -> Optional[T]:
        """Ver último elemento sin remover."""
        return self._items[-1] if self._items else None
    
    def size(self) -> int:
        """Tamaño de la pila."""
        return len(self._items)


class Cache(Generic[T]):
    """Cache genérico con TTL."""
    
    def __init__(self, ttl_seconds: int = 3600):
        self._cache: Dict[str, tuple[T, datetime]] = {}
        self.ttl_seconds = ttl_seconds
    
    def set(self, key: str, value: T) -> None:
        """Guardar valor en cache."""
        self._cache[key] = (value, datetime.now())
    
    def get(self, key: str) -> Optional[T]:
        """Obtener valor del cache."""
        if key not in self._cache:
            return None
        value, timestamp = self._cache[key]
        # Verificar TTL (simplificado)
        return value


# ============================================================================
# 6. CALLABLE - TIPOS DE FUNCIÓN
# ============================================================================

# Callable[[arg1_type, arg2_type], return_type]
def ejecutar_operacion(
    a: int,
    b: int,
    operacion: Callable[[int, int], int]
) -> int:
    """Ejecuta una función recibida como parámetro."""
    return operacion(a, b)


def sumar(x: int, y: int) -> int:
    return x + y


def multiplicar(x: int, y: int) -> int:
    return x * y


# Callable sin parámetros
Callback = Callable[[], None]


def ejecutar_con_callback(accion: str, callback: Callback) -> None:
    """Ejecuta acción y llama al callback."""
    print(f"Ejecutando: {accion}")
    callback()


# Callable con tipos genéricos
Transformador = Callable[[T], T]


def aplicar_transformacion(valor: T, transformador: Transformador[T]) -> T:
    """Aplica función de transformación."""
    return transformador(valor)


# ============================================================================
# 7. OVERLOAD - MÚLTIPLES FIRMAS
# ============================================================================

# overload para documentar diferentes firmas
@overload
def procesar(valor: int) -> str:
    ...


@overload
def procesar(valor: str) -> int:
    ...


def procesar(valor: Union[int, str]) -> Union[str, int]:
    """
    Implementación real.
    - Si recibe int, retorna str
    - Si recibe str, retorna int
    """
    if isinstance(valor, int):
        return f"Número: {valor}"
    else:
        return len(valor)


@overload
def crear_lista(tamaño: int) -> List[None]:
    ...


@overload
def crear_lista(tamaño: int, valor_inicial: T) -> List[T]:
    ...


def crear_lista(tamaño: int, valor_inicial: Optional[T] = None) -> List[Optional[T]]:
    """Crea lista con o sin valor inicial."""
    return [valor_inicial] * tamaño


# ============================================================================
# 8. NEWTYPE - TIPOS SEMÁNTICAMENTE DISTINTOS
# ============================================================================

# NewType crea un tipo distinto (para type checkers)
UserId = NewType('UserId', int)
OrderId = NewType('OrderId', str)
Email = NewType('Email', str)


def obtener_usuario(user_id: UserId) -> str:
    """Solo acepta UserId, no int genérico."""
    return f"Usuario #{user_id}"


def procesar_orden(order_id: OrderId) -> None:
    """Solo acepta OrderId."""
    print(f"Procesando orden: {order_id}")


def enviar_email(destinatario: Email, mensaje: str) -> None:
    """Email es semánticamente diferente de str normal."""
    print(f"Enviando a {destinatario}: {mensaje}")


# Uso
user_id = UserId(123)
order_id = OrderId("ORD-456")
email = Email("usuario@example.com")


# ============================================================================
# 9. ANY Y CAST (USAR CON PRECAUCIÓN)
# ============================================================================

def procesar_json(data: Any) -> Dict[str, Any]:
    """
    Any desactiva verificación de tipos.
    Útil para datos externos (JSON, APIs).
    """
    # Any puede ser cualquier cosa
    return {"resultado": data}


def obtener_configuracion() -> Dict[str, Any]:
    """Retorno con tipos desconocidos."""
    return {
        "host": "localhost",
        "puerto": 8080,
        "opciones": {"debug": True, "timeout": 30}
    }


# cast() para "forzar" un tipo (no verifica en runtime)
def procesar_dato(dato: Any) -> int:
    """Cast cuando sabemos el tipo pero el checker no."""
    # Suponemos que dato es int
    valor = cast(int, dato)
    return valor * 2


# ============================================================================
# 10. EJEMPLO COMPLETO: REPOSITORIO GENÉRICO
# ============================================================================

K = TypeVar('K')  # Key type
V = TypeVar('V')  # Value type


class Repositorio(Generic[K, V]):
    """Repositorio genérico para almacenar entidades."""
    
    def __init__(self) -> None:
        self._storage: Dict[K, V] = {}
    
    def guardar(self, key: K, value: V) -> None:
        """Guardar entidad."""
        self._storage[key] = value
    
    def obtener(self, key: K) -> Optional[V]:
        """Obtener entidad por clave."""
        return self._storage.get(key)
    
    def eliminar(self, key: K) -> bool:
        """Eliminar entidad."""
        if key in self._storage:
            del self._storage[key]
            return True
        return False
    
    def listar(self) -> List[V]:
        """Listar todas las entidades."""
        return list(self._storage.values())
    
    def existe(self, key: K) -> bool:
        """Verificar si existe."""
        return key in self._storage


# Uso con tipos específicos
class UsuarioEntity(TypedDict):
    id: int
    nombre: str
    email: str


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

def main() -> None:
    print("=" * 70)
    print("1. LITERAL TYPES")
    print("=" * 70)
    
    cambiar_estado("activo")
    configurar_app("desarrollo", True)
    establecer_puerto(8080)
    
    print("\n" + "=" * 70)
    print("2. TYPEDDICT")
    print("=" * 70)
    
    usuario: Usuario = crear_usuario("Ana García", "ana@example.com", 25)
    print(procesar_usuario(usuario))
    
    print("\n" + "=" * 70)
    print("3. PROTOCOL")
    print("=" * 70)
    
    circulo = Circulo(5.0, "rojo")
    rectangulo = Rectangulo(10.0, 5.0, "azul")
    
    dibujar_forma(circulo)
    dibujar_forma(rectangulo)
    
    print("\n" + "=" * 70)
    print("4. GENERICS")
    print("=" * 70)
    
    pila_int: Pila[int] = Pila()
    pila_int.push(1)
    pila_int.push(2)
    pila_int.push(3)
    print(f"Top: {pila_int.peek()}")
    print(f"Pop: {pila_int.pop()}")
    
    pila_str: Pila[str] = Pila()
    pila_str.push("Hola")
    pila_str.push("Mundo")
    print(f"Top: {pila_str.peek()}")
    
    print("\n" + "=" * 70)
    print("5. CALLABLE")
    print("=" * 70)
    
    resultado1 = ejecutar_operacion(10, 5, sumar)
    print(f"Suma: {resultado1}")
    
    resultado2 = ejecutar_operacion(10, 5, multiplicar)
    print(f"Multiplicación: {resultado2}")
    
    # Lambda también es Callable
    resultado3 = ejecutar_operacion(10, 5, lambda x, y: x - y)
    print(f"Resta: {resultado3}")
    
    print("\n" + "=" * 70)
    print("6. NEWTYPE")
    print("=" * 70)
    
    print(obtener_usuario(user_id))
    procesar_orden(order_id)
    enviar_email(email, "Hola!")
    
    print("\n" + "=" * 70)
    print("7. REPOSITORIO GENÉRICO")
    print("=" * 70)
    
    repo: Repositorio[int, UsuarioEntity] = Repositorio()
    
    repo.guardar(1, {"id": 1, "nombre": "Juan", "email": "juan@example.com"})
    repo.guardar(2, {"id": 2, "nombre": "Ana", "email": "ana@example.com"})
    
    usuario_1 = repo.obtener(1)
    if usuario_1:
        print(f"Usuario 1: {usuario_1['nombre']}")
    
    print(f"Total usuarios: {len(repo.listar())}")


if __name__ == "__main__":
    main()
