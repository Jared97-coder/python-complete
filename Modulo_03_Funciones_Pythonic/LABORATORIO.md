# Laboratorio 3: Funciones y Programación "Pythonic" 🔬

## Objetivo
Implementar tres componentes avanzados de Python que demuestren dominio de decoradores, generadores y context managers: un sistema de reintentos con backoff exponencial, un generador eficiente por lotes, y un context manager profesional de temporización.

---

## Preparación del Entorno

### 1. Crear proyecto
```powershell
# Navegar a la carpeta del módulo
cd Modulo_03_Funciones_Pythonic

# Crear carpeta para el laboratorio
mkdir laboratorio
cd laboratorio

# Crear archivo principal
New-Item laboratorio.py
```

### 2. Estructura del proyecto
```
Modulo_03_Funciones_Pythonic/
└── laboratorio/
    ├── laboratorio.py          # Código principal
    ├── test_laboratorio.py     # Tests (opcional)
    └── README.md               # Documentación
```

---

## Parte 1: Decorador de Reintentos con Backoff Exponencial ⚡

### Objetivo
Implementar un decorador robusto que reintente operaciones fallidas con espera exponencial entre intentos.

### Especificaciones

```python
"""
Decorador: @retry_with_backoff
==============================

Parámetros:
- max_intentos: int = 3
  Número máximo de intentos

- backoff_factor: float = 2.0
  Factor multiplicador para el delay (2.0 = exponencial)

- delay_inicial: float = 1.0
  Delay en segundos del primer reintento

- excepciones: tuple = (Exception,)
  Tupla de excepciones a capturar

- on_retry: callable = None
  Callback ejecutado en cada reintento (recibe intento_num, excepcion)

Comportamiento:
- Primer intento: sin delay
- Segundo intento: delay_inicial
- Tercer intento: delay_inicial * backoff_factor
- Cuarto intento: delay_inicial * backoff_factor^2
- ...

Si todos los intentos fallan, lanza la última excepción.
"""
```

### Implementación

