DROP TABLE IF EXISTS palabras;

CREATE TABLE palabras (
    id SERIAL PRIMARY KEY,
    palabra VARCHAR(50) NOT NULL,
    porcentaje_identidad NUMERIC(5,2),
    sinonimos TEXT
);

INSERT INTO palabras (palabra, porcentaje_identidad, sinonimos) VALUES
('escritura', 100, 'redacción, textos, escribir'),
('lectura', 90, 'leer, comprensión, interpretación, analisis'),
('gramatica', 100, 'sintaxis, morfología, idioma'),
('lenguaje', 95, 'idioma, comunicación, expresión, interpretación'),
('texto', 90, 'escritos, párrafo, documentos'),
('verbo', 80, 'acción, hacer, conjugación'),
('adjetivo', 60, 'descripción, característica, cualidad'),
('sustantivo', 75, 'nombre, cosa, persona, objeto'),
('signos', 70, 'puntuación, comas, puntos, comillas'),
('palabras', 85, 'vocabulario, frases, términos, ideas'),
('oraciones',80, 'frases, textos, párrafos'),
('ensayo', 65, 'texto largo, reflexión, opinión'),
('acentos', 80, 'tildes, pronunciación, énfasis, gramática'),
('cuento', 55, 'historia, relato, narración'),
('vocabulario', 85, 'léxico, palabras, terminología'),
('ortografía', 95, 'escritura correcta, acentuación, puntuación'),
('redacción',85, 'elaboración de textos, composición, escritura');


SELECT * FROM palabras;