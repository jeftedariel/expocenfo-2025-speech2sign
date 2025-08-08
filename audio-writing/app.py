from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import speech_recognition as sr
from pydub import AudioSegment
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite peticiones desde el navegador

# Configuración
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'webm'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_audio_to_text(audio_path):
    recognizer = sr.Recognizer()

    print(f"Procesando: {audio_path}")

    # Forzar conversión usando ffmpeg con pydub
    try:
        sound = AudioSegment.from_file(audio_path, format="webm")

    except Exception as e:
        print("Error al leer el archivo con pydub:", e)
        return "No se pudo procesar el archivo de audio"

    wav_path = os.path.splitext(audio_path)[0] + '.wav'
    sound.export(wav_path, format="wav")
    audio_path = wav_path

    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='es-ES')
            return text
        except sr.UnknownValueError:
            return "No se pudo entender el audio"
        except sr.RequestError:
            return "Error al conectar con el servicio de reconocimiento"

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No se proporcionó archivo'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        text = convert_audio_to_text(filepath)

        # Limpieza
        try:
            os.remove(filepath)
            wav_version = os.path.splitext(filepath)[0] + '.wav'
            if os.path.exists(wav_version):
                os.remove(wav_version)
        except Exception:
            pass
        
        return jsonify({'text': text})
    
    return jsonify({'error': 'Tipo de archivo no permitido'}), 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=5000)