```python
import functools
import time
from typing import Callable, Type, Tuple, Optional


def retry_with_backoff(
    max_intentos: int = 3,
    backoff_factor: float = 2.0,
    delay_inicial: float = 1.0,
    excepciones: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable] = None
):
    """
    Decorador que reintenta una función con backoff exponencial.
    
    Args:
        max_intentos: Número máximo de intentos
        backoff_factor: Factor multiplicador del delay
        delay_inicial: Delay base en segundos
        excepciones: Tupla de excepciones a capturar
        on_retry: Callback opcional en cada reintento
    
    Example:
        @retry_with_backoff(max_intentos=3, delay_inicial=0.5)
        def fetch_data(url):
            response = requests.get(url)
            return response.json()
    """
    def decorador(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ultima_excepcion = None
            
            for intento in range(1, max_intentos + 1):
                try:
                    # Intentar ejecutar la función
                    print(f"🔄 Intento {intento}/{max_intentos}: {func.__name__}")
                    resultado = func(*args, **kwargs)
                    
                    if intento > 1:
                        print(f"✅ Éxito en intento {intento}")
                    
                    return resultado
                
                except excepciones as e:
                    ultima_excepcion = e
                    print(f"❌ Error en intento {intento}: {type(e).__name__}: {e}")
                    
                    # Callback opcional
                    if on_retry:
                        on_retry(intento, e)
                    
                    # Si no es el último intento, esperar
                    if intento < max_intentos:
                        # Calcular delay: inicial * factor^(intento-1)
                        delay = delay_inicial * (backoff_factor ** (intento - 1))
                        print(f"⏳ Esperando {delay:.2f}s antes del siguiente intento...")
                        time.sleep(delay)
                    else:
                        print(f"💥 Agotados todos los intentos")
            
            # Si llegamos aquí, todos los intentos fallaron
            raise ultima_excepcion
        
        return wrapper
    return decorador


# ============================================================================
# TESTS Y EJEMPLOS
# ============================================================================

def test_decorador_retry():
    """Tests del decorador de retry."""
    print("\n" + "="*70)
    print("TEST 1: Operación que falla 2 veces y luego funciona")
    print("="*70)
    
    intentos = [0]  # Lista para que sea mutable en la función
    
    @retry_with_backoff(
        max_intentos=4,
        delay_inicial=0.5,
        backoff_factor=2.0,
        excepciones=(ConnectionError, TimeoutError)
    )
    def operacion_inestable():
        """Función que falla las primeras 2 veces."""
        intentos[0] += 1
        if intentos[0] < 3:
            raise ConnectionError(f"Conexión perdida (intento {intentos[0]})")
        return "✅ Operación exitosa"
    
    try:
        resultado = operacion_inestable()
        print(f"\n🎉 Resultado final: {resultado}")
    except Exception as e:
        print(f"\n💀 Error final: {e}")
    
    # Test 2: Operación que siempre falla
    print("\n" + "="*70)
    print("TEST 2: Operación que siempre falla")
    print("="*70)
    
    @retry_with_backoff(max_intentos=3, delay_inicial=0.3)
    def operacion_imposible():
        """Función que siempre falla."""
        raise ValueError("Error irrecuperable")
    
    try:
        operacion_imposible()
    except ValueError as e:
        print(f"\n💀 Excepción final capturada: {e}")
    
    # Test 3: Con callback
    print("\n" + "="*70)
    print("TEST 3: Con callback personalizado")
    print("="*70)
    
    def mi_callback(intento_num, excepcion):
        """Callback que registra cada reintento."""
        print(f"  📝 CALLBACK: Reintento #{intento_num} - {excepcion}")
    
    intentos[0] = 0
    
    @retry_with_backoff(
        max_intentos=3,
        delay_inicial=0.2,
        on_retry=mi_callback
    )
    def operacion_con_log():
        """Operación con logging detallado."""
        intentos[0] += 1
        if intentos[0] < 3:
            raise RuntimeError(f"Fallo #{intentos[0]}")
        return "OK"
    
    resultado = operacion_con_log()
    print(f"\n🎉 Resultado: {resultado}")


# Ejecutar test
if __name__ == "__main__":
    test_decorador_retry()
```

### Casos de uso reales

```python
# Ejemplo 1: API request
@retry_with_backoff(max_intentos=5, delay_inicial=1.0)
def fetch_api_data(url):
    """Obtiene datos de API con reintentos."""
    import requests
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()

# Ejemplo 2: Conexión a base de datos
@retry_with_backoff(
    max_intentos=3,
    delay_inicial=2.0,
    excepciones=(ConnectionError, TimeoutError)
)
def conectar_bd(host, puerto):
    """Conecta a base de datos con reintentos."""
    # Código de conexión...
    pass
```

---

## Parte 2: Generador por Lotes (Batch Generator) 📦

### Objetivo
Implementar un generador eficiente que procese datos en lotes, optimizando memoria y permitiendo procesamiento paralelo.

### Especificaciones

```python
"""
Generador: batch_generator
==========================

Parámetros:
- iterable: cualquier iterable (lista, generador, archivo, etc.)
- tamaño_lote: int = 100
  Número de elementos por lote

- transformar: callable = None
  Función opcional para transformar cada elemento

- filtrar: callable = None
  Función opcional para filtrar elementos (retorna bool)

Yields:
- list: Lote de elementos procesados

Características:
- Eficiente en memoria (lazy evaluation)
- Último lote puede ser más pequeño
- Compatible con cualquier iterable
- Soporta transformación y filtrado on-the-fly
"""
```

### Implementación

