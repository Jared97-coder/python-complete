"""
Módulo 6.3: datetime y Zonas Horarias
======================================

Trabajo completo con fechas, horas y zonas horarias en Python.
Incluye parsing, formateo, aritmética y manejo de timezones.

Temas:
- datetime, date, time, timedelta
- Parsing y formateo (strptime/strftime)
- Zonas horarias con zoneinfo (Python 3.9+)
- Timestamps Unix
- Aritmética de fechas
- Librerías alternativas (pendulum, arrow)
"""

from datetime import (
    datetime,
    date,
    time,
    timedelta,
    timezone
)
from zoneinfo import ZoneInfo
from typing import Optional
import time as time_module
import calendar


# =============================================================================
# 1. Fundamentos de datetime
# =============================================================================

def ejemplo_datetime_basico():
    """Tipos básicos de fecha y hora."""
    print("=== datetime Básico ===\n")
    
    # Fecha actual
    hoy = date.today()
    print(f"Fecha hoy: {hoy}")
    print(f"Año: {hoy.year}, Mes: {hoy.month}, Día: {hoy.day}")
    
    # Hora actual
    ahora = datetime.now()
    print(f"\nDatetime ahora: {ahora}")
    print(f"Hora: {ahora.hour}:{ahora.minute}:{ahora.second}")
    
    # Crear fecha específica
    navidad = date(2024, 12, 25)
    print(f"\nNavidad 2024: {navidad}")
    
    # Crear datetime específico
    reunion = datetime(2024, 6, 15, 14, 30, 0)
    print(f"Reunión: {reunion}")
    
    # Solo hora
    hora_inicio = time(9, 30, 0)
    print(f"\nHora de inicio: {hora_inicio}")


def ejemplo_datetime_componentes():
    """Acceder a componentes de fecha/hora."""
    print("\n=== Componentes datetime ===\n")
    
    ahora = datetime.now()
    
    print(f"Datetime: {ahora}")
    print(f"\nComponentes:")
    print(f"  Año: {ahora.year}")
    print(f"  Mes: {ahora.month}")
    print(f"  Día: {ahora.day}")
    print(f"  Hora: {ahora.hour}")
    print(f"  Minuto: {ahora.minute}")
    print(f"  Segundo: {ahora.second}")
    print(f"  Microsegundo: {ahora.microsecond}")
    
    # Día de la semana
    print(f"\nDía de la semana: {ahora.weekday()}")  # 0=Lunes, 6=Domingo
    print(f"Día de la semana (ISO): {ahora.isoweekday()}")  # 1=Lunes, 7=Domingo
    
    # Nombres de días y meses
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    print(f"Nombre del día: {dias[ahora.weekday()]}")


# =============================================================================
# 2. Parsing y Formateo de Fechas
# =============================================================================

def ejemplo_strptime_strftime():
    """Parsear strings a datetime y formatear datetime a strings."""
    print("\n=== strptime / strftime ===\n")
    
    # String → datetime (parsing)
    fecha_str = "2024-06-15 14:30:00"
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
    print(f"String: {fecha_str}")
    print(f"Parseado: {fecha}")
    
    # datetime → String (formateo)
    ahora = datetime.now()
    print(f"\nDatetime: {ahora}")
    print(f"Formato ISO: {ahora.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Formato legible: {ahora.strftime('%d/%m/%Y a las %H:%M')}")
    print(f"Formato largo: {ahora.strftime('%A, %d de %B de %Y')}")
    
    # Formatos comunes
    print("\nFormatos comunes:")
    print(f"  ISO 8601: {ahora.isoformat()}")
    print(f"  RFC 2822: {ahora.strftime('%a, %d %b %Y %H:%M:%S')}")
    print(f"  Solo fecha: {ahora.date()}")
    print(f"  Solo hora: {ahora.time()}")


def ejemplo_formatos_personalizados():
    """Ejemplos de formateo personalizado."""
    print("\n=== Formatos Personalizados ===\n")
    
    ahora = datetime.now()
    
    formatos = {
        "ISO 8601": "%Y-%m-%dT%H:%M:%S",
        "Fecha corta": "%d/%m/%Y",
        "Fecha larga": "%d de %B de %Y",
        "Hora 24h": "%H:%M:%S",
        "Hora 12h": "%I:%M:%S %p",
        "Timestamp legible": "%Y%m%d_%H%M%S",
        "Día de la semana": "%A",
        "Mes completo": "%B",
    }
    
    for nombre, formato in formatos.items():
        print(f"{nombre:20s}: {ahora.strftime(formato)}")


