import wikipedia
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from transformers import pipeline
wikipedia.set_lang("es")


def getDataPersona(person):
    try:
        infoWiki = wikipedia.summary(person, sentences=3)
        ES_MODEL_LANGUAGE="mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es"
        tokenizer_es_language = AutoTokenizer.from_pretrained(ES_MODEL_LANGUAGE)
        model_es_language = AutoModelForQuestionAnswering.from_pretrained(ES_MODEL_LANGUAGE)
        q_a_es = pipeline("question-answering", model=model_es_language, tokenizer=tokenizer_es_language)
        result = q_a_es(question="¿Cuál es su profesión?", context=infoWiki)
        print(result["answer"])
        result = q_a_es(question="¿En qué año nació el o ella?", context=infoWiki)
        print(result["answer"])
    except:
        print("Persona no encontrada en Wikipedia")

