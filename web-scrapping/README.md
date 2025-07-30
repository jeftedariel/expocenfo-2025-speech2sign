# WebScrapping Script

Para obtener algunos videos en lenguaje de señas creamos un script para descargar todos los videos que tenia una web disponibles.

Para el listado de palabras hicimos uso de un json que se encuentra en el repositorio: ![words/an-array-of-spanish-words](https://github.com/words/an-array-of-spanish-words/blob/master/index.json)

---

## ¿Cómo funciona?

Tomando por base_url la de SpreadTheSign en la que ellos realizan la busqueda de palabras en español, comenzamos a concatenar las palabras que tomamos del ``` index.json ```

Luego el script comienza a probar de 30 en 30, las que sí existen y contienen un <video> lo intentará descargar y guardar en /videos


Luego podemos almacenar un json con  los videos que se obtuvieron corriendo el script ``` reader.py ```

---

## Dependencias de Python

1. BeautifulSoup4
2. requests
3. loggin
4. concurrent.futures

---
