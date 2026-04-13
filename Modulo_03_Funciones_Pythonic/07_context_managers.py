"""
Módulo 3 - Ejemplo 7: Context Managers
=======================================

Este script demuestra context managers en Python (with statement).
"""

import time
from contextlib import contextmanager
import tempfile
import os


def seccion(titulo):
    """Helper para mostrar títulos de sección."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70 + "\n")


def demo_with_basico():
    """Demuestra el uso básico de with."""
    seccion("WITH STATEMENT - BÁSICO")
    
    # Sin with (manual)
    print("📌 Sin with (manejo manual):")
    archivo = open('temp_sin_with.txt', 'w')
    try:
        archivo.write("Hola, Mundo!\n")
        print("  Archivo escrito")
    finally:
        archivo.close()
        print("  Archivo cerrado manualmente")
    
    # Con with (automático)
    print("\n📌 Con with (automático):")
    with open('temp_con_with.txt', 'w') as archivo:
        archivo.write("Hola, Mundo con with!\n")
        print("  Archivo escrito")
    # archivo se cierra automáticamente
    print("  Archivo cerrado automáticamente")
    
    # Verificar que se cerró
    print(f"\n¿Archivo cerrado? {archivo.closed}")
    
    # Limpieza
    os.remove('temp_sin_with.txt')
    os.remove('temp_con_with.txt')


def demo_multiples_context_managers():
    """Demuestra múltiples context managers."""
    seccion("MÚLTIPLES CONTEXT MANAGERS")
    
    # Forma antigua (anidada)
    print("📌 Anidado (forma antigua):")
    with open('archivo1.txt', 'w') as f1:
        with open('archivo2.txt', 'w') as f2:
            f1.write("Contenido 1\n")
            f2.write("Contenido 2\n")
            print("  Ambos archivos escritos")
    print("  Ambos archivos cerrados")
    
    # Forma moderna (una sola línea)
    print("\n📌 Una línea (Python 3.1+):")
    with open('archivo3.txt', 'w') as f1, open('archivo4.txt', 'w') as f2:
        f1.write("Contenido 3\n")
        f2.write("Contenido 4\n")
        print("  Ambos archivos escritos")
    print("  Ambos archivos cerrados")
    
    # Limpieza
    for archivo in ['archivo1.txt', 'archivo2.txt', 'archivo3.txt', 'archivo4.txt']:
        if os.path.exists(archivo):
            os.remove(archivo)


def demo_context_manager_clase():
    """Demuestra context manager personalizado con clase."""
    seccion("CONTEXT MANAGER - CLASE")
    
    class Timer:
        """Context manager para medir tiempo."""
        
        def __init__(self, nombre="Operación"):
            """Inicializa el timer."""
            self.nombre = nombre
            self.inicio = None
        
        def __enter__(self):
            """Se ejecuta al entrar al bloque with."""
            print(f"⏱️  Iniciando: {self.nombre}")
            self.inicio = time.time()
            return self  # Valor asignado a 'as variable'
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            """Se ejecuta al salir del bloque with."""
            fin = time.time()
            duracion = fin - self.inicio
            print(f"✅ Completado: {self.nombre} en {duracion:.4f}s")
            
            # Si retorna True, suprime excepciones
            return False
    
    print("📌 Context manager personalizado:")
    with Timer("Proceso 1"):
        time.sleep(0.1)
        print("  Trabajando...")
    
    print("\n📌 Con acceso al objeto:")
    with Timer("Proceso 2") as timer:
        time.sleep(0.05)
        print(f"  Inicio: {timer.inicio}")


def demo_context_manager_decorador():
    """Demuestra context manager con decorador @contextmanager."""
    seccion("CONTEXT MANAGER - @CONTEXTMANAGER")
    
    @contextmanager
    def timer(nombre="Operación"):
        """Context manager para medir tiempo usando decorador."""
        print(f"⏱️  Iniciando: {nombre}")
        inicio = time.time()
        
        try:
            yield inicio  # Lo que se asigna a 'as variable'
        finally:
            fin = time.time()
            duracion = fin - inicio
            print(f"✅ Completado: {nombre} en {duracion:.4f}s")
    
    print("📌 Con @contextmanager:")
    with timer("Operación simple"):
        time.sleep(0.1)
        print("  Trabajando...")
    
    print("\n📌 Con valor de yield:")
    with timer("Operación con timestamp") as inicio:
        print(f"  Timestamp inicio: {inicio}")
        time.sleep(0.05)


def demo_context_manager_excepciones():
    """Demuestra manejo de excepciones en context managers."""
    seccion("MANEJO DE EXCEPCIONES")
    
    # Context manager que maneja excepciones
    class ManejadorErrores:
        """Context manager que captura y registra excepciones."""
        
        def __enter__(self):
            """Entrada."""
            print("  Entrando al bloque protegido")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            """Salida con manejo de excepciones."""
            if exc_type is not None:
                print(f"  ❌ Error capturado: {exc_type.__name__}: {exc_val}")
                print("  Manejando el error...")
                return True  # Suprime la excepción
            print("  ✅ Bloque completado sin errores")
            return False
    
    print("📌 Con error (suprimido):")
    with ManejadorErrores():
        print("  Código antes del error")
        raise ValueError("Algo salió mal")
        print("  Este código no se ejecuta")
    print("  Continuando después del error (fue suprimido)")
    
    print("\n📌 Sin error:")
    with ManejadorErrores():
        print("  Todo funciona correctamente")
    
    # Con @contextmanager
    @contextmanager
    def suprimir_errores(*tipos_error):
        """Suprime tipos específicos de errores."""
        try:
            yield
        except tipos_error as e:
            print(f"  ⚠️  Error suprimido: {type(e).__name__}")
    
    print("\n📌 Suprimir errores específicos:")
    with suprimir_errores(ValueError, TypeError):
        print("  Esto causa ValueError")
        raise ValueError("Error de prueba")
    print("  Continuando...")


def demo_context_manager_archivo():
    """Demuestra context manager para archivos."""
    seccion("CONTEXT MANAGER - ARCHIVO TEMPORAL")
    
    @contextmanager
    def archivo_temporal(nombre, modo='w'):
        """Crea archivo temporal y lo elimina al salir."""
        print(f"  📁 Creando archivo temporal: {nombre}")
        archivo = open(nombre, modo)
        
        try:
            yield archivo
        finally:
            archivo.close()
            print(f"  🗑️  Cerrando y eliminando: {nombre}")
            if os.path.exists(nombre):
                os.remove(nombre)
    
    print("📌 Archivo temporal:")
    with archivo_temporal('temp_demo.txt', 'w') as f:
        f.write("Contenido temporal\n")
        f.write("Este archivo será eliminado\n")
        print("  ✍️  Archivo escrito")
    print("  Archivo eliminado (fuera del contexto)")


def demo_context_manager_transaccional():
    """Demuestra context manager para operaciones transaccionales."""
    seccion("CONTEXT MANAGER - TRANSACCIONAL")
    
    class BaseDatos:
        """Simulador de base de datos."""
        
        def __init__(self):
            """Inicializa BD."""
            self.datos = []
            self.en_transaccion = False
            self.backup = None
        
        @contextmanager
        def transaccion(self):
            """Context manager para transacciones."""
            print("  🔓 Iniciando transacción")
            self.en_transaccion = True
            self.backup = self.datos.copy()
            
            try:
                yield self
                print("  ✅ Commit: guardando cambios")
                self.backup = None
            except Exception as e:
                print(f"  ❌ Rollback: {e}")
                self.datos = self.backup
                self.backup = None
                raise
            finally:
                self.en_transaccion = False
                print("  🔒 Transacción finalizada")
        
        def agregar(self, dato):
            """Agrega dato."""
            self.datos.append(dato)
            print(f"    Agregado: {dato}")
    
    print("📌 Transacción exitosa:")
    bd = BaseDatos()
    
    with bd.transaccion():
        bd.agregar("Usuario 1")
        bd.agregar("Usuario 2")
    
    print(f"Datos finales: {bd.datos}")
    
    print("\n📌 Transacción con error (rollback):")
    try:
        with bd.transaccion():
            bd.agregar("Usuario 3")
            bd.agregar("Usuario 4")
            raise ValueError("Error simulado")
            bd.agregar("Usuario 5")  # No se ejecuta
    except ValueError:
        pass
    
    print(f"Datos finales (rollback aplicado): {bd.datos}")


def demo_context_manager_cambio_directorio():
    """Demuestra context manager para cambiar directorio."""
    seccion("CONTEXT MANAGER - CAMBIAR DIRECTORIO")
    
    @contextmanager
    def cambiar_directorio(ruta):
        """Cambia temporalmente el directorio de trabajo."""
        directorio_original = os.getcwd()
        print(f"  📁 Directorio original: {directorio_original}")
        print(f"  ➡️  Cambiando a: {ruta}")
        
        os.chdir(ruta)
        
        try:
            yield os.getcwd()
        finally:
            print(f"  ⬅️  Regresando a: {directorio_original}")
            os.chdir(directorio_original)
    
    print("📌 Cambiar directorio temporalmente:")
    print(f"Antes: {os.getcwd()}")
    
    with cambiar_directorio(tempfile.gettempdir()) as dir_temp:
        print(f"Dentro del with: {os.getcwd()}")
        print(f"(es temp?: {dir_temp == tempfile.gettempdir()})")
    
    print(f"Después: {os.getcwd()}")


def demo_context_manager_configuracion():
    """Demuestra context manager para configuración temporal."""
    seccion("CONTEXT MANAGER - CONFIGURACIÓN TEMPORAL")
    
    class Configuracion:
        """Sistema de configuración."""
        
        def __init__(self):
            """Inicializa configuración."""
            self.opciones = {
                'debug': False,
                'verbose': False,
                'timeout': 30
            }
        
        @contextmanager
        def temporal(self, **kwargs):
            """Aplica configuración temporal."""
            # Guardar valores originales
            originales = {k: self.opciones.get(k) for k in kwargs}
            print(f"  💾 Guardando config original: {originales}")
            
            # Aplicar temporales
            self.opciones.update(kwargs)
            print(f"  ⚙️  Aplicando config temporal: {kwargs}")
            
            try:
                yield self
            finally:
                # Restaurar originales
                self.opciones.update(originales)
                print(f"  ↩️  Restaurando config: {originales}")
    
    print("📌 Configuración temporal:")
    config = Configuracion()
    
    print(f"Config inicial: {config.opciones}")
    
    with config.temporal(debug=True, verbose=True, timeout=60):
        print(f"Config dentro del with: {config.opciones}")
    
    print(f"Config final: {config.opciones}")


def demo_context_manager_suppress():
    """Demuestra contextlib.suppress."""
    seccion("CONTEXTLIB.SUPPRESS")
    
    from contextlib import suppress
    
    print("📌 Sin suppress (manejo tradicional):")
    try:
        with open('archivo_inexistente.txt') as f:
            contenido = f.read()
    except FileNotFoundError:
        print("  Archivo no encontrado (try-except)")
    
    print("\n📌 Con suppress (más limpio):")
    with suppress(FileNotFoundError):
        with open('archivo_inexistente.txt') as f:
            contenido = f.read()
        print("  Esta línea no se ejecuta si hay error")
    print("  Error suprimido automáticamente")
    
    # Múltiples excepciones
    print("\n📌 Suprimir múltiples excepciones:")
    with suppress(FileNotFoundError, PermissionError, OSError):
        # Código que puede lanzar cualquiera de estos errores
        os.remove('archivo_que_no_existe.txt')
    print("  Cualquier error de archivo fue suprimido")


def ejercicio_practico():
    """Ejercicio práctico integrando conceptos."""
    seccion("EJERCICIO PRÁCTICO: Sistema de Logging")
    
    @contextmanager
    def log_operacion(nombre, nivel="INFO"):
        """Context manager para logging de operaciones."""
        print(f"[{nivel}] Iniciando: {nombre}")
        inicio = time.time()
        error_ocurrido = False
        
        try:
            yield
        except Exception as e:
            error_ocurrido = True
            print(f"[ERROR] {nombre} falló: {e}")
            raise
        finally:
            fin = time.time()
            duracion = fin - inicio
            estado = "❌ FALLIDO" if error_ocurrido else "✅ EXITOSO"
            print(f"[{nivel}] {estado}: {nombre} ({duracion:.4f}s)")
    
    print("📌 Sistema de logging con context manager:")
    
    with log_operacion("Cargar datos", "INFO"):
        time.sleep(0.1)
        print("  Datos cargados")
    
    with log_operacion("Procesar datos", "DEBUG"):
        time.sleep(0.05)
        print("  Datos procesados")
    
    print("\n📌 Con error:")
    try:
        with log_operacion("Operación problemática", "WARNING"):
            time.sleep(0.02)
            raise ValueError("Datos inválidos")
    except ValueError:
        print("  Error manejado externamente")


def demo_context_manager_anidado():
    """Demuestra context managers anidados."""
    seccion("CONTEXT MANAGERS ANIDADOS")
    
    @contextmanager
    def nivel(numero):
        """Context manager que muestra nivel de anidamiento."""
        print("  " * numero + f"→ Entrando nivel {numero}")
        try:
            yield numero
        finally:
            print("  " * numero + f"← Saliendo nivel {numero}")
    
    print("📌 Anidamiento:")
    with nivel(1):
        print("    En nivel 1")
        with nivel(2):
            print("      En nivel 2")
            with nivel(3):
                print("        En nivel 3")


def main():
    """Función principal."""
    print("\n" + "🐍" * 35)
    print("          CONTEXT MANAGERS EN PYTHON")
    print("🐍" * 35)
    
    demo_with_basico()
    demo_multiples_context_managers()
    demo_context_manager_clase()
    demo_context_manager_decorador()
    demo_context_manager_excepciones()
    demo_context_manager_archivo()
    demo_context_manager_transaccional()
    demo_context_manager_cambio_directorio()
    demo_context_manager_configuracion()
    demo_context_manager_suppress()
    ejercicio_practico()
    demo_context_manager_anidado()
    
    print("\n" + "=" * 70)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("=" * 70)
    print("\n💡 Puntos clave:")
    print("   • with: garantiza cleanup automático de recursos")
    print("   • __enter__(): se ejecuta al entrar al bloque")
    print("   • __exit__(): se ejecuta al salir (incluso con error)")
    print("   • @contextmanager: forma simple con yield")
    print("   • Casos de uso: archivos, conexiones, locks, transacciones")
    print("   • contextlib.suppress: suprimir excepciones específicas")
    print("   • Siempre preferir 'with' para manejo de recursos")
    print("   • Útil para setup/cleanup automático\n")


if __name__ == "__main__":
    main()
