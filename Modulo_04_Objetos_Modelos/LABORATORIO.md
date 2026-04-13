# Laboratorio: Objetos y Modelos de Datos

## Objetivos
- Modelar entidades con comportamientos y validaciones
- Implementar cálculos derivados y comparaciones
- Serializar y validar entradas/salidas con Pydantic
- Convertir entre modelos Pydantic y entidades de dominio

---

## Ejercicio 1: Dataclass Order con Cálculos y Comparaciones ⭐⭐⭐

### Descripción
Implementar un sistema de órdenes usando dataclasses con cálculos derivados, comparaciones personalizadas y validación.

### Requisitos

**Parte A: Modelo ItemOrder**
Crear una dataclass `ItemOrder` (inmutable) con:
- `product_id`: str
- `product_name`: str
- `quantity`: int (mayor a 0)
- `unit_price`: float (mayor a 0)
- Método `subtotal()` que retorne quantity × unit_price
- Método `apply_discount(percentage: float)` que retorne nuevo ItemOrder con precio con descuento

**Parte B: Modelo Order con Cálculos Derivados**
Crear una dataclass `Order` con:
- `order_id`: str
- `customer_name`: str
- `items`: List[ItemOrder] (usar default_factory)
- `discount_percentage`: float = 0.0 (entre 0 y 100)
- `tax_rate`: float = 0.16 (IVA)
- `created_at`: datetime (auto-generado con default_factory)
- `status`: str = "pending"

Métodos requeridos:
1. `add_item(item: ItemOrder)` - Agregar item a la orden
2. `remove_item(product_id: str)` - Eliminar item por ID
3. `item_count() -> int` - Total de items (suma de cantidades)
4. `subtotal() -> float` - Suma de subtotales de todos los items
5. `discount_amount() -> float` - Calcular monto de descuento
6. `tax_amount() -> float` - Calcular impuestos sobre (subtotal - descuento)
7. `total() -> float` - Total final
8. `most_expensive_item() -> Optional[ItemOrder]` - Item con mayor subtotal

**Parte C: Comparaciones y Ordenamiento**
Implementar:
- Configurar `order=True` solo comparando por `total()` descendente
- Usar `field()` con `compare=False` en campos que no deben compararse
- Método `__post_init__` para validar:
  - La orden debe tener al menos un item
  - discount_percentage entre 0 y 100
  - tax_rate entre 0 y 1

### Casos de Prueba

```python
def test_order_system():
    # Crear items
    item1 = ItemOrder("PROD-001", "Laptop", 2, 1200.0)
    item2 = ItemOrder("PROD-002", "Mouse", 3, 25.0)
    item3 = ItemOrder("PROD-003", "Teclado", 2, 150.0)
    
    # Crear orden
    order = Order(
        order_id="ORD-001",
        customer_name="Juan Pérez",
        discount_percentage=10.0
    )
    
    # Agregar items
    order.add_item(item1)
    order.add_item(item2)
    order.add_item(item3)
    
    # Verificar cálculos
    assert order.item_count() == 7  # 2 + 3 + 2
    assert order.subtotal() == 2775.0  # 2400 + 75 + 300
    assert order.discount_amount() == 277.5  # 10% de 2775
    assert order.tax_amount() == 399.6  # 16% de (2775 - 277.5)
    assert order.total() == 2897.1  # 2775 - 277.5 + 399.6
    
    # Item más caro
    assert order.most_expensive_item().product_id == "PROD-001"
    
    # Comparación de órdenes
    order2 = Order("ORD-002", "Ana García", discount_percentage=5.0)
    order2.add_item(ItemOrder("PROD-004", "Monitor", 1, 500.0))
    
    # order debería ser "mayor" porque tiene mayor total
    assert order > order2
    
    print("✅ Todas las pruebas pasaron")
```

### Salida esperada del resumen
Implementar método `summary() -> str` que retorne:
```
╔═══════════════════════════════════════════════════════════╗
║ ORDEN: ORD-001                                            ║
║ Cliente: Juan Pérez                                       ║
║ Fecha: 2024-04-13 10:30:45                               ║
║ Estado: pending                                           ║
╠═══════════════════════════════════════════════════════════╣
║ ITEMS:                                                    ║
║   2x Laptop           @ $1,200.00 = $2,400.00            ║
║   3x Mouse            @ $   25.00 = $   75.00            ║
║   2x Teclado          @ $  150.00 = $  300.00            ║
╠═══════════════════════════════════════════════════════════╣
║ Subtotal:                              $2,775.00          ║
║ Descuento (10.0%):                     -$ 277.50          ║
║ Base imponible:                        $2,497.50          ║
║ IVA (16%):                             $  399.60          ║
╠═══════════════════════════════════════════════════════════╣
║ TOTAL:                                 $2,897.10          ║
╚═══════════════════════════════════════════════════════════╝
```

---

