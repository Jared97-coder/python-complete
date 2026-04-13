"""
Módulo 6.4: Logging y Configuración
====================================

Sistema completo de logging para aplicaciones Python profesionales.
Incluye configuración, handlers, formatters y best practices.

Temas:
- Niveles de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Loggers, Handlers, Formatters
- Logging a archivo y consola
- Rotating file handlers
- JSON structured logging
- Configuración desde archivos
"""

import logging
import logging.config
from logging.handlers import (
    RotatingFileHandler,
    TimedRotatingFileHandler
)
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any


# =============================================================================
# 1. Logging Básico
# =============================================================================

def ejemplo_logging_basico():
    """Ejemplo básico de logging."""
    print("=== Logging Básico ===\n")
    
    # Configuración más simple
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s"
    )
    
    # Diferentes niveles de logging
    logging.debug("Mensaje de debug (no se verá con level=INFO)")
    logging.info("Mensaje informativo")
    logging.warning("Mensaje de advertencia")
    logging.error("Mensaje de error")
    logging.critical("Mensaje crítico")


def ejemplo_niveles_logging():
    """Niveles de logging y cuándo usarlos."""
    print("\n=== Niveles de Logging ===\n")
    
    logging.basicConfig(
        level=logging.DEBUG,  # Mostrar todos los niveles
        format="%(levelname)-8s - %(message)s"
    )
    
    print("Niveles de logging (menor a mayor severidad):\n")
    
    logging.debug("DEBUG: Información detallada para diagnóstico")
    logging.info("INFO: Confirmación de que todo funciona")
    logging.warning("WARNING: Algo inesperado, pero la app sigue funcionando")
    logging.error("ERROR: Error grave, alguna funcionalidad no funciona")
    logging.critical("CRITICAL: Error muy grave, la app puede detenerse")
    
    print("\nNiveles numéricos:")
    print(f"  DEBUG: {logging.DEBUG}")
    print(f"  INFO: {logging.INFO}")
    print(f"  WARNING: {logging.WARNING}")
    print(f"  ERROR: {logging.ERROR}")
    print(f"  CRITICAL: {logging.CRITICAL}")


# =============================================================================
# 2. Configuración Avanzada
# =============================================================================

def ejemplo_logging_configurado():
    """Configuración avanzada de logging."""
    print("\n=== Logging Configurado ===\n")
    
    # Configuración completa
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler()  # Consola
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    logger.debug("Mensaje de debug")
    logger.info("Mensaje informativo")
    logger.warning("Mensaje de advertencia")
    logger.error("Mensaje de error")


def ejemplo_logger_custom():
    """Crear logger personalizado."""
    print("\n=== Logger Personalizado ===\n")
    
    # Crear logger
    logger = logging.getLogger("mi_app")
    logger.setLevel(logging.DEBUG)
    
    # Crear handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Crear formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
        datefmt="%H:%M:%S"
    )
    
    # Asociar formatter con handler
    console_handler.setFormatter(formatter)
    
    # Agregar handler al logger
    logger.addHandler(console_handler)
    
    # Usar el logger
    logger.debug("Debug (no se verá)")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")


# =============================================================================
# 3. Logging a Archivos
# =============================================================================

