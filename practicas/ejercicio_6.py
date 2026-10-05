"""
Ejercicio 6 · Sobre el proyecto
Agrega al Controlador la función clientes_por_ciudad() que devuelva un diccionario {"Guayaquil": ["Ana", "Luis"], "Quito": ["Sol"]}.
"""

def clientes_por_ciudad():
    agrupados = {}

    for registro in gestor.leer():
        ciudad = registro.get("ciudad", "").title() or "Sin ciudad"

        agrupados.setdefault(ciudad, []).append(registro["nombre"])

    return agrupados