"""
Módulo 4.1: Clases Básicas, Herencia y Composición
==================================================

Conceptos:
- Definición de clases con __init__
- Métodos de instancia, clase y estáticos
- Properties
- Herencia simple y múltiple
- Composición como alternativa
- Clases abstractas
"""

from abc import ABC, abstractmethod
from typing import List, Optional


# ============================================================================
# 1. CLASES BÁSICAS
# ============================================================================

class Persona:
    """Clase básica que representa una persona."""
    
    # Atributo de clase (compartido por todas las instancias)
    especie = "Homo sapiens"
    contador_instancias = 0
    
    def __init__(self, nombre: str, edad: int):
        """Constructor de la clase."""
        # Atributos de instancia (únicos por objeto)
        self.nombre = nombre
        self.edad = edad
        Persona.contador_instancias += 1
    
    def saludar(self):
        """Método de instancia."""
        return f"Hola, soy {self.nombre} y tengo {self.edad} años"
    
    def es_mayor_edad(self):
        """Método de instancia con lógica."""
        return self.edad >= 18
    
    @classmethod
    def crear_anonimo(cls):
        """Método de clase - Constructor alternativo."""
        return cls("Anónimo", 0)
    
    @staticmethod
    def es_nombre_valido(nombre: str) -> bool:
        """Método estático - No accede a self ni cls."""
        return len(nombre) > 0 and nombre[0].isupper()


# ============================================================================
# 2. PROPERTIES - Encapsulamiento
# ============================================================================

