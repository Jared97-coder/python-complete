"""
Ejemplo: Código CON Type Hints
================================
El mismo código pero con anotaciones de tipos completas.
El IDE, mypy y los desarrolladores pueden entender mejor el código.
"""

from typing import TypedDict, Literal, Optional, Union
from decimal import Decimal


# Definir estructuras con TypedDict
class ProductoDict(TypedDict):
    """Estructura de un producto."""
    id: int
    nombre: str
    precio: float
    cantidad: int
    categoria: str


class ItemCarritoDict(TypedDict):
    """Item en un carrito de compras."""
    producto: ProductoDict
    cantidad: int
    precio: float


class ResumenCarritoDict(TypedDict):
    """Resumen de un carrito."""
    items: list[ItemCarritoDict]
    subtotal: float
    descuentos: dict[str, float]
    total: float


class ItemPedidoDict(TypedDict):
    """Item en un pedido."""
    producto_id: int
    cantidad: int


class ItemFallidoDict(TypedDict):
    """Item que falló al procesarse."""
    producto_id: int
    razon: str


class ResultadoPedidoDict(TypedDict):
    """Resultado del procesamiento de un pedido."""
    exito: bool
    items_procesados: list[ItemPedidoDict]
    items_fallidos: list[ItemFallidoDict]


class PedidoDict(TypedDict):
    """Estructura de un pedido."""
    items: list[ItemPedidoDict]


# Funciones con tipos claros
def calcular_descuento(precio: float, porcentaje: float) -> float:
    """
    Calcula el precio con descuento aplicado.
    
    Args:
        precio: Precio original del producto.
        porcentaje: Porcentaje de descuento (0-100).
    
    Returns:
        Precio con descuento aplicado.
    
    Examples:
        >>> calcular_descuento(100.0, 10.0)
        90.0
    """
    return precio * (1 - porcentaje / 100)


def buscar_usuario(
    usuarios: list[dict[str, Union[int, str]]],
    criterio: Union[int, str]
) -> Optional[Union[dict[str, Union[int, str]], list[dict[str, Union[int, str]]]]]:
    """
    Busca usuarios por ID o nombre.
    
    Args:
        usuarios: Lista de usuarios donde buscar.
        criterio: ID (int) para buscar uno, o nombre (str) para buscar varios.
    
    Returns:
        - Si criterio es int: Retorna un usuario o None.
        - Si criterio es str: Retorna lista de usuarios coincidentes.
        - Caso contrario: None.
    """
    if isinstance(criterio, int):
        return next(
            (u for u in usuarios if u["id"] == criterio),
            None
        )
    elif isinstance(criterio, str):
        return [
            u for u in usuarios 
            if criterio.lower() in str(u["nombre"]).lower()
        ]
    return None


