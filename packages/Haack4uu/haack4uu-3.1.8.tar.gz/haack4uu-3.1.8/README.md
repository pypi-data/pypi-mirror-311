# Hack4U Academy Courses Library

Una biblioteca Python para consultar cursos de la academia Hack4U.

## Cursos disponibles:

- Introducción a Linux [15 horas]
- Personalización de Linux [3 horas]
- Introducció al Hacking [53 horas]
- Python ofensivo [35 horas]

## Instalación

Instala el paquete usando `pip3`:

```python3
pip3 install hack4u
```

## Uso básico

## Listar todos los cursos

```python3
from hack4u import list_courses

for course in list_courses():
    print(course)
```

## Obtener un curso por nombre

```python3
from hack4u import search_course_by_name

course = search_course_by_name("Introduccion a Linux")
print(course)
```

## Calcular duración total de los cursos

```python3
from hack4u.utils import total_duration

print(f"Duracion total: {total_duration()} horas)
```