def ejemplo_logging_archivo():
    """Logging a archivo."""
    print("\n=== Logging a Archivo ===\n")
    
    # Crear directorio para logs
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configurar logger
    logger = logging.getLogger("app_archivo")
    logger.setLevel(logging.DEBUG)
    
    # Handler para archivo
    file_handler = logging.FileHandler(
        log_dir / "app.log",
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Agregar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Generar logs
    logger.debug("Este mensaje solo va al archivo")
    logger.info("Este va a ambos: archivo y consola")
    logger.error("Error registrado en ambos lugares")
    
    print(f"\nLogs guardados en: {log_dir / 'app.log'}")


def ejemplo_rotating_file_handler():
    """Rotating file handler - archivos con rotación por tamaño."""
    print("\n=== Rotating File Handler ===\n")
    
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Crear logger
    logger = logging.getLogger("app_rotating")
    logger.setLevel(logging.DEBUG)
    
    # Rotating handler - rota cuando el archivo llega a 1KB
    rotating_handler = RotatingFileHandler(
        log_dir / "app_rotating.log",
        maxBytes=1024,  # 1KB
        backupCount=5,  # Mantener 5 backups
        encoding="utf-8"
    )
    
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    rotating_handler.setFormatter(formatter)
    
    logger.addHandler(rotating_handler)
    
    # Generar muchos logs para forzar rotación
    for i in range(100):
        logger.info(f"Mensaje de log número {i} " + "x" * 50)
    
    print(f"\nArchivos de log rotados en: {log_dir}")
    print("Archivos creados:")
    for archivo in sorted(log_dir.glob("app_rotating.log*")):
        tamano = archivo.stat().st_size
        print(f"  {archivo.name}: {tamano} bytes")


def ejemplo_timed_rotating_handler():
    """Rotating por tiempo - nuevo archivo cada día/hora."""
    print("\n=== Timed Rotating Handler ===\n")
    
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Crear logger
    logger = logging.getLogger("app_timed")
    logger.setLevel(logging.INFO)
    
    # Rotar cada día a medianoche
    timed_handler = TimedRotatingFileHandler(
        log_dir / "app_daily.log",
        when="midnight",  # 'S', 'M', 'H', 'D', 'W0'-'W6', 'midnight'
        interval=1,
        backupCount=7,  # Mantener 7 días
        encoding="utf-8"
    )
    
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    timed_handler.setFormatter(formatter)
    
    logger.addHandler(timed_handler)
    
    # Generar logs
    logger.info("Log con rotación por tiempo")
    logger.info("Se creará nuevo archivo cada día a medianoche")
    
    print(f"\nLogs con rotación temporal en: {log_dir}")


# =============================================================================
# 4. Formateo Avanzado
# =============================================================================

def ejemplo_formato_custom():
    """Formatos personalizados de logging."""
    print("\n=== Formatos Personalizados ===\n")
    
    # Logger con múltiples formatos
    logger = logging.getLogger("app_formatos")
    logger.setLevel(logging.DEBUG)
    
    # Formato simple para consola
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        fmt="[%(levelname)s] %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    
    # Formato detallado para archivo
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_dir / "detailed.log", encoding="utf-8")
    file_formatter = logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)-8s | "
            "%(filename)s:%(lineno)d | %(funcName)s() | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # Generar logs
    logger.info("Formato simple en consola, detallado en archivo")
    logger.warning("Los dos handlers usan formatos diferentes")
    
    print(f"\nLogs detallados en: {log_dir / 'detailed.log'}")


class JSONFormatter(logging.Formatter):
    """Formatter personalizado para generar logs en JSON."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Formatea el log como JSON."""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Agregar exc_info si existe
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)


def ejemplo_json_logging():
    """Logging estructurado en formato JSON."""
    print("\n=== JSON Structured Logging ===\n")
    
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Crear logger
    logger = logging.getLogger("app_json")
    logger.setLevel(logging.DEBUG)
    
    # Handler con JSON formatter
    json_handler = logging.FileHandler(
        log_dir / "app.json.log",
        encoding="utf-8"
    )
    json_handler.setFormatter(JSONFormatter())
    
    logger.addHandler(json_handler)
    
    # Generar logs
    logger.info("Usuario autenticado correctamente")
    logger.warning("Intento de acceso no autorizado")
    logger.error("Error al conectar con la base de datos")
    
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("Error de división por cero")
    
    print(f"\nLogs JSON en: {log_dir / 'app.json.log'}")
    print("\nEjemplo de log JSON:")
    
    # Leer y mostrar último log
    logs = (log_dir / "app.json.log").read_text(encoding="utf-8").strip().split("\n")
    if logs:
        ultimo_log = json.loads(logs[-1])
        print(json.dumps(ultimo_log, indent=2, ensure_ascii=False))


