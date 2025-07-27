import json
import os

FAVORITOS_FILE = "favoritos.json"

def cargar_favoritos():
    if not os.path.exists(FAVORITOS_FILE):
        return []
    with open(FAVORITOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_favoritos(favoritos):
    with open(FAVORITOS_FILE, "w", encoding="utf-8") as f:
        json.dump(favoritos, f, ensure_ascii=False, indent=2)

def agregar_favorito(usuario, pokemon):
    favoritos = cargar_favoritos()
    nuevo = {
        "id": len(favoritos) + 1,
        "usuario": usuario,
        "pokemon": pokemon
    }
    favoritos.append(nuevo)
    guardar_favoritos(favoritos)
    return nuevo

def eliminar_favorito(usuario, fav_id):
    favoritos = cargar_favoritos()
    nuevos = [f for f in favoritos if not (f["id"] == fav_id and f["usuario"] == usuario)]
    exito = len(nuevos) != len(favoritos)
    guardar_favoritos(nuevos)
    return exito

def listar_favoritos(usuario):
    favoritos = cargar_favoritos()
    return [f for f in favoritos if f["usuario"] == usuario]

def buscar_favorito(usuario, fav_id):
    favoritos = cargar_favoritos()
    for f in favoritos:
        if f["id"] == fav_id and f["usuario"] == usuario:
            return f
    return {}