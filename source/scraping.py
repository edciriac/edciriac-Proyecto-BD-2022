import random
from requests_html import HTMLSession
import w3lib.html
import html
from pymongo import MongoClient
import mariadb
import sys
import time

def format_date(date):
        return(date.split("T")[0])

session = HTMLSession()

xpath_title="//div//h1"
xpath_date="//meta[@property='article:published_time']//@content"
xpath_text="//div[@class='abody-basic']//p"


#Conectarse a Mongo para listar las URLs que escrapear
client = MongoClient("localhost", port=27017)
db=client.info133_2022

# Conectarse a MariaDB para guardar los datos escrapeados
try:
    conn = mariadb.connect(
        user="estefano",
        password="espinoza",
        host="localhost",
        port=3306,
        database="info133_2022"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

#Listar las URLs que escrapear
for doc in db.urls.find({"to_download":True}).limit(2):
    print(doc["url"])

    ## URL que escrapear
    URL = doc["url"]

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
    query= f"INSERT INTO news (url,title,date,content) VALUES ('{URL}', '{title}', '{date}', '{text}')"

    cur.execute(query)
    conn.commit()
    time.sleep(1)

conn.close()