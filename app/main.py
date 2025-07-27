from flask import Flask, request, render_template
from datetime import datetime
from utils.calculos import calcular_signo_zodiacal  
from services.horoscopo_service import obtener_pokemon_para_signo, obtener_datos_pokemon, buscar_pokemones_por_nombre_tipo
from services.favoritos_service import agregar_favorito, eliminar_favorito, listar_favoritos, buscar_favorito

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("formulario.html")  

@app.route('/horoscopo', methods=['POST'])
def horoscopo():
    nombre = request.form.get('nombre')
    fecha_nac_str = request.form.get('fecha_nacimiento')

    if not nombre or not fecha_nac_str:
        return "Faltan datos", 400
    
    try:
        fecha_nac = datetime.strptime(fecha_nac_str, '%Y-%m-%d')
    except ValueError:
        return "Fecha de nacimiento inválida, use YYYY-MM-DD.", 400

    signo = calcular_signo_zodiacal(fecha_nac)
    pokemon_nombre = obtener_pokemon_para_signo(signo)

    if not pokemon_nombre:
        return "No se encontró un Pokémon para el signo zodiacal.", 500

    datos_pokemon = obtener_datos_pokemon(pokemon_nombre)

    if not datos_pokemon:
        return f"No se pudo obtener información del Pokémon '{pokemon_nombre}'", 500

    return render_template("resultado.html",
        nombre=nombre,
        fecha=fecha_nac_str,
        signo=signo,
        pokemon=datos_pokemon
    )

@app.route('/favoritos', methods=['POST'])
def guardar_favorito():
    usuario = request.form.get('nombre')
    pokemon = request.form.get('pokemon')
    if not usuario or not pokemon:
        return {"ok": False, "error": "Faltan datos"}, 400
    favorito = agregar_favorito(usuario, pokemon)
    return favorito, 201

@app.route('/favoritos', methods=['DELETE'])
def borrar_favorito():
    usuario = request.form.get('nombre')
    fav_id = request.form.get('id')
    if not usuario or not fav_id:
        return {"ok": False, "error": "Faltan datos"}, 400
    exito = eliminar_favorito(usuario, int(fav_id))
    return {"ok": exito}

@app.route('/favoritos', methods=['GET'])
def listar_favs():
    usuario = request.args.get('usuario')
    if not usuario:
        return render_template("formulario.html", favoritos=[], error="Falta usuario")
    favoritos = listar_favoritos(usuario)
    return render_template("formulario.html", favoritos=favoritos, usuario=usuario)

@app.route('/favoritos/<int:fav_id>')
def buscar_fav(fav_id):
    usuario = request.args.get('usuario')
    if not usuario:
        return {"ok": False, "error": "Falta usuario"}, 400
    favorito = buscar_favorito(usuario, fav_id)
    if not favorito:
        return render_template("resultado.html", error="Favorito no encontrado")
    datos_pokemon = obtener_datos_pokemon(favorito['pokemon'])
    if not datos_pokemon:
        return render_template("resultado.html", error="No se encontraron datos del Pokémon")
    return render_template("resultado.html",
        nombre=favorito['usuario'],
        signo=None,
        fecha=None,
        pokemon=datos_pokemon
    )

@app.route('/pokemon', methods=['GET'])
def buscar_pokemon():
    nombre = request.args.get('nombre')
    tipo = request.args.get('tipo')
    if not nombre and not tipo:
        return render_template("resultado_pokemon.html", pokemones=[])
    resultado = buscar_pokemones_por_nombre_tipo(nombre=nombre, tipo=tipo)
    return render_template("resultado_pokemon.html", pokemones=resultado)

if __name__ == '__main__':
    app.run(debug=True)
