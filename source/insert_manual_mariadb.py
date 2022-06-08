from pymongo import MongoClient

client = MongoClient("localhost", port=27017)
db=client.info133_project

result = db.dueno.insert_one({
  "nombre": "hello",
  "fecha": "eadaedw",
  "categoria": "awdaw"
})

def insert_dueno(nombre, fecha, categoria):
  raise NotImplementedError()

def insert_medio(nombre, url, ciudad, idioma, dueno_ids):
  raise NotImplementedError()

def insert_noticia(titulo, url,  fecha, categoria, contenido, medio_id):
  raise NotImplementedError()

def insert_citado(nombre, noticia_ids, wikipedia_url = None):
  raise NotImplementedError()

def insert_notoriedad(url, fecha_nac, popularidad, profesion, nacionalidad):
  raise NotImplementedError()