# =============================================================================
# 5. Logging con Contexto
# =============================================================================

def ejemplo_logging_con_extra():
    """Agregar información de contexto a los logs."""
    print("\n=== Logging con Contexto ===\n")
    
    # Configurar logger
    logger = logging.getLogger("app_contexto")
    logger.setLevel(logging.INFO)
    
    # Handler con formato que incluye campos extra
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - [user=%(user_id)s] - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Logs con información de contexto
    logger.info("Usuario inició sesión", extra={"user_id": 123})
    logger.info("Compra realizada", extra={"user_id": 123})
    logger.error("Error al procesar pago", extra={"user_id": 123})


class ContextFilter(logging.Filter):
    """Filtro para agregar información de contexto automáticamente."""
    
    def __init__(self, context: Dict[str, Any]):
        super().__init__()
        self.context = context
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Agrega contexto al record."""
        for key, value in self.context.items():
            setattr(record, key, value)
        return True


def ejemplo_context_filter():
    """Usar filtros para agregar contexto automáticamente."""
    print("\n=== Context Filter ===\n")
    
    logger = logging.getLogger("app_filter")
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - [%(request_id)s] - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S"
    )
    handler.setFormatter(formatter)
    
    # Agregar filtro con contexto
    context = {"request_id": "req-12345"}
    handler.addFilter(ContextFilter(context))
    
    logger.addHandler(handler)
    
    # Todos los logs tendrán el request_id automáticamente
    logger.info("Procesando solicitud")
    logger.info("Consultando base de datos")
    logger.info("Enviando respuesta")


# =============================================================================
# 6. Configuración desde Archivo
# =============================================================================

def ejemplo_config_desde_dict():
    """Configurar logging desde diccionario."""
    print("\n=== Configuración desde Diccionario ===\n")
    
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(levelname)s - %(message)s"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": "logs/app_config.log",
                "encoding": "utf-8"
            }
        },
        "loggers": {
            "mi_app": {
                "level": "DEBUG",
                "handlers": ["console", "file"],
                "propagate": False
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"]
        }
    }
    
    # Aplicar configuración
    logging.config.dictConfig(config)
    
    # Usar logger
    logger = logging.getLogger("mi_app")
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    
    print("\nLogger configurado desde diccionario")


def ejemplo_config_desde_archivo():
    """Configurar logging desde archivo YAML."""
    print("\n=== Configuración desde Archivo ===\n")
    
    # Crear archivo de configuración
    config_yaml = """
version: 1
disable_existing_loggers: false

formatters:
  simple:
    format: '%(levelname)s - %(message)s'
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: simple
    stream: ext://sys.stdout
  
  file:
    class: logging.FileHandler
    level: DEBUG
    formatter: detailed
    filename: logs/from_config.log
    encoding: utf-8

loggers:
  app:
    level: DEBUG
    handlers: [console, file]
    propagate: false

root:
  level: INFO
  handlers: [console]