def ejemplo_parsear_diferentes_formatos():
    """Parsear fechas en diferentes formatos."""
    print("\n=== Parsear Diferentes Formatos ===\n")
    
    fechas = [
        ("2024-06-15", "%Y-%m-%d"),
        ("15/06/2024", "%d/%m/%Y"),
        ("Jun 15, 2024", "%b %d, %Y"),
        ("2024-06-15 14:30:00", "%Y-%m-%d %H:%M:%S"),
        ("15-06-2024 02:30 PM", "%d-%m-%Y %I:%M %p"),
    ]
    
    for fecha_str, formato in fechas:
        fecha = datetime.strptime(fecha_str, formato)
        print(f"{fecha_str:30s} → {fecha}")


# =============================================================================
# 3. Aritmética con Fechas
# =============================================================================

def ejemplo_timedelta():
    """Operaciones con timedelta."""
    print("\n=== timedelta ===\n")
    
    # Crear timedelta
    una_semana = timedelta(weeks=1)
    un_dia = timedelta(days=1)
    dos_horas = timedelta(hours=2)
    treinta_minutos = timedelta(minutes=30)
    
    print(f"Una semana: {una_semana}")
    print(f"Un día: {un_dia}")
    print(f"Dos horas: {dos_horas}")
    
    # Aritmética con fechas
    ahora = datetime.now()
    print(f"\nAhora: {ahora}")
    print(f"Mañana: {ahora + un_dia}")
    print(f"Ayer: {ahora - un_dia}")
    print(f"Próxima semana: {ahora + una_semana}")
    print(f"En 2 horas: {ahora + dos_horas}")
    
    # Diferencia entre fechas
    navidad = datetime(2024, 12, 25)
    diferencia = navidad - ahora
    print(f"\nDías hasta navidad: {diferencia.days}")
    print(f"Segundos hasta navidad: {diferencia.total_seconds():.0f}")


def ejemplo_calculos_fechas():
    """Cálculos comunes con fechas."""
    print("\n=== Cálculos con Fechas ===\n")
    
    # Edad en años
    fecha_nacimiento = date(1995, 6, 15)
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    
    print(f"Fecha nacimiento: {fecha_nacimiento}")
    print(f"Edad: {edad} años")
    
    # Primer día del mes
    primer_dia = hoy.replace(day=1)
    print(f"\nPrimer día del mes: {primer_dia}")
    
    # Último día del mes
    siguiente_mes = hoy.replace(day=28) + timedelta(days=4)
    ultimo_dia = siguiente_mes - timedelta(days=siguiente_mes.day)
    print(f"Último día del mes: {ultimo_dia}")
    
    # Número de días en el mes
    dias_en_mes = calendar.monthrange(hoy.year, hoy.month)[1]
    print(f"Días en el mes: {dias_en_mes}")


def ejemplo_fechas_relativas():
    """Fechas relativas (inicio/fin de periodo)."""
    print("\n=== Fechas Relativas ===\n")
    
    ahora = datetime.now()
    
    # Inicio del día
    inicio_dia = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
    print(f"Ahora: {ahora}")
    print(f"Inicio del día: {inicio_dia}")
    
    # Fin del día
    fin_dia = ahora.replace(hour=23, minute=59, second=59, microsecond=999999)
    print(f"Fin del día: {fin_dia}")
    
    # Hace una semana
    hace_semana = ahora - timedelta(weeks=1)
    print(f"\nHace una semana: {hace_semana}")
    
    # Hace 30 días
    hace_mes = ahora - timedelta(days=30)
    print(f"Hace 30 días: {hace_mes}")


# =============================================================================
# 4. Zonas Horarias
# =============================================================================

def ejemplo_timezone_basico():
    """Trabajo básico con zonas horarias."""
    print("\n=== Zonas Horarias Básicas ===\n")
    
    # datetime sin timezone (naive)
    ahora_naive = datetime.now()
    print(f"Naive datetime: {ahora_naive}")
    print(f"Timezone: {ahora_naive.tzinfo}")
    
    # datetime con timezone UTC
    ahora_utc = datetime.now(timezone.utc)
    print(f"\nUTC datetime: {ahora_utc}")
    print(f"Timezone: {ahora_utc.tzinfo}")
    
    # Convertir naive a aware (agregar timezone)
    ahora_aware = ahora_naive.replace(tzinfo=timezone.utc)
    print(f"\nNaive → Aware: {ahora_aware}")


