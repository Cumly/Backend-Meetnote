import speech_recognition as sr
from pydub import AudioSegment
import os

# Carpeta base (generateActaFromInput)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CARPETA_SOURCES = os.path.join(BASE_DIR, "sources")
CARPETA_FRAGMENT = os.path.join(CARPETA_SOURCES, "fragmento")

def dividir_audio_webm(ruta_entrada, duracion_segmento_ms=60000):
    if not os.path.exists(CARPETA_FRAGMENT):
        os.makedirs(CARPETA_FRAGMENT)

    audio = AudioSegment.from_file(ruta_entrada, format="webm")
    segmentos = [audio[i:i + duracion_segmento_ms] for i in range(0, len(audio), duracion_segmento_ms)]
    rutas_segmentos = []

    for idx, segmento in enumerate(segmentos):
        ruta_segmento = os.path.join(CARPETA_FRAGMENT, f"segmento_{idx}.wav")
        segmento.export(ruta_segmento, format="wav")
        rutas_segmentos.append(ruta_segmento)

    return rutas_segmentos

def transcribir_audio(ruta_wav):
    recognizer = sr.Recognizer()
    with sr.AudioFile(ruta_wav) as source:
        audio = recognizer.record(source)
    try:
        texto = recognizer.recognize_google(audio, language="es-ES")
        print(f"Transcripción de {ruta_wav}:")
        print(texto)
        return texto
    except sr.UnknownValueError:
        print(f"Google no entendió el audio en {ruta_wav}.")
    except sr.RequestError as e:
        print(f"Error al contactar con Google en {ruta_wav}: {e}")
    return ""


