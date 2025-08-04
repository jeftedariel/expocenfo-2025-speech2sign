# 🎙️ speech2sign – ExpoCenfo 2025

Este proyecto permite traducir audio a lenguaje de señas utilizando un microcontrolador **ESP32**, un servidor para procesamiento de audio con el uso de **inteligencia artificial**, y un banco de videos en lenguaje de señas. Fue desarrollado como parte de **ExpoCenfo 2025**, con el objetivo de crear una herramienta inclusiva para personas con discapacidad auditiva.


El banco de videos usado en este proyecto fue extraído del sitio web [SpreadTheSign](https://www.spreadthesign.com/)

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
   <img width="1046" auto alt="image" src="https://github.com/user-attachments/assets/f6eac9eb-0c0b-482e-b78d-24f5775862fb" />


---

## 🔧 Tecnologías Utilizadas

| Componente          | Descripción                                    |
|---------------------|------------------------------------------------|
| Pendiente               | Pendiente         |
---

## Integrantes de Proyecto

| Integrantes         | Roles y Aportes                                    |
|---------------------|------------------------------------------------|
| **Jefté Mendoza**             | Electrónica, WebScrapping, Desarrollo del microcontrolador e integracion de videos         |
|**Justin Rodriguez**|Desarrollo de interfaz y manejo del audio para interpretación del LLM  |
|**Alex Ledezma**|Diseño y Modelado 3D|
|**Daniel Saborio**|Diseño y Modelado 3D|

---

## ⚙️ Diagramas y Prototipos del Microcontrolador


### Versión 1 ♦️

<details>
   <summary>Diagrama</summary>
   <img width="1046" height=auto alt="image" src="https://raw.githubusercontent.com/jeftedariel/expocenfo-2025-speech2sign/refs/heads/main/photos/prototipo-v1.png" />

</details>


### Versión 2 ♦️

<details>
   <summary>Diagrama</summary>
   <img width="1046" height=auto alt="image" src="https://raw.githubusercontent.com/jeftedariel/expocenfo-2025-speech2sign/refs/heads/main/photos/diagrama-v2.png" />

</details>
<details>
<Summary>Prototipo Armado</Summary>


   <img width="1046" height=auto alt="image" src="https://raw.githubusercontent.com/jeftedariel/expocenfo-2025-speech2sign/refs/heads/main/photos/prototipo-v2.jpg" />


</details>

### Versión 3 ♦️

<details>
   <summary>Diagrama</summary>
   <img width="1046" height=auto alt="image" src="https://raw.githubusercontent.com/jeftedariel/expocenfo-2025-speech2sign/refs/heads/main/photos/diagrama-v3.png" />

</details>

   
<details>
<Summary>Prototipo Armado</Summary>


   <img width="1046" height=auto alt="image" src="https://raw.githubusercontent.com/jeftedariel/expocenfo-2025-speech2sign/refs/heads/main/photos/prototipo-v3.jpg" />


</details>
