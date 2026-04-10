# 📝 Ejercicios Prácticos - Módulo 1: Entorno y Herramientas

## 🎯 Objetivo
Poner en práctica los conocimientos adquiridos sobre configuración de entorno, gestión de paquetes y mejores prácticas.

---

## Ejercicio 1: Verificación de Instalación ⭐
**Dificultad: Básica**

### Objetivos
- Verificar que Python está correctamente instalado
- Conocer las rutas y configuraciones del sistema
- Ejecutar tu primer script

### Tareas
1. Abre PowerShell o Terminal
2. Verifica la versión de Python: `python --version`
3. Verifica la versión de pip: `pip --version`
4. Encuentra la ubicación de Python: `where python`
5. Ejecuta el script `01_verificar_instalacion.py`

### Comandos
```powershell
# Navegar al directorio del módulo
cd "c:\Users\jared.trejo\Documents\GitHub\Axity\Python\Modulo_01_Entorno_y_Herramientas"

# Ejecutar el script
python 01_verificar_instalacion.py
```

### Preguntas de Reflexión
- ¿Qué versión de Python tienes instalada?
- ¿Dónde está ubicado el ejecutable de Python?
- ¿Cuántas rutas hay en tu sys.path?

---

## Ejercicio 2: Crear tu Primer Entorno Virtual ⭐⭐
**Dificultad: Básica-Intermedia**

### Objetivos
- Crear y activar un entorno virtual
- Instalar paquetes en el entorno
- Generar archivo requirements.txt

### Tareas

#### Paso 1: Crear el proyecto
```powershell
# Crear directorio
mkdir mi_primer_proyecto
cd mi_primer_proyecto

# Crear entorno virtual
python -m venv venv
```

#### Paso 2: Activar el entorno
```powershell
# PowerShell
venv\Scripts\Activate.ps1

# CMD
venv\Scripts\activate.bat

# Verificar activación
where python  # Debe apuntar a venv\Scripts\python.exe
```

#### Paso 3: Instalar paquetes
```powershell
# Actualizar pip
python -m pip install --upgrade pip

# Instalar paquetes útiles
pip install requests
pip install beautifulsoup4
pip install python-dotenv

# Ver paquetes instalados
pip list
```

#### Paso 4: Guardar dependencias
```powershell
# Generar requirements.txt
pip freeze > requirements.txt

# Ver el contenido
type requirements.txt
```

#### Paso 5: Crear .gitignore
```powershell
# Crear archivo .gitignore
echo "venv/" > .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".env" >> .gitignore
```

### Desafío Extra
Crea un script simple que use `requests` para hacer una petición HTTP y muestre el resultado.

### Entregable
- Captura de pantalla mostrando el entorno activado
- Archivo `requirements.txt` generado
- Archivo `.gitignore` creado

---

## Ejercicio 3: Gestión de Paquetes ⭐⭐
**Dificultad: Intermedia**

### Objetivos
- Explorar comandos de pip
- Gestionar versiones de paquetes
- Resolver conflictos de dependencias

### Tareas

#### Parte A: Exploración
```powershell
# Activar entorno del Ejercicio 2
cd mi_primer_proyecto
venv\Scripts\Activate.ps1

# Instalar versión específica
pip install numpy==1.24.0

# Ver información del paquete
pip show numpy

# Ver paquetes desactualizados
pip list --outdated

# Actualizar un paquete
pip install --upgrade numpy
```

#### Parte B: Experimentación
1. Instala `pandas` (observa que instalará dependencias automáticamente)
2. Usa `pip show pandas` para ver sus dependencias
3. Intenta instalar dos paquetes con versiones conflictivas (documenta el error)

#### Parte C: Script de gestión
Ejecuta el script `02_gestionar_paquetes.py` y analiza su salida:

```powershell
python ..\Modulo_01_Entorno_y_Herramientas\02_gestionar_paquetes.py
```

### Preguntas de Reflexión
- ¿Qué paquetes se instalaron como dependencias de pandas?
- ¿Por qué es importante especificar versiones exactas?
- ¿Cuál es la diferencia entre `pip list` y `pip freeze`?

---

## Ejercicio 4: Variables de Entorno ⭐⭐⭐
**Dificultad: Intermedia-Avanzada**

### Objetivos
- Trabajar con variables de entorno
- Usar archivos .env
- Implementar configuración segura

### Tareas

#### Paso 1: Instalar python-dotenv
```powershell
pip install python-dotenv
```

#### Paso 2: Crear archivo .env
Crea un archivo `.env` en tu proyecto con este contenido:

```env
# .env
APP_NAME=MiAplicacion
DEBUG=True
SECRET_KEY=mi_clave_super_secreta_123
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=abc123xyz789
```

#### Paso 3: Crear script de prueba
Crea un archivo `config.py`:

