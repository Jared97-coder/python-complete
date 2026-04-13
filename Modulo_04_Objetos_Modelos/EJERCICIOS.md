# EJERCICIOS - Módulo 4: Objetos y Modelos de Datos

## Ejercicio 1: Sistema de Biblioteca con POO ⭐⭐

### Objetivo
Practicar clases básicas, herencia y composición.

### Instrucciones

Crear un sistema de biblioteca con las siguientes clases:

1. **Clase `Item`** (clase base abstracta):
   - `titulo`: str
   - `año`: int
   - `disponible`: bool
   - Método abstracto: `info()` que retorna string con información del item

2. **Clase `Libro`** (hereda de Item):
   - `autor`: str
   - `isbn`: str
   - `paginas`: int
   - Implementar `info()`

3. **Clase `Revista`** (hereda de Item):
   - `numero_edicion`: int
   - `mes`: str
   - Implementar `info()`

4. **Clase `Usuario`**:
   - `nombre`: str
   - `id_usuario`: str
   - `items_prestados`: List[Item]
   - Método `prestar_item(item: Item)`
   - Método `devolver_item(item: Item)`
   - Método `puede_prestar() -> bool` (máximo 3 items)

5. **Clase `Biblioteca`** (composición):
   - `catalogo`: List[Item]
   - `usuarios`: List[Usuario]
   - Método `agregar_item(item: Item)`
   - Método `buscar_por_titulo(titulo: str) -> List[Item]`
   - Método `items_disponibles() -> List[Item]`

### Código de prueba
```python
# Crear biblioteca
biblioteca = Biblioteca()

# Agregar items
libro1 = Libro("1984", 1949, "George Orwell", "978-0451524935", 328)
revista1 = Revista("National Geographic", 2024, 150, "Enero")
biblioteca.agregar_item(libro1)
biblioteca.agregar_item(revista1)

# Crear usuario y prestar
usuario = Usuario("Ana García", "U001")
usuario.prestar_item(libro1)

print(usuario.items_prestados[0].info())
# Esperado: "Libro: '1984' por George Orwell (1949) - ISBN: 978-0451524935"
```

---

## Ejercicio 2: Métodos Mágicos para Clase Dinero ⭐⭐

### Objetivo
Implementar dunder methods para operaciones con dinero.

### Instrucciones

Crear clase `Dinero` con:
- `cantidad`: float
- `moneda`: str (ej: "USD", "MXN", "EUR")

Implementar:
- `__str__` → "$1,234.56 USD"
- `__repr__` → "Dinero(1234.56, 'USD')"
- `__add__` → Sumar solo si misma moneda
- `__sub__` → Restar solo si misma moneda
- `__eq__` → Comparar cantidad y moneda
- `__lt__`, `__gt__` → Comparar solo si misma moneda
- `__mul__` → Multiplicar por número
- `__neg__` → Negación (deuda)
- `__abs__` → Valor absoluto

### Código de prueba
```python
d1 = Dinero(100.50, "USD")
d2 = Dinero(50.25, "USD")
d3 = Dinero(75.00, "MXN")

print(d1 + d2)  # Dinero(150.75, "USD")
print(d1 > d2)  # True
print(d1 * 2)   # Dinero(201.00, "USD")
print(-d1)      # Dinero(-100.50, "USD")

# Esto debe lanzar error:
# print(d1 + d3)  # ValueError: No se pueden sumar monedas diferentes
```

---

## Ejercicio 3: Carrito de Compras con Dataclass ⭐⭐⭐

### Objetivo
Usar dataclasses para modelar un carrito de compras.

### Instrucciones

1. **Dataclass `ProductoCarrito`** (frozen):
   - `producto_id`: str
   - `nombre`: str
   - `precio`: float
   - `cantidad`: int = 1
   - Método `subtotal()` → precio × cantidad

