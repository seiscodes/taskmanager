# Gestor de Tareas Inteligente

Un gestor de tareas moderno y potente que integra inteligencia artificial para desglosar tareas complejas en subtareas simples y manejables.

## Descripción del Proyecto

**TaskManager** es una aplicación de línea de comandos desarrollada en Python que permite gestionar tareas de forma eficiente. Su característica principal es la integración con la API de **Google Gemini**, que utiliza inteligencia artificial para analizar tareas complejas y convertirlas automáticamente en subtareas simples y accionables.

### Características Principales

- **Gestión completa de tareas**: Añadir, listar, completar y eliminar tareas
- **Integración con IA**: Desglose automático de tareas complejas usando Google Gemini
- **Persistencia de datos**: Almacenamiento en JSON para mantener las tareas entre sesiones
- **Interfaz intuitiva**: Menú interactivo fácil de usar
- **Suite de pruebas**: Tests unitarios completos con unittest
- **Visualización clara**: Representación visual de tareas completadas e incompletas

## Estructura del Proyecto

```
TaskManager/
├── main.py                 # Punto de entrada principal de la aplicación
├── task_manager.py         # Lógica central del gestor de tareas
├── ia_service.py           # Integración con Google Gemini API
├── task.json               # Almacenamiento de tareas (se crea automáticamente)
├── test_task_manager.py    # Suite de pruebas unitarias
├── requirements.txt        # Dependencias de Python
└── README.md              # Este archivo
```

## Tecnologías Utilizadas

- **Python 3.x**: Lenguaje de programación principal
- **JSON**: Formato de almacenamiento de datos
- **Google Gemini API**: Inteligencia artificial para desglose de tareas
- **unittest**: Framework para pruebas unitarias
- **python-dotenv**: Gestión de variables de entorno

## Instalación

