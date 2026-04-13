"""
Ejemplo: Código SIN Type Hints
================================
Este archivo muestra código funcional pero sin anotaciones de tipos.
"""

# Sin tipos - difícil de entender qué recibe/retorna
def calcular_descuento(precio, porcentaje):
    return precio * (1 - porcentaje / 100)


def buscar_usuario(usuarios, criterio):
    if isinstance(criterio, int):
        return next((u for u in usuarios if u["id"] == criterio), None)
    elif isinstance(criterio, str):
        return [u for u in usuarios if criterio.lower() in u["nombre"].lower()]
    return None


class CarritoCompras:
    def __init__(self):
        self.items = []
        self.descuentos = {}
    
    def agregar_item(self, producto, cantidad):
        self.items.append({
            "producto": producto,
            "cantidad": cantidad,
            "precio": producto["precio"]
        })
    
    def aplicar_descuento(self, codigo, porcentaje):
        self.descuentos[codigo] = porcentaje
    
    def calcular_total(self):
        subtotal = sum(item["precio"] * item["cantidad"] for item in self.items)
        
        descuento_total = 0
        for porcentaje in self.descuentos.values():
            descuento_total += subtotal * (porcentaje / 100)
        
        return subtotal - descuento_total
    
    def obtener_resumen(self):
        return {
            "items": self.items,
            "subtotal": sum(item["precio"] * item["cantidad"] for item in self.items),
            "descuentos": self.descuentos,
            "total": self.calcular_total()
        }


class GestorInventario:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.productos = {}
    
    def agregar_producto(self, producto):
        if len(self.productos) >= self.capacidad:
            raise ValueError("Inventario lleno")
        
        producto_id = producto["id"]
        if producto_id in self.productos:
            self.productos[producto_id]["cantidad"] += producto["cantidad"]
        else:
            self.productos[producto_id] = producto
    
    def buscar(self, producto_id):
        return self.productos.get(producto_id)
    
    def filtrar_por_categoria(self, categoria):
        return [
            p for p in self.productos.values() 
            if p.get("categoria") == categoria
        ]
    
    def productos_bajo_stock(self, minimo):
        return [
            p for p in self.productos.values() 
            if p["cantidad"] < minimo
        ]


def procesar_pedido(pedido, inventario):
    """Procesa un pedido reduciendo el inventario."""
    resultado = {
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
        
        producto["cantidad"] -= item["cantidad"]
        resultado["items_procesados"].append(item)
    
    if resultado["items_fallidos"]:
        resultado["exito"] = False
    
    return resultado


# Uso del código
if __name__ == "__main__":
    # Sin tipos, el IDE no puede ayudar mucho
    inventario = GestorInventario(100)
    
    inventario.agregar_producto({
        "id": 1,
        "nombre": "Laptop",
        "precio": 1200.0,
        "cantidad": 10,
        "categoria": "Electrónica"
    })
    
    carrito = CarritoCompras()
    carrito.agregar_item({"nombre": "Mouse", "precio": 25.0}, 2)
    carrito.aplicar_descuento("VERANO2024", 10)
    
    total = carrito.calcular_total()
    print(f"Total: ${total:.2f}")
    
    # ¿Qué retorna esto? No está claro sin ver la implementación
    resultado = procesar_pedido(
        {"items": [{"producto_id": 1, "cantidad": 2}]},
        inventario
    )
