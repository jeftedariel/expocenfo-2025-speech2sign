from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import json
import webbrowser
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'webm', 'mp4', 'm4a'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configurar Gemini API

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '*')
genai.configure(api_key=GEMINI_API_KEY)

# Cargar palabras permitidas
with open("palabras.json", "r", encoding="utf-8") as f:
    PALABRAS_DISPONIBLES = json.load(f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_audio_to_text_with_gemini(audio_path):
    try:
        audio_file = genai.upload_file(path=audio_path)
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        prompt = (
            "Transcribe el audio a texto utilizando UNICAMENTE las palabras que se encuentran "
            "en la siguiente lista JSON, esta lista representa videos en LENGUAJE DE Señas. No inventes palabras que no estén en la lista, si alguna palabra no se encuentra en la lista, utiliza alguna similar que sí se encuentre para dar sentido a la frase, si se trata de un nombre propio, deberas deletrearlo utilizando las letras de la lista.\n\n"
            "La respuesta debe ser únicamente una URL en el formato exacto: "
            "http://127.0.0.1:5500/index.html?lista=[] — dentro de los [] deben ir las palabras "
            "transcritas, separadas por comas y entre comillas, todas en MAYUSCULA CONSERVANDO EL MISMO FORMATO EN QUE VENIAN EN EL JSON.\n\n"
            f"Lista de palabras permitidas (JSON): {json.dumps(PALABRAS_DISPONIBLES, ensure_ascii=False)}"
        )
        
        
        response = model.generate_content([prompt, audio_file])
        url = response.text.strip()  # Ahora se espera que sea solo la URL
        
        genai.delete_file(audio_file.name)
        return url
        
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No se proporcionó archivo'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400
    
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(filepath)
        
        url = convert_audio_to_text_with_gemini(filepath)
        

        
        # Abrir la URL directamente
        print(f"Abriendo en navegador: {url}")
        webbrowser.open(url)
        
        return jsonify({'url': url})
    
    return jsonify({'error': 'Tipo de archivo no permitido'}), 400

@app.route('/health', methods=['GET'])
def health_check():
    
    return jsonify({'status': 'API funcionando correctamente'})


if __name__ == '__main__':
    
    app.run(debug=True, host="0.0.0.0", port=5000)