def ejemplo_zoneinfo():
    """Trabajar con zonas horarias usando zoneinfo (Python 3.9+)."""
    print("\n=== zoneinfo ===\n")
    
    # Crear datetime en diferentes zonas horarias
    ahora_utc = datetime.now(timezone.utc)
    print(f"UTC: {ahora_utc}")
    
    # México
    tz_mexico = ZoneInfo("America/Mexico_City")
    ahora_mexico = ahora_utc.astimezone(tz_mexico)
    print(f"México: {ahora_mexico}")
    
    # España
    tz_madrid = ZoneInfo("Europe/Madrid")
    ahora_madrid = ahora_utc.astimezone(tz_madrid)
    print(f"Madrid: {ahora_madrid}")
    
    # Tokyo
    tz_tokyo = ZoneInfo("Asia/Tokyo")
    ahora_tokyo = ahora_utc.astimezone(tz_tokyo)
    print(f"Tokyo: {ahora_tokyo}")
    
    # Nueva York
    tz_ny = ZoneInfo("America/New_York")
    ahora_ny = ahora_utc.astimezone(tz_ny)
    print(f"New York: {ahora_ny}")


def ejemplo_conversion_timezones():
    """Convertir entre zonas horarias."""
    print("\n=== Conversión de Timezones ===\n")
    
    # Crear datetime en México
    tz_mexico = ZoneInfo("America/Mexico_City")
    reunion_mexico = datetime(2024, 6, 15, 14, 30, tzinfo=tz_mexico)
    
    print(f"Reunión en México: {reunion_mexico}")
    
    # Convertir a otras zonas horarias
    zonas = [
        ("UTC", timezone.utc),
        ("Madrid", ZoneInfo("Europe/Madrid")),
        ("New York", ZoneInfo("America/New_York")),
        ("Tokyo", ZoneInfo("Asia/Tokyo")),
    ]
    
    print("\n¿A qué hora es en otros lugares?")
    for nombre, tz in zonas:
        hora_local = reunion_mexico.astimezone(tz)
        print(f"  {nombre:10s}: {hora_local.strftime('%H:%M')}")


def ejemplo_timestamp():
    """Trabajar con timestamps Unix."""
    print("\n=== Timestamps Unix ===\n")
    
    # datetime → timestamp
    ahora = datetime.now(timezone.utc)
    timestamp = ahora.timestamp()
    
    print(f"Datetime: {ahora}")
    print(f"Timestamp: {timestamp}")
    
    # timestamp → datetime
    dt_desde_timestamp = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    print(f"Desde timestamp: {dt_desde_timestamp}")
    
    # Timestamp actual
    timestamp_actual = time_module.time()
    print(f"\nTimestamp actual: {timestamp_actual}")
    
    # Epochs conocidos
    epoch_unix = datetime(1970, 1, 1, tzinfo=timezone.utc)
    print(f"Epoch Unix: {epoch_unix}")
    print(f"Timestamp: {epoch_unix.timestamp()}")


# =============================================================================
# 5. Casos de Uso Comunes
# =============================================================================

def calcular_edad(fecha_nacimiento: date) -> int:
    """Calcula edad exacta en años."""
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    
    # Ajustar si aún no ha cumplido años este año
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    
    return edad


def ejemplo_calcular_edad():
    """Calcular edad a partir de fecha de nacimiento."""
    print("\n=== Calcular Edad ===\n")
    
    fechas_nacimiento = [
        date(1995, 3, 15),
        date(2000, 12, 25),
        date(1988, 7, 4),
    ]
    
    for fecha in fechas_nacimiento:
        edad = calcular_edad(fecha)
        print(f"Nacido {fecha}: {edad} años")


def es_dia_laboral(fecha: date) -> bool:
    """Verifica si una fecha es día laboral (lunes-viernes)."""
    return fecha.weekday() < 5  # 0-4 son lunes a viernes


def siguiente_dia_laboral(fecha: date) -> date:
    """Obtiene el siguiente día laboral."""
    siguiente = fecha + timedelta(days=1)
    while not es_dia_laboral(siguiente):
        siguiente += timedelta(days=1)
    return siguiente


def ejemplo_dias_laborales():
    """Trabajar con días laborales."""
    print("\n=== Días Laborales ===\n")
    
    hoy = date.today()
    print(f"Hoy: {hoy} ({'Laboral' if es_dia_laboral(hoy) else 'Fin de semana'})")
    
    siguiente = siguiente_dia_laboral(hoy)
    print(f"Siguiente día laboral: {siguiente}")
    
    # Contar días laborales en un rango
    inicio = date(2024, 6, 1)
    fin = date(2024, 6, 30)
    
    dias_laborales = 0
    fecha_actual = inicio
    while fecha_actual <= fin:
        if es_dia_laboral(fecha_actual):
            dias_laborales += 1
        fecha_actual += timedelta(days=1)
    
    print(f"\nDías laborales en junio 2024: {dias_laborales}")


