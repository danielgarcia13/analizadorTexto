import streamlit as st
from backend import AnalizadorEspanol

@st.cache_resource
def cargar_analizador():
    return AnalizadorEspanol()

analizador = cargar_analizador()

st.title("Analizadr de palabras: Temática ESPAÑOL")
st.write("Ingrese una palabra o frase para analizar si pertenece al tema ESPAÑOL")

texto_usuario = st.text_input("Escribe una palabra o frase:")

if st.button("Analizar"):
    #En caso de no haber texto, solicitarlo al usuario
    if texto_usuario.strip() == "":
        st.warning("Por favor, escribe una palabra")
    #Leer el texto ingresado
    else:
        resultado = analizador.analizarTexto(texto_usuario)
        #Mostrar resultado
        st.subheader("Resultado General")
        st.write(f"**Porcentaje total:** {resultado['porcentaje_total']}%")
        st.write(f"**Palabras encontradas:** {resultado['palabras_encontradas']} / {resultado['palabras_totales']}")
        #Mensaje de éxito, palabra encontrada
        if resultado['pertenece_al_tema']:
            st.success("El texto está relacionado con el tema")
        #Mensaje de error, palabra no encontrada
        else:
            st.error("El texto NO está relacionado con el tema")

        st.subheader("Detalle de coincidencias")
        #Desplegar un json con los detalles del resultado
        for detalle in resultado["detalle"]:
            palabra_mostrar = detalle.get('palabra') or detalle.get('palabra_buscada')
            with st.expander(palabra_mostrar):
                st.json(detalle)