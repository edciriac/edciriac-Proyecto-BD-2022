import mariadb
import sys
import os
from config import *
from insert_manual_mariadb import *

# NOTA: Por si la ejecución retorna el error de "Acces denied for user...", corre esto en mariadb:
# GRANT ALL PRIVILEGES ON database_name.* TO 'username'@'localhost';
# El database_name es igual que lo que tienes abajo y username lo que tienes en el archivo config

try:
    # Los variables existen en el archivo config
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

cursor = conn.cursor()

# Ejecutar los comandos del archivo create_tables.sql
sql_file_path = os.path.join(sys.path[0], "create_tables.sql")
with open(sql_file_path, 'r') as f:
  queries = f.read()
  sqlCommands = queries.split(";")
  # Sacar comandos vacios
  sqlCommands = list(filter(lambda command: command.strip() != "", sqlCommands))
  for command in sqlCommands:
    print("Ejecutando el comando: \n" + command)
    cursor.execute(command)

#Comando para Windows:
#os.system('cmd /k "python insert_medios.py"') 

# INSERTAR LOS MEDIOS DESPUES DE CREAR LAS TABLAS
insert_medio("Diario Los Lagos","https://www.diarioloslagos.cl" , "Puerto Montt", "español")
insert_medio( "El Repuertero", "https://www.elrepuertero.cl","Puerto Montt", "español")
insert_medio("Diario De Puerto Montt", "https://www.diariodepuertomontt.cl", "Puerto Montt", "español")
insert_medio("La Opinión de Chiloé", "https://laopiniondechiloe.cl", "Chiloé", "español")
insert_medio("Noticias Chiloé", "https://www.noticiaschiloe.cl", "Chiloé", "español")
insert_medio("El Heraldo Austral", "https://www.eha.cl", "Puerto Varas", "español")

insert_dueno("Verticecom Producciones EIRL", "2017-06-09", "Empresa")
insert_dueno("COMUNICACIONES VELASQUEZ SPA.", "2020-02-29", "Empresa")
insert_dueno("ASESORIAS E INVERSIONES COMUNIDADES CIUDADANA S A", "2008-05-12 21", "Empresa")
insert_dueno("La Opinion De Chiloe", "2016-06-21", "Empresa")
insert_dueno("Nicolas Herve Fernandez", "2015-06-16", "Persona Natural")

insert_rel_dueno_medio("Verticecom Producciones EIRL", "https://www.diariodepuertomontt.cl")
insert_rel_dueno_medio("COMUNICACIONES VELASQUEZ SPA.", "https://www.diarioloslagos.cl")
insert_rel_dueno_medio("ASESORIAS E INVERSIONES COMUNIDADES CIUDADANA S A", "https://www.elrepuertero.cl")
insert_rel_dueno_medio("La Opinion De Chiloe", "https://laopiniondechiloe.cl")
insert_rel_dueno_medio("Nicolas Herve Fernandez", "https://www.noticiaschiloe.cl")