2. **Dataclass `Carrito`**:
   - `usuario_id`: str
   - `items`: List[ProductoCarrito] = field(default_factory=list)
   - `codigo_descuento`: Optional[str] = None
   - `_creado_en`: datetime = field(default_factory=datetime.now, init=False)
   
   Métodos:
   - `agregar_producto(producto: ProductoCarrito)`
   - `eliminar_producto(producto_id: str)`
   - `actualizar_cantidad(producto_id: str, cantidad: int)`
   - `subtotal() -> float`
   - `aplicar_descuento() -> float` (10% si hay código)
   - `total() -> float`
   - `cantidad_items() -> int`

3. Configurar `order=True` para comparar por total.

### Código de prueba
```python
carrito = Carrito(usuario_id="U123", codigo_descuento="DESC10")
carrito.agregar_producto(ProductoCarrito("P1", "Laptop", 1000.0, 1))
carrito.agregar_producto(ProductoCarrito("P2", "Mouse", 25.0, 2))

print(f"Subtotal: ${carrito.subtotal():.2f}")  # 1050.00
print(f"Descuento: ${carrito.aplicar_descuento():.2f}")  # 105.00
print(f"Total: ${carrito.total():.2f}")  # 945.00
```

---

## Ejercicio 4: Validación de Formulario con Pydantic ⭐⭐⭐

### Objetivo
Validar datos de formulario de registro de usuario.

### Instrucciones

Crear modelo Pydantic `RegistroUsuario` con:
- `username`: str (3-20 caracteres, solo alfanuméricos y guion bajo)
- `email`: EmailStr
- `password`: str (mínimo 8 caracteres)
- `password_confirmacion`: str
- `edad`: int (18-100)
- `fecha_nacimiento`: date
- `telefono`: str (formato: "XXX-XXX-XXXX")
- `acepta_terminos`: bool
- `newsletter`: bool = False

Validadores:
1. `username` debe empezar con letra
2. `password` debe tener al menos 1 mayúscula, 1 minúscula, 1 número
3. `password == password_confirmacion`
4. `edad` debe coincidir con `fecha_nacimiento` (±1 año tolerancia)
5. `acepta_terminos` debe ser True
6. `telefono` debe seguir regex pattern

### Código de prueba
```python
# Caso válido
datos_validos = {
    "username": "ana_garcia",
    "email": "ana@example.com",
    "password": "Segura123",
    "password_confirmacion": "Segura123",
    "edad": 25,
    "fecha_nacimiento": "1999-01-15",
    "telefono": "555-123-4567",
    "acepta_terminos": True
}

usuario = RegistroUsuario.model_validate(datos_validos)
print("✅ Usuario válido")

# Caso inválido
datos_invalidos = {
    "username": "ab",  # Muy corto
    "email": "no-es-email",
    "password": "corta",  # Sin mayúsculas ni números
    "password_confirmacion": "diferente",
    "edad": 17,  # Menor de edad
    "fecha_nacimiento": "2007-01-01",
    "telefono": "123456789",  # Formato incorrecto
    "acepta_terminos": False
}

try:
    RegistroUsuario.model_validate(datos_invalidos)
except ValidationError as e:
    print(f"❌ Errores encontrados: {len(e.errors())}")
    for error in e.errors():
        print(f"  - {error['loc'][0]}: {error['msg']}")
```

---

## Ejercicio 5: API de Blog con DTOs ⭐⭐⭐⭐

### Objetivo
Crear modelos Pydantic para API de blog con conversión a entidades.

### Instrucciones

**Modelos Pydantic:**

1. `CreatePostRequest`:
   - `title`: str (5-200 caracteres)
   - `content`: str (mínimo 10 caracteres)
   - `tags`: List[str] (máximo 5 tags)
   - `author_id`: str
   - `publish_immediately`: bool = False

2. `UpdatePostRequest`:
   - Todos los campos opcionales
   - Al menos uno debe estar presente (model_validator)

3. `PostResponse`:
   - `id`: str
   - `title`: str
   - `content`: str
   - `author_id`: str
   - `author_name`: str
   - `tags`: List[str]
   - `created_at`: datetime
   - `updated_at`: datetime
   - `published_at`: Optional[datetime]
   - `view_count`: int
   - `comment_count`: int
   - `status`: Literal["draft", "published", "archived"]

