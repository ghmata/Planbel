import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL")

print(f"Checking limits for model: {model_name}")
genai.configure(api_key=api_key)

try:
    model_info = genai.get_model(f"models/{model_name}")
    print(f"--- {model_info.display_name} ---")
    print(f"Input Token Limit: {model_info.input_token_limit}")
    print(f"Output Token Limit: {model_info.output_token_limit}")
except Exception as e:
    print(f"Error fetching model info: {e}")
    # Fallback: try listing and finding it
    print("Attempting to find in list...")
    found = False
    for m in genai.list_models():
        if model_name in m.name:
            print(f"FOUND: {m.name}")
            print(f"Input Limit: {m.input_token_limit}")
            print(f"Output Limit: {m.output_token_limit}")
            found = True
            break
    if not found:
        print("Model not found in list either.")
