import os
import json
import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://www.spreadthesign.com/es.es/search/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
OUTPUT_DIR = "videos"
INDEX_FILE = "index.json"
MAX_THREADS = 20
DELAY = 0.5

os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_video(word, video_url):
    clean_word = "".join(c if c.isalnum() else "_" for c in word)
    filepath = os.path.join(OUTPUT_DIR, f"{clean_word}.mp4")
    
    if os.path.exists(filepath): # Detiene la descarga de los videos que ya estén descargados
        return
    
    try:
        response = requests.get(video_url, headers=HEADERS, stream=True)
        response.raise_for_status()
        
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=16384):
                f.write(chunk)
        
        print(f"Video descargado: {word}")
    except Exception as e:
        print(f"Error al descargar el video: {word}: {e}")

def get_video_url(word):
    try:
        response = requests.get(BASE_URL, params={"cls": "2", "q": word}, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        video_tag = soup.find('video', class_='js-enforce-speed')
        
        return video_tag['src'] if video_tag and video_tag.get('src') else None
    except:
        return None

def process_word(word):
    video_url = get_video_url(word)
    if video_url:
        print(f"→ Video encontrado para: {word}")
        download_video(word, video_url)
        time.sleep(DELAY + random.uniform(0, 1))

def main():
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            words = json.load(f)
        words = list(set(w.strip().lower() for w in words if isinstance(w, str) and w.strip()))
    except:
        print(f"Error cargando {INDEX_FILE}")
        return
    
    print(f"Procesando {len(words)} palabras con {MAX_THREADS} hilos...")
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(process_word, word): word for word in words}
        for future in as_completed(futures):
            pass
    
    print("Descarga completada")

if __name__ == "__main__":
    main()