class CarritoCompras:
    """
    Carrito de compras con gestión de items y descuentos.
    
    Attributes:
        items: Lista de items en el carrito.
        descuentos: Diccionario de códigos de descuento y sus porcentajes.
    """
    
    def __init__(self) -> None:
        """Inicializa un carrito vacío."""
        self.items: list[ItemCarritoDict] = []
        self.descuentos: dict[str, float] = {}
    
    def agregar_item(self, producto: ProductoDict, cantidad: int) -> None:
        """
        Agrega un item al carrito.
        
        Args:
            producto: Producto a agregar.
            cantidad: Cantidad del producto.
        
        Raises:
            ValueError: Si la cantidad es menor o igual a 0.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        
        self.items.append({
            "producto": producto,
            "cantidad": cantidad,
            "precio": producto["precio"]
        })
    
    def aplicar_descuento(self, codigo: str, porcentaje: float) -> None:
        """
        Aplica un código de descuento.
        
        Args:
            codigo: Código del descuento.
            porcentaje: Porcentaje de descuento (0-100).
        
        Raises:
            ValueError: Si el porcentaje está fuera del rango válido.
        """
        if not 0 <= porcentaje <= 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        
        self.descuentos[codigo] = porcentaje
    
    def calcular_total(self) -> float:
        """
        Calcula el total del carrito con descuentos aplicados.
        
        Returns:
            Total a pagar después de descuentos.
        """
        subtotal = sum(
            item["precio"] * item["cantidad"] 
            for item in self.items
        )
        
        descuento_total = 0.0
        for porcentaje in self.descuentos.values():
            descuento_total += subtotal * (porcentaje / 100)
        
        return subtotal - descuento_total
    
    def obtener_resumen(self) -> ResumenCarritoDict:
        """
        Obtiene un resumen completo del carrito.
        
        Returns:
            Diccionario con items, subtotal, descuentos y total.
        """
        subtotal = sum(
            item["precio"] * item["cantidad"] 
            for item in self.items
        )
        
        return {
            "items": self.items,
            "subtotal": subtotal,
            "descuentos": self.descuentos,
            "total": self.calcular_total()
        }


class GestorInventario:
    """
    Gestor de inventario de productos.
    
    Attributes:
        capacidad: Capacidad máxima del inventario.
        productos: Diccionario de productos por ID.
    """
    
    def __init__(self, capacidad: int) -> None:
        """
        Inicializa el gestor con una capacidad máxima.
        
        Args:
            capacidad: Número máximo de productos distintos.
        
        Raises:
            ValueError: Si la capacidad es menor o igual a 0.
        """
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor a 0")
        
        self.capacidad: int = capacidad
        self.productos: dict[int, ProductoDict] = {}
    
    def agregar_producto(self, producto: ProductoDict) -> None:
        """
        Agrega un producto al inventario.
        
        Args:
            producto: Producto a agregar.
        
        Raises:
            ValueError: Si el inventario está lleno.
        """
        if len(self.productos) >= self.capacidad:
            raise ValueError("Inventario lleno")
        
        producto_id = producto["id"]
        if producto_id in self.productos:
            self.productos[producto_id]["cantidad"] += producto["cantidad"]
        else:
            self.productos[producto_id] = producto
    
    def buscar(self, producto_id: int) -> Optional[ProductoDict]:
        """
        Busca un producto por ID.
        
        Args:
            producto_id: ID del producto a buscar.
        
        Returns:
            Producto encontrado o None si no existe.
        """
        return self.productos.get(producto_id)
    
    def filtrar_por_categoria(self, categoria: str) -> list[ProductoDict]:
        """
        Filtra productos por categoría.
        
        Args:
            categoria: Categoría a filtrar.
        
        Returns:
            Lista de productos de la categoría.
        """
        return [
            p for p in self.productos.values()
            if p.get("categoria") == categoria
        ]
    
    def productos_bajo_stock(self, minimo: int) -> list[ProductoDict]:
        """
        Encuentra productos con stock bajo.
        
        Args:
            minimo: Cantidad mínima de stock.
        
        Returns:
            Lista de productos con cantidad menor al mínimo.
        """
        return [
            p for p in self.productos.values()
            if p["cantidad"] < minimo
        ]


def procesar_pedido(
    pedido: PedidoDict,
    inventario: GestorInventario
) -> ResultadoPedidoDict:
    """
    Procesa un pedido reduciendo el inventario.
    
    Args:
        pedido: Pedido a procesar con lista de items.
        inventario: Gestor de inventario donde verificar stock.
    
    Returns:
        Resultado del procesamiento con items exitosos y fallidos.
    
    Examples:
        >>> inv = GestorInventario(100)
        >>> pedido = {"items": [{"producto_id": 1, "cantidad": 2}]}
        >>> resultado = procesar_pedido(pedido, inv)
        >>> resultado["exito"]
        False
    """
    resultado: ResultadoPedidoDict = {
        "exito": True,
        "items_procesados": [],
        "items_fallidos": []
    }
    
    for item in pedido["items"]:
        producto = inventario.buscar(item["producto_id"])
        
        if producto is None:
            resultado["items_fallidos"].append({
                "producto_id": item["producto_id"],
                "razon": "Producto no encontrado"
            })
            continue
        
        if producto["cantidad"] < item["cantidad"]:
            resultado["items_fallidos"].append({
                "producto_id": item["producto_id"],
                "razon": "Stock insuficiente"
            })
            continue
        
        # mypy verifica que producto["cantidad"] es int
        producto["cantidad"] -= item["cantidad"]
        resultado["items_procesados"].append(item)
    
    if resultado["items_fallidos"]:
        resultado["exito"] = False
    
    return resultado


# Uso del código CON tipos
if __name__ == "__main__":
    # Con tipos, el IDE proporciona autocompletado y verifica tipos
    inventario: GestorInventario = GestorInventario(100)
    
    producto: ProductoDict = {
        "id": 1,
        "nombre": "Laptop",
        "precio": 1200.0,
        "cantidad": 10,
        "categoria": "Electrónica"
    }
    inventario.agregar_producto(producto)
    
    carrito: CarritoCompras = CarritoCompras()
    
    mouse: ProductoDict = {
        "id": 2,
        "nombre": "Mouse",
        "precio": 25.0,
        "cantidad": 50,
        "categoria": "Accesorios"
    }
    
    carrito.agregar_item(mouse, 2)
    carrito.aplicar_descuento("VERANO2024", 10.0)
    
    # El IDE sabe que total es float
    total: float = carrito.calcular_total()
    print(f"Total: ${total:.2f}")
    
    # El IDE sabe exactamente qué retorna y su estructura
    pedido: PedidoDict = {
        "items": [{"producto_id": 1, "cantidad": 2}]
    }
    resultado: ResultadoPedidoDict = procesar_pedido(pedido, inventario)
    
    # Autocompletado funciona perfecto aquí
    if resultado["exito"]:
        print(f"Pedido procesado: {len(resultado['items_procesados'])} items")
    else:
        print(f"Pedido con errores: {len(resultado['items_fallidos'])} items fallidos")
        for item_fallido in resultado["items_fallidos"]:
            print(f"  - Producto {item_fallido['producto_id']}: {item_fallido['razon']}")
