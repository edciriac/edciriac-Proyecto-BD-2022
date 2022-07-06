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
from datetime import datetime
import locale

# Importar de la carpeta source
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from utils import filter_persons
from insert_manual_mariadb import *
from config import *

session = HTMLSession()

MEDIO_URL = "https://www.noticiaschiloe.cl"
## URL "SEED" para hacer el crawling
URL_SEED = "https://www.noticiaschiloe.cl/category/politica-y-economia"
## Analizar ("to parse") el contenido
xpath_url="//h3[@class='entry-title mh-loop-title']/a/@href" # 



urls = []

# Loop las páginas
for i in range(0,2):
    seed = URL_SEED+f"/page/{i+1}" 
    print(seed)
    response = session.get(seed,headers=headers)
    all_urls = response.html.xpath(xpath_url)
    # all_urls = list(map(lambda url: MEDIO_URL + url, all_urls))
    all_urls = response.html.xpath(xpath_url)
    print(len(all_urls))
    time.sleep(3)

    # Usar este para solo crawl los primeros 3 urls
    for i in range(1,3):
        print("crawl number:", {i} )
        print(all_urls[i])
        article_url = all_urls[i]
        urls.append(article_url)
        

    # Usar este codigo abajo para crawl todos los urls de esa pagina
    # for url in all_urls: 
    #     print(url)
    #     article_url = url

    #     urls.append(article_url)

    time.sleep(3)

#---------------------------------------------------------
# Parte scraping:

xpath_title="//div[@class='mh-content']//h1"
xpath_date="//div[@class='mh-content']//a"
xpath_text="//div[@class='entry-content mh-clearfix']//p"
xpath_categoria = ""

# Puede que esto retorne un error si no tienes el locale de es_ES.UTF-8 instalado a tu computador.
# Comprueba esto con el comando "locale -a" en terminal (Al menos esto funciona con mac)
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

# Formatear las fechas, desde texto como: Miércoles, 1 Junio, 2022 a las 11:42
def format_date(date):
    date = date.split(", ", maxsplit = 1)[1]
    print(date)
    date = date.split("a las")[0]
    date = date.strip()
    return(datetime.strptime(date, '%d %B, %Y').strftime('%Y-%m-%d'))

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
    print("Iniciciando el scrape para url: " + url)
    ## URL que escrapear
    URL = url
    response = session.get(URL,headers=headers)    

    ## Analizar el contenido
    title = response.html.xpath(xpath_title)[0].text
    print("title:")
    print(response.html.xpath(xpath_title)[0].text)
    print("Date:")
    print(response.html.xpath(xpath_date)[0].text)
    date = format_date(response.html.xpath(xpath_date)[0].text)
    list_p = response.html.xpath(xpath_text)
    #TODO: escrapear la categoria 
    categoria = "Sin categoría" #response.html.xpath(xpath_categoria)
    content=""
    for p in list_p:
        text = p.text
        text = w3lib.html.remove_tags(text)
        text = w3lib.html.replace_escape_chars(text)
        text = html.unescape(text)
        text = text.strip()
        content = content +" "+text
    

    insert_noticia(url,  date, title, categoria, text, MEDIO_URL)
    # Insertar las personas mencionadas en la noticia
    personas = filter_persons(content)
    for per in personas:
      insert_persona(per, url)
conn.close()