```python
from typing import Iterable, Callable, Optional, Any, List


def batch_generator(
    iterable: Iterable,
    tamaño_lote: int = 100,
    transformar: Optional[Callable[[Any], Any]] = None,
    filtrar: Optional[Callable[[Any], bool]] = None
) -> Iterable[List[Any]]:
    """
    Genera lotes de elementos de un iterable.
    
    Args:
        iterable: Fuente de datos (lista, generador, archivo, etc.)
        tamaño_lote: Número de elementos por lote
        transformar: Función para transformar cada elemento
        filtrar: Función para filtrar elementos
    
    Yields:
        List: Lote de elementos procesados
    
    Examples:
        # Lotes simples
        for lote in batch_generator(range(250), tamaño_lote=100):
            print(f"Procesando lote de {len(lote)} elementos")
        
        # Con transformación
        for lote in batch_generator(
            range(10),
            tamaño_lote=3,
            transformar=lambda x: x ** 2
        ):
            print(lote)  # [0, 1, 4], [9, 16, 25], [36, 49, 64], [81]
        
        # Con filtrado
        for lote in batch_generator(
            range(20),
            tamaño_lote=5,
            filtrar=lambda x: x % 2 == 0  # Solo pares
        ):
            print(lote)
    """
    lote = []
    
    for elemento in iterable:
        # Aplicar filtro si existe
        if filtrar and not filtrar(elemento):
            continue
        
        # Aplicar transformación si existe
        if transformar:
            elemento = transformar(elemento)
        
        # Agregar al lote
        lote.append(elemento)
        
        # Si el lote está completo, producirlo
        if len(lote) == tamaño_lote:
            yield lote
            lote = []
    
    # Producir último lote (puede ser incompleto)
    if lote:
        yield lote


# ============================================================================
# TESTS Y EJEMPLOS
# ============================================================================

def test_generador_lotes():
    """Tests del generador por lotes."""
    
    print("\n" + "="*70)
    print("TEST 1: Lotes básicos")
    print("="*70)
    
    datos = range(25)
    print(f"Datos: 0-24 (25 elementos)")
    print(f"Tamaño de lote: 10")
    
    for i, lote in enumerate(batch_generator(datos, tamaño_lote=10), 1):
        print(f"  Lote {i}: {len(lote)} elementos - {lote[:3]}...{lote[-3:]}")
    
    # Test 2: Con transformación
    print("\n" + "="*70)
    print("TEST 2: Con transformación (elevar al cuadrado)")
    print("="*70)
    
    for i, lote in enumerate(
        batch_generator(
            range(15),
            tamaño_lote=5,
            transformar=lambda x: x ** 2
        ), 1
    ):
        print(f"  Lote {i}: {lote}")
    
    # Test 3: Con filtrado
    print("\n" + "="*70)
    print("TEST 3: Con filtrado (solo números pares)")
    print("="*70)
    
    for i, lote in enumerate(
        batch_generator(
            range(20),
            tamaño_lote=5,
            filtrar=lambda x: x % 2 == 0
        ), 1
    ):
        print(f"  Lote {i}: {lote}")
    
    # Test 4: Procesamiento de archivo grande (simulado)
    print("\n" + "="*70)
    print("TEST 4: Procesamiento de archivo (simulado)")
    print("="*70)
    
    def leer_archivo_simulado():
        """Generador que simula lectura de archivo."""
        for i in range(1000):
            yield f"Línea {i}"
    
    lineas_procesadas = 0
    for i, lote in enumerate(
        batch_generator(leer_archivo_simulado(), tamaño_lote=250), 1
    ):
        lineas_procesadas += len(lote)
        print(f"  Lote {i}: {len(lote)} líneas")
        # Aquí se procesaría el lote (ej: insertar en BD, enviar a API, etc.)
    
    print(f"\n✅ Total procesado: {lineas_procesadas} líneas")
    
    # Test 5: Pipeline de transformaciones
    print("\n" + "="*70)
    print("TEST 5: Pipeline complejo")
    print("="*70)
    
    # Simular datos de ventas
    ventas = [
        {'producto': f'Producto_{i}', 'precio': 10 + i, 'cantidad': i % 5}
        for i in range(50)
    ]
    
    def calcular_total(venta):
        """Transforma venta agregando total."""
        return {
            **venta,
            'total': venta['precio'] * venta['cantidad']
        }
    
    def tiene_ventas(venta):
        """Filtra ventas con cantidad > 0."""
        return venta['cantidad'] > 0
    
    totales_por_lote = []
    for i, lote in enumerate(
        batch_generator(
            ventas,
            tamaño_lote=10,
            transformar=calcular_total,
            filtrar=tiene_ventas
        ), 1
    ):
        total_lote = sum(v['total'] for v in lote)
        totales_por_lote.append(total_lote)
        print(f"  Lote {i}: {len(lote)} ventas - Total: ${total_lote:.2f}")
    
    print(f"\n💰 Total general: ${sum(totales_por_lote):.2f}")


# ============================================================================
# EJEMPLO AVANZADO: Procesamiento paralelo con batch_generator
# ============================================================================

def ejemplo_procesamiento_paralelo():
    """Ejemplo de procesamiento paralelo por lotes."""
    print("\n" + "="*70)
    print("EJEMPLO AVANZADO: Procesamiento paralelo")
    print("="*70)
    
    from concurrent.futures import ThreadPoolExecutor
    
    def procesar_lote_pesado(lote):
        """Simula procesamiento pesado de un lote."""
        time.sleep(0.1)  # Simular trabajo
        return sum(x ** 2 for x in lote)
    
    datos = range(1000)
    resultados = []
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Crear lotes y procesarlos en paralelo
        futures = []
        for i, lote in enumerate(batch_generator(datos, tamaño_lote=100)):
            future = executor.submit(procesar_lote_pesado, lote)
            futures.append(future)
        
        # Recoger resultados
        for i, future in enumerate(futures, 1):
            resultado = future.result()
            resultados.append(resultado)
            print(f"  Lote {i} procesado: suma = {resultado}")
    
    print(f"\n✅ Total final: {sum(resultados)}")


# Ejecutar tests
if __name__ == "__main__":
    test_generador_lotes()
    ejemplo_procesamiento_paralelo()
```

