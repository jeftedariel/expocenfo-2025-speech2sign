# Codigos ESP32

Las libs necesarias se encuentran dentro de /lib
Acciones de los ficheros de codigo:

## code.py

Une ambos archivos, tanto record.py como upload.py  y espera una entrada de los botones para ejecutar alguna de las tareas


## Record.py

Graba un fragmento de audio de ~11 seg a ~5000Hz y lo guarda en memoria como grabacion.wav

## Upload.py

Envia el archvio de audio al servidor mcp mediante el endpoint /transcribe