```python
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Configuración
class Config:
    APP_NAME = os.getenv('APP_NAME', 'App')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    API_KEY = os.getenv('API_KEY')
    
    @classmethod
    def display(cls):
        print("=" * 60)
        print("CONFIGURACIÓN DE LA APLICACIÓN")
        print("=" * 60)
        print(f"Nombre: {cls.APP_NAME}")
        print(f"Debug: {cls.DEBUG}")
        print(f"Secret Key: {cls.SECRET_KEY[:10]}... (oculta)")
        print(f"Database: {cls.DATABASE_URL}")
        print(f"API Key: {cls.API_KEY[:5]}... (oculta)")
        print("=" * 60)

if __name__ == "__main__":
    Config.display()
```

#### Paso 4: Ejecutar y probar
```powershell
python config.py
```

#### Paso 5: Crear .env.example
Crea un archivo `.env.example` sin valores sensibles:

```env
APP_NAME=
DEBUG=
SECRET_KEY=
DATABASE_URL=
API_KEY=
```

### Desafío Extra
1. Modifica el script para validar que todas las variables requeridas están presentes
2. Agrega soporte para diferentes entornos (development, production, testing)

### Entregable
- Archivo `config.py` funcionando
- Archivo `.env.example` (sin valores reales)
- Captura de pantalla de la ejecución

---

## Ejercicio 5: Proyecto Completo ⭐⭐⭐
**Dificultad: Avanzada**

### Objetivos
- Integrar todos los conocimientos del módulo
- Crear un proyecto con estructura profesional
- Implementar mejores prácticas

### Descripción
Crea una aplicación de gestión de tareas simple que:
- Use entorno virtual
- Gestione configuración con variables de entorno
- Almacene datos en un archivo JSON
- Tenga una interfaz de línea de comandos

### Estructura del Proyecto
```
gestor_tareas/
│
├── venv/                   # Entorno virtual
├── src/                    # Código fuente
│   ├── __init__.py
│   ├── config.py          # Configuración
│   ├── task_manager.py    # Lógica principal
│   └── cli.py             # Interfaz de línea de comandos
│
├── data/                   # Datos
│   └── tasks.json
│
├── tests/                  # Tests (opcional)
│   └── test_task_manager.py
│
├── .env                    # Variables de entorno (no versionar)
├── .env.example           # Ejemplo de variables
├── .gitignore             # Ignorar archivos
├── requirements.txt       # Dependencias
└── README.md              # Documentación
```

### Tareas

#### 1. Configuración Inicial
```powershell
# Crear estructura
mkdir gestor_tareas
cd gestor_tareas

mkdir src
mkdir data
mkdir tests

# Crear entorno virtual
python -m venv venv
venv\Scripts\Activate.ps1

# Instalar dependencias
pip install python-dotenv
pip freeze > requirements.txt
```

#### 2. Crear archivos de configuración

**src/config.py**
```python
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    APP_NAME = os.getenv('APP_NAME', 'Gestor de Tareas')
    DATA_DIR = Path(os.getenv('DATA_DIR', 'data'))
    TASKS_FILE = DATA_DIR / 'tasks.json'
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

**src/task_manager.py**
```python
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class TaskManager:
    def __init__(self, tasks_file: Path):
        self.tasks_file = tasks_file
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> List[Dict]:
        """Carga las tareas desde el archivo JSON."""
        if not self.tasks_file.exists():
            return []
        
        with open(self.tasks_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_tasks(self):
        """Guarda las tareas en el archivo JSON."""
        self.tasks_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)
    
    def add_task(self, title: str, description: str = "") -> Dict:
        """Agrega una nueva tarea."""
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'completed': False,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        self.tasks.append(task)
        self._save_tasks()
        return task
    
    def list_tasks(self, completed: Optional[bool] = None) -> List[Dict]:
        """Lista las tareas (opcionalmente filtradas por estado)."""
        if completed is None:
            return self.tasks
        return [t for t in self.tasks if t['completed'] == completed]
    
    def complete_task(self, task_id: int) -> Optional[Dict]:
        """Marca una tarea como completada."""
        task = self.get_task(task_id)
        if task:
            task['completed'] = True
            task['updated_at'] = datetime.now().isoformat()
            self._save_tasks()
        return task
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """Obtiene una tarea por su ID."""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def delete_task(self, task_id: int) -> bool:
        """Elimina una tarea."""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self._save_tasks()
            return True
        return False
```

**src/cli.py**
```python
from task_manager import TaskManager
from config import Config

def display_menu():
    print("\n" + "=" * 60)
    print(f"{Config.APP_NAME:^60}")
    print("=" * 60)
    print("1. Agregar tarea")
    print("2. Listar todas las tareas")
    print("3. Listar tareas pendientes")
    print("4. Listar tareas completadas")
    print("5. Completar tarea")
    print("6. Eliminar tarea")
    print("7. Salir")
    print("=" * 60)

