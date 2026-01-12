import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print(f"Testing generation with key: {api_key[:10]}...")

models_to_test = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-2.0-flash-exp",
    "models/gemini-1.5-flash",
]

# Get list from API to verify
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            if m.name not in models_to_test and 'gemini' in m.name:
                models_to_test.append(m.name)
except:
    pass

print(f"Models to test: {models_to_test}")

for model_name in models_to_test:
    print(f"\n--- Testing {model_name} ---")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello, are you working?")
        print(f"SUCCESS! Response: {response.text[:20]}...")
    except Exception as e:
        print(f"FAILED: {e}")
