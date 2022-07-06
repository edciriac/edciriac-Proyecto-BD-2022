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
import insert_manual_mariadb
from config import *

session = HTMLSession()

MEDIO_URL = "https://laopiniondechiloe.cl"
## URL "SEED" para hacer el crawling
URL_SEED = "http://laopiniondechiloe.cl/category/politica/"
## Analizar ("to parse") el contenido
xpath_url="//h3[@class='entry-title mh-posts-list-title']/a/@href" #Da un url completo


urls = []#['http://laopiniondechiloe.cl/cadem-rechazo-en-plebiscito-de-salida-llega-al-51-y-desconfianza-en-convencion-llega-al-58/']

# Loop las páginas
for i in range(0,1):
    seed = URL_SEED+f"page/{i}" 
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
xpath_text="//div[@class='mh-content']//p"
xpath_categoria = ""

# Puede que esto retorne un error si no tienes el locale de es_ES.UTF-8 instalado a tu computador.
# Comprueba esto con el comando "locale -a" en terminal (Al menos esto funciona con mac)
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')


# Formatear las fechas, desde texto como: junio 27, 2022
def format_date(date):
    return(datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d'))

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

    insert_manual_mariadb.insert_noticia(url,  date, title, categoria, text, MEDIO_URL)
conn.close()