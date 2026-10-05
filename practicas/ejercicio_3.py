"""
Ejercicio 3 · Conjuntos en acción
inscritos_matematica = {"Ana","Luis","Sol","Marco"} y inscritos_ingles = {"Luis","Marco","Ruth"}.
Responde con código: ¿quiénes están en las dos?,
¿quiénes solo en matemática?, ¿cuántos estudiantes distintos hay en total
"""

inscritos_matematica = {"Ana", "Luis", "Sol", "Marco"}
inscritos_ingles = {"Luis", "Marco", "Ruth"}

ambas = inscritos_matematica & inscritos_ingles
solo_mate = inscritos_matematica - inscritos_ingles
total = len(inscritos_matematica | inscritos_ingles)

print(sorted(ambas), sorted(solo_mate), total)