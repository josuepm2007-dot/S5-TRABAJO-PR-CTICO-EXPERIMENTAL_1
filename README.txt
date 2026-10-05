TAREA 1 - SISTEMA DE ESTUDIANTES

Estructura:
proyecto_estudiantes/
├── main.py
├── views.py
├── models.py
├── shared/
│   ├── __init__.py
│   ├── herramientas.py
│   └── json_manager.py
└── data/
    └── estudiantes.json

Ejecutar:
1. Abrir terminal dentro de proyecto_estudiantes
2. Ejecutar: python main.py

Incluye:
- Crear
- Leer todos
- Buscar
- Ver por ID
- Actualizar
- Eliminar
- Carnet único
- Email único
- Agregar nota (0 a 20)
- Ver promedio
- Materias ofertadas
- Materias en común
- Persistencia en JSON

Colecciones:
- list: registros y listas de notas
- tuple: campos y respuestas fijas
- set: carnets/materias sin repetición e intersección
- dict: registros, notas y menú
