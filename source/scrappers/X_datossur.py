from datetime import datetime
import locale
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
#Importar de la carpeta source
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import insert_manual_mariadb
from config import *

#Formatear las fechas
def format_date(date):
    return(date.split("T")[0])

session = HTMLSession()

MEDIO_URL = "https://www.datossur.cl"
## URL "SEED" para hacer el crawling
URL_SEED = "https://www.datossur.cl/index.php/ds/noticiasds.html"
## Analizar ("to parse") el contenido
xpath_url="//div[@class = 'items-row']"

## Para scraping
xpath_title="//div//h1"
xpath_date="//div[@id ='printableArea']//small"
xpath_text="//div[@class='col-12 col-md-12 ck-content']//p"
xpath_categoria = ""

# 
urls = []
for i in range(0,1):
    # Las paginas tienen 17 noticias por presa y se controla esto con el parametro de start. O sea, una pagina contiene 17 noticias.
    # Por lo tanto cambiamos el parametro de start con saltos de 17
    seed = URL_SEED+f"?start={i*17}"
    print(seed)
    response = session.get(seed,headers=headers)
    print(response)
    all_urls = response.html.xpath(xpath_url)
    # all_urls = list(map(lambda url: MEDIO_URL + url, all_urls))
    print(all_urls)

    # Usar este para solo crawl los primeros 3 urls
    # for i in range(1,4):
    #     print("crawl number:", {i} )
    #     print(all_urls[i])
    #     article_url = all_urls[i]
        # urls.append(article_url)

    # Usar este codigo abajo para crawl todos los urls
    # for url in all_urls: 
    #     print(url)
    #     article_url = url

    #     urls.append(article_url)
    #     #Insert into mongo
    #     # news = {'url':article_url,'to_download':True}
    #     # result=db.urls.insert_one(news)

    time.sleep(2)

#---------------------------------------------------------
# Parte scraping:

# Puede que esto retorne un error si no tienes el locale de es_ES.UTF-8 instalado a tu computador.
# Comprueba esto con el comando "locale -a" en terminal (Al menos esto funciona con mac)
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

# Formatear fecha de este tipo de secuencia 'Por Claudia Sepúlveda , 27 de junio de 2022 | 11:57'
def format_date(date):
  date = date.split(", ")[1]
  date = date.split(" |")[0]
  return datetime.strptime(date, '%d de %B de %Y').strftime('%Y-%m-%d')


#Conectarse a Mongo para listar las URLs que escrapear
# client = MongoClient("localhost", port=27017)
# db=client.info133_2022

# Conectarse a MariaDB para guardar los datos escrapeados
try:
    conn = mariadb.connect(
        # user="estefano",
        # password="espinoza",
        # host="localhost",
        # port=3306,
        # database="info133_2022"
        
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

# Listar las URLs que escrapear
for url in urls:
    print(url)
    ## URL que escrapear
    URL = url
    response = session.get(URL,headers=headers)

    ## Analizar el contenido
    title = response.html.xpath(xpath_title)[0].text
    date = format_date(response.html.xpath(xpath_date)[0].text)
    list_p = response.html.xpath(xpath_text)
    #TODO: escrapear la categoria 
    categoria = "Sin categoría" #response.html.xpath(xpath_categoria)
    text=""
    for p in list_p:
        content = p.text
        content = w3lib.html.remove_tags(content)
        content = w3lib.html.replace_escape_chars(content)
        content = html.unescape(content)
        content = content.strip()
        text=text+" "+content
    print(title)
    print(date)
    print(text)


    # insert_manual_mariadb.insert_noticia(url,  date, title, categoria, text, MEDIO_URL)
conn.close()