### Requisitos Previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)
- Una clave API de Google Gemini

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd TaskManager
   ```

2. **Crear un entorno virtual**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la API de Gemini**
   - Obtener una clave API desde [Google AI Studio](https://ai.google.dev/)
   - Crear un archivo `.env` en la raíz del proyecto:
   ```env
   GEMINI_API_KEY=tu_clave_api_aqui
   ```

## Uso

### Ejecutar la Aplicación

```bash
python main.py
```

### Menú Principal

Una vez iniciada la aplicación, verás el siguiente menú:

```
--- Gestor de Tareas Inteligente ---
1. Añadir tarea
2. Añadir tarea compleja (con IA)
3. Listar tareas
4. Completar tarea
5. Eliminar tarea
6. Salir
```

### Opciones Disponibles

#### 1. Añadir Tarea Simple
Permite agregar una tarea básica de forma manual:
```
Elige una opcion: 1
Descripcion de la tarea: Comprar leche
Tarea añadida con exito
```

#### 2. Añadir Tarea Compleja (con IA)
Utiliza Google Gemini para analizar una tarea compleja y desglosaría en 3-5 subtareas:
```
Elige una opcion: 2
Descripcion de la tarea compleja: Organizar una reunión de equipo en línea
```
La IA generará automáticamente:
- Subtarea 1: Seleccionar la plataforma de videoconferencia
- Subtarea 2: Enviar invitaciones a los participantes
- Subtarea 3: Preparar la agenda de la reunión
- Subtarea 4: Enviar recordatorio el día anterior
- Subtarea 5: Documentar los puntos tratados

#### 3. Listar Tareas
Muestra todas las tareas con su estado:
```
Elige una opcion: 3
[ ] #1: Comprar leche
[✓] #2: Llamar al cliente
[ ] #3: Revisar documentos
```

#### 4. Completar Tarea
Marca una tarea como completada:
```
Elige una opcion: 4
ID de la tarea a completar: 1
Tarea completada: [✓] #1: Comprar leche
```

#### 5. Eliminar Tarea
Elimina una tarea de la lista:
```
Elige una opcion: 5
ID de la tarea a eliminar: 3
Tarea #3 eliminada
```

#### 6. Salir
Cierra la aplicación guardando todos los cambios.

## Descripción de Archivos Clave

### `main.py`
Punto de entrada de la aplicación. Implementa:
- Función `print_menu()`: Muestra el menú principal
- Función `main()`: Bucle principal que gestiona las interacciones del usuario
- Manejo de entrada de usuario y llamadas a métodos del `TaskManager`

### `task_manager.py`
Contiene la lógica central:

**Clase `Task`**:
- Representa una tarea individual
- Propiedades: `id`, `description`, `completed`
- Métodos: `__str__()` para representación visual

**Clase `TaskManager`**:
- Gestiona colecciones de tareas
- Métodos principales:
  - `add_task(description)`: Añade una nueva tarea
  - `list_task()`: Muestra todas las tareas
  - `complete_task(id)`: Marca una tarea como completada
  - `delete_task(id)`: Elimina una tarea
  - `save_task()`: Persiste las tareas en JSON
  - `load_tasks()`: Carga las tareas desde JSON

### `ia_service.py`
Integración con Google Gemini:
- `create_simple_tasks(description)`: Función principal
  - Toma una descripción compleja de tarea
  - Usa Gemini para generar 3-5 subtareas
  - Retorna lista de subtareas procesadas
  - Manejo robusto de errores

### `test_task_manager.py`
Suite completa de pruebas unitarias:

**Clases de Test**:
- `TestTask`: Pruebas de la clase Task
  - Creación de tareas
  - Representación en string
  - Estados de completación
- `TestTaskManagerAddTask`: Pruebas de adición de tareas
  - Uso de directorios temporales
  - Validación de ID automático
  - Persistencia en JSON

### `task.json`
Archivo de almacenamiento automático con formato:
```json
[
    {
        "id": 1,
        "description": "Comprar leche",
        "completed": false
    },
    {
        "id": 2,
        "description": "Llamar al cliente",
        "completed": true
    }
]
```

## Ejecución de Pruebas

Ejecutar todos los tests:
```bash
python -m unittest test_task_manager.py
```

Ejecutar con verbosidad:
```bash
python -m unittest test_task_manager.py -v
```

Ejecutar un test específico:
```bash
python -m unittest test_task_manager.TestTask.test_task_creation
```

## Dependencias

Ver [`requirements.txt`](requirements.txt) para la lista completa. Principales:
- `google-genai`: Cliente oficial de Google Generative AI
- `google-api-core`: Utilidades de Google Cloud
- `python-dotenv`: Gestión de variables de entorno

## Configuración Avanzada

### Variables de Entorno
En el archivo `.env`:
```env
GEMINI_API_KEY=tu_clave_api_aqui
```

### Personalización de IA
En `ia_service.py`, puedes ajustar:
- `model`: Cambiar versión de Gemini (actualmente `gemini-2.5-flash-lite`)
- `max_output_tokens`: Límite de respuesta
- `temperature`: Control de creatividad (0.0-1.0)
- `system_instruction`: Prompt del sistema para Gemini

## Seguridad

**IMPORTANTE**: 
- Nunca compartir la clave API en repositorios públicos
- Usar `.env` y añadir a `.gitignore`:
  ```
  .env
  .venv/
  __pycache__/
  *.pyc
  task.json
  ```

## Solución de Problemas

| Problema | Solución |
|----------|----------|
| Error: "La api de gemini no esta configurada" | Verificar que `.env` existe y contiene `GEMINI_API_KEY` |
| ImportError con google-genai | Ejecutar `pip install -r requirements.txt` |
| No se cargan las tareas | Verificar permisos de lectura/escritura en el directorio |
| Gemini no genera subtareas | Verificar conexión a internet y límite de API |

## Estados de Tareas

Las tareas tienen dos estados:
- **Incompleta** `[ ]`: Tarea pendiente de realizar
- **Completada** `[✓]`: Tarea finalizada

## Mejoras Futuras

- Interfaz gráfica (GUI) con Tkinter o PyQt
- Sincronización en la nube (Firebase, MongoDB)
- Notificaciones por correo
- Integración con calendarios
- Soporte multi-usuario
- Sistema de etiquetas y categorías
- Estadísticas y reportes
- Recordatorios de tareas vencidas

## Licencia

Este proyecto es educativo y forma parte del Master IA de Bigschool.

## Autor

Desarrollado como proyecto de aprendizaje en el Master IA - Bigschool 2da edición

---

**Última actualización**: Abril 2026
