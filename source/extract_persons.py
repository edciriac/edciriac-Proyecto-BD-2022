from ctypes import util
import mariadb
import sys
from config import *
from utils import *
from extract_data_from_wikipedia import *

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

cur = conn.cursor()

def getPersons():
    query= f"SELECT contenido FROM Noticias"
    cur.execute(query)
    for contenido in cur:   
        per = filter_persons(contenido[0])
        #print(per)
        if(len(per) > 0 ):
            for x in per:
                print(x)
                getDataPersona(x)

getPersons()
conn.close()
