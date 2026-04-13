"""
Módulo 4.3: Dataclasses y Attrs
===============================

Conceptos:
- @dataclass para reducir boilerplate
- Valores por defecto y factory functions
- field() para configuración avanzada
- frozen (inmutabilidad)
- post_init para validación
- order=True para ordenamiento
- Attrs como alternativa más potente
"""

from dataclasses import dataclass, field, asdict, astuple, replace
from typing import List, ClassVar
from datetime import datetime
import attr


# ============================================================================
# 1. DATACLASS BÁSICA
# ============================================================================

@dataclass
class Persona:
    """Dataclass genera automáticamente __init__, __repr__, __eq__."""
    nombre: str
    edad: int
    email: str
    
    # Sin dataclass necesitaríamos:
    # def __init__(self, nombre, edad, email):
    #     self.nombre = nombre
    #     self.edad = edad
    #     self.email = email
    # def __repr__(self): ...
    # def __eq__(self, other): ...


# ============================================================================
# 2. VALORES POR DEFECTO
# ============================================================================

@dataclass
class Configuracion:
    """Valores por defecto para algunos campos."""
    host: str = "localhost"
    puerto: int = 8080
    debug: bool = False
    timeout: float = 30.0
    
    # Campos sin default DEBEN ir antes de los que sí tienen


@dataclass
class Usuario:
    """Combina campos obligatorios y opcionales."""
    username: str
    email: str
    activo: bool = True
    intentos_login: int = 0


# ============================================================================
# 3. FIELD() PARA CONFIGURACIÓN AVANZADA
# ============================================================================

@dataclass
class Producto:
    """Uso de field() para listas mutables y metadata."""
    nombre: str
    precio: float
    categorias: List[str] = field(default_factory=list)  # IMPORTANTE: usar factory
    etiquetas: List[str] = field(default_factory=list)
    
    # NUNCA hacer: categorias: List[str] = []
    # Porque todas las instancias compartirían la misma lista
    
    _id: str = field(default="", init=False, repr=False)  # No en __init__, ni __repr__
    
    def __post_init__(self):
        """Se ejecuta después de __init__."""
        import uuid
        self._id = str(uuid.uuid4())


# ============================================================================
# 4. FROZEN - INMUTABILIDAD
# ============================================================================

@dataclass(frozen=True)
class Punto:
    """Dataclass inmutable - no se puede modificar después de crear."""
    x: float
    y: float
    
    # Ahora la instancia es hashable y puede usarse en sets/dicts
    
    def distancia_origen(self) -> float:
        """Los métodos de lectura funcionan normalmente."""
        return (self.x ** 2 + self.y ** 2) ** 0.5


@dataclass(frozen=True)
class Coordenadas:
    """Coordenadas inmutables."""
    latitud: float
    longitud: float
    
    def __post_init__(self):
        """Validación en __post_init__ (antes de congelar)."""
        if not -90 <= self.latitud <= 90:
            raise ValueError("Latitud debe estar entre -90 y 90")
        if not -180 <= self.longitud <= 180:
            raise ValueError("Longitud debe estar entre -180 y 180")


# ============================================================================
# 5. ORDER - ORDENAMIENTO AUTOMÁTICO
# ============================================================================

@dataclass(order=True)
class Tarea:
    """Ordenamiento basado en todos los campos."""
    prioridad: int
    nombre: str = field(compare=False)  # No usar este campo para comparar
    completada: bool = field(default=False, compare=False)
    
    # Se ordena solo por 'prioridad' debido a compare=False en otros


@dataclass(order=True)
class Empleado:
    """Ordenamiento personalizado."""
    sort_index: float = field(init=False, repr=False)
    nombre: str
    salario: float
    departamento: str = field(compare=False)
    
    def __post_init__(self):
        # Ordenar por salario (descendente) usando sort_index
        self.sort_index = -self.salario


# ============================================================================
# 6. COMPOSICIÓN Y ANIDAMIENTO
# ============================================================================

@dataclass
class Direccion:
    """Dataclass anidada."""
    calle: str
    numero: int
    ciudad: str
    codigo_postal: str


@dataclass
class Cliente:
    """Composición de dataclasses."""
    nombre: str
    email: str
    direccion: Direccion
    telefonos: List[str] = field(default_factory=list)


# ============================================================================
# 7. CLASS VARIABLES
# ============================================================================

