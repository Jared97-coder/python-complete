# Laboratorio: Sistema de Ingesta y Procesamiento de Datos

## Objetivos
- Ingestar datos desde archivos CSV
- Procesar y validar datos
- Calcular métricas y estadísticas
- Exportar resultados a JSON
- Implementar logging estructurado en múltiples niveles

---

## Escenario

Eres responsable de crear un sistema de procesamiento de ventas que:
1. Lee archivos CSV con datos de ventas
2. Valida y transforma los datos
3. Genera métricas (totales, promedios, tendencias)
4. Exporta resultados a JSON
5. Registra todo el proceso con logging apropiado

---

## Ejerc icio 1: Ingesta de CSV con Validación ⭐⭐⭐

### Descripción
Crear sistema para leer y validar datos de ventas desde CSV.

### Archivo de datos: `ventas.csv`

Crear este archivo primero:

```csv
id,fecha,producto,cantidad,precio_unitario,vendedor,region
1,2024-01-15,Laptop,2,1200.50,Ana García,Norte
2,2024-01-16,Mouse,10,25.00,Juan Pérez,Sur
3,2024-01-16,Teclado,5,75.50,Ana García,Norte
4,2024-01-17,Monitor,3,350.00,María López,Centro
5,2024-01-17,Laptop,1,1200.50,Juan Pérez,Sur
6,2024-01-18,Mouse,invalid,25.00,Carlos Ruiz,Este
7,2024-01-18,SSD,4,180.00,Ana García,Norte
8,2024-01-19,RAM,8,90.50,María López,Centro
9,2024-01-19,Teclado,3,75.50,Juan Pérez,Sur
10,2024-01-20,Monitor,2,350.00,Ana García,Norte
```

**Nota:** La fila 6 tiene un error intencional (`invalid` en cantidad).

### Tareas

**Parte A: Crear Modelo de Datos**

```python
from pydantic import BaseModel, Field, field_validator
from datetime import date
from decimal import Decimal

class Venta(BaseModel):
    """Modelo de venta con validación."""
    id: int
    fecha: date
    producto: str
    cantidad: int = Field(gt=0)
    precio_unitario: Decimal = Field(gt=0, decimal_places=2)
    vendedor: str
    region: str
    
    @field_validator('producto')
    @classmethod
    def producto_no_vacio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Producto no puede estar vacío")
        return v.strip()
    
    @property
    def total(self) -> Decimal:
        """Calcula el total de la venta."""
        return self.cantidad * self.precio_unitario
```

**Parte B: Implementar Ingesta**

```python
import csv
import logging
from pathlib import Path
from typing import List, Tuple

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ventas_proceso.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def leer_ventas_csv(archivo: Path) -> Tuple[List[Venta], List[dict]]:
    """
    Lee archivo CSV de ventas y valida.
    
    Returns:
        Tupla con (ventas_validas, ventas_con_error)
    """
    logger.info(f"Iniciando lectura de {archivo}")
    
    ventas_validas = []
    ventas_error = []
    
    with archivo.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for i, row in enumerate(reader, start=2):  # start=2 para línea del CSV
            try:
                venta = Venta(**row)
                ventas_validas.append(venta)
                logger.debug(f"Línea {i}: Venta {venta.id} procesada")
            
            except Exception as e:
                logger.error(f"Línea {i}: Error al procesar - {e}")
                ventas_error.append({
                    'linea': i,
                    'datos': row,
                    'error': str(e)
                })
    
    logger.info(
        f"Lectura completada: {len(ventas_validas)} válidas, "
        f"{len(ventas_error)} con errores"
    )
    
    return ventas_validas, ventas_error
```

**Parte C: Probar Ingesta**

```python
def main():
    archivo_csv = Path("ventas.csv")
    
    if not archivo_csv.exists():
        logger.critical(f"Archivo {archivo_csv} no encontrado")
        return
    
    ventas, errores = leer_ventas_csv(archivo_csv)
    
    print(f"\n✅ Ventas válidas: {len(ventas)}")
    print(f"❌ Ventas con error: {len(errores)}")
    
    if errores:
        print("\nErrores encontrados:")
        for error in errores:
            print(f"  Línea {error['linea']}: {error['error']}")


if __name__ == "__main__":
    main()
```

---

## Ejercicio 2: Cálculo de Métricas ⭐⭐⭐⭐

### Descripción
Calcular estadísticas y métricas sobre las ventas.

### Tareas

**Parte A: Métricas Básicas**

