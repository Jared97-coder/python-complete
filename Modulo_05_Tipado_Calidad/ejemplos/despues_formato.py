"""
Ejemplo: Código CON Formateo Adecuado
======================================
El mismo código pero siguiendo PEP 8, formateado con Black e isort.
"""

import json
import os
import sys
from typing import Dict, List


# Bueno: espacios consistentes según PEP 8
def calcular(a: int, b: int, c: int) -> int:
    """Calcula a + b * c."""
    resultado = a + b * c
    return resultado


# Bueno: línea partida en múltiples líneas cuando es muy larga
def procesar_datos(
    nombre: str,
    apellido: str,
    email: str,
    telefono: str,
    direccion: str,
    ciudad: str,
    codigo_postal: str,
    pais: str,
) -> Dict[str, str]:
    """Procesa y retorna datos de usuario en un diccionario."""
    return {
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "telefono": telefono,
        "direccion": direccion,
        "ciudad": ciudad,
        "codigo_postal": codigo_postal,
        "pais": pais,
    }


# Bueno: espaciado correcto, comentarios en línea separada
class Usuario:
    """Representa un usuario del sistema."""

    def __init__(self, nombre: str, edad: int) -> None:
        """
        Inicializa un usuario.

        Args:
            nombre: Nombre del usuario.
            edad: Edad del usuario.
        """
        self.nombre = nombre
        self.edad = edad

    def saludar(self) -> None:
        """Imprime un saludo personalizado."""
        print(f"Hola, soy {self.nombre}")


# Bueno: strings consistentes (Black usa dobles por defecto)
def obtener_config() -> Dict[str, str | int | bool]:
    """Retorna configuración por defecto."""
    config = {
        "host": "localhost",
        "puerto": 8080,
        "debug": True,
        "timeout": "30",
    }
    return config


# Bueno: dict/list formateados consistentemente por Black
datos = {
    "usuarios": [
        {"id": 1, "nombre": "Ana", "activo": True},
        {"id": 2, "nombre": "Juan", "activo": True},
        {"id": 3, "nombre": "Pedro", "activo": False},
    ],
    "total": 3,
}


# Bueno: imports ordenados por isort (stdlib, third-party, local)
import datetime
import random
from os import environ, path
from pathlib import Path
from typing import Any, Optional


# Bueno: función en múltiples líneas, clara
def validar_edad(edad: int) -> bool:
    """
    Valida que la edad esté en rango válido.

    Args:
        edad: Edad a validar.

    Returns:
        True si la edad es válida (entre 18 y 120).
    """
    return 18 <= edad <= 120


# Bueno: comparación con None usando 'is'
def buscar(item: Optional[str]) -> Optional[str]:
    """
    Busca un item.

    Args:
        item: Item a buscar.

    Returns:
        El item si existe, None en caso contrario.
    """
    if item is None:
        return None
    return item


# Bueno: simplificar comparaciones con bool
def esta_activo(usuario: Dict[str, Any]) -> bool:
    """
    Verifica si un usuario está activo.

    Args:
        usuario: Diccionario con datos del usuario.

    Returns:
        True si el usuario está activo.
    """
    return bool(usuario.get("activo", False))


# Bueno: función clara en múltiples líneas
def procesar() -> int:
    """Procesa y retorna suma de x e y."""
    x = 1
    y = 2
    return x + y


class Producto:
    """Representa un producto con precio y descuentos."""

    def __init__(self, id: int, nombre: str, precio: float) -> None:
        """
        Inicializa un producto.

        Args:
            id: ID único del producto.
            nombre: Nombre del producto.
            precio: Precio base del producto.
        """
        self.id = id
        self.nombre = nombre
        self.precio = precio

    def aplicar_descuento(self, porcentaje: float) -> float:
        """
        Aplica un descuento al producto.

        Args:
            porcentaje: Porcentaje de descuento (0-100).

        Returns:
            Precio con descuento aplicado.

        Raises:
            ValueError: Si el porcentaje está fuera del rango válido.
        """
        if not 0 <= porcentaje <= 100:
            raise ValueError(
                f"Porcentaje inválido: {porcentaje}. Debe estar entre 0 y 100."
            )

        self.precio = self.precio * (1 - porcentaje / 100)
        return self.precio


