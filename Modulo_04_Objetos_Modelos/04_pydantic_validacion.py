"""
Módulo 4.4: Pydantic para Validación y Serialización
====================================================

Conceptos:
- BaseModel para definir esquemas
- Validación automática de tipos
- Validadores personalizados
- Serialización/deserialización (JSON, dict)
- model_validate y model_dump
- Campos opcionales y obligatorios
- Modelos anidados
- Config y configuración
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from enum import Enum

try:
    from pydantic import (
        BaseModel,
        Field,
        EmailStr,
        field_validator,
        model_validator,
        ConfigDict
    )
    PYDANTIC_AVAILABLE = True
except ImportError:
    print("⚠️  Pydantic no está instalado. Ejecuta: pip install pydantic pydantic[email]")
    PYDANTIC_AVAILABLE = False
    # Definir clases dummy para que el código no falle
    class BaseModel: pass
    class Field: pass
    class EmailStr: pass
    def field_validator(*args, **kwargs): 
        def decorator(func): return func
        return decorator
    def model_validator(*args, **kwargs):
        def decorator(func): return func
        return decorator
    class ConfigDict(dict): pass


if PYDANTIC_AVAILABLE:
    # ============================================================================
    # 1. MODELO BÁSICO
    # ============================================================================
    
    class Usuario(BaseModel):
        """Modelo básico con validación automática."""
        username: str
        email: EmailStr  # Validación de email (requiere: pip install pydantic[email])
        edad: int
        activo: bool = True  # Valor por defecto
        
        # Pydantic valida tipos automáticamente y convierte cuando es posible
    
    
    # ============================================================================
    # 2. FIELD() PARA CONFIGURACIÓN AVANZADA
    # ============================================================================
    
    class Producto(BaseModel):
        """Field() permite constrains y metadata."""
        nombre: str = Field(..., min_length=1, max_length=100)
        descripcion: Optional[str] = Field(None, max_length=500)
        precio: float = Field(..., gt=0, description="Precio debe ser mayor a 0")
        stock: int = Field(default=0, ge=0, description="Stock no puede ser negativo")
        categorias: List[str] = Field(default_factory=list)
        
        # ... significa campo obligatorio
        # gt = greater than, ge = greater or equal
        # lt = less than, le = less or equal
    
    
    # ============================================================================
    # 3. VALIDADORES PERSONALIZADOS
    # ============================================================================
    
    class Empleado(BaseModel):
        """Validadores personalizados con @field_validator."""
        nombre: str
        apellido: str
        email: EmailStr
        salario: float
        fecha_ingreso: date
        
        @field_validator('nombre', 'apellido')
        @classmethod
        def validar_nombre(cls, v: str) -> str:
            """Validar que nombres empiecen con mayúscula."""
            if not v[0].isupper():
                raise ValueError('Debe empezar con mayúscula')
            return v.strip().title()
        
        @field_validator('salario')
        @classmethod
        def validar_salario(cls, v: float) -> float:
            """Validar rango de salario."""
            if v < 0:
                raise ValueError('Salario no puede ser negativo')
            if v > 1000000:
                raise ValueError('Salario excede el máximo permitido')
            return v
        
        @field_validator('fecha_ingreso')
        @classmethod
        def validar_fecha(cls, v: date) -> date:
            """Validar que fecha no sea futura."""
            if v > date.today():
                raise ValueError('Fecha de ingreso no puede ser futura')
            return v
    
    
    # ============================================================================
    # 4. MODEL VALIDATOR - VALIDACIÓN ENTRE CAMPOS
    # ============================================================================
    
    class RangoFechas(BaseModel):
        """Validar relación entre múltiples campos."""
        fecha_inicio: date
        fecha_fin: date
        
        @model_validator(mode='after')
        def validar_rango(self):
            """Validar que fecha_fin > fecha_inicio."""
            if self.fecha_fin <= self.fecha_inicio:
                raise ValueError('fecha_fin debe ser posterior a fecha_inicio')
            return self
    
    
    class Usuario(BaseModel):
        """Validación con modo 'before' (antes de parsing)."""
        username: str
        password: str
        password_confirmacion: str
        
        @model_validator(mode='after')
        def validar_passwords_coincidan(self):
            """Validar que passwords coincidan."""
            if self.password != self.password_confirmacion:
                raise ValueError('Las contraseñas no coinciden')
            return self
    
    
    # ============================================================================
    # 5. ENUMS Y LITERALES
    # ============================================================================
    
    class EstadoOrden(str, Enum):
        """Enum para estados válidos."""
        PENDIENTE = "pendiente"
        PROCESANDO = "procesando"
        ENVIADO = "enviado"
        ENTREGADO = "entregado"
        CANCELADO = "cancelado"
    
    
    class Orden(BaseModel):
        """Modelo con Enum."""
        id_orden: str
        estado: EstadoOrden = EstadoOrden.PENDIENTE
        monto: float = Field(gt=0)
        
        # estado solo puede ser uno de los valores del Enum
    
    
    # ============================================================================
    # 6. MODELOS ANIDADOS
    # ============================================================================
    
    class Direccion(BaseModel):
        """Modelo anidado."""
        calle: str
        numero: int
        ciudad: str
        codigo_postal: str = Field(pattern=r'^\d{5}$')  # Regex para validar
    
    
    class Cliente(BaseModel):
        """Modelo que contiene otro modelo."""
        nombre: str
        email: EmailStr
        direccion: Direccion  # Modelo anidado
        direcciones_alternativas: List[Direccion] = Field(default_factory=list)
        metadata: Dict[str, Any] = Field(default_factory=dict)
    
    
    # ============================================================================
    # 7. CONFIG Y CONFIGURACIÓN
    # ============================================================================
    
    class PersonaConfig(BaseModel):
        """Configuración del modelo con ConfigDict."""
        model_config = ConfigDict(
            str_strip_whitespace=True,  # Quitar espacios de strings
            str_to_lower=False,         # No convertir a minúsculas
            validate_assignment=True,   # Validar también en asignaciones posteriores
            frozen=False,               # False = mutable, True = inmutable
            populate_by_name=True,      # Permitir alias
        )
        
        nombre: str
        edad: int = Field(ge=0, le=150)
    
    
    # ============================================================================
    # 8. SERIALIZACIÓN Y DESERIALIZACIÓN
    # ============================================================================
    
    class ArticuloBlog(BaseModel):
        """Modelo para demostrar serialización."""
        titulo: str
        contenido: str
        autor: str
        fecha_publicacion: datetime
        etiquetas: List[str] = Field(default_factory=list)
        publicado: bool = False
        vistas: int = 0
    
    
    # ============================================================================
    # 9. EJEMPLO COMPLETO: API DE ÓRDENES
    # ============================================================================
    
    class ItemOrden(BaseModel):
        """Item individual en una orden."""
        producto_id: str
        nombre_producto: str
        cantidad: int = Field(gt=0)
        precio_unitario: float = Field(gt=0)
        
        def subtotal(self) -> float:
            """Calcular subtotal."""
            return self.cantidad * self.precio_unitario
    
    
    class OrdenIn(BaseModel):
        """Esquema de entrada para crear orden (datos del cliente)."""
        cliente_id: str
        items: List[ItemOrden] = Field(min_length=1)
        direccion_envio: Direccion
        notas: Optional[str] = None
        
        @field_validator('items')
        @classmethod
        def validar_items_no_vacio(cls, v: List[ItemOrden]) -> List[ItemOrden]:
            """Validar que haya al menos un item.""" 
            if not v:
                raise ValueError('La orden debe tener al menos un item')
            return v
    
    
    class OrdenOut(BaseModel):
        """Esquema de salida (respuesta de API) - incluye campos calculados."""
        id_orden: str
        cliente_id: str
        items: List[ItemOrden]
        direccion_envio: Direccion
        estado: EstadoOrden
        subtotal: float
        impuestos: float
        total: float
        fecha_creacion: datetime
        notas: Optional[str] = None
        
        model_config = ConfigDict(from_attributes=True)  # Permitir crear desde objeto
    
    
    # Entidad de dominio (no es Pydantic)
    class OrdenEntity:
        """Entidad de negocio (sin Pydantic) - lógica de dominio."""
        
        IVA_PORCENTAJE = 0.16
        
        def __init__(self, id_orden: str, cliente_id: str, items: List[ItemOrden], 
                     direccion_envio: Direccion, notas: Optional[str] = None):
            self.id_orden = id_orden
            self.cliente_id = cliente_id
            self.items = items
            self.direccion_envio = direccion_envio
            self.estado = EstadoOrden.PENDIENTE
            self.fecha_creacion = datetime.now()
            self.notas = notas
        
        @property
        def subtotal(self) -> float:
            """Suma de todos los items."""
            return sum(item.subtotal() for item in self.items)
        
        @property
        def impuestos(self) -> float:
            """Calcular impuestos."""
            return self.subtotal * self.IVA_PORCENTAJE
        
        @property
        def total(self) -> float:
            """Total con impuestos."""
            return self.subtotal + self.impuestos
        
        def procesar(self):
            """Cambiar estado a procesando."""
            if self.estado != EstadoOrden.PENDIENTE:
                raise ValueError(f"No se puede procesar orden en estado {self.estado}")
            self.estado = EstadoOrden.PROCESANDO
        
        def cancelar(self):
            """Cancelar orden."""
            if self.estado in [EstadoOrden.ENVIADO, EstadoOrden.ENTREGADO]:
                raise ValueError(f"No se puede cancelar orden en estado {self.estado}")
            self.estado = EstadoOrden.CANCELADO
    
    
    # ============================================================================
    # FUNCIONES DE CONVERSIÓN
    # ============================================================================
    
    def crear_orden_desde_input(orden_in: OrdenIn, id_orden: str) -> OrdenEntity:
        """Convertir OrdenIn (Pydantic) a OrdenEntity (dominio)."""
        return OrdenEntity(
            id_orden=id_orden,
            cliente_id=orden_in.cliente_id,
            items=orden_in.items,
            direccion_envio=orden_in.direccion_envio,
            notas=orden_in.notas
        )
    
    
    def orden_entity_a_output(orden: OrdenEntity) -> OrdenOut:
        """Convertir OrdenEntity a OrdenOut (Pydantic para respuesta)."""
        return OrdenOut(
            id_orden=orden.id_orden,
            cliente_id=orden.cliente_id,
            items=orden.items,
            direccion_envio=orden.direccion_envio,
            estado=orden.estado,
            subtotal=orden.subtotal,
            impuestos=orden.impuestos,
            total=orden.total,
            fecha_creacion=orden.fecha_creacion,
            notas=orden.notas
        )


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

def main():
    if not PYDANTIC_AVAILABLE:
        print("❌ Pydantic no está disponible. Instálalo con:")
        print("   pip install pydantic pydantic[email]")
        return
    
    print("=" * 70)
    print("1. VALIDACIÓN BÁSICA")
    print("=" * 70)
    
    # Datos válidos
    usuario = Usuario(username="jperez", email="juan@example.com", edad=30)
    print(f"Usuario válido: {usuario}")
    
    # Conversión automática
    usuario2 = Usuario(username="amartinez", email="ana@example.com", edad="25")
    print(f"Edad convertida de string a int: {usuario2.edad} (tipo: {type(usuario2.edad).__name__})")
    
    # Error de validación
    try:
        usuario_invalido = Usuario(username="error", email="no-es-email", edad=30)
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("2. FIELD CONSTRAINTS")
    print("=" * 70)
    
    producto = Producto(nombre="Laptop", precio=1200.0, stock=10)
    print(f"Producto: {producto}")
    
    try:
        producto_invalido = Producto(nombre="", precio=-100, stock=-5)
    except Exception as e:
        print(f"❌ Validación falló: {str(e)[:100]}...")
    
    print("\n" + "=" * 70)
    print("3. VALIDADORES PERSONALIZADOS")
    print("=" * 70)
    
    empleado = Empleado(
        nombre="juan",  # Se convertirá a "Juan"
        apellido="pérez",  # Se convertirá a "Pérez"
        email="juan.perez@company.com",
        salario=50000.0,
        fecha_ingreso=date(2024, 1, 15)
    )
    print(f"Empleado: {empleado.nombre} {empleado.apellido}")
    
    print("\n" + "=" * 70)
    print("4. SERIALIZACIÓN JSON")
    print("=" * 70)
    
    articulo = ArticuloBlog(
        titulo="Introducción a Pydantic",
        contenido="Pydantic es una librería para validación...",
        autor="María López",
        fecha_publicacion=datetime.now(),
        etiquetas=["python", "pydantic", "validación"]
    )
    
    # Convertir a dict
    articulo_dict = articulo.model_dump()
    print(f"Como dict: {articulo_dict}")
    
    # Convertir a JSON
    articulo_json = articulo.model_dump_json(indent=2)
    print(f"\nComo JSON:\n{articulo_json}")
    
    # Desde JSON
    json_str = '{"titulo":"Nuevo Artículo","contenido":"Contenido...","autor":"Pedro","fecha_publicacion":"2024-01-15T10:30:00","etiquetas":["test"]}'
    articulo_desde_json = ArticuloBlog.model_validate_json(json_str)
    print(f"\nDesde JSON: {articulo_desde_json.titulo}")
    
    print("\n" + "=" * 70)
    print("5. MODELOS ANIDADOS")
    print("=" * 70)
    
    cliente = Cliente(
        nombre="Carlos Ramírez",
        email="carlos@example.com",
        direccion=Direccion(
            calle="Reforma",
            numero=123,
            ciudad="CDMX",
            codigo_postal="06600"
        )
    )
    print(f"Cliente: {cliente.nombre}")
    print(f"Ciudad: {cliente.direccion.ciudad}")
    
    # Serializar anidado
    cliente_dict = cliente.model_dump()
    print(f"Dirección anidada: {cliente_dict['direccion']}")
    
    print("\n" + "=" * 70)
    print("6. EJEMPLO COMPLETO: FLUJO DE ORDEN")
    print("=" * 70)
    
    # 1. Recibir datos de entrada (simulando request de API)
    orden_input_data = {
        "cliente_id": "CLI-001",
        "items": [
            {
                "producto_id": "PROD-001",
                "nombre_producto": "Laptop Dell",
                "cantidad": 1,
                "precio_unitario": 1200.00
            },
            {
                "producto_id": "PROD-002",
                "nombre_producto": "Mouse Logitech",
                "cantidad": 2,
                "precio_unitario": 25.00
            }
        ],
        "direccion_envio": {
            "calle": "Insurgentes Sur",
            "numero": 456,
            "ciudad": "CDMX",
            "codigo_postal": "03100"
        },
        "notas": "Entregar en horario de oficina"
    }
    
    # 2. Validar con Pydantic
    orden_in = OrdenIn.model_validate(orden_input_data)
    print("✅ Datos de entrada validados")
    
    # 3. Convertir a entidad de dominio
    orden_entity = crear_orden_desde_input(orden_in, "ORD-12345")
    print(f"📦 Orden creada: {orden_entity.id_orden}")
    print(f"   Subtotal: ${orden_entity.subtotal:.2f}")
    print(f"   Impuestos: ${orden_entity.impuestos:.2f}")
    print(f"   Total: ${orden_entity.total:.2f}")
    
    # 4. Procesar orden
    orden_entity.procesar()
    print(f"   Estado: {orden_entity.estado.value}")
    
    # 5. Convertir a modelo de salida para API
    orden_out = orden_entity_a_output(orden_entity)
    print(f"\n📤 Respuesta de API:")
    print(orden_out.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