```python
from datetime import datetime
from decimal import Decimal
from collections import defaultdict
from typing import Dict, List

class AnalizadorVentas:
    """Calcula métricas sobre ventas."""
    
    def __init__(self, ventas: List[Venta]):
        self.ventas = ventas
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def total_ventas(self) -> Decimal:
        """Total de ventas."""
        total = sum(v.total for v in self.ventas)
        self.logger.info(f"Total ventas: ${total:,.2f}")
        return total
    
    def promedio_venta(self) -> Decimal:
        """Promedio por venta."""
        if not self.ventas:
            return Decimal(0)
        promedio = self.total_ventas() / len(self.ventas) promedio = sum(v.total for v in self.ventas) / len(self.ventas)
        self.logger.info(f"Promedio por venta: ${promedio:,.2f}")
        return promedio
    
    def ventas_por_producto(self) -> Dict[str, Dict]:
        """Ventas agrupadas por producto."""
        self.logger.debug("Calculando ventas por producto")
        
        productos = defaultdict(lambda: {
            'cantidad': 0,
            'total': Decimal(0),
            'ventas': 0
        })
        
        for venta in self.ventas:
            productos[venta.producto]['cantidad'] += venta.cantidad
            productos[venta.producto]['total'] += venta.total
            productos[venta.producto]['ventas'] += 1
        
        return dict(productos)
    
    def ventas_por_region(self) -> Dict[str, Decimal]:
        """Total de ventas por región."""
        self.logger.debug("Calculando ventas por región")
        
        regiones = defaultdict(Decimal)
        for venta in self.ventas:
            regiones[venta.region] += venta.total
        
        return dict(regiones)
    
    def ventas_por_vendedor(self) -> Dict[str, Dict]:
        """Ventas por vendedor."""
        self.logger.debug("Calculando ventas por vendedor")
        
        vendedores = defaultdict(lambda: {
            'ventas': 0,
            'total': Decimal(0),
            'productos_vendidos': set()
        })
        
        for venta in self.ventas:
            vendedores[venta.vendedor]['ventas'] += 1
            vendedores[venta.vendedor]['total'] += venta.total
            vendedores[venta.vendedor]['productos_vendidos'].add(venta.producto)
        
        # Convertir sets a listas para serialización
        resultado = {}
        for vendedor, datos in vendedores.items():
            resultado[vendedor] = {
                'ventas': datos['ventas'],
                'total': float(datos['total']),
                'productos_vendidos': list(datos['productos_vendidos'])
            }
        
        return resultado
    
    def top_productos(self, n: int = 5) -> List[Dict]:
        """Top N productos más vendidos."""
        productos = self.ventas_por_producto()
        
        top = sorted(
            productos.items(),
            key=lambda x: x[1]['total'],
            reverse=True
        )[:n]
        
        self.logger.info(f"Top {n} productos calculado")
        
        return [
            {
                'producto': nombre,
                'cantidad': datos['cantidad'],
                'total': float(datos['total']),
                'num_ventas': datos['ventas']
            }
            for nombre, datos in top
        ]
```

**Parte B: Usar Analizador**

```python
def analizar_ventas(ventas: List[Venta]):
    """Analiza ventas y muestra métricas."""
    analizador = AnalizadorVentas(ventas)
    
    print("\n=== MÉTRICAS DE VENTAS ===\n")
    
    # Total y promedio
    total = analizador.total_ventas()
    promedio = analizador.promedio_venta()
    print(f"Total ventas: ${total:,.2f}")
    print(f"Promedio por venta: ${promedio:,.2f}")
    print(f"Número de ventas: {len(ventas)}")
    
    # Por región
    print("\n--- Ventas por Región ---")
    for region, total in analizador.ventas_por_region().items():
        print(f"  {region}: ${total:,.2f}")
    
    # Top productos
    print("\n--- Top 3 Productos ---")
    for i, producto in enumerate(analizador.top_productos(3), 1):
        print(f"  {i}. {producto['producto']}: "
              f"${producto['total']:,.2f} "
              f"({producto['cantidad']} unidades en {producto['num_ventas']} ventas)")
```

---

## Ejercicio 3: Exportación a JSON ⭐⭐⭐

### Descripción
Exportar análisis completo a formato JSON.

### Tareas

**Parte A: Crear Reporte JSON**

```python
import json
from datetime import datetime

def exportar_reporte_json(
    ventas: List[Venta],
    analizador: AnalizadorVentas,
    archivo_salida: Path
):
    """Exporta reporte completo a JSON."""
    logger.info(f"Generando reporte JSON: {archivo_salida}")
    
    # Construir reporte
    reporte = {
        'metadata': {
            'fecha_generacion': datetime.now().isoformat(),
            'total_ventas_procesadas': len(ventas),
            'archivo_fuente': 'ventas.csv'
        },
        'resumen': {
            'total_ventas': float(analizador.total_ventas()),
            'promedio_venta': float(analizador.promedio_venta()),
            'numero_ventas': len(ventas)
        },
        'por_region': {
            region: float(total)
            for region, total in analizador.ventas_por_region().items()
        },
        'por_vendedor': analizador.ventas_por_vendedor(),
        'top_productos': analizador.top_productos(5),
        'detalle_ventas': [
            {
                'id': v.id,
                'fecha': v.fecha.isoformat(),
                'producto': v.producto,
                'cantidad': v.cantidad,
                'precio_unitario': float(v.precio_unitario),
                'total': float(v.total),
                'vendedor': v.vendedor,
                'region': v.region
            }
            for v in ventas
        ]
    }
    
    # Guardar JSON
    with archivo_salida.open('w', encoding='utf-8') as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Reporte JSON generado: {archivo_salida}")
    logger.info(f"Tamaño: {archivo_salida.stat().st_size} bytes")
```

