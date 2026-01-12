import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure sua chave (lendo do .env para segurança, mas é a mesma chave)
key = os.getenv("GEMINI_API_KEY") or "AIzaSyD3w-nG0Qq9kJqaVe0tbi1ZYqbe1fk64Y8"
genai.configure(api_key=key)

print(f"Usando chave: {key[:10]}...")

# Liste os modelos disponíveis
print("Listando modelos...")
try:
    for model in genai.list_models():
        print(f"Nome: {model.name}")
        print(f"Versão: {model.version}")
        print(f"Display Name: {model.display_name}")
        print("---")
except Exception as e:
    print(f"ERRO FATAL: {e}")
