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
  query= f"INSERT INTO Duenos (nombre, fecha_cargo, categoria) VALUES ('{nombre}', '{fecha}', '{categoria}')"
  cur.execute(query)
  conn.commit()

def insert_medio(nombre, url, ciudad, idioma):
  query= f"INSERT INTO Medios (nombre, url, ciudad, idioma) VALUES ('{nombre}', '{url}', '{ciudad}', '{idioma}')"
  cur.execute(query)
  conn.commit()

def insert_noticia(url,  fecha_publicacion,titulo, categoria, contenido, medio_url):
  query= f"INSERT INTO Noticias (url,fecha_publicacion,titulo,categoria,contenido,medio_url) VALUES ('{url}', '{fecha_publicacion}', '{titulo}', '{categoria}', '{contenido}', '{medio_url}')"
  cur.execute(query)
  conn.commit()

def insert_persona_rich(nombre, noticia_url, wikipedia_url, fecha_nac, popularidad, profesion, nacionalidad):
  query= f"INSERT INTO Personas (nombre,wikipedia_url,fecha_nacimiento,popularidad,profesion,nacionalidad) VALUES ('{nombre}', '{wikipedia_url}', '{fecha_nac}', {popularidad}, '{profesion}', '{nacionalidad}')"
  try:
    cur.execute(query)
    conn.commit()
  except mariadb.IntegrityError:
    print(f"Person with name {nombre} already exists, only adding relation to noticia")
  insert_noticia_persona_rel(nombre, noticia_url)

def insert_persona(nombre, noticia_url):
  query= f"INSERT INTO Personas (nombre) VALUES ('{nombre}')"
  try:
    cur.execute(query)
    conn.commit()
  except mariadb.IntegrityError:
    print(f"Person with name {nombre} already exists, only adding relation to noticia")
  insert_noticia_persona_rel(nombre, noticia_url)

def insert_noticia_persona_rel(persona_nombre, noticia_url):
  query= f"INSERT INTO NoticiaPersonaRelacion (persona_nombre,noticia_url) VALUES ('{persona_nombre}', '{noticia_url}')"
  cur.execute(query)
  conn.commit()

def insert_rel_dueno_medio(dueno_nombre, medio_url):
  query= f"INSERT INTO MedioDuenoRelacion (dueno_nombre,medio_url) VALUES ('{dueno_nombre}', '{medio_url}')"
  cur.execute(query)
  conn.commit()