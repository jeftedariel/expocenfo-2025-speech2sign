import time
import array
import math
import board
import analogio
import struct
from ideaboard import IdeaBoard

# Configuración del micrófono
MIC_PIN = board.IO27
SAMPLE_RATE_HZ = 16000
RECORD_SECONDS = 15
CHUNK_SIZE = 1024  # Buffer circular

ib = IdeaBoard()

ARCHIVO_SALIDA = "/grabacion.wav"

# 2KB en RAM
audio_buffer = array.array('H', (0 for _ in range(CHUNK_SIZE)))

print("Inicializando ADC...")
adc = analogio.AnalogIn(MIC_PIN)
print(f"Iniciando grabación de {RECORD_SECONDS} segundos a {SAMPLE_RATE_HZ} Hz...")
print("Por favor, hable ahora...")

def escribir_cabecera_wav(f, total_muestras, sample_rate):
    f.write(b"RIFF")
    f.write(struct.pack("<I", 36 + total_muestras * 2))  # Tamaño total
    f.write(b"WAVEfmt ")
    f.write(struct.pack("<I", 16))  # Subchunk1Size
    f.write(struct.pack("<H", 1))   # AudioFormat PCM
    f.write(struct.pack("<H", 1))   # NumChannels (mono)
    f.write(struct.pack("<I", int(sample_rate)))  # SampleRate
    f.write(struct.pack("<I", int(sample_rate) * 2))  # ByteRate
    f.write(struct.pack("<H", 2))   # BlockAlign
    f.write(struct.pack("<H", 16))  # BitsPerSample
    f.write(b"data")
    f.write(struct.pack("<I", total_muestras * 2))

def escribir_chunk_audio(f, chunk_buffer, muestras_en_chunk):
    pcm_data = array.array('h', (chunk_buffer[i] - 32768 for i in range(muestras_en_chunk))) # Conversión optimizada: unsigned 16-bit → signed 16-bit
    f.write(pcm_data.tobytes())

def grabar_con_buffer_circular():
    total_muestras = SAMPLE_RATE_HZ * RECORD_SECONDS
    chunks_totales = (total_muestras + CHUNK_SIZE - 1) // CHUNK_SIZE # División con redondeo hacia arriba
    muestras_grabadas = 0
    
    try:
        with open(ARCHIVO_SALIDA, "wb") as f:
            escribir_cabecera_wav(f, total_muestras, SAMPLE_RATE_HZ)
            
            t_start = time.monotonic_ns()
            ib.pixel = (0, 0, 255)  
            
            for chunk_num in range(chunks_totales):
                muestras_restantes = total_muestras - muestras_grabadas # Calcular muestras en este chunk
                muestras_en_chunk = min(CHUNK_SIZE, muestras_restantes)
                
                for i in range(muestras_en_chunk): # Llenar buffer circular
                    audio_buffer[i] = adc.value
                
                # Escribir chunk inmediatamente al archivo
                escribir_chunk_audio(f, audio_buffer, muestras_en_chunk)
                
                muestras_grabadas += muestras_en_chunk
            
            t_end = time.monotonic_ns()
            ib.pixel = (0, 0, 0) 
            
        return muestras_grabadas, (t_end - t_start) / 1_000_000_000
        
    except OSError as e:
        print(f"Error escribiendo archivo: {e}")
        ib.pixel = (255, 0, 0) 
        return 0, 0

def actualizar_cabecera_wav(muestras_reales, frecuencia_real):
    try:
        with open(ARCHIVO_SALIDA, "r+b") as f:
            f.seek(4) # Actualizar tamaño total del archivo
            f.write(struct.pack("<I", 36 + muestras_reales * 2))
            
            f.seek(24) # Actualizar sample rate real
            f.write(struct.pack("<I", int(frecuencia_real)))
            f.write(struct.pack("<I", int(frecuencia_real) * 2))  # ByteRate
            
            f.seek(40) # Actualizar tamaño de datos
            f.write(struct.pack("<I", muestras_reales * 2))
            
    except OSError as e:
        print(f"Advertencia: No se pudo actualizar cabecera: {e}")

print("=== INICIO DE GRABACIÓN ===")
muestras_grabadas, tiempo_real = grabar_con_buffer_circular()

if muestras_grabadas > 0:
    frecuencia_real = muestras_grabadas / tiempo_real
    actualizar_cabecera_wav(muestras_grabadas, frecuencia_real)
    
    print(f"\n=== GRABACIÓN COMPLETADA ===")
    print(f"Muestras grabadas: {muestras_grabadas:,}")
    print(f"Tiempo real: {tiempo_real:.3f} segundos")
    print(f"Frecuencia real: {frecuencia_real:.2f} Hz")
    print(f"Frecuencia objetivo: {SAMPLE_RATE_HZ} Hz")
    print(f"Precisión: {(frecuencia_real/SAMPLE_RATE_HZ)*100:.1f}%")
    print(f"Tamaño archivo: {(muestras_grabadas * 2 + 44)} bytes")
    print(f"Memoria RAM usada: ~{CHUNK_SIZE * 2} bytes")
    print(f"Archivo guardado: {ARCHIVO_SALIDA}")
    
    if abs(frecuencia_real - SAMPLE_RATE_HZ) / SAMPLE_RATE_HZ < 0.05: 
        ib.pixel = (0, 255, 0) 
        print("✅ Calidad de grabación: EXCELENTE")
    else:
        ib.pixel = (255, 255, 0)  
        print("⚠️  Calidad de grabación: ACEPTABLE (diferencia >5%)")
    
    time.sleep(2)
    ib.pixel = (0, 0, 0) 
    
else:
    print("❌ Error: No se pudo completar la grabación")
    
print("=== PROGRAMA FINALIZADO ===")