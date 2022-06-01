from insert_manual import *
import datetime

# Usar los metodos de insert_manual para inicializar el base da datos

result_dueno = insert_dueno("Claudio Marquez Maragaño", datetime.datetime(2005, 4, 1), "Persona natural")
print("Se insertó un dueño: ", result_dueno)

# Dueno ids (solo una) del resultado del inserción anterior
result_medio = insert_medio("Chilevision", "www.elcalbucano.cl", "Puerto Montt", "Espanol", [result_dueno.inserted_id])
print("Se insertó un medio: ", result_medio)

result_noticia = insert_noticia("TELETÓN SUMA NUEVO Y MODERNO ROBOT PARA REHABILITAR A PACIENTES",
                                "https://www.elcalbucano.cl/2022/04/teleton-suma-nuevo-y-moderno-robot-para-rehabilitar-a-pacientes/",
                                datetime.datetime(2022, 4, 17),
                                "Salud",
                                "Se llama Andago y se utilizará...",
                                result_medio.inserted_id # medio_id del resultado del inserción anterior
                                )
print("Se insertó un noticia: ", result_noticia)

result_citado = insert_citado("Pedro caro", [result_noticia.inserted_id])
print("Se insertó un citado: ", result_citado)

print("Todos inserciónes se insertaron exitosamente. Terminando el programa...")
