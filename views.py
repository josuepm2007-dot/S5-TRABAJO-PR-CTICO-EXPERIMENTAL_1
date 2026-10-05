from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/estudiantes.json")

# Tuplas: configuración fija del sistema.
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")


def carnets_registrados(excepto_id=None):
    # Set: detectar carnets duplicados rápidamente.
    return {
        registro["carnet"].strip().lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def emails_registrados(excepto_id=None):
    return {
        registro["email"].strip().lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def siguiente_id():
    ids = [registro["id"] for registro in gestor.leer()]
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

def crear_estudiante(datos):
    valores = {
        campo: str(datos.get(campo, "")).strip()
        for campo in CAMPOS_ESTUDIANTE
    }

    faltantes = [
        campo for campo in CAMPOS_OBLIGATORIOS
        if not valores[campo]
    ]

    if faltantes:
        return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

    if not es_email_valido(valores["email"]):
        return False, "El email no tiene un formato válido"

    if valores["carnet"].lower() in carnets_registrados():
        return False, "Ese carnet ya está registrado"

    if valores["email"].lower() in emails_registrados():
        return False, "Ese email ya está registrado"

    estudiante = Estudiante(
        siguiente_id(),
        valores["nombre"],
        valores["apellido"],
        valores["email"],
        valores["carnet"],
    )

    registros = gestor.leer()
    registros.append(estudiante.a_diccionario())

    if not gestor.guardar(registros):
        return False, "No se pudo escribir el archivo"

    return (
        True,
        f"Estudiante {estudiante.obtener_nombre_completo()} "
        f"creado con id {estudiante.id}",
    )


# ===================== R · READ =====================

def obtener_todos():
    return [
        Estudiante.desde_diccionario(registro)
        for registro in gestor.leer()
    ]


def obtener_por_id(id_estudiante):
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante

    return None


# ===================== S · SEARCH =====================

def buscar_estudiantes(termino):
    termino = termino.strip().lower()

    if not termino:
        return []

    encontrados = []

    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(
                    Estudiante.desde_diccionario(registro)
                )
                break

    return encontrados


# ===================== U · UPDATE =====================

def actualizar_estudiante(id_estudiante, cambios):
    campos_validos = set(CAMPOS_ESTUDIANTE)
    desconocidos = set(cambios) - campos_validos

    if desconocidos:
        return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

    if not cambios:
        return False, "No se indicó ningún cambio"

    cambios = {
        clave: str(valor).strip()
        for clave, valor in cambios.items()
    }

    if "email" in cambios:
        if not es_email_valido(cambios["email"]):
            return False, "El email no tiene un formato válido"

        if cambios["email"].lower() in emails_registrados(
            excepto_id=id_estudiante
        ):
            return False, "Ese email ya lo usa otro estudiante"

    if "carnet" in cambios:
        if not cambios["carnet"]:
            return False, "El carnet no puede quedar vacío"

        if cambios["carnet"].lower() in carnets_registrados(
            excepto_id=id_estudiante
        ):
            return False, "Ese carnet ya lo usa otro estudiante"

    registros = gestor.leer()
    posicion = None

    for indice, registro in enumerate(registros):
        if registro["id"] == id_estudiante:
            posicion = indice
            break

    if posicion is None:
        return False, f"No existe un estudiante con id {id_estudiante}"

    registros[posicion].update(cambios)

    if not gestor.guardar(registros):
        return False, "No se pudo guardar la actualización"

    return (
        True,
        f"Estudiante {id_estudiante} actualizado "
        f"({len(cambios)} campo/s)",
    )


# ===================== D · DELETE =====================

def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()

    quedan = [
        registro
        for registro in registros
        if registro["id"] != id_estudiante
    ]

    if len(quedan) == len(registros):
        return False, f"No existe un estudiante con id {id_estudiante}"

    if not gestor.guardar(quedan):
        return False, "No se pudo guardar el archivo"

    return True, f"Estudiante {id_estudiante} eliminado"


# ===================== EXTRA · NOTAS =====================

def agregar_nota(id_estudiante, materia, nota):
    materia = str(materia).strip()

    if not materia:
        return False, "La materia es obligatoria"

    try:
        nota = float(nota)
    except (TypeError, ValueError):
        return False, "La nota debe ser un número"

    if nota < 0 or nota > 20:
        return False, "La nota debe estar entre 0 y 20"

    registros = gestor.leer()

    for registro in registros:
        if registro["id"] == id_estudiante:
            estudiante = Estudiante.desde_diccionario(registro)
            estudiante.agregar_nota(materia, nota)

            registros[
                registros.index(registro)
            ] = estudiante.a_diccionario()

            if not gestor.guardar(registros):
                return False, "No se pudo guardar la nota"

            return True, "Nota agregada correctamente"

    return False, f"No existe un estudiante con id {id_estudiante}"


def materias_ofertadas():
    # Set: reúne todas las materias sin repetir.
    materias = set()

    for estudiante in obtener_todos():
        materias.update(estudiante.materias)

    return materias


def estudiantes_en_comun(id_a, id_b):
    estudiante_a = obtener_por_id(id_a)
    estudiante_b = obtener_por_id(id_b)

    if estudiante_a is None:
        return None, f"No existe un estudiante con id {id_a}"

    if estudiante_b is None:
        return None, f"No existe un estudiante con id {id_b}"

    # Intersección de sets.
    return estudiante_a.materias & estudiante_b.materias, None
