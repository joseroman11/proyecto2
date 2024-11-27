# Sistema de Gestión de Turnos Médicos

Una aplicación en Python que permite gestionar turnos médicos de pacientes utilizando una interfaz gráfica con `tkinter`. Los turnos se organizan usando un árbol AVL para las fechas y una cola de prioridad según el nivel de urgencia.

## Funcionalidades

- **Registrar Turnos**: Ingreso de paciente con ID, nombre, urgencia y fecha del turno.
- **Ver Turnos**: Visualización de todos los turnos registrados en una tabla ordenada.
- **Exportar a CSV**: Opción para exportar los turnos a un archivo CSV.
- **Gestión Eficiente**: Uso de un árbol AVL para organizar los turnos por fecha y una cola de prioridad para manejar urgencias.

## Requisitos

- Python 3.x
- `tkcalendar` (para el selector de fechas)

Instalar dependencias:

```bash
pip install tkcalendar
