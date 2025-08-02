import os
import json
from datetime import datetime
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils.ia_utils import generar_acta
from .utils.text_utils import extraer_texto_de_archivo
from .utils.audio_utils import dividir_audio_webm, transcribir_audio
from .utils.video_utils import video_a_audio
from .utils.file_utils import limpiar_carpeta

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CARPETA_SOURCES = os.path.join(BASE_DIR, "generateActaFromInput/sources")
CARPETA_TRANSCRIPCION = os.path.join(CARPETA_SOURCES, "transcripciones")
CARPETA_UPLOAD = os.path.join(CARPETA_SOURCES, "upload")

@api_view(["POST"])
def TranscriptionByVideo(request):

    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No se recibió ningún archivo"}, status=400)
    
    if not os.path.exists(CARPETA_UPLOAD):
        os.makedirs(CARPETA_UPLOAD)
    
    ruta = os.path.join(CARPETA_UPLOAD, file.name)

    with open(ruta, 'wb+') as destino:
        for chunk in file.chunks():
            destino.write(chunk)

    data = request.data
    titulo = data.get("titulo", "").strip()
    fecha = data.get("fecha", "").strip()
    horaInicio = data.get("horaInicio", "").strip()
    horaFin = data.get("horaFin", "").strip()
    participantes = data.get("participantes", "")

    if not all([titulo, fecha, horaInicio, horaFin]) or not participantes:
        return Response({"error": "Error en los parámetros del request"}, status=400)

    try:
        # Crear carpeta transcripciones si no existe
        if not os.path.exists(CARPETA_TRANSCRIPCION):
            os.makedirs(CARPETA_TRANSCRIPCION)

        # 🎞️ Convertir video a audio
        ruta_audio = video_a_audio(ruta)
        if not ruta_audio or not os.path.exists(ruta_audio):
            return Response({"error": "Error al convertir video a audio"}, status=500)
            
        rutas_wav = dividir_audio_webm(ruta_audio)

        nombre_base = os.path.splitext(os.path.basename(ruta))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_txt_final = f"{nombre_base}_{timestamp}.txt"
        ruta_txt_final = os.path.join(CARPETA_TRANSCRIPCION, nombre_txt_final)

        with open(ruta_txt_final, "w", encoding="utf-8") as f:
            f.write(f"Título: {titulo}\n")
            f.write(f"Fecha: {fecha}\n")
            f.write(f"Hora inicio: {horaInicio}\n")
            f.write(f"Hora fin: {horaFin}\n")
            f.write(f"Participantes: {', '.join(participantes)}\n")
            f.write("\n--- Transcripción ---\n\n")

            for ruta_wav in rutas_wav:
                texto = transcribir_audio(ruta_wav)
                if texto:
                    f.write(texto + " ")

        print(f"✅ Transcripción completa guardada en: {ruta_txt_final}")
        acta = generar_acta(extraer_texto_de_archivo(ruta_txt_final))

        return Response({"Acta generada": acta})

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    finally:
        limpiar_carpeta(CARPETA_SOURCES)
        
        

@api_view(["POST"])
def TranscriptionByAudio(request):
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No se recibió ningún archivo"}, status=400)
    
    if not os.path.exists(CARPETA_UPLOAD):
        os.makedirs(CARPETA_UPLOAD)
    
    ruta = os.path.join(CARPETA_UPLOAD, file.name)

    with open(ruta, 'wb+') as destino:
        for chunk in file.chunks():
            destino.write(chunk)

    data = request.data
    titulo = data.get("titulo", "").strip()
    fecha = data.get("fecha", "").strip()
    horaInicio = data.get("horaInicio", "").strip()
    horaFin = data.get("horaFin", "").strip()
    participantes = data.get("participantes", "")
    
    if not all ([ruta, titulo, fecha, horaInicio, horaFin]) or not participantes:
        return Response({"error": "Error los parametros del request"}, status=400)
    
    try:
        # 📁 Asegurar carpeta de transcripciones
        if not os.path.exists(CARPETA_TRANSCRIPCION):
            os.makedirs(CARPETA_TRANSCRIPCION)

        # 🎞️ audio y dividirlo
        rutas_wav = dividir_audio_webm(ruta)

        # 📝 Preparar archivo final de transcripción
        nombre_base = os.path.splitext(os.path.basename(ruta))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_txt_final = f"{nombre_base}_{timestamp}.txt"
        ruta_txt_final = os.path.join(CARPETA_TRANSCRIPCION, nombre_txt_final)

        # 🧠 Transcribir y guardar
        with open(ruta_txt_final, "w", encoding="utf-8") as f:
            # 📝 Escribir encabezado con los datos
            f.write(f"Título: {titulo}\n")
            f.write(f"Fecha: {fecha}\n")
            f.write(f"Hora inicio: {horaInicio}\n")
            f.write(f"Hora fin: {horaFin}\n")
            f.write(f"Participantes: {', '.join(participantes)}\n")
            f.write("\n--- Transcripción ---\n\n")
            # Luego la transcripción
            for ruta_wav in rutas_wav:
                texto = transcribir_audio(ruta_wav)
                if texto:
                    f.write(texto + " ")

        print(f"✅ Transcripción completa guardada en: {ruta_txt_final}")
        acta = generar_acta(extraer_texto_de_archivo(ruta_txt_final))

        limpiar_carpeta(CARPETA_SOURCES)

        return Response({"Acta generada": acta})

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    finally:
        limpiar_carpeta(CARPETA_SOURCES)
    

@api_view(["POST"])
def TranscriptionByText(request):

    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No se recibió ningún archivo"}, status=400)
    
    if not os.path.exists(CARPETA_UPLOAD):
        os.makedirs(CARPETA_UPLOAD)
    
    ruta = os.path.join(CARPETA_UPLOAD, file.name)

    with open(ruta, 'wb+') as destino:
        for chunk in file.chunks():
            destino.write(chunk)

    data = request.data
    titulo = data.get("titulo", "").strip()
    fecha = data.get("fecha", "").strip()
    horaInicio = data.get("horaInicio", "").strip()
    horaFin = data.get("horaFin", "").strip()
    participantes = data.get("participantes", "")

    if not all([titulo, fecha, horaInicio, horaFin]) or not participantes:
        return Response({"error": "Error los parámetros del request"}, status=400)

    try:
        if not os.path.exists(ruta):
            return Response({"error": "El archivo no existe"}, status=404)

        # Leer contenido original del archivo
        contenido_original = extraer_texto_de_archivo(ruta)

        # Construir encabezado con la información recibida
        encabezado = (
            f"Título: {titulo}\n"
            f"Fecha: {fecha}\n"
            f"Hora inicio: {horaInicio}\n"
            f"Hora fin: {horaFin}\n"
            f"Participantes: {', '.join(participantes) if isinstance(participantes, list) else participantes}\n"
            "\n--- Transcripción ---\n\n"
        )

        # Concatenar encabezado + contenido
        texto_final = encabezado + contenido_original

        # Generar acta con ese texto final
        acta = generar_acta(texto_final)

        return Response({"Acta generada": acta})

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    finally:
        limpiar_carpeta(CARPETA_SOURCES)



    