"""
    
    # Guardar configuración
    config_file = Path("logging_config.yaml")
    config_file.write_text(config_yaml, encoding="utf-8")
    
    # Cargar y aplicar configuración
    import yaml
    with config_file.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    logging.config.dictConfig(config)
    
    # Usar logger
    logger = logging.getLogger("app")
    logger.debug("Debug desde config YAML")
    logger.info("Info desde config YAML")
    logger.warning("Warning desde config YAML")
    
    print(f"\nLogger configurado desde: {config_file}")
    
    # Limpiar
    config_file.unlink()


# =============================================================================
# 7. Mejores Prácticas
# =============================================================================

def ejemplo_mejores_practicas():
    """Mejores prácticas de logging."""
    print("\n=== Mejores Prácticas ===\n")
    
    # ✅ BUENO: Usar logger por módulo
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    
    # ✅ BUENO: Lazy formatting
    user_id = 123
    logger.info("Usuario %s inició sesión", user_id)
    
    # ❌ MALO: Formateo anticipado
    # logger.info(f"Usuario {user_id} inició sesión")  # Se evalúa siempre
    
    # ✅ BUENO: Usar niveles apropiados
    logger.debug("Información de depuración detallada")
    logger.info("Evento normal del sistema")
    logger.warning("Algo inusual, pero no crítico")
    logger.error("Error que impide alguna funcionalidad")
    logger.critical("Error crítico que puede detener la app")
    
    # ✅ BUENO: Usar exception() para errores con traceback
    try:
        resultado = 10 / 0
    except ZeroDivisionError:
        logger.exception("Error al calcular resultado")
    
    # ✅ BUENO: Agregar contexto útil
    logger.info(
        "Procesando pedido",
        extra={"order_id": "ORD-123", "user_id": 456}
    )
    
    print("\n✅ Mejores prácticas de logging aplicadas")


# =============================================================================
# 8. Ejemplo Completo: Aplicación con Logging
# =============================================================================

class MiAplicacion:
    """Aplicación ejemplo con logging completo."""
    
    def __init__(self):
        """Inicializa la aplicación y configura logging."""
        self._configurar_logging()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Aplicación inicializada")
    
    def _configurar_logging(self):
        """Configura el sistema de logging."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "console": {
                    "format": "%(levelname)-8s - %(message)s"
                },
                "file": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "formatter": "console"
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "file",
                    "filename": str(log_dir / "app.log"),
                    "maxBytes": 1048576,  # 1MB
                    "backupCount": 5,
                    "encoding": "utf-8"
                }
            },
            "root": {
                "level": "DEBUG",
                "handlers": ["console", "file"]
            }
        }
        
        logging.config.dictConfig(config)
    
    def procesar_datos(self, datos: list):
        """Procesa datos con logging en cada paso."""
        self.logger.info(f"Iniciando procesamiento de {len(datos)} registros")
        
        procesados = 0
        errores = 0
        
        for i, dato in enumerate(datos):
            try:
                self.logger.debug(f"Procesando registro {i+1}/{len(datos)}")
                # Simular procesamiento
                if dato < 0:
                    raise ValueError("Valor negativo no permitido")
                procesados += 1
            except ValueError as e:
                self.logger.error(f"Error en registro {i+1}: {e}")
                errores += 1
        
        self.logger.info(
            f"Procesamiento completado: {procesados} exitosos, {errores} errores"
        )
        
        return procesados, errores


def ejemplo_aplicacion_completa():
    """Ejemplo de aplicación con logging completo."""
    print("\n=== Aplicación con Logging Completo ===\n")
    
    app = MiAplicacion()
    
    datos = [10, 20, -5, 30, 40, -10, 50]
    exitosos, errores = app.procesar_datos(datos)
    
    print(f"\nResultado: {exitosos} exitosos, {errores} errores")
    print(f"Ver logs en: logs/app.log")


# =============================================================================
# Main
# =============================================================================

def main():
    """Ejecuta todos los ejemplos."""
    # Limpiar configuración previa
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    ejemplos = [
        ejemplo_logging_basico,
        ejemplo_niveles_logging,
        ejemplo_logging_configurado,
        ejemplo_logger_custom,
        ejemplo_logging_archivo,
        ejemplo_rotating_file_handler,
        ejemplo_timed_rotating_handler,
        ejemplo_formato_custom,
        ejemplo_json_logging,
        ejemplo_logging_con_extra,
        ejemplo_context_filter,
        ejemplo_config_desde_dict,
        ejemplo_config_desde_archivo,
        ejemplo_mejores_practicas,
        ejemplo_aplicacion_completa,
    ]
    
    for ejemplo in ejemplos:
        try:
            # Limpiar handlers antes de cada ejemplo
            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)
            
            ejemplo()
        except Exception as e:
            print(f"❌ Error en {ejemplo.__name__}: {e}")
        print("\n" + "="*70)


if __name__ == "__main__":
    main()
