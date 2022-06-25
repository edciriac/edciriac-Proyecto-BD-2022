from multiprocessing.dummy import Array
from wsgiref import headers

from numpy import insert, source
from requests_html import HTMLSession
from pymongo import MongoClient
import time
from nav_config import USER_AGENT_LIST, headers

import w3lib.html
import html
import mariadb
import sys
import os
# sys.path.append('../source')
# from insert_manual_mariadb import insert_noticia

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
  
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
  
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)
  
# now we can import the module in the parent
# directory.
import insert_manual_mariadb

#Formatear las fechas
def format_date(date):
    return(date.split("T")[0])

#Conexión a Mongo
client = MongoClient("localhost", port=27017)
db=client.info133_project

session = HTMLSession()

## URL "SEED" que escrapear
URL_SEED = "https://www.diarioloslagos.cl/categorias/noticias/regionales/page/"

## Analizar ("to parse") el contenido
xpath_url="//article/a/@href"

urls = []

for i in range(1,3):
    seed = URL_SEED+str(i)
    print(seed)
    response = session.get(seed,headers=headers)
    print(response)
    all_urls = response.html.xpath(xpath_url)

    # Usar este para solo crawl 3 urls
    for i in range(1,4):
        print("crawl number:", {i} )
        print(all_urls[i])
        article_url = all_urls[i]

        urls.append(article_url)

    # Usar este codigo abajo para crawl todos los urls
    # for url in all_urls: 
    #     print(url)
    #     article_url = url

    #     urls.append(article_url)
    #     #Insert into mongo
    #     # news = {'url':article_url,'to_download':True}
    #     # result=db.urls.insert_one(news)

    time.sleep(2)


# Parte scraping:


def format_date(date):
        return(date.split("T")[0])

session = HTMLSession()

xpath_title="//div//h1"
xpath_date="//meta[@property='article:published_time']//@content"
xpath_text="//div[@class='entry-content clearfix']//p"



#Conectarse a Mongo para listar las URLs que escrapear
# client = MongoClient("localhost", port=27017)
# db=client.info133_2022

db_user = "user" # Nombre del user del mariadb
db_password = "password" # Contraseña del user
db_name = "project" # Nombre del database a que vamos a conectarnos

# Conectarse a MariaDB para guardar los datos escrapeados
try:
    conn = mariadb.connect(
        # user="estefano",
        # password="espinoza",
        # host="localhost",
        # port=3306,
        # database="info133_2022"

        # user="root",
        # password="0570",
        # host="localhost",
        # port=3306,
        # database="info133_2022"
        
        user=db_user,
        password=db_password,
        host="localhost",
        port=3306,
        database=db_name
    )
    print("connected successfully")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

# Listar las URLs que escrapear
# for doc in db.urls.find({"to_download":True}).limit(2):
for url in urls:
    print(url)

    ## URL que escrapear
    URL = url

    response = session.get(URL,headers=headers)

    ## Analizar el contenido
    title = response.html.xpath(xpath_title)[0].text
    date = format_date(response.html.xpath(xpath_date)[0])

    list_p = response.html.xpath(xpath_text)
    text=""
    for p in list_p:
        content = p.text
        content = w3lib.html.remove_tags(content)
        content = w3lib.html.replace_escape_chars(content)
        content = html.unescape(content)
        content = content.strip()
        text=text+" "+content

    #Guardar los datos en MariaDB
    # print("{0}, {1}, {2}".format(URL,title,date))
    # query= f"INSERT INTO noticias (url,title,date,content) VALUES ('{URL}', '{title}', '{date}', '{text}')"
    
    # cur.execute(query)

    insert_manual_mariadb.insert_noticia(url,  date, title, "", text, 1)
    
    # conn.commit()
    # time.sleep(1)

conn.close()