def formatear_fecha_relativa(dt: datetime) -> str:
    """Formatea fecha en términos relativos (hace X tiempo)."""
    ahora = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    diferencia = ahora - dt
    segundos = diferencia.total_seconds()
    
    if segundos < 60:
        return "hace unos segundos"
    elif segundos < 3600:
        minutos = int(segundos / 60)
        return f"hace {minutos} minuto{'s' if minutos != 1 else ''}"
    elif segundos < 86400:
        horas = int(segundos / 3600)
        return f"hace {horas} hora{'s' if horas != 1 else ''}"
    elif segundos < 604800:
        dias = int(segundos / 86400)
        return f"hace {dias} día{'s' if dias != 1 else ''}"
    else:
        return dt.strftime("%d/%m/%Y")


def ejemplo_fechas_relativas_humanizadas():
    """Formatear fechas de forma relativa."""
    print("\n=== Fechas Relativas Humanizadas ===\n")
    
    ahora = datetime.now(timezone.utc)
    
    tiempos = [
        ahora - timedelta(seconds=30),
        ahora - timedelta(minutes=5),
        ahora - timedelta(hours=2),
        ahora - timedelta(days=1),
        ahora - timedelta(days=3),
        ahora - timedelta(weeks=2),
    ]
    
    for dt in tiempos:
        relativo = formatear_fecha_relativa(dt)
        print(f"{dt.strftime('%Y-%m-%d %H:%M:%S')} → {relativo}")


def generar_rango_fechas(
    inicio: date,
    fin: date
) -> list[date]:
    """Genera lista de fechas en un rango."""
    fechas = []
    fecha_actual = inicio
    while fecha_actual <= fin:
        fechas.append(fecha_actual)
        fecha_actual += timedelta(days=1)
    return fechas


def ejemplo_rango_fechas():
    """Generar rango de fechas."""
    print("\n=== Rango de Fechas ===\n")
    
    inicio = date(2024, 6, 1)
    fin = date(2024, 6, 7)
    
    print(f"Del {inicio} al {fin}:")
    for fecha in generar_rango_fechas(inicio, fin):
        dia_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"][fecha.weekday()]
        print(f"  {fecha} ({dia_semana})")


# =============================================================================
# 6. Mejores Prácticas
# =============================================================================

def ejemplo_mejores_practicas():
    """Ejemplos de mejores prácticas con datetime."""
    print("\n=== Mejores Prácticas ===\n")
    
    # ✅ BUENO: Siempre usar UTC para storage
    ahora_utc = datetime.now(timezone.utc)
    print(f"✅ UTC para storage: {ahora_utc}")
    
    # ❌ MALO: datetime naive (sin timezone)
    ahora_naive = datetime.now()
    print(f"❌ Naive (ambiguo): {ahora_naive}")
    
    # ✅ BUENO: Convertir a timezone local solo para display
    tz_local = ZoneInfo("America/Mexico_City")
    ahora_local = ahora_utc.astimezone(tz_local)
    print(f"✅ Local para display: {ahora_local}")
    
    # ✅ BUENO: Usar ISO format para serializar
    iso_string = ahora_utc.isoformat()
    print(f"\n✅ ISO format: {iso_string}")
    
    # ✅ BUENO: Parsear con timezone
    dt_parseado = datetime.fromisoformat(iso_string)
    print(f"✅ Parseado: {dt_parseado}")


# =============================================================================
# Main
# =============================================================================

def main():
    """Ejecuta todos los ejemplos."""
    ejemplos = [
        ejemplo_datetime_basico,
        ejemplo_datetime_componentes,
        ejemplo_strptime_strftime,
        ejemplo_formatos_personalizados,
        ejemplo_parsear_diferentes_formatos,
        ejemplo_timedelta,
        ejemplo_calculos_fechas,
        ejemplo_fechas_relativas,
        ejemplo_timezone_basico,
        ejemplo_zoneinfo,
        ejemplo_conversion_timezones,
        ejemplo_timestamp,
        ejemplo_calcular_edad,
        ejemplo_dias_laborales,
        ejemplo_fechas_relativas_humanizadas,
        ejemplo_rango_fechas,
        ejemplo_mejores_practicas,
    ]
    
    for ejemplo in ejemplos:
        try:
            ejemplo()
        except Exception as e:
            print(f"❌ Error en {ejemplo.__name__}: {e}")
        print("\n" + "="*70)


if __name__ == "__main__":
    main()
