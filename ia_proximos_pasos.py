from openai import OpenAI

import streamlit as st

# Configuración de la API Key (leer desde secrets)

def generar_proximos_pasos(texto_usuario):
    prompt = f"""
    El siguiente texto es una nota de sesión personal o de coaching. A partir de su contenido, generá 2 a 3 pasos concretos y útiles que la persona podría seguir como próximos pasos. Sé claro, breve y empático.

    Texto de la sesión:
    "{texto_usuario}"

    Próximos pasos sugeridos:
    """

    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        respuesta = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sos un asistente de coaching que brinda próximos pasos breves y útiles."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=200)
        pasos = respuesta.choices[0].message.content.strip()
        return pasos
    except Exception as e:
        return f"⚠️ Error al generar los pasos: {e}"
