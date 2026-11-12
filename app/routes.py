from flask import render_template, request, abort
from app import app
from app.utilities.personajes import (
    listar_categorias,
    listar_personajes,
    obtener_personaje,
    Personaje
)

@app.route('/')
def index():
    try:
        categorias = listar_categorias()
    except Exception:
        categorias = []
        
    if not categorias:
        categorias = ["Bronce", "Plata", "Oro", "Otros"]
        
    try:
        todos = listar_personajes()[:6]
    except Exception as e:
        print("ERROR AL TRAER PERSONAJES EN INDEX:", e)
        todos = []

    if not todos:
        todos = [
            Personaje(1, "Seiya de Pegasus", "", "Japón", "Caballero de Bronce de Pegaso.", "M", 13, 53, 165, "Marin", "Pegasus", "Cloth de Pegasus", "seiya_pegaso.jpg", "Bronce"),
            Personaje(2, "Hyōga de Cygnus", "", "Siberia", "Caballero de Bronce del Cisne.", "M", 14, 60, 173, "Camus", "Cygnus", "Cloth de Cygnus", "hyoga_cisne.jpg", "Bronce"),
            Personaje(3, "Shiryū de Dragón", "", "China", "Caballero de Bronce del Dragón.", "M", 14, 53, 172, "Dohko", "Draco", "Cloth de Dragón", "shiryu_dragon.jpg", "Bronce"),
            Personaje(4, "Shun de Andromeda", "", "Japón", "Caballero de Bronce de Andrómeda.", "M", 13, 51, 165, "Daidalos", "Andromeda", "Cloth de Andromeda", "shun_andromeda.jpg", "Bronce"),
            Personaje(5, "Ikki de Phoenix", "", "Isla de la Reina Muerte", "Caballero de Bronce del Fénix.", "M", 15, 62, 175, "Guilty", "Phoenix", "Cloth de Phoenix", "ikki_fenix.jpg", "Bronce"),
            Personaje(6, "June de Chamaeleon", "", "Etiopía", "Amazona de Bronce del Camaleón.", "F", 14, 45, 160, "Daidalos", "Chamaeleon", "Cloth de Chamaeleon", "jabu_unicornio.jpg", "Bronce")
        ]
        
    return render_template('index.html', categorias=categorias, personajes=todos)

@app.route('/personajes')
def personajes():
    busqueda = request.args.get('q')
    categoria = request.args.get('categoria')
    lista = listar_personajes()

    if busqueda:
        lista = [p for p in lista if busqueda.lower() in p.nombre.lower()]
    if categoria:
        lista = [p for p in lista if str(p.id_categoria).lower() == categoria.lower()]

    return render_template('personajes.html', titulo="Personajes", personajes=lista)

@app.route('/personaje/<int:id_personaje>')
def personaje(id_personaje):
    caballero = obtener_personaje(id_personaje)
    if not caballero:
        abort(404)
    return render_template('detalle.html', titulo=caballero.nombre, personaje=caballero)

@app.route('/categorias')
def categorias():
    try:
        lista_categorias = listar_categorias()
    except Exception:
        lista_categorias = []
    return render_template('categorias.html', titulo="Categorías", categorias=lista_categorias)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return "<h1>404 - Página no encontrada</h1>", 404
