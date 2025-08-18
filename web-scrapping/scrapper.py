import os
import json
import requests
from bs4 import BeautifulSoup
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# Migrated to LESCO dictionary
BASE_URL = "https://lesco.cenarec.go.cr/DiccLESCO.php"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
OUTPUT_DIR = "videos"
INDEX_FILE = "querys.json"  
MAX_THREADS = 3  
DELAY = 0.2

os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_video(word, video_url):
    clean_word = "".join(c if c.isalnum() else "_" for c in word)
    filepath = os.path.join(OUTPUT_DIR, f"{clean_word}.mp4")
    
    if os.path.exists(filepath):  # Detiene la descarga de los videos que ya estén descargados
        print(f"El video ya se habia descargado: {word}")
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

def get_video_url(query_item):
    # Extract idw from query (e.g., "idw=45" -> "45")
    idw = query_item.split("=")[1] if "=" in query_item else query_item
    
    try:
        
        response = requests.get(BASE_URL, params={"idw": idw}, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Setea el nombre del archivo de video como el nombre de la palabra
        word_element = soup.find('h1')
        word_name = word_element.get_text().strip() if word_element else f"word_{idw}"
        
        video_div = soup.find('div', id='video')
        if not video_div:
            return word_name, None
            
        #  tag video/mp4 type
        source_tag = video_div.find('source', {'type': 'video/mp4'})
        if source_tag and source_tag.get('src'):
            video_src = source_tag['src']
            #  relative URL to absolute
            if video_src.startswith('/'):
                video_url = "https://lesco.cenarec.go.cr" + video_src
            else:
                video_url = video_src
            return word_name, video_url
        
        return word_name, None
    except:
        return None, None

def process_word(query_item):
    word_name, video_url = get_video_url(query_item)
    
    if video_url and word_name:
        print(f"→ Video encontrado para: {word_name}")
        download_video(word_name, video_url)
        time.sleep(DELAY + random.uniform(0, 1))

def main():
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            queries = json.load(f)
            
        queries = [q for q in queries if isinstance(q, str) and q.strip() and "idw=" in q]
    except:
        print(f"Error cargando {INDEX_FILE}")
        return
    
    print(f"Procesando {len(queries)} palabras con {MAX_THREADS} hilos...")
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(process_word, query): query for query in queries}
        for future in as_completed(futures):
            pass
    
    print("Descarga completada")

if __name__ == "__main__":
    main()