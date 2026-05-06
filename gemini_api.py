import os
import google.generativeai as genai

# Obtiene la API Key desde la variable de entorno GEMINI_API_KEY
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Debes definir la variable de entorno GEMINI_API_KEY con tu clave de acceso de Gemini.")

genai.configure(api_key=API_KEY)

def chat_with_gemini(prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(prompt)
    return response.text