---

## Ejercicio 4: Sistema Completo con Logging ⭐⭐⭐⭐⭐

### Descripción
Integrar todo en un sistema completo con logging multinivel.

### Configuración de Logging

```python
from logging.handlers import RotatingFileHandler

def configurar_logging():
    """Configura logging con múltiples handlers."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Logger raíz
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Handler para consola (INFO y superior)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(levelname)-8s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    
    # Handler para archivo detallado (DEBUG y superior)
    file_handler = RotatingFileHandler(
        log_dir / 'ventas_detallado.log',
        maxBytes=1048576,  # 1MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_format)
    
    # Handler para errores (WARNING y superior)
    error_handler = logging.FileHandler(
        log_dir / 'ventas_errores.log',
        encoding='utf-8'
    )
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(file_format)
    
    # Agregar handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    
    return logger
```

### Sistema Completo

```python
def procesar_sistema_completo():
    """Sistema completo de procesamiento."""
    # Configurar logging
    logger = configurar_logging()
    logger.info("="*60)
    logger.info("INICIANDO SISTEMA DE PROCESAMIENTO DE VENTAS")
    logger.info("="*60)
    
    try:
        # 1. Leer CSV
        archivo_csv = Path("ventas.csv")
        ventas, errores = leer_ventas_csv(archivo_csv)
        
        if errores:
            logger.warning(f"Se encontraron {len(errores)} ventas con errores")
        
        if not ventas:
            logger.critical("No hay ventas válidas para procesar")
            return
        
        # 2. Analizar ventas
        logger.info("Iniciando análisis de ventas")
        analizador = AnalizadorVentas(ventas)
        analizar_ventas(ventas)
        
        # 3. Exportar a JSON
        archivo_json = Path("reporte_ventas.json")
        exportar_reporte_json(ventas, analizador, archivo_json)
        
        # 4. Resumen final
        logger.info("="*60)
        logger.info("PROCESAMIENTO COMPLETADO EXITOSAMENTE")
        logger.info(f"  - Ventas procesadas: {len(ventas)}")
        logger.info(f"  - Total ventas: ${analizador.total_ventas():,.2f}")
        logger.info(f"  - Reporte generado: {archivo_json}")
        logger.info("="*60)
        
        print(f"\n✅ Proceso completado")
        print(f"📄 Reporte JSON: {archivo_json}")
        print(f"📋 Logs detallados: logs/ventas_detallado.log")
        print(f"⚠️  Logs de errores: logs/ventas_errores.log")
    
    except Exception as e:
        logger.exception(f"Error crítico en el sistema: {e}")
        raise


if __name__ == "__main__":
    procesar_sistema_completo()
```

---

## Criterios de Evaluación

### Ejercicio 1: Ingesta CSV (25 puntos)
- [ ] Modelo Pydantic con validación (5 pts)
- [ ] Lectura CSV con DictReader (5 pts)
- [ ] Manejo de errores de validación (5 pts)
- [ ] Logging apropiado (DEBUG/INFO/ERROR) (5 pts)
- [ ] Separación de válidas/inválidas (5 pts)

### Ejercicio 2: Métricas (25 puntos)
- [ ] Cálculo de totales y promedios (5 pts)
- [ ] Agrupación por producto/región/vendedor (10 pts)
- [ ] Top N productos (5 pts)
- [ ] Logging en cada cálculo (5 pts)

### Ejercicio 3: Exportación JSON (20 puntos)
- [ ] Estructura JSON completa (10 pts)
- [ ] Serialización correcta de tipos (5 pts)
- [ ] Metadata incluida (5 pts)

### Ejercicio 4: Sistema Completo (30 puntos)
- [ ] Configuración logging multinivel (10 pts)
- [ ] Integración de todos los componentes (10 pts)
- [ ] Manejo de excepciones (5 pts)
- [ ] Logs en archivos separados (5 pts)

---

## Entrega

**Archivos requeridos:**
1. `ventas.csv` - Datos de entrada
2. `procesar_ventas.py`- Script principal
3. `reporte_ventas.json` - Reporte generado
4. `logs/ventas_detallado.log` - Log detallado
5. `logs/ventas_errores.log` - Log de errores

**Ejecutar:**
```bash
python procesar_ventas.py
```

**Salida esperada:**
```
INFO     - Iniciando lectura de ventas.csv
ERROR    - Línea 7: Error al procesar - cantidad debe ser entero
INFO     - Lectura completada: 9 válidas, 1 con errores
...
✅ Proceso completado
📄 Reporte JSON: reporte_ventas.json
📋 Logs detallados: logs/ventas_detallado.log
⚠️  Logs de errores: logs/ventas_errores.log
```

---

## Bonus (Opcional)

1. **Gráficos** ⭐: Generar gráficos con matplotlib
2. **Dashboard HTML** ⭐⭐: Exportar HTML con resumen visual
3. **Streaming** ⭐⭐⭐: Procesar CSV muy grandes en chunks
4. **Alertas** ⭐⭐: Enviar email si errores > umbral
5. **CLI** ⭐⭐⭐: Interfaz de línea de comandos con argparse
