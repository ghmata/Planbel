"""
Script rápido para testar o prompt modular atualizado
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from groq import Groq
from src.prompts.prompt_modular import (
    montar_system_prompt,
    build_prompt_modular,
    MODULO_METODOLOGIAS
)
from src.bncc import get_bncc_context

load_dotenv()

def testar_prompt():
    """Testa o prompt modular com um cenário específico."""
    
    # Configurar cliente Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    # Cenário de teste: 3º ano com gamificação
    cenario = {
        "disciplina": "Matemática",
        "ano_escolar": "3º ano - Ensino Fundamental",
        "tema": "Multiplicação com material concreto",
        "duracao_aulas": 1,
        "metodologia": "Gamificação",
        "recursos": ["Quadro/Lousa", "Material Manipulável", "Jogos Digitais"],
        "observacoes": "Turma com 25 alunos, 2 com TDAH, gostam muito de jogos"
    }
    
    print("=" * 60)
    print("🧪 TESTANDO PROMPT MODULAR v2.0")
    print("=" * 60)
    print(f"\n📋 Cenário: {cenario['disciplina']} - {cenario['ano_escolar']}")
    print(f"📝 Tema: {cenario['tema']}")
    print(f"🎮 Metodologia: {cenario['metodologia']}")
    print(f"📦 Recursos: {', '.join(cenario['recursos'])}")
    print(f"👥 Observações: {cenario['observacoes']}")
    print("\n" + "-" * 60)
    
    # Montar prompt
    system_prompt = montar_system_prompt()
    
    # Adicionar metodologias ao contexto
    bncc_context = get_bncc_context(cenario["disciplina"], cenario["ano_escolar"])
    
    user_prompt = build_prompt_modular(
        disciplina=cenario["disciplina"],
        ano_escolar=cenario["ano_escolar"],
        tema=cenario["tema"],
        duracao_aulas=cenario["duracao_aulas"],
        bncc_context=bncc_context,
        metodologia=cenario["metodologia"],
        recursos=cenario["recursos"],
        observacoes=cenario["observacoes"],
        gerar_material_impresso=True  # Ativar para teste
    )
    
    print("\n⏳ Gerando plano de aula com Groq...")
    
    # Chamar Groq
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=6000 # Aumentado para comportar o material
    )
    
    plano = response.choices[0].message.content
    tokens = response.usage.total_tokens
    
    print(f"\n✅ Gerado com sucesso! ({tokens} tokens)")
    print("=" * 60)
    print("\n📄 PLANO DE AULA GERADO:\n")
    print(plano)
    
    # Salvar em arquivo com tratamento de erro
    try:
        output_dir = os.path.join(os.path.dirname(__file__), "outputs")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "teste_prompt_modular.md")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(plano)
        print(f"\n💾 Salvo em: {output_file}")
    except Exception as e:
        print(f"\n⚠️ Não foi possível salvar o arquivo: {e}")
        print("Mas o plano foi gerado e exibido acima.")
    
    return plano


if __name__ == "__main__":
    testar_prompt()
