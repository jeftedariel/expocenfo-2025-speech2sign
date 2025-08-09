import os  
import json  

def get_videos():
    try:
        videos = [entry.name[:-4] for entry in os.scandir("videos")  # Esto se hace para quitar guardar el nombre de la palabra sin la extensión mp4
                  if entry.is_file() and entry.name.endswith('.mp4')]  # Filtra solo archivos que terminen en '.mp4'
        
        data = {  
            "total_palabras": len(videos), 
            "palabras": videos 
        }
        
        with open("videos_disponibles.json", 'w', encoding='utf-8') as f:  # Abre el archivo JSON para escritura con codificación UTF-8
            json.dump(data, f, indent=4, ensure_ascii=False)  # Guarda 'data' en formato JSON
        
        print(f"Guardados {len(videos)} videos en 'videos_disponibles.json'")  
        
    except FileNotFoundError:  
        print("Error: Carpeta 'videos' no existe")
    except PermissionError:  
        print("Error: Sin permisos para escribir archivo")

if __name__ == "__main__":  
    get_videos(), 