# Bueno: nombres descriptivos
def calcular_promedio_ponderado(valor1: float, valor2: float) -> float:
    """
    Calcula un promedio ponderado.

    Args:
        valor1: Primer valor.
        valor2: Segundo valor.

    Returns:
        Promedio ponderado de los valores.
    """
    suma = valor1 + valor2
    doble_suma = suma * 2
    resultado = doble_suma / 3
    return resultado


# Bueno: reducir anidamiento con returns tempranos
def procesar_usuario(usuario: Optional[Dict[str, Any]]) -> bool:
    """
    Valida email de usuario.

    Args:
        usuario: Diccionario con datos del usuario.

    Returns:
        True si el email es válido.
    """
    if not usuario:
        return False

    email = usuario.get("email")
    if not email:
        return False

    if "@" not in email:
        return False

    if not email.endswith(".com"):
        return False

    return True


# Bueno: funciones normales en lugar de lambdas simples
def suma(x: int, y: int) -> int:
    """Suma dos números."""
    return x + y


def multiplica(x: int, y: int) -> int:
    """Multiplica dos números."""
    return x * y


# Bueno: list comprehension partida en múltiples líneas si es compleja
resultado = [
    x * 2
    for x in range(100)
    if x % 2 == 0
    if x % 3 == 0
    if x > 10
]

# O mejor aún, usar filter y map
numeros_validos = filter(
    lambda x: x % 2 == 0 and x % 3 == 0 and x > 10,
    range(100)
)
resultado_alternativo = [x * 2 for x in numeros_validos]


# Bueno: sin trailing whitespace, espaciado consistente
class Calculadora:
    """Calculadora básica."""

    def sumar(self, a: float, b: float) -> float:
        """Suma dos números."""
        return a + b

    def restar(self, a: float, b: float) -> float:
        """Resta dos números."""
        return a - b


# Bueno: dos líneas en blanco antes de definiciones de clase a nivel de módulo
class Animal:
    """Clase base para animales."""

    def __init__(self, nombre: str) -> None:
        """
        Inicializa un animal.

        Args:
            nombre: Nombre del animal.
        """
        self.nombre = nombre

    def hablar(self) -> str:
        """Retorna el sonido del animal."""
        return ""


class Perro(Animal):
    """Un perro es un animal que ladra."""

    def hablar(self) -> str:
        """Retorna el ladrido del perro."""
        return "Guau"


# Bueno: usar f-strings para concatenación
def construir_mensaje(usuario: Dict[str, Any]) -> str:
    """
    Construye mensaje de bienvenida.

    Args:
        usuario: Diccionario con datos del usuario.

    Returns:
        Mensaje personalizado.
    """
    mensaje = (
        f"Hola, {usuario['nombre']} {usuario['apellido']}. "
        f"Tu email es {usuario['email']} "
        f"y tu teléfono es {usuario['telefono']}."
    )
    return mensaje


# Bueno: usar dict.get() con valor por defecto
def obtener_valor(
    diccionario: Dict[str, Any],
    clave: str
) -> Optional[Any]:
    """
    Obtiene valor de diccionario.

    Args:
        diccionario: Diccionario donde buscar.
        clave: Clave a buscar.

    Returns:
        Valor asociado a la clave o None.
    """
    return diccionario.get(clave)


# Bueno: usar literales [] y {} en lugar de list() y dict()
lista_vacia: List[Any] = []
dict_vacio: Dict[str, Any] = {}


def main() -> None:
    """Función principal."""
    usuario = Usuario("Ana", 25)
    usuario.saludar()

    edad_valida = validar_edad(30)
    print(f"Edad válida: {edad_valida}")

    producto = Producto(1, "Laptop", 1200.0)
    precio_descuento = producto.aplicar_descuento(10)
    print(f"Precio con descuento: {precio_descuento:.2f}")


if __name__ == "__main__":
    main()