## Ejercicio 2: Modelos Pydantic (OrderIn/OrderOut) ⭐⭐⭐⭐

### Descripción
Crear modelos Pydantic para validación de entrada/salida en una API de órdenes, con conversión entre DTOs y entidades de dominio.

### Requisitos

**Parte A: Modelos de Entrada (DTOs)**

1. `ItemOrderDTO` (BaseModel):
   - `product_id`: str (longitud 3-50)
   - `product_name`: str (longitud 1-200)
   - `quantity`: int (min=1, max=1000)
   - `unit_price`: float (min=0.01, max=1000000)

2. `CreateOrderRequest` (BaseModel):
   - `customer_name`: str (longitud 2-100)
   - `customer_email`: EmailStr
   - `items`: List[ItemOrderDTO] (mínimo 1 item)
   - `discount_code`: Optional[str] = None
   - `shipping_address`: str (longitud 10-500)
   - `notes`: Optional[str] = None
   
   Validadores:
   - `customer_name` debe tener al menos 2 palabras (nombre y apellido)
   - Si hay `discount_code`, debe tener formato "DESC-XXXX" (regex)
   - Model validator: validar que el subtotal sea mayor a $10

**Parte B: Modelos de Salida (Respuestas)**

1. `ItemOrderResponse` (BaseModel):
   - `product_id`: str
   - `product_name`: str
   - `quantity`: int
   - `unit_price`: float
   - `subtotal`: float  # Campo calculado

2. `OrderResponse` (BaseModel):
   - `order_id`: str
   - `customer_name`: str
   - `customer_email`: EmailStr
   - `items`: List[ItemOrderResponse]
   - `status`: Literal["pending", "processing", "shipped", "delivered", "cancelled"]
   - `subtotal`: float
   - `discount_percentage`: float
   - `discount_amount`: float
   - `tax_amount`: float
   - `total`: float
   - `created_at`: datetime
   - `updated_at`: datetime
   - `shipping_address`: str
   - `notes`: Optional[str] = None
   
   Config: `from_attributes=True` para construir desde entidad

**Parte C: Entidad de Dominio (NO Pydantic)**

Crear clase `OrderEntity` (Python puro, sin Pydantic ni dataclass):
- Similar a la dataclass del Ejercicio 1 pero con lógica de negocio
- Métodos de negocio: `process()`, `ship()`, `deliver()`, `cancel()`
- Validaciones de transiciones de estado
- Propiedades para cálculos derivados

**Parte D: Funciones de Conversión**

Implementar:
```python
def apply_discount_code(code: str) -> float:
    """Retornar porcentaje de descuento según código."""
    # Implementar lógica (ej: DESC-2024 = 20%, DESC-PROMO = 15%)
    pass

def create_order_from_request(
    request: CreateOrderRequest, 
    order_id: str
) -> OrderEntity:
    """Convertir DTO de entrada a entidad de dominio."""
    pass

def order_entity_to_response(
    order: OrderEntity
) -> OrderResponse:
    """Convertir entidad de dominio a DTO de salida."""
    pass
```

### Casos de Prueba

```python
def test_pydantic_validation():
    # Datos de entrada válidos
    request_data = {
        "customer_name": "María García López",
        "customer_email": "maria@example.com",
        "items": [
            {
                "product_id": "PROD-001",
                "product_name": "Laptop Dell XPS",
                "quantity": 1,
                "unit_price": 1500.00
            },
            {
                "product_id": "PROD-002",
                "product_name": "Mouse Inalámbrico",
                "quantity": 2,
                "unit_price": 25.50
            }
        ],
        "discount_code": "DESC-2024",
        "shipping_address": "Av. Reforma 123, Col. Centro, CDMX, 06000",
        "notes": "Entregar en horario de oficina"
    }
    
    # 1. Validar entrada
    request = CreateOrderRequest.model_validate(request_data)
    assert len(request.items) == 2
    
    # 2. Crear entidad
    order_entity = create_order_from_request(request, "ORD-2024-001")
    assert order_entity.total() > 0
    
    # 3. Procesar orden
    order_entity.process()
    assert order_entity.status == "processing"
    
    # 4. Convertir a respuesta
    response = order_entity_to_response(order_entity)
    assert response.order_id == "ORD-2024-001"
    assert response.status == "processing"
    
    # 5. Serializar a JSON
    response_json = response.model_dump_json(indent=2)
    print(response_json)
    
    # 6. Deserializar desde JSON
    response_copy = OrderResponse.model_validate_json(response_json)
    assert response_copy.total == response.total
    
    print("✅ Todas las pruebas de Pydantic pasaron")

def test_validation_errors():
    """Probar que las validaciones funcionen."""
    # Nombre inválido (una sola palabra)
    try:
        CreateOrderRequest.model_validate({
            "customer_name": "María",
            "customer_email": "maria@example.com",
            "items": [...],
            "shipping_address": "Dirección..."
        })
        assert False, "Debería fallar"
    except ValidationError:
        print("✅ Validación de nombre funciona")
    
    # Email inválido
    try:
        CreateOrderRequest.model_validate({
            "customer_name": "María García",
            "customer_email": "no-es-email",
            ...
        })
        assert False, "Debería fallar"
    except ValidationError:
        print("✅ Validación de email funciona")
    
    # Código de descuento inválido
    try:
        CreateOrderRequest.model_validate({
            "customer_name": "María García",
            "customer_email": "maria@example.com",
            "discount_code": "INVALIDO",
            ...
        })
        assert False, "Debería fallar"
    except ValidationError:
        print("✅ Validación de código funciona")
```

