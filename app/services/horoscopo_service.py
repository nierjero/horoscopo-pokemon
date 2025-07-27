import random
import requests


signo_a_pokemon = {
    "Aries": ["Charizard", "Blaziken", "Incineroar"],
    "Tauro": ["Snorlax", "Miltank", "Tauros"],
    "Géminis": ["Pikachu", "Jolteon", "Rotom"],
    "Cáncer": ["Lapras", "Vaporeon", "Blastoise"],
    "Leo": ["Arcanine", "Pyroar", "Herdier"], 
    "Virgo": ["Audino", "Clefable", "Granbull"],
    "Libra": ["Gardevoir", "Sylveon", "Mismagius"],
    "Escorpio": ["Gyarados", "Hydreigon", "Tyranitar"],
    "Sagitario": ["Rapidash", "Archeops", "Talonflame"],
    "Capricornio": ["Steelix", "Aggron", "Bastiodon"],
    "Acuario": ["Alakazam", "Espeon", "Gallade"],
    "Piscis": ["Gyarados", "Lanturn", "Vaporeon"]
}

def obtener_pokemon_para_signo(signo):
    if signo in signo_a_pokemon:
        return random.choice(signo_a_pokemon[signo])
    else:
        return "Signo no válido"

def obtener_datos_pokemon(nombre):
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "nombre": data["name"],
            "sprite": data["sprites"]["front_default"],
            "peso": data["weight"] / 10,    # hectogramos a kg
            "altura": data["height"] / 10,  # decímetros a metros
            "habilidades": [h["ability"]["name"] for h in data["abilities"]]
        }
    else:
        return {"error": "Pokemon no encontrado"}

def buscar_pokemones_por_nombre_tipo(nombre=None, tipo=None):
    pokemones = []
    if nombre:
        resp = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}")
        if resp.status_code == 200:
            data = resp.json()
            if not tipo or any(t['type']['name'] == tipo.lower() for t in data['types']):
                pokemones.append({"nombre": data['name'], "tipos": [t['type']['name'] for t in data['types']]})
    elif tipo:
        resp = requests.get(f"https://pokeapi.co/api/v2/type/{tipo.lower()}")
        if resp.status_code == 200:
            data = resp.json()
            for poke in data['pokemon']:
                pokemones.append({"nombre": poke['pokemon']['name']})
    return pokemones