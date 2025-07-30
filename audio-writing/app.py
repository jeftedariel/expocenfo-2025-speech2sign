from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import speech_recognition as sr
from pydub import AudioSegment
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Esto permite peticiones desde cualquier origen (útil para desarrollo)

# Configuración
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear directorio si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    
    # Convertir a WAV si es necesario (SpeechRecognition funciona mejor con WAV)
    if audio_path.lower().endswith(('.mp3', '.ogg', '.flac')):
        sound = AudioSegment.from_file(audio_path)
        wav_path = os.path.splitext(audio_path)[0] + '.wav'
        sound.export(wav_path, format="wav")
        audio_path = wav_path
    
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='es-ES')  # Cambia el idioma según necesites
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
        
        # Limpiar: eliminar archivos temporales
        os.remove(filepath)
        if filepath.lower().endswith('.wav') and not file.filename.lower().endswith('.wav'):
            os.remove(filepath)
        
        return jsonify({'text': text})
    
    return jsonify({'error': 'Tipo de archivo no permitido'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)