"""
Módulo 9.3 - Pydantic y Validación

Schemas con Pydantic, validaciones avanzadas, custom validators,
settings, y manejo de errores personalizados.

Para ejecutar:
    uvicorn 03_pydantic_validacion:app --reload
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    HttpUrl,
    field_validator,
    model_validator,
    ConfigDict
)
from typing import Optional, List, Literal
from datetime import datetime, date
from decimal import Decimal
from enum import Enum

app = FastAPI(title="Pydantic y Validación", version="1.0.0")


# =============================================================================
# Ejemplo 1: Schemas Básicos con Field
# =============================================================================

class Product(BaseModel):
    """Schema de Producto con validaciones."""
    
    name: str = Field(
        ...,  # Obligatorio
        min_length=3,
        max_length=100,
        description="Nombre del producto"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Descripción opcional"
    )
    price: Decimal = Field(
        ...,
        gt=0,  # Greater than 0
        max_digits=10,
        decimal_places=2,
        description="Precio en USD"
    )
    stock: int = Field(
        default=0,
        ge=0,  # Greater or equal
        description="Cantidad en stock"
    )
    is_available: bool = Field(default=True)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop Pro",
                "description": "High performance laptop",
                "price": 1299.99,
                "stock": 10,
                "is_available": True
            }
        }
    )


@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):
    """Crear producto con validación automática."""
    return product


# =============================================================================
# Ejemplo 2: Tipos de Datos Especializados
# =============================================================================

class UserProfile(BaseModel):
    """Schema con tipos especializados de Pydantic."""
    
    username: str = Field(..., pattern="^[a-zA-Z0-9_-]{3,20}$")
    email: EmailStr  # Valida formato de email
    website: Optional[HttpUrl] = None  # Valida URL
    birth_date: date  # Solo fecha
    created_at: datetime = Field(default_factory=datetime.now)
    age: Optional[int] = Field(None, ge=0, le=150)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "website": "https://johndoe.com",
                "birth_date": "1990-01-15",
                "age": 34
            }
        }
    )


@app.post("/users/profile", response_model=UserProfile)
async def create_profile(profile: UserProfile):
    """Crear perfil con validaciones especializadas."""
    return profile


# =============================================================================
# Ejemplo 3: Field Validators (Custom Validation)
# =============================================================================

class Order(BaseModel):
    """Order con validadores personalizados."""
    
    order_id: str
    customer_email: EmailStr
    items: List[str] = Field(..., min_length=1)
    total: Decimal = Field(..., gt=0)
    discount_percent: float = Field(0, ge=0, le=100)
    
    @field_validator('order_id')
    @classmethod
    def validate_order_id(cls, v):
        """Validar formato de order_id."""
        if not v.startswith('ORD-'):
            raise ValueError('order_id debe comenzar con ORD-')
        if len(v) != 10:  # ORD-XXXXXX
            raise ValueError('order_id debe tener 10 caracteres')
        return v
    
    @field_validator('total')
    @classmethod
    def validate_total(cls, v):
        """Validar que el total no sea múltiplo de 666 (ejemplo)."""
        if v == 666:
            raise ValueError('Total no puede ser 666')
        return v
    
    @field_validator('discount_percent')
    @classmethod
    def validate_discount(cls, v):
        """Validar descuento razonable."""
        if v > 50:
            raise ValueError('Descuento no puede ser mayor a 50%')
        return v


@app.post("/orders", response_model=Order)
async def create_order(order: Order):
    """Crear orden con validaciones custom."""
    return order


# =============================================================================
# Ejemplo 4: Model Validators (Validación entre campos)
# =============================================================================

class Booking(BaseModel):
    """Reserva con validación de fechas."""
    
    booking_id: str
    check_in: date
    check_out: date
    guests: int = Field(..., ge=1, le=10)
    
    @model_validator(mode='after')
    def validate_dates(self):
        """Validar que check_out sea después de check_in."""
        if self.check_out <= self.check_in:
            raise ValueError('check_out debe ser después de check_in')
        
        # Validar duración máxima
        duration = (self.check_out - self.check_in).days
        if duration > 30:
            raise ValueError('Duración máxima: 30 días')
        
        return self


@app.post("/bookings", response_model=Booking)
async def create_booking(booking: Booking):
    """Crear reserva con validación de fechas."""
    return booking


# =============================================================================
# Ejemplo 5: Nested Models (Modelos Anidados)
# =============================================================================

class Address(BaseModel):
    """Dirección."""
    street: str
    city: str
    state: str
    zip_code: str = Field(..., pattern="^\d{5}$")
    country: str = "USA"


class ContactInfo(BaseModel):
    """Información de contacto."""
    phone: str = Field(..., pattern="^\+?1?\d{9,15}$")
    email: EmailStr
    address: Address  # Modelo anidado


class Customer(BaseModel):
    """Cliente con modelos anidados."""
    name: str
    contact: ContactInfo  # Modelo anidado
    is_premium: bool = False


@app.post("/customers", response_model=Customer)
async def create_customer(customer: Customer):
    """
    Crear cliente con modelos anidados.
    
    Request body:
    {
        "name": "Alice Johnson",
        "contact": {
            "phone": "+1234567890",
            "email": "alice@example.com",
            "address": {
                "street": "123 Main St",
                "city": "NYC",
                "state": "NY",
                "zip_code": "10001"
            }
        }
    }
    """
    return customer


# =============================================================================
# Ejemplo 6: List and Dict Fields
# =============================================================================

class ShoppingCart(BaseModel):
    """Carrito de compras con listas y diccionarios."""
    
    user_id: int
    items: List[Product]  # Lista de productos
    metadata: dict = {}  # Diccionario libre
    tags: List[str] = Field(default_factory=list)
    
    @field_validator('items')
    @classmethod
    def validate_items(cls, v):
        """Validar que haya al menos 1 item."""
        if not v:
            raise ValueError('Carrito debe tener al menos 1 item')
        return v


@app.post("/cart", response_model=ShoppingCart)
async def create_cart(cart: ShoppingCart):
    """Crear carrito con lista de productos."""
    return cart


# =============================================================================
# Ejemplo 7: Union Types y Literal
# =============================================================================

class PaymentMethod(str, Enum):
    """Métodos de pago permitidos."""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    CASH = "cash"


class Payment(BaseModel):
    """Pago con Union y Literal."""
    
    amount: Decimal
    method: PaymentMethod  # Enum
    status: Literal["pending", "completed", "failed"]  # Solo estos valores
    currency: Literal["USD", "EUR", "MXN"] = "USD"


@app.post("/payments", response_model=Payment)
async def create_payment(payment: Payment):
    """
    Crear pago con tipos restringidos.
    
    method: solo credit_card, debit_card, paypal, cash
    status: solo pending, completed, failed
    currency: solo USD, EUR, MXN
    """
    return payment


# =============================================================================
# Ejemplo 8: Optional y Defaults
# =============================================================================

class Article(BaseModel):
    """Artículo con campos opcionales."""
    
    title: str
    content: str
    author: str = "Anonymous"  # Default
    published: bool = False
    views: int = 0
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None


@app.post("/articles", response_model=Article)
async def create_article(article: Article):
    """Crear artículo (muchos campos opcionales)."""
    return article


# =============================================================================
# Ejemplo 9: Response Models - Exclude Fields
# =============================================================================

class UserCreateSchema(BaseModel):
    """Schema para crear usuario (incluye password)."""
    email: EmailStr
    username: str
    password: str = Field(..., min_length=8)
    full_name: str


class UserResponseSchema(BaseModel):
    """Schema de respuesta (excluye password)."""
    id: int
    email: EmailStr
    username: str
    full_name: str
    created_at: datetime
    
    # No incluye password!


fake_users_db = []
user_id_counter = 1


@app.post("/auth/register", response_model=UserResponseSchema)
async def register_user(user: UserCreateSchema):
    """
    Registrar usuario.
    
    Request incluye password, pero response NO lo devuelve.
    """
    global user_id_counter
    
    user_dict = user.model_dump()
    user_dict["id"] = user_id_counter
    user_dict["created_at"] = datetime.now()
    
    fake_users_db.append(user_dict)
    user_id_counter += 1
    
    # FastAPI filtra automáticamente según UserResponseSchema
    return user_dict


# =============================================================================
# Ejemplo 10: Config Settings con pydantic-settings
# =============================================================================

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """
    Configuración de aplicación desde variables de entorno.
    
    Leer de .env automáticamente.
    """
    
    app_name: str = "FastAPI App"
    debug: bool = False
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "change-me-in-production"
    api_key: str = ""
    max_connections: int = 10
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


# Singleton de settings
settings = AppSettings()


@app.get("/config")
async def get_config():
    """Obtener configuración de la app."""
    return {
        "app_name": settings.app_name,
        "debug": settings.debug,
        "database_url": settings.database_url[:20] + "...",  # Truncar
        "max_connections": settings.max_connections
    }


# =============================================================================
# Ejemplo 11: Error Handling Personalizado
# =============================================================================

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handler personalizado para errores de validación."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation Error",
            "errors": errors
        }
    )


# =============================================================================
# Ejemplo 12: Serialization Modes
# =============================================================================

class Item(BaseModel):
    """Item con diferentes modos de serialización."""
    
    name: str
    price: Decimal
    internal_code: str
    
    model_config = ConfigDict(
        # Configurar serialización JSON
        json_encoders={
            Decimal: lambda v: float(v)  # Convertir Decimal a float
        }
    )


@app.post("/items", response_model=Item)
async def create_item(item: Item):
    """Crear item con serialización personalizada."""
    return item


@app.get("/items/json-dict")
async def get_item_serialization():
    """Diferentes modos de serialización."""
    item = Item(name="Test", price=Decimal("99.99"), internal_code="ABC123")
    
    return {
        "model_dump": item.model_dump(),  # Dict
        "model_dump_json": item.model_dump_json(),  # JSON string
        "model_dump_exclude": item.model_dump(exclude={"internal_code"})  # Excluir campo
    }


# =============================================================================
# Ejemplo 13: Computed Fields
# =============================================================================

from pydantic import computed_field


class Invoice(BaseModel):
    """Factura con campo computado."""
    
    subtotal: Decimal
    tax_rate: float = Field(0.16, ge=0, le=1)
    
    @computed_field
    @property
    def tax_amount(self) -> Decimal:
        """Calcular monto de impuesto."""
        return self.subtotal * Decimal(str(self.tax_rate))
    
    @computed_field
    @property
    def total(self) -> Decimal:
        """Calcular total."""
        return self.subtotal + self.tax_amount


@app.post("/invoices", response_model=Invoice)
async def create_invoice(invoice: Invoice):
    """
    Crear factura con campos computados.
    
    Request solo necesita subtotal y tax_rate.
    Response incluye tax_amount y total calculados.
    """
    return invoice


# =============================================================================
# Ejemplo 14: Model Inheritance
# =============================================================================

class BaseUser(BaseModel):
    """Clase base para usuarios."""
    email: EmailStr
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class AdminUser(BaseUser):
    """Usuario admin (hereda de BaseUser)."""
    is_superuser: bool = True
    permissions: List[str]


class RegularUser(BaseUser):
    """Usuario regular (hereda de BaseUser)."""
    subscription_tier: Literal["free", "basic", "premium"] = "free"


@app.post("/users/admin", response_model=AdminUser)
async def create_admin(user: AdminUser):
    """Crear usuario admin."""
    return user


@app.post("/users/regular", response_model=RegularUser)
async def create_regular_user(user: RegularUser):
    """Crear usuario regular."""
    return user


# =============================================================================
# Ejemplo 15: Partial Updates con PATCH
# =============================================================================

class ProductUpdate(BaseModel):
    """Schema para actualización parcial."""
    name: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None
    is_available: Optional[bool] = None


products_db = {
    1: Product(name="Laptop", price=Decimal("1299.99"), stock=10)
}


@app.patch("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, update: ProductUpdate):
    """
    Actualización parcial de producto.
    
    Solo los campos enviados se actualizan.
    """
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = products_db[product_id]
    
    # Actualizar solo campos no-None
    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    return product


# =============================================================================
# Instrucciones
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("PYDANTIC Y VALIDACIÓN - MÓDULO 9.3")
    print("=" * 70)
    print("\nPara ejecutar:")
    print("  uvicorn 03_pydantic_validacion:app --reload")
    print("\nDocumentación:")
    print("  http://localhost:8000/docs")
    print("\nEndpoints destacados:")
    print("  POST /products         - Validación con Field")
    print("  POST /orders           - Field validators")
    print("  POST /bookings         - Model validators")
    print("  POST /customers        - Modelos anidados")
    print("  POST /auth/register    - Exclude password en response")
    print("  POST /invoices         - Computed fields")
    print("  PATCH /products/{id}   - Actualización parcial")
    print("\n" + "=" * 70)
    print("💡 Prueba enviar datos inválidos para ver mensajes de error")
    print("=" * 70 + "\n")
