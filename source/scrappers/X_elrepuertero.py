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

MEDIO_URL = "https://www.elrepuertero.cl"
## URL "SEED" para hacer el crawling
URL_SEED = "https://www.elrepuertero.cl/economia"
## Analizar ("to parse") el contenido
xpath_url="//div[@class = 'node']/a/@href"

## Para scraping
xpath_title="//div//h1"
xpath_date="//meta[@property='article:published_time']//@content"
xpath_text="//div[@class='content content-node']//p"
xpath_categoria = "//div[@class='terms terms-top']/ul/li[1]/a"

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

#---------------------------------------------------------
# Parte scraping:
def format_date(date):
        return(date.split("T")[0])


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
    date = format_date(response.html.xpath(xpath_date)[0])
    list_p = response.html.xpath(xpath_text)
    #TODO: escrapear la categoria 
    categoria = "" #response.html.xpath(xpath_categoria)
    text=""
    for p in list_p:
        content = p.text
        content = w3lib.html.remove_tags(content)
        content = w3lib.html.replace_escape_chars(content)
        content = html.unescape(content)
        content = content.strip()
        text=text+" "+content

    insert_manual_mariadb.insert_noticia(url,  date, title, categoria, text, MEDIO_URL)
conn.close()