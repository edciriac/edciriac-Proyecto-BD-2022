from pymongo import MongoClient

client = MongoClient("localhost", port=27017)
db=client.info133_project

result = db.dueno.insert_one({
  "nombre": "hello",
  "fecha": "eadaedw",
  "categoria": "awdaw"
})

def insert_dueno(nombre, fecha, categoria):
  return db.dueno.insert_one({
    "nombre": nombre,
    "fecha": fecha,
    "categoria": categoria
  })

def insert_medio(nombre, url, ciudad, idioma, dueno_ids):
  return db.medio.insert_one({
    "nombre": nombre,
    "url": url,
    "ciudad": ciudad,
    "idioma": idioma,
    "duenos": dueno_ids
  })

def insert_noticia(titulo, url,  fecha, categoria, contenido, medio_id):
  return db.noticia.insert_one({
    "titulo": titulo,
    "url": url,
    "fecha": fecha,
    "categoria": categoria,
    "contenido": contenido,
    "medio": medio_id
  })

def insert_citado(nombre, noticia_ids, wikipedia_url = None):
  return db.citado.insert_one({
    "nombre": nombre,
    "noticias": noticia_ids,
    "wikipedia_url": wikipedia_url
  })

def insert_notoriedad(url, fecha_nac, popularidad, profesion, nacionalidad):
  return db.notoriedad.insert_one({
    "url": url,
    "fecha_nacionamiento": fecha_nac,
    "popularidad": popularidad,
    "profesion": profesion,
    "nacionalidad": nacionalidad
  })