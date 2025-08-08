import wifi
import socketpool
import time

SSID = "Fran1_EXT"
PASSWORD = "fran1234"

SERVER_IP = "192.168.1.112"
SERVER_PORT = 5000
ENDPOINT = "/transcribe"
WAV_FILENAME = "grabacion.wav"

def connect_wifi(ssid, password):
    print("Conectando a WiFi...")
    wifi.radio.connect(ssid, password)
    print("Conectado con IP:", wifi.radio.ipv4_address)

def send_wav_in_chunks():
    pool = socketpool.SocketPool(wifi.radio)
    sock = pool.socket()

    print("Conectando al servidor...")
    sock.connect((SERVER_IP, SERVER_PORT))

    # Obtener tamaño del archivo WAV
    with open(WAV_FILENAME, "rb") as f:
        f.seek(0, 2)  # Ir al final del archivo
        file_size = f.tell()

    print(f"Tamaño del archivo: {file_size} bytes")

    # Preparar headers HTTP POST
    headers = (
        "POST {} HTTP/1.1\r\n"
        "Host: {}:{}\r\n"
        "Content-Type: audio/wav\r\n"
        "Content-Length: {}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).format(ENDPOINT, SERVER_IP, SERVER_PORT, file_size)

    # Enviar headers
    sock.send(headers.encode())

    # Enviar archivo en chunks con manejo de EAGAIN
    chunk_size = 1024
    with open(WAV_FILENAME, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break

            bytes_sent = 0
            while bytes_sent < len(chunk):
                try:
                    sent = sock.send(chunk[bytes_sent:])
                    if sent == 0:
                        raise RuntimeError("socket connection broken")
                    bytes_sent += sent
                except OSError as e:
                    if e.args[0] == 11:  # EAGAIN
                        time.sleep(0.01)  # Esperar 10ms y reintentar
                    else:
                        raise

    print("Archivo enviado, esperando respuesta...")

    # Recibir respuesta simple
    response = b""
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            response += data
    except Exception:
        pass

    print("Respuesta del servidor:")

    sock.close()

def main():
    connect_wifi(SSID, PASSWORD)
    send_wav_in_chunks()

if __name__ == "__main__":
    main()
