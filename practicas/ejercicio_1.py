"""
Ejercicio 1 · Quitar duplicados conservando el orden
Dada ciudades = ["Quito","Guayaquil","Quito","Cuenca","Guayaquil"], 
obtén una lista sin repetidos respetando el orden de aparición (un set solo no alcanza)
"""

ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]

vistas = set()
unicas = []

for ciudad in ciudades:
    if ciudad not in vistas:
        vistas.add(ciudad)
        unicas.append(ciudad)

print(unicas)