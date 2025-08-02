import requests

def generar_acta(texto: str) -> str:
    prompt = f"""
Por favor, genera un acta profesional de reunión basada en el siguiente texto. Incluye y estructura claramente:

1. titulo
1. Fecha 
2. hora inicio y fin
2. Participantes
3. Temas discutidos
4. Decisiones y acuerdos
5. Observaciones y Conclusiones

Texto original:
{texto}

Formato sugerido:

1 titulo
1. Fecha 
2. hora inicio y fin
2. Participantes
3. Temas discutidos
4. Decisiones y acuerdos
5. Observaciones y Conclusiones
"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",  # o llama3.2 si ya lo bajaste
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code == 200:
        return response.json().get("response", "").strip()
    else:
        raise Exception(f"Error al generar acta: {response.text}")