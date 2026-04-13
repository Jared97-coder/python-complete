"""
Módulo 5.3: mypy y pyright - Verificadores de Tipos
===================================================

Este archivo contiene ejemplos específicos para demostrar cómo usar
mypy y pyright, errores comunes y cómo solucionarlos.

COMANDOS ÚTILES:
    mypy archivo.py              # Verificar un archivo
    mypy .                       # Verificar todo el proyecto
    mypy --strict archivo.py     # Modo estricto
    mypy --install-types         # Instalar stubs faltantes
    
    pyright archivo.py           # Usar pyright
    pyright --stats              # Con estadísticas
"""

from typing import Optional, List, Dict, Any, Union, cast
import json


# ============================================================================
# 1. ERRORES COMUNES Y CÓMO SOLUCIONARLOS
# ============================================================================

# ERROR: Missing return statement
def obtener_nombre_malo(user_id: int) -> str:
    """mypy error: Not all code paths return a value"""
    if user_id > 0:
        return "Usuario"
    # Falta return para el caso user_id <= 0


def obtener_nombre_bueno(user_id: int) -> str:
    """Corregido: todos los paths retornan"""
    if user_id > 0:
        return "Usuario"
    return "Desconocido"


# ERROR: Incompatible return type
def calcular_promedio_malo(numeros: List[int]) -> int:
    """mypy error: Incompatible return value type (got "float")"""
    return sum(numeros) / len(numeros)  # División retorna float


def calcular_promedio_bueno(numeros: List[int]) -> float:
    """Corregido: tipo de retorno correcto"""
    if not numeros:
        return 0.0
    return sum(numeros) / len(numeros)


# ERROR: Argument type mismatch
def procesar_numero(n: int) -> str:
    return f"Número: {n}"


def ejemplo_error_argumento() -> None:
    """mypy error: Argument 1 has incompatible type"""
    # procesar_numero("123")  # Error: espera int, recibe str
    procesar_numero(123)  # OK


# ERROR: None not allowed
def buscar_malo(id: int) -> str:
    """mypy error: Incompatible return value type (got "None")"""
    usuarios = {1: "Ana", 2: "Juan"}
    return usuarios.get(id)  # get() puede retornar None


def buscar_bueno(id: int) -> Optional[str]:
    """Corregido: Optional[str] permite None"""
    usuarios = {1: "Ana", 2: "Juan"}
    return usuarios.get(id)


# ============================================================================
# 2. TYPE NARROWING (REFINAMIENTO DE TIPOS)
# ============================================================================

def procesar_valor(valor: Optional[str]) -> int:
    """Type narrowing con isinstance/if."""
    # mypy sabe que después del check, valor no es None
    if valor is None:
        return 0
    # Aquí mypy sabe que valor es str (no None)
    return len(valor)


def procesar_union(dato: Union[int, str, List[int]]) -> int:
    """Type narrowing con isinstance."""
    if isinstance(dato, int):
        # Aquí mypy sabe que dato es int
        return dato * 2
    elif isinstance(dato, str):
        # Aquí mypy sabe que dato es str
        return len(dato)
    else:
        # Aquí mypy sabe que dato es List[int]
        return sum(dato)


# ============================================================================
# 3. TYPE: IGNORE - CUÁNDO Y CÓMO USAR
# ============================================================================

def ejemplo_type_ignore() -> None:
    """Usar type: ignore solo cuando sea necesario."""
    
    # Caso 1: Librería sin tipos
    import requests  # type: ignore  # Si requests no tiene stubs
    
    # Caso 2: Código legacy que no se puede cambiar
    valor: int = obtener_valor_dinamico()  # type: ignore
    
    # Caso 3: False positive de mypy (raro)
    resultado = operacion_compleja()  # type: ignore[misc]


def obtener_valor_dinamico() -> Any:
    """Simula código sin tipos."""
    return 42


def operacion_compleja() -> Any:
    """Simula operación compleja."""
    return {}


