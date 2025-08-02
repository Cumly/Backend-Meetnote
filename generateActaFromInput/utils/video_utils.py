from pydub import AudioSegment
import os

# Carpeta base y carpeta para guardar audio convertido
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CARPETA_AUDIO = os.path.join(BASE_DIR, "sources", "audio")

def video_a_audio(ruta_video, formato_salida="wav"):
    if not os.path.exists(CARPETA_AUDIO):
        os.makedirs(CARPETA_AUDIO)

    nombre_base = os.path.splitext(os.path.basename(ruta_video))[0]
    ruta_audio_salida = os.path.join(CARPETA_AUDIO, f"{nombre_base}.{formato_salida}")

    audio = AudioSegment.from_file(ruta_video)
    audio.export(ruta_audio_salida, format=formato_salida)
    print(f"Audio guardado en: {ruta_audio_salida}")
    return ruta_audio_salida

