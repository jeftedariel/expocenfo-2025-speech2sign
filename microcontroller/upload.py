import wifi
import socketpool
import gc
import time

from ideaboard import IdeaBoard


# Configuración WiFi
WIFI_SSID = "UTN"
WIFI_PASSWORD = None

# Configuración del endpoint
IP_ADDRESS = "10.60.40.79"
PORT = 5000
ENDPOINT_URL = "/transcribe"
AUDIO_FILE = "grabacion.wav"
CHUNK_SIZE = 1024  

ib = IdeaBoard()

class SimpleAudioUploader:
    def __init__(self):
        self.pool = None
        
    def connect_wifi(self):
        """Conecta a WiFi"""
        print("Conectando a WiFi...")
        try:
            wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
            print(f"Conectado a {WIFI_SSID}")
            print(f"IP: {wifi.radio.ipv4_address}")
            
            self.pool = socketpool.SocketPool(wifi.radio)
            return True
            
        except Exception as e:
            print(f"Error conectando WiFi: {e}")
            return False
    
    def get_file_size(self, filename):
        """Obtiene el tamaño del archivo"""
        try:
            import os
            stat = os.stat(filename)
            return stat[6]  # st_size
        except Exception as e:
            print(f"Error obteniendo tamaño del archivo: {e}")
            return None
    
    def send_audio_raw(self):
        """Método RAW eliminado - no compatible con Flask que espera multipart"""
        return False

    def send_audio(self):
        """Envía el archivo de audio - versión super simplificada"""
        
        # Verificar archivo
        file_size = self.get_file_size(AUDIO_FILE)
        if file_size is None:
            return False
            
        print(f"Enviando archivo de {file_size} bytes...")
        
        # Crear boundary simple
        boundary = f"----ESP32Upload{int(time.monotonic())}"
        
        # Preparar headers multipart (formato correcto para Flask)
        multipart_start = f'--{boundary}\r\n'
        multipart_start += 'Content-Disposition: form-data; name="file"; filename="grabacion.wav"\r\n'
        multipart_start += 'Content-Type: audio/wav\r\n\r\n'
        multipart_end = f'\r\n--{boundary}--\r\n'
        
        # Calcular tamaño total
        content_length = len(multipart_start.encode()) + file_size + len(multipart_end.encode())
        
        try:
            # Crear socket
            sock = self.pool.socket()
            sock.settimeout(10.0)
            
            # Conectar
            addr_info = self.pool.getaddrinfo(IP_ADDRESS, PORT)[0]
            sock.connect(addr_info[-1])
            print("Conectado al servidor")
            
            # Preparar headers HTTP
            http_headers = f"POST /transcribe HTTP/1.1\r\n"
            http_headers += f"Host: {IP_ADDRESS}:{PORT}\r\n" 
            http_headers += f"Content-Type: multipart/form-data; boundary={boundary}\r\n"
            http_headers += f"Content-Length: {content_length}\r\n"
            http_headers += f"Connection: close\r\n\r\n"
            
            # Enviar headers
            sock.send(http_headers.encode())
            sock.send(multipart_start.encode())
            
            # Enviar archivo
            bytes_sent = 0
            with open(AUDIO_FILE, "rb") as f:
                while True:
                    if bytes_sent % 10240 == 0:  # GC cada 10KB
                        gc.collect()
                    
                    chunk = f.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    
                    sock.send(chunk)
                    bytes_sent += len(chunk)
                    
                    # Progreso cada 5%
                    if bytes_sent % 5000 == 0:
                        progress = (bytes_sent / file_size) * 100
                        print(f"{progress:.0f}% ({bytes_sent}/{file_size})")
                    
                    time.sleep(0.02)  # Pequeña pausa
            
            # Finalizar
            sock.send(multipart_end.encode())
            print(f"Archivo enviado: {bytes_sent} bytes")
            
            # Cerrar inmediatamente sin esperar respuesta
            sock.close()
            
            # Si enviamos todo, es éxito
            success = (bytes_sent >= file_size)
            print(f"Resultado: {'ÉXITO' if success else 'FALLO'}")
            return success
            
        except Exception as e:
            print(f"Error: {e}")
            try:
                sock.close()
            except:
                pass
            return False

def main():
    print("=== ESP32 Audio Uploader ===")
    ib.pixel=(0,255,0)
    # Mostrar memoria
    gc.collect()
    print(f"Memoria libre: {gc.mem_free()} bytes")
    
    uploader = SimpleAudioUploader()
    
    # Conectar WiFi
    if not uploader.connect_wifi():
        print("FALLO: No se pudo conectar a WiFi")
        return
    
    # Enviar archivo
    print("\nIniciando envío...")
    success = uploader.send_audio()
    
    if success:
        print("\nARCHIVO ENVIADO EXITOSAMENTE")
    else:
        print("\nERROR ENVIANDO ARCHIVO")
    
    # Memoria final
    gc.collect()
    print(f"Memoria libre final: {gc.mem_free()} bytes")

# Ejecutar
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrumpido")
    except Exception as e:
        print(f"Error crítico: {e}")