def main():
    manager = TaskManager(Config.TASKS_FILE)
    
    while True:
        display_menu()
        choice = input("\nSelecciona una opción (1-7): ").strip()
        
        if choice == '1':
            title = input("Título de la tarea: ")
            description = input("Descripción (opcional): ")
            task = manager.add_task(title, description)
            print(f"✅ Tarea #{task['id']} creada: {task['title']}")
        
        elif choice == '2':
            tasks = manager.list_tasks()
            print_tasks(tasks, "TODAS LAS TAREAS")
        
        elif choice == '3':
            tasks = manager.list_tasks(completed=False)
            print_tasks(tasks, "TAREAS PENDIENTES")
        
        elif choice == '4':
            tasks = manager.list_tasks(completed=True)
            print_tasks(tasks, "TAREAS COMPLETADAS")
        
        elif choice == '5':
            task_id = int(input("ID de la tarea a completar: "))
            task = manager.complete_task(task_id)
            if task:
                print(f"✅ Tarea #{task_id} completada")
            else:
                print(f"❌ Tarea #{task_id} no encontrada")
        
        elif choice == '6':
            task_id = int(input("ID de la tarea a eliminar: "))
            if manager.delete_task(task_id):
                print(f"✅ Tarea #{task_id} eliminada")
            else:
                print(f"❌ Tarea #{task_id} no encontrada")
        
        elif choice == '7':
            print("\n👋 ¡Hasta pronto!")
            break
        
        else:
            print("⚠️  Opción no válida")

def print_tasks(tasks, title):
    print("\n" + "=" * 60)
    print(f"{title:^60}")
    print("=" * 60)
    
    if not tasks:
        print("No hay tareas.")
    else:
        for task in tasks:
            status = "✅" if task['completed'] else "⏳"
            print(f"{status} #{task['id']}: {task['title']}")
            if task['description']:
                print(f"   Descripción: {task['description']}")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
```

#### 3. Crear archivos de soporte

**.env**
```env
APP_NAME=Gestor de Tareas
DATA_DIR=data
DEBUG=True
```

**.gitignore**
```
venv/
*.pyc
__pycache__/
.env
data/*.json
```

**README.md**
```markdown
# Gestor de Tareas

Aplicación simple de línea de comandos para gestionar tareas.

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno: `venv\Scripts\activate`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Copiar `.env.example` a `.env` y configurar

## Uso

```bash
python src/cli.py
```

## Características

- Agregar tareas
- Listar tareas (todas, pendientes, completadas)
- Completar tareas
- Eliminar tareas
- Persistencia en JSON
```

### Criterios de Evaluación
- ✅ Proyecto usa entorno virtual
- ✅ Tiene archivo .gitignore apropiado
- ✅ Usa variables de entorno para configuración
- ✅ Tiene requirements.txt
- ✅ La aplicación funciona correctamente
- ✅ El código está bien documentado
- ✅ Estructura de proyecto es clara

---

## 🎓 Evaluación Final

### Checklist de Conocimientos

Marca cada ítem cuando lo hayas dominado:

**Instalación y Configuración**
- [ ] Puedo verificar la versión de Python instalada
- [ ] Entiendo dónde está instalado Python en mi sistema
- [ ] Sé cómo configurar variables de entorno en Windows

**Entornos Virtuales**
- [ ] Puedo crear un entorno virtual
- [ ] Sé activar y desactivar entornos virtuales
- [ ] Entiendo por qué son importantes los entornos virtuales
- [ ] Puedo verificar si estoy en un entorno virtual

**Gestión de Paquetes**
- [ ] Puedo instalar paquetes con pip
- [ ] Sé cómo especificar versiones de paquetes
- [ ] Puedo crear y usar requirements.txt
- [ ] Entiendo cómo ver información de paquetes instalados

**Variables de Entorno**
- [ ] Sé cómo leer variables de entorno en Python
- [ ] Puedo usar archivos .env con python-dotenv
- [ ] Entiendo qué información debe ir en .env
- [ ] Sé cómo proteger información sensible

**Mejores Prácticas**
- [ ] Sé crear un .gitignore apropiado
- [ ] Puedo estructurar un proyecto Python básico
- [ ] Entiendo la importancia de la documentación
- [ ] Puedo escribir código limpio y comentado

---

## 📚 Recursos Adicionales

### Lecturas Recomendadas
- [Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/)
- [pip Documentation](https://pip.pypa.io/en/stable/)
- [Python .gitignore Template](https://github.com/github/gitignore/blob/main/Python.gitignore)

### Videos
- Tutorial de entornos virtuales
- Gestión de dependencias con pip
- Buenas prácticas en proyectos Python

### Ejercicios Adicionales
1. Crea un proyecto que use APIs externas (ej: weather, exchange rates)
2. Implementa un CLI más complejo con argparse
3. Crea un script de automatización para tareas repetitivas

---

*¡Felicitaciones por completar el Módulo 1!*
