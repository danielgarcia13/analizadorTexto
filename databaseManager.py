import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self, host="localhost", database="palabras_db", user="postgres", password="postgres", port="5432"):
        #Inicia la conexión a la base de datos
        self.parametrosConexion = {
            "host": host,
            "database": database,
            "user": user,
            "password": password,
            "port": port
        }
    #Establecer conexion con la base de datos
    def hacerConexion(self):
        return psycopg2.connect(**self.parametrosConexion)
    #Obtener palabras de la base de datos mediante una consulta
    def obtenerPalabras(self):
        conn = self.hacerConexion()
        cursor = conn.cursor(cursor_factory=RealDictCursor) 

        try:
            cursor.execute("SELECT * FROM palabras")
            palabras = cursor.fetchall()
            return palabras
        finally:
            cursor.close()
            conn.close()
    #Buscar en la base de datos si existe la palabra
    def buscarPalabra(self, palabra):
        conn = self.hacerConexion()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            query = "SELECT * FROM palabras WHERE LOWER(palabra) = LOWER(%s)"
            cursor.execute(query, (palabra,))
            resultado = cursor.fetchone()
            return resultado   
        finally:   
            cursor.close()
            conn.close()
    #Si la palabra no existe directamente, buscarla en los sinonimos 
    def buscarEnSinonimos(self, palabra):
        conn = self.hacerConexion()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        palabra = palabra.lower().strip()

        try:
            cursor.execute("SELECT * FROM palabras")
            resultados_raw = cursor.fetchall()

            coincidencias = []

            for r in resultados_raw:
                # Convertir los sinonimos a una lista limpia
                lista_sin = [s.strip().lower() for s in r["sinonimos"].split(",")]

                # En caso de coincidencia
                if palabra in lista_sin:
                    porcentajeFinal = float(r["porcentaje_identidad"]) * 0.85

                    coincidencias.append({
                        'palabra_original': r['palabra'],
                        'palabra_buscada': palabra,
                        'porcentaje': round(porcentajeFinal, 2),
                        'tipo': 'sinonimo',
                        'encontrada': True
                    })

            return coincidencias
    
        finally:
            cursor.close()
            conn.close()