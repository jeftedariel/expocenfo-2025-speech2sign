import os
import json

def get_videos():
    # Configuración
    videos_dir = "videos"
    output_file = "videos_disponibles.json"
    
    # Verificar si la carpeta existe
    if not os.path.exists(videos_dir):
        print(f"Error: La carpeta '{videos_dir}' no existe.")
        return
    
    # Obtener todos los archivos en la carpeta (excluyendo subdirectorios)
    video_files = [f for f in os.listdir(videos_dir) 
                  if os.path.isfile(os.path.join(videos_dir, f))]
    
    # Extraer nombres sin extensión
    videos = [os.path.splitext(f)[0] for f in video_files]
    
    # Crear estructura JSON
    result = {
        "total_videos": len(videos),
        "videos": videos
    }
    
    # Guardar como JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"Se han guardado {len(videos)} nombres en '{output_file}'")

if __name__ == "__main__":
    get_videos()