class CuentaBancaria:
    """Ejemplo de properties para controlar acceso a atributos."""
    
    def __init__(self, titular: str, saldo_inicial: float = 0):
        self.titular = titular
        self._saldo = saldo_inicial  # Atributo "privado" por convención
        self._historial = []
    
    @property
    def saldo(self) -> float:
        """Getter - Acceso de solo lectura al saldo."""
        return self._saldo
    
    @property
    def ultima_transaccion(self) -> Optional[str]:
        """Property computada."""
        return self._historial[-1] if self._historial else None
    
    def depositar(self, cantidad: float):
        """Modifica saldo de forma controlada."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")
        self._saldo += cantidad
        self._historial.append(f"Depósito: +${cantidad:.2f}")
    
    def retirar(self, cantidad: float):
        """Retiro con validación."""
        if cantidad > self._saldo:
            raise ValueError("Saldo insuficiente")
        self._saldo -= cantidad
        self._historial.append(f"Retiro: -${cantidad:.2f}")


# ============================================================================
# 3. HERENCIA
# ============================================================================

class Empleado(Persona):
    """Herencia simple - Empleado ES UNA Persona."""
    
    def __init__(self, nombre: str, edad: int, cargo: str, salario: float):
        # Llamar al constructor de la clase padre
        super().__init__(nombre, edad)
        self.cargo = cargo
        self.salario = salario
    
    def saludar(self):
        """Sobrescritura de método (override)."""
        saludo_base = super().saludar()
        return f"{saludo_base} y trabajo como {self.cargo}"
    
    def calcular_salario_anual(self) -> float:
        """Método específico de Empleado."""
        return self.salario * 12


class Gerente(Empleado):
    """Herencia multinivel."""
    
    def __init__(self, nombre: str, edad: int, salario: float, departamento: str):
        super().__init__(nombre, edad, "Gerente", salario)
        self.departamento = departamento
        self.equipo: List[Empleado] = []
    
    def agregar_empleado(self, empleado: Empleado):
        """Gestión de equipo."""
        self.equipo.append(empleado)
    
    def calcular_salario_anual(self) -> float:
        """Override con bono adicional."""
        base = super().calcular_salario_anual()
        bono = len(self.equipo) * 1000  # Bono por empleado
        return base + bono


# ============================================================================
# 4. HERENCIA MÚLTIPLE y MRO
# ============================================================================

class Trabajador:
    """Mixin para funcionalidad de trabajo."""
    
    def trabajar(self):
        return "Trabajando..."


class Estudiante:
    """Mixin para funcionalidad de estudio."""
    
    def estudiar(self):
        return "Estudiando..."


class Becario(Trabajador, Estudiante, Persona):
    """Herencia múltiple - combina comportamientos."""
    
    def __init__(self, nombre: str, edad: int, beca: float):
        Persona.__init__(self, nombre, edad)
        self.beca = beca
    
    def saludar(self):
        base = super().saludar()
        return f"{base} y soy becario con ${self.beca:.2f} de beca"


# ============================================================================
# 5. COMPOSICIÓN (preferida sobre herencia)
# ============================================================================

class Motor:
    """Componente independiente."""
    
    def __init__(self, potencia: int, tipo: str):
        self.potencia = potencia
        self.tipo = tipo
        self.encendido = False
    
    def encender(self):
        self.encendido = True
        return f"Motor {self.tipo} de {self.potencia}HP encendido"
    
    def apagar(self):
        self.encendido = False
        return "Motor apagado"


class Vehiculo:
    """Composición - Vehiculo TIENE UN Motor."""
    
    def __init__(self, marca: str, modelo: str, motor: Motor):
        self.marca = marca
        self.modelo = modelo
        self.motor = motor  # Composición: inyección de dependencia
    
    def arrancar(self):
        """Delega funcionalidad al componente."""
        if not self.motor.encendido:
            return self.motor.encender()
        return f"{self.marca} {self.modelo} ya está encendido"
    
    def detener(self):
        return self.motor.apagar()


# ============================================================================
# 6. CLASES ABSTRACTAS (ABC)
# ============================================================================

class FormaGeometrica(ABC):
    """Clase base abstracta - No se puede instanciar."""
    
    @abstractmethod
    def calcular_area(self) -> float:
        """Método abstracto - debe ser implementado por subclases."""
        pass
    
    @abstractmethod
    def calcular_perimetro(self) -> float:
        """Otro método abstracto."""
        pass
    
    def describir(self):
        """Método concreto disponible para todas las subclases."""
        return f"Área: {self.calcular_area():.2f}, Perímetro: {self.calcular_perimetro():.2f}"


class Rectangulo(FormaGeometrica):
    """Implementación concreta de forma abstracta."""
    
    def __init__(self, base: float, altura: float):
        self.base = base
        self.altura = altura
    
    def calcular_area(self) -> float:
        return self.base * self.altura
    
    def calcular_perimetro(self) -> float:
        return 2 * (self.base + self.altura)


class Circulo(FormaGeometrica):
    """Otra implementación."""
    
    PI = 3.14159
    
    def __init__(self, radio: float):
        self.radio = radio
    
    def calcular_area(self) -> float:
        return self.PI * self.radio ** 2
    
    def calcular_perimetro(self) -> float:
        return 2 * self.PI * self.radio


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

def main():
    print("=" * 70)
    print("1. CLASES BÁSICAS")
    print("=" * 70)
    
    persona1 = Persona("Ana", 25)
    print(persona1.saludar())
    print(f"¿Es mayor de edad? {persona1.es_mayor_edad()}")
    print(f"Instancias creadas: {Persona.contador_instancias}")
    
    anonimo = Persona.crear_anonimo()
    print(f"\nPersona anónima: {anonimo.nombre}")
    
    print(f"\n¿'Juan' es válido? {Persona.es_nombre_valido('Juan')}")
    print(f"¿'pedro' es válido? {Persona.es_nombre_valido('pedro')}")
    
    print("\n" + "=" * 70)
    print("2. PROPERTIES")
    print("=" * 70)
    
    cuenta = CuentaBancaria("Carlos Gómez", 1000)
    print(f"Saldo inicial: ${cuenta.saldo:.2f}")
    
    cuenta.depositar(500)
    cuenta.retirar(200)
    print(f"Saldo actual: ${cuenta.saldo:.2f}")
    print(f"Última transacción: {cuenta.ultima_transaccion}")
    
    print("\n" + "=" * 70)
    print("3. HERENCIA")
    print("=" * 70)
    
    empleado = Empleado("Luis Pérez", 30, "Desarrollador", 5000)
    print(empleado.saludar())
    print(f"Salario anual: ${empleado.calcular_salario_anual():.2f}")
    
    gerente = Gerente("María López", 40, 8000, "IT")
    gerente.agregar_empleado(empleado)
    print(f"\n{gerente.saludar()}")
    print(f"Salario anual (con bono): ${gerente.calcular_salario_anual():.2f}")
    
    print("\n" + "=" * 70)
    print("4. HERENCIA MÚLTIPLE")
    print("=" * 70)
    
    becario = Becario("Pedro Sánchez", 22, 2000)
    print(becario.saludar())
    print(becario.trabajar())
    print(becario.estudiar())
    
    # Ver el MRO (Method Resolution Order)
    print(f"\nMRO de Becario: {[c.__name__ for c in Becario.__mro__]}")
    
    print("\n" + "=" * 70)
    print("5. COMPOSICIÓN")
    print("=" * 70)
    
    motor_v8 = Motor(450, "V8")
    coche = Vehiculo("Ford", "Mustang", motor_v8)
    
    print(coche.arrancar())
    print(f"Motor del coche: {coche.motor.tipo}, {coche.motor.potencia}HP")
    print(coche.detener())
    
    print("\n" + "=" * 70)
    print("6. CLASES ABSTRACTAS")
    print("=" * 70)
    
    # forma = FormaGeometrica()  # ERROR: No se puede instanciar
    
    rectangulo = Rectangulo(5, 3)
    print(f"Rectángulo (5x3): {rectangulo.describir()}")
    
    circulo = Circulo(4)
    print(f"Círculo (r=4): {circulo.describir()}")
    
    # Polimorfismo
    formas: List[FormaGeometrica] = [rectangulo, circulo]
    print("\nÁreas de todas las formas:")
    for forma in formas:
        print(f"  - {forma.__class__.__name__}: {forma.calcular_area():.2f}")


if __name__ == "__main__":
    main()
