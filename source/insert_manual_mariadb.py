import mariadb
import sys
from config import *

# Conectarse a MariaDB para guardar los datos escrapeados
try:
    conn = mariadb.connect(
        user=db_user,
        password=db_password,
        host="localhost",
        port=3306,
        database=db_name
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


def insert_dueno(nombre, fecha, categoria):
  raise NotImplementedError()

def insert_medio(nombre, url, ciudad, idioma):
  query= f"INSERT INTO Medios (nombre, url, ciudad, idioma) VALUES ('{nombre}', '{url}', '{ciudad}', '{idioma}')"
  cur.execute(query)
  conn.commit()

def insert_noticia(url,  fecha_publicacion,titulo, categoria, contenido, medio_url):
  query= f"INSERT INTO Noticias (url,fecha_publicacion,titulo,categoria,contenido,medio_url) VALUES ('{url}', '{fecha_publicacion}', '{titulo}', '{categoria}', '{contenido}', '{medio_url}')"
  cur.execute(query)
  conn.commit()

def insert_citado(nombre, noticia_ids, wikipedia_url = None):
  raise NotImplementedError()

def insert_notoriedad(url, fecha_nac, popularidad, profesion, nacionalidad):
  raise NotImplementedError()