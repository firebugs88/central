# Registro de Novedades Diarias

Una aplicación de escritorio desarrollada en Python con Tkinter para el registro y gestión de novedades diarias con soporte multiplataforma optimizado.

## Características

- **Interfaz Gráfica Intuitiva**: Interfaz limpia y fácil de usar con Tkinter
- **Base de Datos SQLite**: Almacenamiento persistente de datos
- **Exportación a Excel**: Capacidad de exportar registros a archivos .xlsx
- **Multiplataforma**: Optimizado para funcionar en Windows, macOS y Linux
- **Gestión Completa**: Crear, editar, eliminar y marcar novedades como terminadas
- **Registro de Actividad**: Sistema de logging integrado
- **Arquitectura Robusta**: Patrón Singleton para conexiones de BD y pool de conexiones

## Requisitos del Sistema

- Python 3.7 o superior
- Tkinter (incluido con Python)
- SQLite3 (incluido con Python)

## Dependencias

```bash
pip install openpyxl
```

## Instalación

1. Clona este repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd central
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:
```bash
python app.py
```

## Estructura del Proyecto

```
central/
├── app.py              # Aplicación principal
├── pro.db              # Base de datos SQLite (se crea automáticamente)
├── novedades.log       # Archivo de logs
└── README.md           # Este archivo
```

## Funcionalidades

### Gestión de Novedades

- **Crear**: Agrega nuevas novedades con fecha y hora automática
- **Editar**: Modifica el texto de novedades existentes
- **Eliminar**: Borra novedades con confirmación
- **Terminar**: Marca novedades como completadas con fecha de finalización
- **Exportar**: Genera archivos Excel con todos los registros

### Características Técnicas

- **Pool de Conexiones**: Gestión eficiente de conexiones a la base de datos
- **Threading**: Operaciones de BD ejecutadas en hilos separados para mejor rendimiento
- **Logging**: Registro detallado de errores y operaciones
- **Validación**: Validación de entrada de datos (longitud máxima, campos requeridos)

## Optimizaciones Multiplataforma

### Rutas de Datos
- **Windows**: `%APPDATA%/NovedadesApp/`
- **macOS**: `~/Library/Application Support/NovedadesApp/`
- **Linux**: `~/.local/share/NovedadesApp/`

### Fuentes del Sistema
- **Windows**: Segoe UI → Tahoma → Arial
- **macOS**: SF Pro Text → .AppleSystemUIFont → Helvetica Neue
- **Linux**: Ubuntu → DejaVu Sans → Liberation Sans

### Estilos Adaptativos
- Colores de selección nativos para cada OS
- Mejores contrastes y apariencia visual
- Menú de aplicación nativo en macOS

## Uso

1. **Agregar Novedad**: Escribe en el campo de texto y presiona Enter o haz clic en "Crear"
2. **Editar Novedad**: Selecciona una novedad, escribe el nuevo texto y haz clic en "Editar"
3. **Terminar Novedad**: Selecciona una novedad y haz clic en "Terminar"
4. **Eliminar Novedad**: Selecciona una novedad y haz clic en "Eliminar"
5. **Exportar**: Haz clic en "Exportar" para generar un archivo Excel

## Arquitectura

### Clases Principales

- **DatabaseConnection**: Patrón Singleton para gestión de conexiones
- **NovedadesRepository**: Capa de acceso a datos con operaciones CRUD
- **NovedadesGUI**: Interfaz gráfica principal con componentes Tkinter

### Base de Datos

Tabla `novedades`:
- `id`: INTEGER PRIMARY KEY
- `novedad`: TEXT NOT NULL
- `fecha_inicio`: TEXT NOT NULL
- `fecha_fin`: TEXT (nullable)

## Contribución

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Para reportar bugs o solicitar nuevas características, por favor abre un issue en este repositorio.

---

**Versión**: 1.0  
**Última actualización**: 2025  
**Compatibilidad**: Windows, macOS, Linux