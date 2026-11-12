from app.database import conectar

class Personaje:
    def __init__(self, id, nombre, fecha_nacimiento, lugar_nacimiento, descripcion, genero, edad, peso, altura, maestro, constelacion, armadura, imagen, id_categoria):
        self.id = id
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.lugar_nacimiento = lugar_nacimiento
        self.descripcion = descripcion
        self.genero = genero
        self.edad = edad
        self.peso = peso
        self.altura = altura
        self.maestro = maestro
        self.constelacion = constelacion
        self.armadura = armadura
        self.imagen = imagen
        self.id_categoria = id_categoria

    def resumen(self):
        if not self.descripcion:
            return ""
        texto = str(self.descripcion)
        if len(texto) > 100:
            return texto[:100] + '...'
        return texto


def listar_categorias():
    try:
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT nombre_categoria FROM categorias ORDER BY id_categoria")
        filas = cursor.fetchall()
        conexion.close()
        lista = [fila['nombre_categoria'] for fila in filas]
        return lista if lista else ["Bronce", "Plata", "Oro", "Otros"]
    except Exception as e:
        print("Error en categorias:", e)
        return ["Bronce", "Plata", "Oro", "Otros"]


def listar_personajes():
    try:
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM personajes")
        filas = cursor.fetchall()
        
        cursor.execute("SELECT id_categoria, nombre_categoria FROM categorias")
        mapa_cat = {c['id_categoria']: c['nombre_categoria'] for c in cursor.fetchall()}
        conexion.close()

        lista = []
        for f in filas:
            cat_id = f.get('id_categoria') or f.get('id_categorias')
            cat_nombre = mapa_cat.get(cat_id, cat_id)
            
            p = Personaje(
                id=f.get('id') or f.get('id_personaje'),
                nombre=f.get('nombre', ''),
                fecha_nacimiento=f.get('fecha_nacimiento', ''),
                lugar_nacimiento=f.get('lugar_nacimiento', ''),
                descripcion=f.get('descripcion', ''),
                genero=f.get('genero', ''),
                edad=f.get('edad', ''),
                peso=f.get('peso', ''),
                altura=f.get('altura', ''),
                maestro=f.get('maestro', ''),
                constelacion=f.get('constelacion', ''),
                armadura=f.get('armadura', ''),
                imagen=f.get('imagen', ''),
                id_categoria=cat_nombre
            )
            lista.append(p)
        return lista
    except Exception as e:
        print("ERROR SQL PERSONAJES:", e)
        return []


def obtener_personaje(id_personaje):
    for p in listar_personajes():
        if str(p.id) == str(id_personaje):
            return p
    return None