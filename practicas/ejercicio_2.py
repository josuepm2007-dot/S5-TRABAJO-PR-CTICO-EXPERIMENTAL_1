"""
Ejercicio 2 · Contar con un diccionario
Con la misma lista, arma un diccionario {"Quito": 2, "Guayaquil": 2, "Cuenca": 1}.
"""

ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]

conteo = {}

for ciudad in ciudades:
    conteo[ciudad] = conteo.get(ciudad, 0) + 1

print(conteo)

mas_repetida = max(conteo, key=conteo.get)
print(mas_repetida)