### Casos de uso reales

```python
# Ejemplo 1: Inserción masiva en BD
def insertar_usuarios_por_lotes(usuarios, conexion_bd):
    """Inserta usuarios en lotes para optimizar."""
    for lote in batch_generator(usuarios, tamaño_lote=1000):
        conexion_bd.insert_many(lote)
        print(f"Insertados {len(lote)} usuarios")

# Ejemplo 2: Procesamiento de archivo CSV gigante
def procesar_csv_grande(ruta_archivo):
    """Procesa CSV en lotes sin cargar todo en memoria."""
    with open(ruta_archivo) as f:
        for lote in batch_generator(f, tamaño_lote=5000):
            # Procesar lote
            datos_procesados = [procesar_linea(linea) for linea in lote]
            guardar_resultados(datos_procesados)

# Ejemplo 3: ETL con transformación
def etl_pipeline(origen, destino):
    """Pipeline ETL eficiente."""
    for lote in batch_generator(
        origen,
        tamaño_lote=500,
        transformar=limpiar_dato,
        filtrar=validar_dato
    ):
        destino.write_batch(lote)
```

---

## Parte 3: Context Manager de Temporización ⏱️

### Objetivo
Implementar un context manager profesional para medir y registrar tiempos de ejecución con múltiples características avanzadas.

### Especificaciones

```python
"""
Context Manager: Timer
======================

Características:
- Mide tiempo transcurrido en bloque with
- Divide tiempo en fases (splits)
- Calcula estadísticas (min, max, promedio)
- Formatea salida legible
- Genera reportes detallados
- Soporta contextos anidados

Uso básico:
    with Timer("Operación"):
        # código a medir
        pass

Uso avanzado:
    with Timer("Proceso") as timer:
        # Fase 1
        timer.split("Fase 1")
        
        # Fase 2
        timer.split("Fase 2")
    
    print(timer.reporte())
"""
```

### Implementación