# ============================================================================
# 4. CAST - CONVERSIÓN DE TIPOS (SIN VERIFICACIÓN RUNTIME)
# ============================================================================

def procesar_json(data: str) -> Dict[str, Any]:
    """Cast cuando sabemos el tipo pero mypy no."""
    parsed = json.loads(data)  # parsed es Any
    # Sabemos que es Dict, pero mypy no
    return cast(Dict[str, Any], parsed)


def procesar_config(config: Any) -> int:
    """Cast para obtener un tipo específico."""
    # Asumimos que config["puerto"] es int
    puerto = cast(int, config.get("puerto", 8080))
    return puerto


# ============================================================================
# 5. STUB FILES (.pyi) - PARA LIBRERÍAS SIN TIPOS
# ============================================================================

# Si usas una librería sin tipos, puedes crear stub files
# Ejemplo: libreria_sin_tipos.pyi
#
# def funcion_sin_tipos(arg: str) -> int: ...
# class ClaseSinTipos:
#     def metodo(self) -> None: ...


# ============================================================================
# 6. CONFIGURACIÓN INCREMENTAL
# ============================================================================

# mypy.ini o pyproject.toml
"""
# mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = False  # False al inicio
check_untyped_defs = True

# Ignorar módulos específicos
[mypy-requests.*]
ignore_missing_imports = True

[mypy-pytest.*]
ignore_missing_imports = True
"""

# pyproject.toml
"""
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
check_untyped_defs = true

[[tool.mypy.overrides]]
module = ["requests.*", "pytest.*"]
ignore_missing_imports = true
"""


# ============================================================================
# 7. STRICT MODE - PARA NUEVOS PROYECTOS
# ============================================================================

# En modo estricto, mypy requiere tipos en todo
def funcion_estricta(nombre: str, edad: int) -> Dict[str, Union[str, int]]:
    """En strict mode, todos los parámetros necesitan tipo."""
    return {"nombre": nombre, "edad": edad}


# Sin strict mode, esto es válido:
# def funcion_sin_tipos(x, y):
#     return x + y

# Con --strict, mypy error: Function is missing a type annotation


# ============================================================================
# 8. GENERIC STUB PARA CÓDIGO EXTERNO
# ============================================================================

class ServicioExterno:
    """Simula clase de librería externa sin tipos."""
    
    def obtener_datos(self):  # Sin tipo de retorno
        """Método sin tipos."""
        return {"id": 1, "nombre": "Test"}
    
    def procesar(self, valor):  # Sin tipos en parámetro
        """Otro método sin tipos."""
        return valor * 2


# Para usar con mypy, crear wrapper tipado
class ServicioExternoTipado:
    """Wrapper con tipos para ServicioExterno."""
    
    def __init__(self) -> None:
        self._servicio = ServicioExterno()
    
    def obtener_datos(self) -> Dict[str, Any]:
        """Versión tipada."""
        return self._servicio.obtener_datos()
    
    def procesar(self, valor: int) -> int:
        """Versión tipada."""
        return self._servicio.procesar(valor)


# ============================================================================
# 9. PYRIGHT - CONFIGURACIÓN
# ============================================================================

# pyrightconfig.json o pyproject.toml
"""
// pyrightconfig.json
{
  "include": ["src"],
  "exclude": ["**/__pycache__", "build", "dist"],
  "pythonVersion": "3.11",
  "typeCheckingMode": "basic",  // basic, standard, strict
  "reportMissingImports": true,
  "reportMissingTypeStubs": false,
  "reportUnusedImport": true,
  "reportUnusedVariable": true
}
"""

# pyproject.toml para pyright
"""
[tool.pyright]
include = ["src"]
exclude = ["**/__pycache__", "build", "dist"]
pythonVersion = "3.11"
typeCheckingMode = "basic"
reportMissingImports = true
reportMissingTypeStubs = false
reportUnusedImport = true
reportUnusedVariable = true
"""


# ============================================================================
# 10. COMPARACIÓN mypy vs pyright
# ============================================================================