**Entidad de Dominio:**

4. `PostEntity` (clase Python pura):
   - Atributos similares a PostResponse
   - Métodos: `publish()`, `archive()`, `increment_views()`, `add_comment()`
   - Validar transiciones de estado

**Funciones de Conversión:**
- `create_post_from_request(request, post_id) -> PostEntity`
- `post_to_response(post: PostEntity, author_name: str) -> PostResponse`
- `update_post_from_request(post: PostEntity, request: UpdatePostRequest) -> PostEntity`

### Código de prueba
```python
# Crear post
request = CreatePostRequest(
    title="Introducción a Python",
    content="Python es un lenguaje de programación...",
    tags=["python", "tutorial", "programación"],
    author_id="AUTH-001",
    publish_immediately=True
)

post = create_post_from_request(request, "POST-001")
if request.publish_immediately:
    post.publish()

response = post_to_response(post, author_name="Juan Pérez")
print(response.model_dump_json(indent=2))

# Actualizar post
update = UpdatePostRequest(title="Introducción a Python 3.12")
post = update_post_from_request(post, update)

# Incrementar vistas
for _ in range(5):
    post.increment_views()

print(f"Vistas: {post.view_count}")  # 5
```

---

## Ejercicio 6: Context Manager para Base de Datos ⭐⭐⭐

### Objetivo
Crear context manager personalizado para transacciones.

### Instrucciones

Crear clase `DatabaseTransaction` que:
1. Simule conexión a base de datos en `__enter__`
2. Simule commit en `__exit__` si no hay errores
3. Simule rollback en `__exit__` si hay excepción
4. Registre todas las operaciones en un log

```python
class DatabaseTransaction:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.operations = []
        self.connected = False
    
    def __enter__(self):
        # Implementar
        pass
    
    def __exit__(self, exc_type, exc_value, traceback):
        # Implementar
        pass
    
    def execute(self, operation: str):
        # Simular operación
        pass

# Uso
with DatabaseTransaction("mi_db") as db:
    db.execute("INSERT INTO users ...")
    db.execute("UPDATE products ...")
    # Auto-commit al salir

try:
    with DatabaseTransaction("mi_db") as db:
        db.execute("INSERT ...")
        raise ValueError("Error!")  # Auto-rollback
except ValueError:
    print("Transacción revertida")
```

---

## Ejercicio 7: Comparable y Sortable ⭐⭐

### Objetivo
Implementar comparaciones para clase Employee.

### Instrucciones

Crear clase `Employee` con:
- `name`: str
- `salary`: float
- `years_experience`: int
- `department`: str

Implementar comparaciones para:
- Ordenar por salario (descendente) como default
- Método `sorted_by_experience()` usando key function
- Método `sorted_by_name()` usando key function

```python
employees = [
    Employee("Ana", 50000, 5, "IT"),
    Employee("Bob", 60000, 3, "Sales"),
    Employee("Carlos", 50000, 7, "IT")
]

# Por salario (default)
sorted_emp = sorted(employees)
print([e.name for e in sorted_emp])  # ["Bob", "Ana", "Carlos"]

# Por experiencia
sorted_exp = sorted(employees, key=lambda e: e.years_experience)
print([e.name for e in sorted_exp])  # ["Bob", "Ana", "Carlos"]
```

---

## Soluciones

Las soluciones están disponibles en:
- `ejercicios_04_soluciones.py`

Para verificar tu implementación:
```bash
python ejercicios_04_soluciones.py
```

---

## Consejos

1. **POO**: Pensar en "is-a" (herencia) vs "has-a" (composición)
2. **Dataclasses**: Usar frozen=True cuando sea posible para inmutabilidad
3. **Pydantic**: Separar claramente DTOs de entidades de dominio
4. **Validación**: Validar formato en DTOs, validar negocio en entidades
5. **Type hints**: Usar siempre para mejor documentación y detección de errores

¡Éxito con los ejercicios! 🚀
