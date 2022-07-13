#pip install git+https://github.com/Commonists/pageview-api.git
#pip install transformers
# o pip install transformers[torch]
import pageviewapi
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from transformers import pipeline

def extraer_popularidad(nombre, fecha_inicio, fecha_fin):
    result=pageviewapi.per_article('es.wikipedia', nombre, fecha_inicio, fecha_fin,
                        access='all-access', agent='all-agents', granularity='monthly')

    for item in result.items():
        for article in item[1]:
            timestamp=article['timestamp'][:8] #first 8 digits
            views=article['views']
            print(timestamp)
            print(views)
    return result

ES_MODEL_LANGUAGE="mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es"
tokenizer_es_language = AutoTokenizer.from_pretrained(ES_MODEL_LANGUAGE)
model_es_language = AutoModelForQuestionAnswering.from_pretrained(ES_MODEL_LANGUAGE)
q_a_es = pipeline("question-answering", model=model_es_language, tokenizer=tokenizer_es_language)

def extraer_fecha_de_nacimiento(contenido):
    result = q_a_es(question="¿En qué año nació el o ella?", context=contenido)
    fecha = result["answer"]
    print(fecha)
    return fecha

def extraer_nacionalidad(contenido):
    result = q_a_es(question="¿Cuál es su nacionalidad?", context=contenido)
    nacionalidad = result["answer"]
    print(nacionalidad)
    return nacionalidad

# extraer_popularidad("Joe Biden" ,"20200701", "20220705")
extraer_nacionalidad("""Joseph Robinette Biden Jr. (Scranton, Pensilvania, 20 de noviembre de 1942), ( /dʒoʊ ˈbaɪdən/) 
    es un político estadounidense que es el 46.º y actual presidente de los Estados Unidos.""")
extraer_fecha_de_nacimiento("""Joseph Robinette Biden Jr. (Scranton, Pensilvania, 20 de noviembre de 1942), ( /dʒoʊ ˈbaɪdən/) 
    es un político estadounidense que es el 46.º y actual presidente de los Estados Unidos.""")

