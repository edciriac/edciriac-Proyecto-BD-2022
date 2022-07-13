import spacy

nlp = spacy.load("es_core_news_md")

def filter_persons(text):
  doc = nlp(text)
  # Filtrar todos otros entidades que los que tienen la etiqueta "PER" (person)
  entitys = list(filter(lambda ent: ent.label_ == "PER", doc.ents))
  # Sacar solo los textos de entidades
  persons = list(map(lambda entity: entity.text, entitys))
  # Eliminar duplicados
  persons = list(set(persons))
  return persons

# text = "Joseph Robinette Biden Jr. (Scranton, Pensilvania, 20 de noviembre de 1942), ( /dʒoʊ ˈbaɪdən/) es un político estadounidense que es el 46.º y actual presidente de los Estados Unidos."
# print(filter_persons(text))