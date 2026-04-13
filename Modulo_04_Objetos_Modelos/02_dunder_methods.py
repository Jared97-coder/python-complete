"""
Módulo 4.2: Métodos Especiales (Dunder Methods)
===============================================

Conceptos:
- Métodos mágicos para personalizar comportamiento de objetos
- Representación: __str__, __repr__
- Comparación: __eq__, __lt__, etc.
- Operadores aritméticos: __add__, __sub__, etc.
- Comportamiento de colecciones: __len__, __getitem__, __setitem__
- Context managers: __enter__, __exit__
- Callable objects: __call__
"""

from typing import Any, List


# ============================================================================
# 1. REPRESENTACIÓN DE OBJETOS
# ============================================================================

class Libro:
    """Ejemplo de __str__ y __repr__."""
    
    def __init__(self, titulo: str, autor: str, paginas: int):
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas
    
    def __str__(self) -> str:
        """Representación amigable para el usuario (print)."""
        return f'"{self.titulo}" por {self.autor}'
    
    def __repr__(self) -> str:
        """Representación técnica para desarrolladores (debugger)."""
        return f"Libro(titulo='{self.titulo}', autor='{self.autor}', paginas={self.paginas})"


# ============================================================================
# 2. OPERADORES DE COMPARACIÓN
# ============================================================================

class Producto:
    """Ejemplo de comparaciones personalizadas."""
    
    def __init__(self, nombre: str, precio: float):
        self.nombre = nombre
        self.precio = precio
    
    def __eq__(self, other) -> bool:
        """Igualdad (==)."""
        if not isinstance(other, Producto):
            return NotImplemented
        return self.nombre == other.nombre and self.precio == other.precio
    
    def __lt__(self, other) -> bool:
        """Menor que (<) - permite ordenamiento."""
        if not isinstance(other, Producto):
            return NotImplemented
        return self.precio < other.precio
    
    def __le__(self, other) -> bool:
        """Menor o igual (<=)."""
        return self == other or self < other
    
    def __gt__(self, other) -> bool:
        """Mayor que (>)."""
        if not isinstance(other, Producto):
            return NotImplemented
        return self.precio > other.precio
    
    def __ge__(self, other) -> bool:
        """Mayor o igual (>=)."""
        return self == other or self > other
    
    def __str__(self):
        return f"{self.nombre}: ${self.precio:.2f}"


# ============================================================================
# 3. OPERADORES ARITMÉTICOS
# ============================================================================

class Vector2D:
    """Vector matemático con operaciones."""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        """Suma (+)."""
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        """Resta (-)."""
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float):
        """Multiplicación por escalar (*)."""
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar: float):
        """División (/)."""
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        if scalar == 0:
            raise ValueError("División por cero")
        return Vector2D(self.x / scalar, self.y / scalar)
    
    def __neg__(self):
        """Negación unaria (-)."""
        return Vector2D(-self.x, -self.y)
    
    def __abs__(self):
        """Valor absoluto (magnitud del vector)."""
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def __str__(self):
        return f"Vector2D({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector2D(x={self.x}, y={self.y})"


# ============================================================================
# 4. COMPORTAMIENTO DE COLECCIONES
# ============================================================================

class Playlist:
    """Lista de reproducción con acceso tipo lista."""
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._canciones: List[str] = []
    
    def agregar(self, cancion: str):
        """Agregar canción."""
        self._canciones.append(cancion)
    
    def __len__(self) -> int:
        """len(playlist)."""
        return len(self._canciones)
    
    def __getitem__(self, index: int) -> str:
        """playlist[index]."""
        return self._canciones[index]
    
    def __setitem__(self, index: int, cancion: str):
        """playlist[index] = cancion."""
        self._canciones[index] = cancion
    
    def __delitem__(self, index: int):
        """del playlist[index]."""
        del self._canciones[index]
    
    def __contains__(self, cancion: str) -> bool:
        """cancion in playlist."""
        return cancion in self._canciones
    
    def __iter__(self):
        """for cancion in playlist."""
        return iter(self._canciones)
    
    def __reversed__(self):
        """reversed(playlist)."""
        return reversed(self._canciones)
    
    def __str__(self):
        return f"Playlist '{self.nombre}' con {len(self)} canciones"


# ============================================================================
# 5. CONTEXT MANAGERS
# ============================================================================

