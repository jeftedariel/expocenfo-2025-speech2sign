import time
import array
import math
import board
import analogio
import struct
from ideaboard import IdeaBoard


# Configuración del micrófono
MIC_PIN = board.IO27
SAMPLE_RATE_HZ = 5000     # Valor deseado (aprox)
RECORD_SECONDS = 10
ib = IdeaBoard()

BUFFER_SIZE = SAMPLE_RATE_HZ * RECORD_SECONDS

# Buffer para audio (16 bits)
audio_buffer = array.array('H', (0 for _ in range(BUFFER_SIZE)))

print("Inicializando ADC...")
adc = analogio.AnalogIn(MIC_PIN)

print(f"Iniciando grabación de {RECORD_SECONDS} segundos (objetivo {SAMPLE_RATE_HZ} Hz)...")
print("Por favor, hable ahora...")

# Inicia grabación y mide tiempo real
t_start = time.monotonic()
ib.pixel=(0,0,255)
for i in range(BUFFER_SIZE):
    audio_buffer[i] = adc.value
    time.sleep(1.0 / SAMPLE_RATE_HZ)
t_end = time.monotonic()
ib.pixel=(0,0,0)
# Calcular frecuencia real
frecuencia_real = BUFFER_SIZE / (t_end - t_start)
print(f"\nGrabación finalizada. Frecuencia real: {frecuencia_real:.2f} Hz")

# Guardar como archivo WAV
def guardar_wav(nombre_archivo, muestras, sample_rate):
    with open(nombre_archivo, "wb") as f:
        # Cabecera WAV
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + len(muestras) * 2))
        f.write(b"WAVEfmt ")
        f.write(struct.pack("<I", 16))  # Subchunk1Size
        f.write(struct.pack("<H", 1))   # AudioFormat PCM
        f.write(struct.pack("<H", 1))   # NumChannels (mono)
        f.write(struct.pack("<I", int(sample_rate)))
        f.write(struct.pack("<I", int(sample_rate) * 2))  # ByteRate
        f.write(struct.pack("<H", 2))   # BlockAlign
        f.write(struct.pack("<H", 16))  # BitsPerSample
        f.write(b"data")
        f.write(struct.pack("<I", len(muestras) * 2))

        # Escribir datos (unsigned 16-bit → signed 16-bit)
        for m in muestras:
            pcm_val = m - 32768
            f.write(struct.pack("<h", pcm_val))

# Usar frecuencia real para que el audio no se acelere
guardar_wav("/grabacion.wav", audio_buffer, frecuencia_real)

print("Grabación guardada como grabacion.wav")

