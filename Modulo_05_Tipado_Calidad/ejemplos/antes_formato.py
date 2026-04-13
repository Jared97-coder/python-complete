"""
Ejemplo: Código SIN Formateo Adecuado
======================================
Este código funciona pero viola PEP 8 y no está formateado consistentemente.
"""

import sys,os
from typing import Dict,List
import json


# Malo: espacios inconsistentes
def calcular(a,b,c):
    resultado=a+b*c
    return resultado

# Malo: línea muy larga que excede 88 caracteres (límite de Black)
def procesar_datos(nombre, apellido, email, telefono, direccion, ciudad, codigo_postal, pais):
    return {"nombre": nombre, "apellido": apellido, "email": email, "telefono": telefono, "direccion": direccion, "ciudad": ciudad, "codigo_postal": codigo_postal, "pais": pais}


class   Usuario:# Malo: espacios extras, comentario mal ubicado
    def __init__(self,nombre,edad):# Malo: sin espacios después de comas
        self.nombre=nombre
        self.edad=edad# Malo: sin espacios alrededor de =
    def saludar( self ):# Malo: espacios innecesarios
        print("Hola, soy "+self.nombre)


# Malo: strings inconsistentes (single/double quotes)
def obtener_config():
    config={'host':"localhost",'puerto':8080,"debug":True,'timeout':"30"}
    return config


# Malo: dict/list con formato inconsistente
datos = {
    'usuarios': [
        {'id': 1,'nombre': 'Ana','activo':True},
        {'id':2, 'nombre':'Juan' ,'activo': True },
        { 'id' : 3 , 'nombre' : 'Pedro' , 'activo' : False}
    ],
    'total':3
}


# Malo: imports no ordenados, wildcards
from os import *
import random
from typing import *
import datetime
from pathlib import Path


# Malo: lógica en una sola línea
def validar_edad(edad): return edad >= 18 and edad <= 120


# Malo: comparación con None incorrecta
def buscar(item):
    resultado = None
    if item == None: return resultado  # Debe ser 'is None'
    return item


# Malo: comparación con True/False
def esta_activo(usuario):
    if usuario['activo'] == True:  # Malo: debe ser 'if usuario["activo"]:'
        return True
    else:
        return False


# Malo: múltiples statements en una línea
def procesar(): x = 1; y = 2; return x + y


class Producto:
    """Malo: docstring sin formato consistente"""
    def __init__(self,id,nombre,precio):
        """
        Constructor
        """
        self.id=id
        self.nombre=nombre
        self.precio=precio
    
    def aplicar_descuento(self,porcentaje):
        """Aplica descuento"""  # Malo: docstring inconsistente
        if porcentaje<0 or porcentaje>100:raise ValueError('Porcentaje inválido')
        self.precio=self.precio*(1-porcentaje/100)
        return self.precio


# Malo: nombres de variables no descriptivos
def f(x,y):
    z=x+y
    a=z*2
    b=a/3
    return b


# Malo: código muy anidado
def procesar_usuario(usuario):
    if usuario:
        if 'email' in usuario:
            if usuario['email']:
                if '@' in usuario['email']:
                    if usuario['email'].endswith('.com'):
                        return True
    return False


# Malo: usar lambda cuando no es necesario
suma = lambda x, y: x + y
multiplica = lambda x, y: x * y


# Malo: lista comprehension compleja en una línea
resultado = [x*2 for x in range(100) if x % 2 == 0 if x % 3 == 0 if x > 10]


# Malo: trailing whitespace (espacios al final de líneas)
class Calculadora:  
    def sumar(self, a, b):  
        return a + b  
    
    def restar(self, a, b):  
        return a - b  


# Malo: líneas en blanco inconsistentes
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre


    def hablar(self):


        pass



class Perro(Animal):

    def hablar(self):
        return "Guau"


# Malo: concatenación de strings ineficiente
def construir_mensaje(usuario):
    mensaje = "Hola, " + usuario['nombre'] + " " + usuario['apellido'] + ". "
    mensaje = mensaje + "Tu email es " + usuario['email'] + " y tu teléfono es " + str(usuario['telefono']) + "."
    return mensaje


# Malo: no usar dict.get()
def obtener_valor(diccionario, clave):
    if clave in diccionario:
        return diccionario[clave]
    else:
        return None


# Malo: usar list() y dict() innecesariamente
lista_vacia = list()
dict_vacio = dict()


if __name__ == '__main__':
    usuario = Usuario('Ana',25)
    usuario.saludar()
    
    print("Edad válida:",validar_edad(30))
    
    producto = Producto(1,'Laptop',1200.0)
    producto.aplicar_descuento(10)
    print('Precio con descuento:',producto.precio)