"""
MYPY:
  + Verificador oficial de tipos de Python
  + Más maduro y estable
  + Mejor documentación
  + Configuración más granular
  - Más lento en proyectos grandes
  - A veces verbose en errores

PYRIGHT:
  + Mucho más rápido
  + Mejor integración con VS Code (Pylance)
  + Errores más claros
  + Detecta algunos errores que mypy no
  - Menos configurable
  - Documentación menos completa

RECOMENDACIÓN:
  - Proyectos nuevos: Usar pyright (velocidad)
  - Proyectos existentes: Usar mypy (estabilidad)
  - Ideal: Usar ambos en CI
"""


# ============================================================================
# 11. EJEMPLO PRÁCTICO: CÓDIGO CON TIPOS COMPLETOS
# ============================================================================

class Usuario:
    """Clase completamente tipada."""
    
    def __init__(self, id: int, nombre: str, email: str) -> None:
        self.id = id
        self.nombre = nombre
        self.email = email
        self._activo = True
    
    @property
    def activo(self) -> bool:
        """Property con tipo."""
        return self._activo
    
    @activo.setter
    def activo(self, valor: bool) -> None:
        """Setter con tipo."""
        self._activo = valor
    
    def to_dict(self) -> Dict[str, Union[int, str, bool]]:
        """Convertir a diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "activo": self.activo
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Usuario":
        """Crear desde diccionario."""
        return cls(
            id=int(data["id"]),
            nombre=str(data["nombre"]),
            email=str(data["email"])
        )


class RepositorioUsuarios:
    """Repositorio completamente tipado."""
    
    def __init__(self) -> None:
        self._usuarios: Dict[int, Usuario] = {}
    
    def guardar(self, usuario: Usuario) -> None:
        """Guardar usuario."""
        self._usuarios[usuario.id] = usuario
    
    def obtener(self, id: int) -> Optional[Usuario]:
        """Obtener usuario por ID."""
        return self._usuarios.get(id)
    
    def listar(self) -> List[Usuario]:
        """Listar todos los usuarios."""
        return list(self._usuarios.values())
    
    def buscar_por_nombre(self, nombre: str) -> List[Usuario]:
        """Buscar usuarios por nombre."""
        return [
            u for u in self._usuarios.values()
            if nombre.lower() in u.nombre.lower()
        ]
    
    def contar(self) -> int:
        """Contar usuarios."""
        return len(self._usuarios)


# ============================================================================
# 12. EJERCICIO: EJECUTAR MYPY
# ============================================================================

"""
PASOS PARA VERIFICAR ESTE ARCHIVO:

1. Instalar mypy:
   pip install mypy

2. Ejecutar mypy en este archivo:
   mypy 03_mypy_pyright.py

3. Ejecutar en modo estricto:
   mypy --strict 03_mypy_pyright.py

4. Ver errores específicos:
   mypy --show-error-codes 03_mypy_pyright.py

5. Generar reporte HTML:
   mypy --html-report ./mypy-report 03_mypy_pyright.py

6. Instalar tipos faltantes automáticamente:
   mypy --install-types 03_mypy_pyright.py
"""


def main() -> None:
    """Función principal completamente tipada."""
    print("=" * 70)
    print("VERIFICACIÓN DE TIPOS CON MYPY/PYRIGHT")
    print("=" * 70)
    
    # Crear repositorio
    repo = RepositorioUsuarios()
    
    # Agregar usuarios
    usuario1 = Usuario(1, "Ana García", "ana@example.com")
    usuario2 = Usuario(2, "Juan Pérez", "juan@example.com")
    
    repo.guardar(usuario1)
    repo.guardar(usuario2)
    
    # Buscar usuario
    usuario = repo.obtener(1)
    if usuario:
        print(f"Usuario encontrado: {usuario.nombre}")
    
    # Listar todos
    print(f"\nTotal usuarios: {repo.contar()}")
    for u in repo.listar():
        print(f"  - {u.nombre} ({u.email})")
    
    print("\n" + "=" * 70)
    print("EJECUTA: mypy 03_mypy_pyright.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
