import re
import nltk
from databaseManager import Database

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class AnalizadorEspanol:
    def __init__(self):
        self.db = Database(
            host="localhost",
            database="palabras_db",
            user="postgres",
            password="postgres"
        )
    #Eliminar caracteres especiales y espacios innecesarios
    def limpiarTexto(self, texto):
        texto = texto.lower()
        texto = re.sub(r'[^\w\s]', '', texto)
        texto = re.sub(r'\s+', ' ', texto).strip()
        return texto
    
    #Separar el texto por palabras
    def separarPalabras(self, texto):
        textoLimpio = self.limpiarTexto(texto)
        return textoLimpio.split()
    
    #Llamar la función del databaseManager y buscar una coincidencia exacta
    def buscarCoincidenciaDirecta(self, palabra):
        resultado = self.db.buscarPalabra(palabra)
        if resultado:
            return {
                'palabra': resultado['palabra'],
                'porcentaje': float(resultado['porcentaje_identidad']),
                'tipo': 'directa',
                'encontrado': True
            }
        return None
    #Llamar la función del databaseManager y buscar coincidencia en sinonimos
    def buscarCoincidenciaSinonimo(self, palabra):
        resultados = self.db.buscarEnSinonimos(palabra)
        coincidencias = []

        for r in resultados:
            coincidencias.append({
                'palabra_original': r['palabra_original'],
                'palabra_buscada': palabra,
                'porcentaje': r['porcentaje'],
                'tipo': 'sinonimo',
                'encontrada': True
            })
        return coincidencias
    #Función para analizar el texto, calcular coincidencias más altas y 
    def analizarTexto(self, texto):
        palabras = self.separarPalabras(texto)
        totalPalabras = len(palabras)

        #En caso de no haber texto
        if totalPalabras == 0:
            return {
                'porcentaje_total': 0,
                'palabras_encontradas': 0,
                'palabras_totales': 0,
                'detalle': [],
                'pertenece_al_tema': False
            }

        coincidencias = []
        sumaPorcentaje = 0
        palabrasEncontradas = 0
        #Analizar cada palabra del texto ingresado
        for palabra in palabras:
            coincidenciaDirecta = self.buscarCoincidenciaDirecta(palabra)
            #En caso de existir una coincidencia exacta
            if coincidenciaDirecta:
                coincidencias.append(coincidenciaDirecta)
                palabrasEncontradas += 1
                sumaPorcentaje += coincidenciaDirecta['porcentaje']
            else:
                #Buscar en sinonimos
                coincidenciaSinonimo = self.buscarCoincidenciaSinonimo(palabra)
                #Seleccionar la coincidencia en sinonimo con porcentaje de relación más alto
                if coincidenciaSinonimo:
                    mejor = max(coincidenciaSinonimo, key=lambda x: x['porcentaje'])
                    coincidencias.append(mejor)
                    palabrasEncontradas += 1
                    sumaPorcentaje += mejor['porcentaje']
                else:
                    coincidencias.append({
                        'palabra': palabra,
                        'porcentaje': 0,
                        'tipo': 'no encontrado',
                        'encontrada': False
                    })
        #Cálculo del porcentaje final del análisis
        if totalPalabras > 0:
            porcentajeTotal = sumaPorcentaje / totalPalabras
        else:
            porcentajeTotal = 0
        #En caso de al menos tener 30% de coincidencia, se considera que el texto ingresado 
        #sí coincide con el tema 
        pertenece = porcentajeTotal >= 30

        return {
            'porcentaje_total': round(porcentajeTotal, 2),
            'palabras_encontradas': palabrasEncontradas,
            'palabras_totales': totalPalabras,
            'detalle': coincidencias,
            'pertenece_al_tema': pertenece,
            'texto_original': texto
        }