@dataclass
class Factura:
    """Variables de clase vs variables de instancia."""
    numero: int
    cliente: str
    monto: float
    
    # Variable de clase (compartida)
    iva_porcentaje: ClassVar[float] = 0.16
    contador: ClassVar[int] = 0
    
    def __post_init__(self):
        Factura.contador += 1
    
    def total_con_iva(self) -> float:
        """Cálculo usando variable de clase."""
        return self.monto * (1 + Factura.iva_porcentaje)


# ============================================================================
# 8. CONVERSIÓN Y CLONACIÓN
# ============================================================================

@dataclass
class Libro:
    """Dataclass para demostrar conversiones."""
    titulo: str
    autor: str
    año: int
    precio: float = 0.0


# ============================================================================
# 9. ATTRS - ALTERNATIVA MÁS POTENTE
# ============================================================================

@attr.s(auto_attribs=True)
class PersonaAttrs:
    """Attrs ofrece más funcionalidades que dataclasses."""
    nombre: str
    edad: int = attr.ib()
    email: str = attr.ib()
    
    @edad.validator
    def validar_edad(self, attribute, valor):
        """Validador automático."""
        if valor < 0 or valor > 150:
            raise ValueError(f"Edad inválida: {valor}")
    
    @email.validator
    def validar_email(self, attribute, valor):
        """Validación de email."""
        if '@' not in valor:
            raise ValueError(f"Email inválido: {valor}")


@attr.s(auto_attribs=True, frozen=True)
class ConfiguracionApp:
    """Attrs con conversión automática."""
    nombre: str
    version: str
    puerto: int = attr.ib(converter=int)  # Convierte automáticamente a int
    debug: bool = attr.ib(default=False, converter=bool)
    
    @version.validator
    def validar_version(self, attribute, valor):
        """Validar formato de versión."""
        partes = valor.split('.')
        if len(partes) != 3:
            raise ValueError("Versión debe tener formato X.Y.Z")


@attr.define
class CuentaBancaria:
    """Attrs con define (sintaxis moderna)."""
    titular: str
    saldo: float = attr.field(default=0.0)
    
    @saldo.validator
    def validar_saldo(self, attribute, valor):
        if valor < 0:
            raise ValueError("El saldo no puede ser negativo")
    
    def depositar(self, cantidad: float):
        """Attrs permite mutación a menos que sea frozen."""
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser positiva")
        # object.__setattr__(self, 'saldo', self.saldo + cantidad)  # Si fuera frozen
        self.saldo += cantidad


# ============================================================================
# 10. EJEMPLO COMPLETO: SISTEMA DE PEDIDOS
# ============================================================================

@dataclass(frozen=True)
class ItemPedido:
    """Item individual en un pedido."""
    producto: str
    cantidad: int
    precio_unitario: float
    
    def subtotal(self) -> float:
        """Calcular subtotal."""
        return self.cantidad * self.precio_unitario


@dataclass
class Pedido:
    """Pedido completo con cálculos derivados."""
    id_pedido: str
    cliente: str
    items: List[ItemPedido] = field(default_factory=list)
    fecha: datetime = field(default_factory=datetime.now)
    descuento_porcentaje: float = 0.0
    
    def agregar_item(self, item: ItemPedido):
        """Agregar item al pedido."""
        # Como items NO es frozen, podemos modificar
        self.items.append(item)
    
    def subtotal(self) -> float:
        """Suma de todos los items."""
        return sum(item.subtotal() for item in self.items)
    
    def descuento(self) -> float:
        """Calcular descuento."""
        return self.subtotal() * (self.descuento_porcentaje / 100)
    
    def total(self) -> float:
        """Total final."""
        return self.subtotal() - self.descuento()
    
    def resumen(self) -> str:
        """Resumen del pedido."""
        lineas = [
            f"Pedido #{self.id_pedido} - Cliente: {self.cliente}",
            f"Fecha: {self.fecha.strftime('%Y-%m-%d %H:%M')}",
            "-" * 50
        ]
        for item in self.items:
            lineas.append(f"  {item.cantidad}x {item.producto} @ ${item.precio_unitario:.2f} = ${item.subtotal():.2f}")
        lineas.append("-" * 50)
        lineas.append(f"Subtotal: ${self.subtotal():.2f}")
        if self.descuento_porcentaje > 0:
            lineas.append(f"Descuento ({self.descuento_porcentaje}%): -${self.descuento():.2f}")
        lineas.append(f"TOTAL: ${self.total():.2f}")
        return "\n".join(lineas)


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

