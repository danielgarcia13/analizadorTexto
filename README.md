Resumen del proyecto: Este proyecto implementa un sistema que analiza un texto ingresado por el usuario y se encarga de determinar si el texto pertenece o está relacionado al tema principal ESPAÑOL, esto se calcula en base a un diccionario de palabras en una base de datos postgresSQL. Asímismo, implementa una interfaz construida con Streamlit y el backend en Python.


El proyecto se divide en tres modulos:

app.py se encarga del frontend con Streamlit: Recibe texto, envia texto al backedn y muestra resultados

backend.py se encarga de la lógica de analisis: Busca coincidencias en las palabras o sus sinonimos, calcula el porcentaje de relación al tema y define si pertenece o no

databaseManager.py se encarga de cargar los datos: conecta con la base de datos, recupera los registros