class ArchivoLog:
    """Context manager personalizado para logging."""
    
    def __init__(self, nombre_archivo: str):
        self.nombre_archivo = nombre_archivo
        self.archivo = None
    
    def __enter__(self):
        """Se ejecuta al inicio del bloque 'with'."""
        print(f"Abriendo archivo: {self.nombre_archivo}")
        self.archivo = open(self.nombre_archivo, 'a', encoding='utf-8')
        return self  # Retorna el objeto para usar en 'as'
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Se ejecuta al salir del bloque 'with' (incluso si hay error)."""
        if self.archivo:
            print(f"Cerrando archivo: {self.nombre_archivo}")
            self.archivo.close()
        
        # Si retorna True, suprime la excepción
        # Si retorna None/False, propaga la excepción
        if exc_type is not None:
            print(f"Ocurrió un error: {exc_type.__name__}: {exc_value}")
        return False  # Propagar excepciones
    
    def escribir(self, mensaje: str):
        """Método de ayuda para escribir."""
        if self.archivo:
            self.archivo.write(f"{mensaje}\n")


class Temporizador:
    """Context manager para medir tiempo de ejecución."""
    
    def __init__(self, nombre: str = "Bloque"):
        self.nombre = nombre
        self.inicio = None
    
    def __enter__(self):
        import time
        self.inicio = time.time()
        print(f"Iniciando: {self.nombre}")
        return self
    
    def __exit__(self, *args):
        import time
        duracion = time.time() - self.inicio
        print(f"Finalizó: {self.nombre} en {duracion:.4f} segundos")
        return False


# ============================================================================
# 6. OBJETOS LLAMABLES (__call__)
# ============================================================================

class Multiplicador:
    """Objeto que se comporta como función."""
    
    def __init__(self, factor: float):
        self.factor = factor
    
    def __call__(self, valor: float) -> float:
        """Permite usar el objeto como función."""
        return valor * self.factor
    
    def __repr__(self):
        return f"Multiplicador(factor={self.factor})"


class Contador:
    """Contador que incrementa en cada llamada."""
    
    def __init__(self):
        self.cuenta = 0
    
    def __call__(self) -> int:
        """Incrementa y retorna el contador."""
        self.cuenta += 1
        return self.cuenta
    
    def reset(self):
        """Reiniciar contador."""
        self.cuenta = 0


# ============================================================================
# 7. OTROS DUNDER METHODS ÚTILES
# ============================================================================

class Rango:
    """Ejemplo de __bool__, __hash__, __format__."""
    
    def __init__(self, inicio: int, fin: int):
        self.inicio = inicio
        self.fin = fin
    
    def __bool__(self) -> bool:
        """bool(rango) - True si el rango no está vacío."""
        return self.fin > self.inicio
    
    def __hash__(self) -> int:
        """Permite usar el objeto en sets y como clave de dict."""
        return hash((self.inicio, self.fin))
    
    def __format__(self, format_spec: str) -> str:
        """Formato personalizado con f-strings."""
        if format_spec == 'short':
            return f"[{self.inicio}..{self.fin}]"
        elif format_spec == 'long':
            return f"Rango desde {self.inicio} hasta {self.fin}"
        return str(self)
    
    def __str__(self):
        return f"Rango({self.inicio}, {self.fin})"


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

def main():
    print("=" * 70)
    print("1. REPRESENTACIÓN DE OBJETOS")
    print("=" * 70)
    
    libro = Libro("1984", "George Orwell", 328)
    print(f"str(): {str(libro)}")      # Llama a __str__
    print(f"repr(): {repr(libro)}")    # Llama a __repr__
    print(f"print: {libro}")           # Usa __str__
    
    print("\n" + "=" * 70)
    print("2. COMPARACIONES")
    print("=" * 70)
    
    p1 = Producto("Laptop", 1200)
    p2 = Producto("Mouse", 25)
    p3 = Producto("Laptop", 1200)
    
    print(f"{p1} == {p3}: {p1 == p3}")
    print(f"{p1} < {p2}: {p1 < p2}")
    print(f"{p2} < {p1}: {p2 < p1}")
    
    productos = [p1, p2, Producto("Teclado", 80)]
    print("\nProductos ordenados por precio:")
    for p in sorted(productos):
        print(f"  {p}")
    
    print("\n" + "=" * 70)
    print("3. OPERADORES ARITMÉTICOS")
    print("=" * 70)
    
    v1 = Vector2D(3, 4)
    v2 = Vector2D(1, 2)
    
    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 2 = {v1 * 2}")
    print(f"v1 / 2 = {v1 / 2}")
    print(f"-v1 = {-v1}")
    print(f"|v1| = {abs(v1):.2f}")
    
    print("\n" + "=" * 70)
    print("4. COMPORTAMIENTO DE COLECCIONES")
    print("=" * 70)
    
    playlist = Playlist("Rock Clásico")
    playlist.agregar("Bohemian Rhapsody")
    playlist.agregar("Stairway to Heaven")
    playlist.agregar("Hotel California")
    
    print(playlist)
    print(f"Longitud: {len(playlist)}")
    print(f"Primera canción: {playlist[0]}")
    print(f"¿Contiene 'Hotel California'? {'Hotel California' in playlist}")
    
    print("\nIteración:")
    for i, cancion in enumerate(playlist, 1):
        print(f"  {i}. {cancion}")
    
    print("\n" + "=" * 70)
    print("5. CONTEXT MANAGERS")
    print("=" * 70)
    
    # Context manager para archivo
    with ArchivoLog("ejemplo.log") as log:
        log.escribir("Primera entrada")
        log.escribir("Segunda entrada")
    
    # Context manager para timing
    with Temporizador("Operación lenta"):
        import time
        time.sleep(0.1)  # Simular operación
    
    print("\n" + "=" * 70)
    print("6. OBJETOS LLAMABLES")
    print("=" * 70)
    
    duplicar = Multiplicador(2)
    triplicar = Multiplicador(3)
    
    print(f"duplicar(5) = {duplicar(5)}")
    print(f"triplicar(5) = {triplicar(5)}")
    
    contador = Contador()
    print(f"Llamada 1: {contador()}")
    print(f"Llamada 2: {contador()}")
    print(f"Llamada 3: {contador()}")
    contador.reset()
    print(f"Después de reset: {contador()}")
    
    print("\n" + "=" * 70)
    print("7. OTROS MÉTODOS")
    print("=" * 70)
    
    rango1 = Rango(1, 10)
    rango2 = Rango(5, 5)
    
    print(f"bool(rango1): {bool(rango1)}")
    print(f"bool(rango2): {bool(rango2)}")
    
    print(f"Format short: {rango1:short}")
    print(f"Format long: {rango1:long}")
    
    # Usar en set (requiere __hash__)
    rangos = {rango1, Rango(1, 10), rango2}
    print(f"Set de rangos (sin duplicados): {len(rangos)} elementos")


if __name__ == "__main__":
    main()
