# WebScrapping Script

Para obtener algunos videos en lenguaje de señas creamos un script para descargar todos los videos que tenia una web disponibles.

Para el listado de palabras hicimos un escaneo de las palabras disponibles en el sitio web del Cenarec y las almacenamos en un json (querys.json)

---

## ¿Cómo funciona?

Tomando por base_url la de Cenarec en la que ellos realizan la busqueda de palabras, comenzamos a concatenar las palabras que tomamos del ``` querys.json ```

Luego el script comienza a probar por chuncks o trozos del archivo, las que sí existen y contienen un <video> lo intentará descargar y guardar en /videos, colocando por nombre lo que contenia el <h1> 

Luego podemos almacenar un json con  los videos que se obtuvieron corriendo el script ``` reader.py ```

---

## Dependencias de Python

1. BeautifulSoup4
2. requests
3. loggin
4. concurrent.futures

---
