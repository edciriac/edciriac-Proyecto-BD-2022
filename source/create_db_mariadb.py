from insert_manual_mongodb import *
import datetime
import mariadb
import sys
import os

db_user = "user" # Nombre del user del mariadb
db_password = "password" # Contraseña del user
# El database de este nombre hay que existir para que este script funcione
#
# NOTA: Por si la ejecución retorna el error de "Acces denied for user...", corre esto en mariadb:
# GRANT ALL PRIVILEGES ON database_name.* TO 'username'@'localhost';
# El database_name es igual que lo que tienes abajo y username lo que tienes arriba
db_name = "project" # Nombre del database a que vamos a conectarnos

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