```python
import time
from contextlib import contextmanager
from typing import Optional, Dict, List
from dataclasses import dataclass, field


@dataclass
class Fase:
    """Representa una fase dentro de la temporización."""
    nombre: str
    inicio: float
    fin: Optional[float] = None
    
    @property
    def duracion(self) -> Optional[float]:
        """Calcula duración de la fase."""
        if self.fin is None:
            return None
        return self.fin - self.inicio


class Timer:
    """
    Context manager profesional para temporización.
    
    Attributes:
        nombre: Nombre de la operación
        inicio: Timestamp de inicio
        fin: Timestamp de fin
        fases: Lista de fases registradas
        nivel: Nivel de anidamiento
    
    Examples:
        # Uso básico
        with Timer("Operación"):
            time.sleep(1)
        
        # Con splits
        with Timer("Proceso complejo") as timer:
            time.sleep(0.5)
            timer.split("Fase 1")
            
            time.sleep(0.3)
            timer.split("Fase 2")
        
        print(timer.reporte())
    """
    
    # Variable de clase para tracking de nivel
    _nivel_actual = 0
    
    def __init__(self, nombre: str = "Operación", verbose: bool = True):
        """
        Inicializa el timer.
        
        Args:
            nombre: Nombre de la operación a medir
            verbose: Si True, imprime información automáticamente
        """
        self.nombre = nombre
        self.verbose = verbose
        self.inicio: Optional[float] = None
        self.fin: Optional[float] = None
        self.fases: List[Fase] = []
        self.nivel = 0
    
    def __enter__(self):
        """Inicia la temporización."""
        Timer._nivel_actual += 1
        self.nivel = Timer._nivel_actual
        
        self.inicio = time.time()
        
        if self.verbose:
            indent = "  " * (self.nivel - 1)
            print(f"{indent}⏱️  Iniciando: {self.nombre}")
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Finaliza la temporización."""
        self.fin = time.time()
        
        # Cerrar última fase si existe
        if self.fases and self.fases[-1].fin is None:
            self.fases[-1].fin = self.fin
        
        if self.verbose:
            indent = "  " * (self.nivel - 1)
            duracion = self.duracion
            print(f"{indent}✅ Completado: {self.nombre} - {self._formatear_tiempo(duracion)}")
            
            # Mostrar fases si existen
            if self.fases and len(self.fases) > 1:
                print(f"{indent}   Desglose:")
                for fase in self.fases:
                    if fase.duracion:
                        porcentaje = (fase.duracion / duracion) * 100
                        print(f"{indent}     • {fase.nombre}: "
                              f"{self._formatear_tiempo(fase.duracion)} ({porcentaje:.1f}%)")
        
        Timer._nivel_actual -= 1
        
        return False  # No suprimir excepciones
    
    def split(self, nombre: str):
        """
        Registra un split (división) en el tiempo.
        
        Args:
            nombre: Nombre de la fase
        """
        tiempo_actual = time.time()
        
        # Cerrar fase anterior si existe
        if self.fases and self.fases[-1].fin is None:
            self.fases[-1].fin = tiempo_actual
        
        # Crear nueva fase
        nueva_fase = Fase(nombre=nombre, inicio=tiempo_actual)
        self.fases.append(nueva_fase)
    
    @property
    def duracion(self) -> Optional[float]:
        """Retorna duración total en segundos."""
        if self.inicio is None or self.fin is None:
            return None
        return self.fin - self.inicio
    
    def _formatear_tiempo(self, segundos: float) -> str:
        """Formatea tiempo de manera legible."""
        if segundos < 0.001:
            return f"{segundos * 1_000_000:.2f}μs"
        elif segundos < 1:
            return f"{segundos * 1000:.2f}ms"
        elif segundos < 60:
            return f"{segundos:.2f}s"
        else:
            minutos = int(segundos // 60)
            segundos_resto = segundos % 60
            return f"{minutos}m {segundos_resto:.2f}s"
    
    def reporte(self) -> str:
        """Genera reporte detallado."""
        if self.duracion is None:
            return "Timer no completado"
        
        lineas = []
        lineas.append("=" * 60)
        lineas.append(f"REPORTE DE TEMPORIZACIÓN: {self.nombre}")
        lineas.append("=" * 60)
        lineas.append(f"Duración total: {self._formatear_tiempo(self.duracion)}")
        
        if self.fases:
            lineas.append(f"\nFases ({len(self.fases)}):")
            for i, fase in enumerate(self.fases, 1):
                if fase.duracion:
                    porcentaje = (fase.duracion / self.duracion) * 100
                    lineas.append(
                        f"  {i}. {fase.nombre}: "
                        f"{self._formatear_tiempo(fase.duracion)} ({porcentaje:.1f}%)"
                    )
            
            # Estadísticas
            duraciones = [f.duracion for f in self.fases if f.duracion]
            if duraciones:
                lineas.append(f"\nEstadísticas de fases:")
                lineas.append(f"  Más rápida: {self._formatear_tiempo(min(duraciones))}")
                lineas.append(f"  Más lenta: {self._formatear_tiempo(max(duraciones))}")
                lineas.append(f"  Promedio: {self._formatear_tiempo(sum(duraciones) / len(duraciones))}")
        
        lineas.append("=" * 60)
        return "\n".join(lineas)
    
    @contextmanager
    def fase(self, nombre: str):
        """Context manager para medir una fase específica."""
        self.split(nombre)
        yield
        # La fase se cerrará automáticamente en el siguiente split o al salir


# ============================================================================
# TESTS Y EJEMPLOS
# ============================================================================

def test_timer_basico():
    """Test básico del timer."""
    print("\n" + "="*70)
    print("TEST 1: Timer básico")
    print("="*70 + "\n")
    
    with Timer("Operación simple"):
        time.sleep(0.5)
    
    print("\n" + "="*70)
    print("TEST 2: Timer con acceso al objeto")
    print("="*70 + "\n")
    
    with Timer("Operación con info") as timer:
        time.sleep(0.3)
        print(f"  Tiempo transcurrido hasta ahora: {timer._formatear_tiempo(time.time() - timer.inicio)}")


def test_timer_con_splits():
    """Test de timer con divisiones."""
    print("\n" + "="*70)
    print("TEST 3: Timer con splits")
    print("="*70 + "\n")
    
    with Timer("Proceso por fases") as timer:
        # Fase 1: Inicialización
        time.sleep(0.2)
        timer.split("Inicialización")
        
        # Fase 2: Procesamiento
        time.sleep(0.5)
        timer.split("Procesamiento")
        
        # Fase 3: Finalización
        time.sleep(0.1)
        timer.split("Finalización")
    
    print("\n" + timer.reporte())


def test_timer_anidado():
    """Test de timers anidados."""
    print("\n" + "="*70)
    print("TEST 4: Timers anidados")
    print("="*70 + "\n")
    
    with Timer("Proceso principal"):
        time.sleep(0.1)
        
        with Timer("Subproceso 1"):
            time.sleep(0.2)
        
        with Timer("Subproceso 2"):
            time.sleep(0.15)
            
            with Timer("Sub-subproceso"):
                time.sleep(0.1)


def test_timer_con_context_manager_fase():
    """Test usando fase como context manager."""
    print("\n" + "="*70)
    print("TEST 5: Timer con context manager de fase")
    print("="*70 + "\n")
    
    with Timer("Pipeline de datos") as timer:
        with timer.fase("Carga de datos"):
            time.sleep(0.3)
        
        with timer.fase("Transformación"):
            time.sleep(0.5)
        
        with timer.fase("Guardado"):
            time.sleep(0.2)
    
    print("\n" + timer.reporte())


def test_timer_sin_verbose():
    """Test de timer silencioso."""
    print("\n" + "="*70)
    print("TEST 6: Timer silencioso (verbose=False)")
    print("="*70 + "\n")
    
    with Timer("Operación silenciosa", verbose=False) as timer:
        time.sleep(0.2)
        timer.split("Fase 1")
        time.sleep(0.3)
        timer.split("Fase 2")
    
    print("Timer ejecutado silenciosamente")
    print("\nReporte generado manualmente:")
    print(timer.reporte())


def ejemplo_uso_real():
    """Ejemplo de uso en caso real."""
    print("\n" + "="*70)
    print("EJEMPLO USO REAL: Pipeline ETL")
    print("="*70 + "\n")
    
    def cargar_datos():
        """Simula carga de datos."""
        time.sleep(0.3)
        return list(range(1000))
    
    def transformar_datos(datos):
        """Simula transformación."""
        time.sleep(0.5)
        return [x * 2 for x in datos]
    
    def validar_datos(datos):
        """Simula validación."""
        time.sleep(0.2)
        return True
    
    def guardar_datos(datos):
        """Simula guardado."""
        time.sleep(0.4)
    
    # Pipeline completo
    with Timer("Pipeline ETL completo") as timer:
        with timer.fase("Extracción"):
            datos = cargar_datos()
            print(f"    Cargados {len(datos)} registros")
        
        with timer.fase("Transformación"):
            datos_transformados = transformar_datos(datos)
            print(f"    Transformados {len(datos_transformados)} registros")
        
        with timer.fase("Validación"):
            validacion_ok = validar_datos(datos_transformados)
            print(f"    Validación: {'✅ OK' if validacion_ok else '❌ Error'}")
        
        with timer.fase("Carga"):
            guardar_datos(datos_transformados)
            print(f"    Guardados {len(datos_transformados)} registros")
    
    print("\n" + timer.reporte())


# Ejecutar todos los tests
if __name__ == "__main__":
    test_timer_basico()
    test_timer_con_splits()
    test_timer_anidado()
    test_timer_con_context_manager_fase()
    test_timer_sin_verbose()
    ejemplo_uso_real()
```

