import os
import shutil


def limpiar_carpeta(carpeta):
    if os.path.exists(carpeta):
        for archivo_o_carpeta in os.listdir(carpeta):
            ruta_completa = os.path.join(carpeta, archivo_o_carpeta)
            if os.path.isfile(ruta_completa) or os.path.islink(ruta_completa):
                os.unlink(ruta_completa)
            elif os.path.isdir(ruta_completa):
                shutil.rmtree(ruta_completa)