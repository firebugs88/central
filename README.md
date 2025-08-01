# Registro de Novedades Diarias

Este es un sencillo programa de escritorio desarrollado en Python con una interfaz gráfica de usuario (GUI) construida con Tkinter. La aplicación permite a los usuarios registrar, ver, editar, eliminar y exportar "novedades" o incidentes diarios.

## Características

- **Crear Novedades**: Añade nuevas entradas de novedades con una descripción y una fecha y hora de inicio automáticas.
- **Visualizar Novedades**: Muestra todas las novedades en una lista clara y organizada. Las novedades pendientes (sin fecha de finalización) se resaltan visualmente.
- **Marcar como Terminadas**: Permite a los usuarios seleccionar una novedad y marcarla como "terminada", añadiendo la fecha y hora de finalización actuales.
- **Editar y Eliminar**: Modifica el texto de una novedad existente o elimínala por completo de la base de datos.
- **Contador de Pendientes**: Muestra un recuento en tiempo real de cuántas novedades están aún sin terminar.
- **Exportar a Excel**: Exporta la lista completa de novedades a un archivo `.xlsx` para facilitar la generación de informes.
- **Persistencia de Datos**: Utiliza una base de datos SQLite (`pro.db`) para almacenar todas las novedades de forma persistente.
- **Registro de Errores**: Guarda un registro de las operaciones y los errores en el archivo `novedades.log`.
- **Interfaz Responsiva**: Las operaciones de base de datos se ejecutan en hilos separados para mantener la interfaz de usuario fluida y sin bloqueos.

## Tecnologías Utilizadas

- **Lenguaje**: Python 3
- **Interfaz Gráfica**: Tkinter (biblioteca estándar de Python)
- **Base de Datos**: SQLite 3 (biblioteca estándar de Python)
- **Exportación**: Openpyxl

## Prerrequisitos

Para ejecutar este programa, necesitas tener Python 3 instalado en tu sistema. Además, debes instalar la biblioteca `openpyxl`.

```bash
pip install openpyxl
```

## Cómo Ejecutar el Programa

1.  Asegúrate de tener Python 3 y `openpyxl` instalados.
2.  Clona o descarga este repositorio en tu máquina local.
3.  Abre una terminal o línea de comandos y navega hasta el directorio del proyecto.
4.  Ejecuta el siguiente comando:

```bash
python pro.py
```

Al ejecutar el script, se iniciará la aplicación de escritorio. La base de datos (`pro.db`) y el archivo de registro (`novedades.log`) se crearán automáticamente en el mismo directorio si no existen.

## Descripción de Archivos

-   `pro.py`: El script principal de Python que contiene toda la lógica de la aplicación y la interfaz gráfica.
-   `pro.db`: El archivo de la base de datos SQLite donde se almacenan las novedades.
-   `novedades.log`: Un archivo de registro que captura eventos importantes y errores.
-   `README.md`: Este archivo.
