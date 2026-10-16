\# JARVIS — Personal Voice Assistant



A desktop voice assistant built with Python. JARVIS has a dark dashboard, accepts typed or spoken commands, and can speak its replies.



\## Features



\- Dark desktop interface built with CustomTkinter

\- Typed commands and push-to-talk microphone input

\- Text-to-speech replies

\- Tells the current time and date

\- Opens Google and YouTube

\- Searches the web

\- Shows voice and system status in the dashboard



\## Preview



Add a screenshot of the app to `assets/jarvis-dashboard.png`, then uncomment this line:



<!-- !\[JARVIS dashboard](assets/jarvis-dashboard.png) -->



\## Requirements



\- Python 3.11

\- Windows

\- Internet access for speech recognition and web searches

\- A working microphone for voice input



\## Setup



Clone this repository, then open PowerShell in the project folder:



```powershell

py -3.11 -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

py -m pip install -r requirements.txt

py app.py

