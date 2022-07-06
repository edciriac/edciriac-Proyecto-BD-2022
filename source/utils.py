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
