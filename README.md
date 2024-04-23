# Cifrados clásicos
### Criptografía y Seguridad 2024-2. Tarea 1
### Equipo DinamitaBB. 
#### Integrantes
- Flores Ayala Luis Edgar. 317251340
- Robles Huerta Rosa Maria. 317061521
- Sánchez Reza Neider. 317020931
- Sánchez Velasco Eduardo Leonel. 420004035

## Requerimientos
Se requiere `Python3` instalado. La instalación viene incluída en distribuciones Linux basadas en `Ubuntu`.

## Cómo ejecutar
Para ejecutar el programa, basta con ejecutar el _script_ `cifrados.py`, ubicado en el directorio `src/` de este proyecto, de la siguiente manera:

    python3 cifrados.py
    
El programa entonces mostrará los resultados de las estadísticas relacionadas con los cifrados monoalfabético y polialfabético, realizado sobre una noticia en español del 2024. El archivo de texto correspondiente con la noticia se encuentra en los archivos `Texto1.txt` y `Texto2.txt`, en el directorio `data/`.

## Descripción del programa
Dentro del directorio `src/` se encuentra todo el código necesario para desarrollar la tarea:
- El archivo `monoalfabetico.py` contiene todas las funciones necesarias para llevar a cabo el cifrado de un texto por medio de una función afín. Se incluyen funciones auxiliares para la aritmética modular, así como para realizar el criptoanálisis (cálculo de frecuencias).
- El archivo `polialfabetico.py` contiene todas las funciones necesarias para llevar a cabo el cifrado de un texto por medio del cifrado de Vigenère. Se incluyen funciones auxiliares para realizar el criptoanálisis, como calcular el índice de coincidencias, calcular subcadenas repetidas, sus distancias y los factores primos de dichas distancias.
- El archivo `cifrados.py` utiliza las funciones definidas en los archivos anteriores para realizar el cifrado y análisis de una noticia. 
 
En el caso del archivo `cifrados.py`, el _script_ se encuentra dividido en dos secciones:
1. Cifrado monoalfabético. La noticia leída del archivo `data/Texto1.txt` se cifra usando la función afín $f(x)=19x+2$. El criptograma resultante se escribe en el archivo `data/Criptograma1.txt`.  
Se realiza además el cálculo de frecuencias de cada letra del texto plano y cifrado, así como el cálculo del índice de coincidencias.
2. Cifrado polialfabético. La noticia leída del archivo `data/Texto2.txt` se cifra con Vigenère, usando la clave `dinamitabb`. El criptograma resultante se escribe en el archivo `data/Criptograma2.txt`.  
Se realiza además el cálculo de frecuencias de cada letra del texto plano y cifrado, así como el cálculo del índice de coincidencias y los factores primos de las distancias entre subcadenas repetidas del texto plano y cifrado.