def main():
    print("=" * 70)
    print("1. DATACLASS BÁSICA")
    print("=" * 70)
    
    persona = Persona("Ana García", 28, "ana@example.com")
    print(persona)  # __repr__ automático
    
    persona2 = Persona("Ana García", 28, "ana@example.com")
    print(f"¿Son iguales? {persona == persona2}")  # __eq__ automático
    
    print("\n" + "=" * 70)
    print("2. VALORES POR DEFECTO")
    print("=" * 70)
    
    config1 = Configuracion()
    print(f"Config con defaults: {config1}")
    
    config2 = Configuracion(host="0.0.0.0", puerto=3000, debug=True)
    print(f"Config personalizada: {config2}")
    
    print("\n" + "=" * 70)
    print("3. FIELD() Y DEFAULT_FACTORY")
    print("=" * 70)
    
    p1 = Producto("Laptop", 1200.0, categorias=["Electrónica", "Computadoras"])
    p2 = Producto("Mouse", 25.0)
    
    print(f"p1: {p1.nombre}, ID: {p1._id}")
    print(f"p2: {p2.nombre}, ID: {p2._id}")
    print(f"IDs diferentes: {p1._id != p2._id}")
    
    print("\n" + "=" * 70)
    print("4. FROZEN - INMUTABILIDAD")
    print("=" * 70)
    
    punto = Punto(3.0, 4.0)
    print(f"Punto: {punto}")
    print(f"Distancia al origen: {punto.distancia_origen():.2f}")
    
    # punto.x = 5  # ERROR: cannot assign to field 'x'
    
    # Frozen permite usar en sets
    puntos = {Punto(0, 0), Punto(1, 1), Punto(0, 0)}
    print(f"Set de puntos (sin duplicados): {len(puntos)} elementos")
    
    print("\n" + "=" * 70)
    print("5. ORDER - ORDENAMIENTO")
    print("=" * 70)
    
    tareas = [
        Tarea(prioridad=2, nombre="Revisar email"),
        Tarea(prioridad=1, nombre="Llamar cliente urgente"),
        Tarea(prioridad=3, nombre="Actualizar documentación"),
    ]
    
    print("Tareas ordenadas por prioridad:")
    for tarea in sorted(tareas):
        print(f"  [{tarea.prioridad}] {tarea.nombre}")
    
    print("\n" + "=" * 70)
    print("6. COMPOSICIÓN")
    print("=" * 70)
    
    direccion = Direccion("Av. Reforma", 123, "CDMX", "06600")
    cliente = Cliente(
        nombre="Carlos Martínez",
        email="carlos@example.com",
        direccion=direccion,
        telefonos=["555-1234", "555-5678"]
    )
    print(cliente)
    
    print("\n" + "=" * 70)
    print("7. CONVERSIÓN Y CLONACIÓN")
    print("=" * 70)
    
    libro = Libro("Clean Code", "Robert Martin", 2008, 45.99)
    
    # Convertir a dict
    libro_dict = asdict(libro)
    print(f"Como dict: {libro_dict}")
    
    # Convertir a tuple
    libro_tuple = astuple(libro)
    print(f"Como tuple: {libro_tuple}")
    
    # Clonar con modificaciones
    libro_oferta = replace(libro, precio=39.99)
    print(f"Original: {libro}")
    print(f"En oferta: {libro_oferta}")
    
    print("\n" + "=" * 70)
    print("8. ATTRS - VALIDACIÓN")
    print("=" * 70)
    
    try:
        persona_attrs = PersonaAttrs("Juan", 30, "juan@example.com")
        print(f"Persona válida: {persona_attrs}")
        
        persona_invalida = PersonaAttrs("Pedro", 200, "pedro@example.com")
    except ValueError as e:
        print(f"Error de validación: {e}")
    
    print("\n" + "=" * 70)
    print("9. ATTRS - CONVERSIÓN")
    print("=" * 70)
    
    config = ConfiguracionApp(
        nombre="MiApp",
        version="1.2.3",
        puerto="8080",  # String se convierte a int
        debug="1"       # String se convierte a bool
    )
    print(f"Config: puerto={config.puerto} (tipo: {type(config.puerto).__name__})")
    print(f"Debug: {config.debug} (tipo: {type(config.debug).__name__})")
    
    print("\n" + "=" * 70)
    print("10. EJEMPLO COMPLETO: PEDIDO")
    print("=" * 70)
    
    pedido = Pedido(
        id_pedido="ORD-001",
        cliente="María López",
        descuento_porcentaje=10
    )
    
    pedido.agregar_item(ItemPedido("Laptop Dell", 1, 1200.00))
    pedido.agregar_item(ItemPedido("Mouse Logitech", 2, 25.00))
    pedido.agregar_item(ItemPedido("Teclado Mecánico", 1, 150.00))
    
    print(pedido.resumen())


if __name__ == "__main__":
    main()
