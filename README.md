# 🎙️ speech2sign – ExpoCenfo 2025

Este proyecto permite traducir audio a lenguaje de señas utilizando un microcontrolador **ESP32**, un servidor para procesamiento de audio con el uso de **inteligencia artificial**, y un banco de videos en lenguaje de señas. Fue desarrollado como parte de **ExpoCenfo 2025**, con el objetivo de crear una herramienta inclusiva para personas con discapacidad auditiva.


El banco de videos usado en este proyecto fue extraído del sitio web  [SpreadTheSign](https://www.spreadthesign.com/)   [Cenarec](https://lesco.cenarec.go.cr)

---

## 🚀 ¿Cómo funciona?

1. **Captura de Audio:**  
   El ESP32 graba audio del entorno a través de un micrófono.

2. **Envío al Servidor MCP:**  
   El audio se transmite vía Wi-Fi a un servidor (MCP).

3. **Procesamiento por IA:**  
   El servidor convierte el audio a texto utilizando reconocimiento de voz.

4. **Traducción a Señas:**  
   El texto se interpreta y se asocia a un video en lenguaje de señas previamente almacenado, el cual se muestra al usuario.
   Ejemplo de algunos archivos de video:
   <img width="1046" height="879" alt="image" src="https://github.com/user-attachments/assets/0229b9ae-d1c7-4e0d-a95e-f092bdbf1a10" />

---

## 🔧 Componentes Utilizados

| Componente          | Descripción                                    |
|---------------------|------------------------------------------------|
| [IDEABoard ESP32  ](https://www.crcibernetica.com/crcibernetica-ideaboard/)             | Placa y Microcontrolador         |
|[Electret Microphone](https://www.crcibernetica.com/breakout-board-for-electret-microphone/?searchid=2464241&search_query=electret+mic)| Microfono analogo para la captura de voz|
|2x [Push Button](https://www.crcibernetica.com/mini-push-button-switch/?searchid=2464245&search_query=button)| Pulsadores para envio de instrucciones|
|[Potentiometer](https://www.crcibernetica.com/rotary-potentiometer-20-kohms/?searchid=2464252&search_query=potentiometer)| Potenciometro para manejo de volumen|
|[High Precision Power Bank Module 5V@2A](https://www.crcibernetica.com/high-precision-power-bank-module-5v-2a-listo/?searchid=2464259&search_query=High+Precision+Power+Bank+Module+5V%402A) o Similar| Modulo de carga para la bateria |
|[Li-Ion Battery 2500mAh 3.7V](https://www.crcibernetica.com/samsung-li-ion-battery-18650-2500mah-3-7v/?searchid=0&search_query=battery) o Similar| Bateria para el uso del microcontrolador sin necesidad de cables|
---

## Integrantes de Proyecto

| Integrantes         | Roles y Aportes                                    |
|---------------------|------------------------------------------------|
| **Jefté Mendoza**             | Electrónica, WebScrapping, Desarrollo del microcontrolador e integracion de videos         |
|**Justin Rodriguez**|Desarrollo de interfaz y manejo del audio para interpretación del LLM  |
|**Alex Ledezma**|Mediciones de Componentes, Optimización de Codigo|
|**Daniel Saborio**|Diseño y Modelado 3D|

---
## ⚙️ Diagramas y Prototipos del Microcontrolador


### Versión 0.1 ♦️

<details>
   <summary>Diagrama</summary>
   <img width="1046" height=auto alt="image" src="https://raw.githubusercontent.com/jeftedariel/expocenfo-2025-speech2sign/refs/heads/main/photos/diagrama-v0.1.png" />

</details>


### Versión 0.2 ♦️

<details>
   <summary>Diagrama</summary>
   <img width="1046" height=auto alt="image" src="https://raw.githubusercontent.com/jeftedariel/expocenfo-2025-speech2sign/refs/heads/main/photos/diagrama-v0.2.png" />

</details>
<details>
<Summary>Prototipo Armado</Summary>


   <img width="1046" height=auto alt="image" src="https://raw.githubusercontent.com/jeftedariel/expocenfo-2025-speech2sign/refs/heads/main/photos/prototipo-v0.2.jpg" />


</details>

### Versión 0.3 ♦️

<details>
   <summary>Diagrama</summary>
   <img width="1046" height=auto alt="image" src="https://raw.githubusercontent.com/jeftedariel/expocenfo-2025-speech2sign/refs/heads/main/photos/diagrama-v0.3.png" />

</details>

   
<details>
<Summary>Prototipo Armado</Summary>


   <img width="1046" height=auto alt="image" src="https://raw.githubusercontent.com/jeftedariel/expocenfo-2025-speech2sign/refs/heads/main/photos/prototipo-v0.3.jpg" />


</details>


### Versión 0.4 ♦️

<details>
   <summary>Diagrama</summary>
   <img width="1046" height=auto alt="image" src="https://raw.githubusercontent.com/jeftedariel/expocenfo-2025-speech2sign/refs/heads/main/photos/diagrama-v0.4.png" />

</details>

   
<details>
<Summary>Prototipo Armado</Summary>
   <img width="1046" height=auto alt="image" src="https://raw.githubusercontent.com/jeftedariel/expocenfo-2025-speech2sign/refs/heads/main/photos/prototipo-v0.4.jpg" />

</details>


### Modelo 3D 🚀


   
   <img width="300px" height=auto alt="image" src="https://github.com/jeftedariel/expocenfo-2025-speech2sign/blob/main/photos/FOTOCASE3.png?raw=true" />
   <details>
   <Summary>Mas perspectivas</Summary>
      <img width="500" height=auto alt="image" src="https://github.com/jeftedariel/expocenfo-2025-speech2sign/blob/main/photos/FOTOCASE2.png?raw=true" />
         <img width="500" height=auto alt="image" src="https://github.com/jeftedariel/expocenfo-2025-speech2sign/blob/main/photos/FOTOCASE.png?raw=true" />
   </details>
<details>
<Summary>Interior del modelo</Summary>
         <img width="500" height=auto alt="image" src="https://github.com/jeftedariel/expocenfo-2025-speech2sign/blob/main/photos/interiorr.png?raw=true" />

</details>

