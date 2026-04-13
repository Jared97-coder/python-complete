# Módulo 4: Objetos y Modelos de Datos

## Objetivos de aprendizaje
- Modelar entidades con comportamientos y validaciones
- Serializar y validar entradas/salidas
- Aplicar principios de POO en Python
- Utilizar herramientas modernas para definición de modelos

## Contenidos

### 1. Clases y POO en Python
**Archivo:** `01_clases_basicas.py`

Conceptos fundamentales:
- Definición de clases y métodos
- Constructor `__init__` y atributos de instancia
- Métodos de instancia vs métodos de clase vs métodos estáticos
- Atributos privados y públicos (convenciones)
- Properties y decorador @property

**Herencia:**
- Herencia simple y múltiple
- super() y MRO (Method Resolution Order)
- Polimorfismo
- Clases abstractas (ABC)

**Composición:**
- Composición vs herencia
- Ejemplo de "has-a" relationship
- Inyección de dependencias

### 2. Métodos Especiales (Dunder Methods)
**Archivo:** `02_dunder_methods.py`

Métodos mágicos para personalizar comportamiento:
- `__str__` y `__repr__` - Representación de objetos
- `__eq__`, `__lt__`, `__le__`, etc. - Comparaciones
- `__add__`, `__sub__`, etc. - Operadores aritméticos
- `__len__`, `__getitem__`, `__setitem__` - Comportamiento de colecciones
- `__call__` - Hacer objetos llamables
- `__enter__` y `__exit__` - Context managers

### 3. Dataclasses y Attrs
**Archivo:** `03_dataclasses.py`

**Dataclasses (Python 3.7+):**
- Decorador @dataclass
- Generación automática de `__init__`, `__repr__`, `__eq__`
- Campos con valores por defecto
- field() y metadata
- post_init processing
- frozen dataclasses (inmutabilidad)
- Ordenamiento con order=True

**Attrs:**
- Alternativa más poderosa a dataclasses
- Validadores y convertidores
- Slots para optimización de memoria

### 4. Pydantic para Validación
**Archivo:** `04_pydantic_validacion.py`

**Pydantic:**
- BaseModel y definición de esquemas
- Validación automática de tipos
- Validadores personalizados (@validator)
- Serialización/deserialización (dict, JSON)
- Campo obligatorio vs opcional
- Config y configuraciones
- Modelos anidados
- Casos de uso: APIs, configuraciones, data pipelines

## Estructura de archivos
```
Modulo_04_Objetos_Modelos/
├── 01_clases_basicas.py          # Clases, herencia, composición
├── 02_dunder_methods.py          # Métodos especiales de Python
├── 03_dataclasses.py             # dataclasses y attrs
├── 04_pydantic_validacion.py     # Pydantic para validación/serialización
├── LABORATORIO.md                # Ejercicios prácticos
├── README.md                     # Este archivo
└── requirements.txt              # Dependencias del módulo
```

## Instalación de dependencias
```bash
pip install -r requirements.txt
```

## Progresión sugerida
1. **01_clases_basicas.py** - Fundamentos de POO
2. **02_dunder_methods.py** - Personalización de comportamiento
3. **03_dataclasses.py** - Simplificación con dataclasses
4. **04_pydantic_validacion.py** - Validación robusta
5. **LABORATORIO.md** - Aplicación práctica

## Recursos adicionales
- [Python Data Classes](https://docs.python.org/3/library/dataclasses.html)
- [Attrs Documentation](https://www.attrs.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Abstract Base Classes](https://docs.python.org/3/library/abc.html)
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)

## Notas importantes
- **Dataclasses**: Ideal para datos simples sin validación compleja
- **Attrs**: Más flexible que dataclasses, con validadores
- **Pydantic**: Mejor opción para APIs y validación estricta
- **Herencia vs Composición**: Preferir composición salvo que haya clara relación "is-a"
