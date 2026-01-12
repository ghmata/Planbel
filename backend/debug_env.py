import os
from dotenv import load_dotenv

load_dotenv()

print("--- DEBUG ENV ---")
print(f"GEMINI_MODEL do .env: '{os.getenv('GEMINI_MODEL')}'")
print(f"GEMINI_API_KEY set: {bool(os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY'))}")
print("-----------------")