---

## Integración: Sistema Completo 🎯

### Combinar los tres componentes

```python
def sistema_completo_ejemplo():
    """Ejemplo que integra los tres componentes."""
    print("\n" + "="*70)
    print("SISTEMA COMPLETO: Integración de los 3 componentes")
    print("="*70 + "\n")
    
    # Simular operación con reintentos, por lotes, y temporización
    intentos = [0]
    
    @retry_with_backoff(max_intentos=3, delay_inicial=0.3, backoff_factor=1.5)
    def procesar_lote_con_reintentos(lote):
        """Procesa lote con posibilidad de fallo."""
        intentos[0] += 1
        if intentos[0] % 3 == 0:  # Falla cada 3 intentos
            raise ConnectionError("Error de red simulado")
        return sum(lote)
    
    # Pipeline completo
    with Timer("Sistema completo") as timer:
        datos = range(500)
        resultados = []
        
        with timer.fase("Procesamiento por lotes"):
            for i, lote in enumerate(
                batch_generator(
                    datos,
                    tamaño_lote=100,
                    transformar=lambda x: x ** 2
                ), 1
            ):
                print(f"    Procesando lote {i}...")
                try:
                    resultado = procesar_lote_con_reintentos(lote)
                    resultados.append(resultado)
                except Exception as e:
                    print(f"    ❌ Lote {i} falló finalmente: {e}")
        
        with timer.fase("Consolidación"):
            time.sleep(0.1)
            total =sum(resultados)
            print(f"    Total consolidado: {total}")
    
    print("\n" + timer.reporte())


if __name__ == "__main__":
    sistema_completo_ejemplo()
```

---

## Recursos Adicionales 📚

- [PEP 318 - Decorators](https://www.python.org/dev/peps/pep-0318/)
- [PEP 342 - Coroutines via Enhanced Generators](https://www.python.org/dev/peps/pep-0342/)
- [PEP 343 - The "with" Statement](https://www.python.org/dev/peps/pep-0343/)
- [Python contextlib documentation](https://docs.python.org/3/library/contextlib.html)
- [Exponential Backoff And Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)

---
