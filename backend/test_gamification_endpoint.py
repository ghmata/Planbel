import requests
import time

print("Waiting for server to ensure it is up...")
time.sleep(5)

url = "http://localhost:5000/api/gerar-material"

payload = {
    "plano": {
        "titulo": "Aula de Matemática Divertida",
        "disciplinas": ["Matemática"],
        "serie": "5º Ano",
        "metodologia": "Gamificação",
        "detalhes_gamificacao": "Jogo de Bingo das Tabuadas",
        "desenvolvimento": "Os alunos receberão cartelas...",
        "fechamento": "Vence quem preencher primeiro."
    }
}

try:
    print("Sending request to /api/gerar-material with gamification payload...")
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    html = response.json().get('html', '')
    
    print(f"Status Code: {response.status_code}")
    print(f"HTML Length: {len(html)}")
    
    # Validation checks
    checks = {
        "CSS: game-card": ".game-card" in html,
        "CSS: rules-box": ".rules-box" in html,
        "CSS: cards-grid": ".cards-grid" in html
    }
    
    all_passed = True
    for name, result in checks.items():
        print(f"Check {name}: {'PASSED' if result else 'FAILED'}")
        if not result:
            all_passed = False
            
    if all_passed:
        print("\nSUCCESS: Gamification prompt was correctly triggered and returned expected layout.")
    else:
        print("\nFAILURE: Response did not contain expected gamification elements.")
        print("Preview of HTML start:", html[:500])

except Exception as e:
    print(f"ERROR: {e}")
