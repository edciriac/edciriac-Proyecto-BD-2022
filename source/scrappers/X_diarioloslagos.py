from wsgiref import headers
from requests_html import HTMLSession
from pymongo import MongoClient
import time
from nav_config import USER_AGENT_LIST, headers

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

for i in range(1,3):
    seed = URL_SEED+str(i)
    print(seed)
    response = session.get(seed,headers=headers)
    print(response)
    all_urls = response.html.xpath(xpath_url)

    for url in all_urls:
        print(url)
        article_url = url

        #Insert into mongo
        news = {'url':article_url,'to_download':True}
        result=db.urls.insert_one(news)

    time.sleep(2)