---

## Ejercicio 3: Sistema Completo de Gestión de Inventario ⭐⭐⭐⭐⭐

### Descripción
Integrar todos los conceptos en un sistema completo con múltiples entidades relacionadas.

### Requisitos

**Entidades a Implementar:**

1. **Product** (dataclass):
   - Información base del producto
   - SKU, nombre, descripción, categoría
   - Precio base, costo
   - Stock actual, stock mínimo
   - Estado (activo/inactivo)

2. **Supplier** (dataclass):
   - Información del proveedor
   - Productos que suministra
   - Términos de pago

3. **PurchaseOrder** (dataclass + Pydantic):
   - Orden de compra a proveedor
   - Items ordenados
   - Estados y aprobaciones

4. **Inventory Transaction** (Pydantic):
   - Movimientos de inventario
   - Tipos: entrada, salida, ajuste
   - Validación de stock suficiente

**Funcionalidades:**

1. Validación de stock antes de venta
2. Alertas de stock bajo
3. Cálculo de valor de inventario
4. Historial de transacciones
5. Reportes de rotación de productos

### Ejemplo de Uso

```python
# Crear productos
laptop = Product(
    sku="ELEC-001",
    name="Laptop Dell XPS 15",
    category="Electronics",
    base_price=1500.0,
    cost=1200.0,
    current_stock=10,
    min_stock=3
)

# Validar venta
sale_request = SaleRequest(
    product_sku="ELEC-001",
    quantity=2,
    customer_id="CUST-001"
)

# Procesar con validación
if laptop.can_fulfill(sale_request.quantity):
    transaction = process_sale(sale_request)
    laptop.current_stock -= sale_request.quantity
    print(f"✅ Venta procesada: {transaction.id}")
else:
    print("❌ Stock insuficiente")

# Alerta de stock bajo
if laptop.is_low_stock():
    purchase_order = generate_purchase_order(laptop, quantity=20)
    print(f"⚠️ Stock bajo. Orden de compra creada: {purchase_order.id}")
```

---

## Consejos y Mejores Prácticas

1. **Dataclasses:**
   - Usar `frozen=True` para objetos inmutables
   - `default_factory` para listas/dicts mutables
   - `field(compare=False)` para excluir de comparaciones
   - `__post_init__` para validaciones complejas

2. **Pydantic:**
   - Separar modelos de entrada/salida (DTOs) de entidades de dominio
   - Usar `Field()` con constraints apropiados
   - Validadores personalizados para lógica compleja
   - `ConfigDict(from_attributes=True)` para crear desde objetos

3. **Arquitectura:**
   - DTOs (Pydantic) para fronteras del sistema (APIs)
   - Entidades (dataclass o clases puras) para lógica de negocio
   - Funciones de conversión explícitas entre capas
   - Validación de negocio en entidades, validación de formato en DTOs

4. **Testing:**
   - Probar casos válidos e inválidos
   - Verificar que las validaciones fallen correctamente
   - Probar conversiones entre modelos
   - Usar `pytest.raises()` para errores esperados

---

## Entrega

Crear archivo `laboratorio_04_solucion.py` con:
1. Todas las clases y funciones implementadas
2. Función `main()` que ejecute casos de prueba
3. Documentación en docstrings
4. Type hints en todas las funciones
5. Comentarios explicativos en lógica compleja

**Ejecutar:**
```bash
python laboratorio_04_solucion.py
```

**Salida esperada:**
```
=== EJERCICIO 1: Dataclass Order ===
✅ Todas las pruebas pasaron
[Mostrar resumen de orden]

=== EJERCICIO 2: Pydantic Models ===
✅ Validación de entrada correcta
✅ Conversión a entidad exitosa
✅ Conversión a respuesta exitosa
[Mostrar JSON de respuesta]

=== EJERCICIO 3: Sistema de Inventario ===
✅ Productos creados
✅ Venta procesada
⚠️ Alerta de stock bajo generada
✅ Sistema funcionando correctamente
```

---

## Recursos Adicionales

- [Dataclasses Guide](https://docs.python.org/3/library/dataclasses.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Type Hints Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- Revisar ejemplos en `04_pydantic_validacion.py` para patrones de conversión
