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

def get_medio_by_url(url):
  cur = conn.cursor()
  query = f"SELECT * FROM Medios WHERE url='{url}'"
  cur.execute(query)
  result = cur.next()
  print(result)
  # Puede que ocurran bugs si no cerramos el cursor despues de la consulta
  cur.close()
  if (result == None): raise Exception(f"No Medio with url '{url}' were found")
  return result