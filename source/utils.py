import spacy

nlp = spacy.load("es_core_news_md")

def filter_persons(text):
  doc = nlp(text)
  # Filtrar todos otros entidades que los que tienen la etiqueta "PER" (person)
  persons = list(filter(lambda ent: ent.label_ == "PER", doc.ents))
  return persons
