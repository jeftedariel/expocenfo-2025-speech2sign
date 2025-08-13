import board
import digitalio
import time

# Configurar botones en IO04 e IO05
button1 = digitalio.DigitalInOut(board.IO4)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.DOWN  # Pull-down interno

button2 = digitalio.DigitalInOut(board.IO5)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.DOWN  # Pull-down interno

# Variables para debounce
last_button1_state = False
last_button2_state = False
debounce_time = 0.2

print("Sistema iniciado. Presiona los botones:")
print("- IO04: Ejecuta record.py")
print("- IO05: Ejecuta upload.py")
print("Esperando pulsaciones...")

while True:
    # Leer estado actual de los botones
    current_button1_state = button1.value
    current_button2_state = button2.value
    
    # Detectar pulsación del botón 1 (IO04) - flanco ascendente
    if not last_button1_state and current_button1_state:
        print("Botón IO04 presionado - Ejecutando record.py")
        time.sleep(debounce_time)  # Debounce
        
        try:
            # Recargar el módulo en caso de que ya esté importado
            import sys
            if 'record' in sys.modules:
                del sys.modules['record']
            
            import record
            
            # Intentar llamar a main() si existe
            if hasattr(record, 'main'):
                record.main()
            
            print("record.py ejecutado correctamente")
        except ImportError:
            print("Error: No se pudo importar record.py")
        except Exception as e:
            print(f"Error ejecutando record.py: {e}")
    
    # Detectar pulsación del botón 2 (IO05) - flanco ascendente
    if not last_button2_state and current_button2_state:
        print("Botón IO05 presionado - Ejecutando upload.py")
        time.sleep(debounce_time)  # Debounce
        
        try:
            # Recargar el módulo en caso de que ya esté importado
            import sys
            if 'upload' in sys.modules:
                del sys.modules['upload']
            
            import upload
            
            # Llamar explícitamente a la función main()
            upload.main()
            
            print("upload.py ejecutado correctamente")
        except ImportError:
            print("Error: No se pudo importar upload.py")
        except Exception as e:
            print(f"Error ejecutando upload.py: {e}")
    
    # Actualizar estados anteriores
    last_button1_state = current_button1_state
    last_button2_state = current_button2_state
    
    # Pequeña pausa para no sobrecargar el procesador
    time.sleep(0.05)