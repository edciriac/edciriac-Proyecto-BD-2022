from datetime import datetime
import locale
from multiprocessing.dummy import Array
from wsgiref import headers
from numpy import insert, source
from requests_html import HTMLSession
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
from utils import filter_persons
from insert_manual_mariadb import *
from config import *

#Formatear las fechas
def format_date(date):
    return(date.split("T")[0])

session = HTMLSession()

MEDIO_URL = "https://www.diariodepuertomontt.cl"
## URL "SEED" para hacer el crawling
URL_SEED = "https://www.diariodepuertomontt.cl/noticias/actualidad/"
## Analizar ("to parse") el contenido
xpath_url="//div[@class = 'col-md-5 col-5 m-0 px-3 py-2']//a/@href"


urls = ['https://www.diariodepuertomontt.cl/noticia/actualidad/2022/07/industria-del-salmon-avanza-en-pos-de-la-equidad-de-genero']
for i in range(0,2):
    seed = URL_SEED+str(i)
    response = session.get(seed,headers=headers)
    all_urls = response.html.xpath(xpath_url)
    all_urls = list(map(lambda url: MEDIO_URL + url, all_urls))

    # Usar este para solo crawl los primeros 3 urls
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

#---------------------------------------------------------
# Parte scraping:

xpath_title="//div//h1"
xpath_date="//div[@id ='printableArea']//small"
xpath_text="//div[@class='col-12 col-md-12 ck-content']//p"
xpath_categoria = ""

# Puede que esto retorne un error si no tienes el locale de es_ES.UTF-8 instalado a tu computador.
# Comprueba esto con el comando "locale -a" en terminal (Al menos esto funciona con mac)
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

# Formatear fecha de este tipo de secuencia 'Por Claudia Sep??lveda , 27 de junio de 2022 | 11:57'
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
    categoria = "Sin categor??a" #response.html.xpath(xpath_categoria)
    text=""
    for p in list_p:
        content = p.text
        content = w3lib.html.remove_tags(content)
        content = w3lib.html.replace_escape_chars(content)
        content = html.unescape(content)
        content = content.strip()
        text=text+" "+content

    insert_noticia(url,  date, title, categoria, text, MEDIO_URL)
    # Insertar las personas mencionadas en la noticia
    personas = filter_persons(content)
    for per in personas:
      insert_persona(per, url)
conn.close()