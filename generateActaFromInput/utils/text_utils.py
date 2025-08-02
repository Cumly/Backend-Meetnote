import os
from PyPDF2 import PdfReader

def extraer_texto_de_archivo(ruta: str) -> str:
    if not os.path.exists(ruta):
        raise FileNotFoundError("El archivo no existe.")

    extension = os.path.splitext(ruta)[1].lower()

    if extension == ".txt":
        return extraer_texto_txt(ruta)
    elif extension == ".pdf":
        return extraer_texto_pdf(ruta)
    else:
        raise ValueError(f"Tipo de archivo no soportado: {extension}")

def extraer_texto_txt(ruta: str) -> str:
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()

def extraer_texto_pdf(ruta: str) -> str:
    reader = PdfReader(ruta)
    texto = ""
    for page in reader.pages:
        contenido = page.extract_text()
        if contenido:
            texto += contenido + "\n"
    return texto.strip()


