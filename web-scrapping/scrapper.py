import os
import json
import requests
from bs4 import BeautifulSoup
import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuración
BASE_URL = "https://www.spreadthesign.com/es.es/search/"
PARAMS = {"cls": "2"}  # cls=2 para palabras
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
OUTPUT_DIR = "videos"
DELAY = 0.2  # Delay base entre descargas
INDEX_FILE = "index.json"
MAX_THREADS = 30  # Cambia este valor según el número de hilos que desees
LOG_FILE = "log.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()  # Saca el log a la term
    ]
)

def download_video(word, video_url):
    try:
        clean_word = "".join(c if c.isalnum() else "_" for c in word)
        filename = f"{clean_word}.mp4"
        filepath = os.path.join(OUTPUT_DIR, filename)

        if os.path.exists(filepath):
            logging.info(f"[+] '{word}' ya existe. Saltando.")
            return

        logging.info(f"[>] Descargando '{word}'...")
        response = requests.get(video_url, headers=HEADERS, stream=True)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logging.info(f"[v] Descargado '{word}'.")
    except Exception as e:
        logging.error(f"[-] Error con '{word}': {e}")

def get_video_url(word):
    try:
        params = PARAMS.copy()
        params["q"] = word
        response = requests.get(BASE_URL, params=params, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        video_tag = soup.find('video', class_='js-enforce-speed')

        if video_tag and video_tag.get('src'):
            return video_tag['src']

        logging.warning(f"[-] No se encontró video para '{word}'")
        return None
    except Exception as e:
        logging.error(f"[-] Error buscando '{word}': {e}")
        return None

def load_words_from_index():
    if not os.path.exists(INDEX_FILE):
        logging.error(f"No se encontró el archivo {INDEX_FILE}")
        return []

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        try:
            words = json.load(f)
            return sorted(set(w.strip().lower() for w in words if isinstance(w, str)))
        except Exception as e:
            logging.error(f"Error leyendo {INDEX_FILE}: {e}")
            return []

def process_word(word):
    video_url = get_video_url(word)
    if video_url:
        download_video(word, video_url)
    time.sleep(DELAY + random.uniform(0, 1))  # Espera entre hilos

def main():
    words = load_words_from_index()

    if not words:
        logging.error("No hay palabras para procesar.")
        return

    logging.info(f"Procesando {len(words)} palabras con hasta {MAX_THREADS} hilos...\n")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(process_word, word): word for word in words}
        for future in as_completed(futures):
            pass  

    logging.info("\nDescarga completada.")

if __name__ == "__main__":
    main()
