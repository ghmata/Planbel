"""
PlanBel 2.0 - Ciclo de Melhoria do Prompt com CrewAI
====================================================
Este script usa 3 agentes para avaliar e melhorar o prompt:
1. Gerador - Cria planos de aula
2. Avaliador - Dá notas de 0-10 em 5 critérios
3. Refinador - Sugere melhorias no prompt
"""

import os
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.prompts.prompt_modular import montar_system_prompt, build_prompt_modular
from src.bncc import get_bncc_context

load_dotenv()
console = Console()

# Cenários variados para testar o prompt
CENARIOS_TESTE = [
    {
        "nome": "Anos Iniciais + Gamificação",
        "disciplina": "Matemática",
        "ano_escolar": "3º ano - Ensino Fundamental",
        "tema": "Multiplicação com material concreto",
        "duracao_aulas": 1,
        "metodologia": "Gamificação",
        "recursos": ["Quadro/Lousa", "Material Manipulável"],
        "observacoes": "Turma com 25 alunos, gostam muito de jogos"
    },
    {
        "nome": "Anos Finais + PBL",
        "disciplina": "Ciências",
        "ano_escolar": "7º ano - Ensino Fundamental",
        "tema": "Ecossistemas e cadeias alimentares",
        "duracao_aulas": 2,
        "metodologia": "PBL",
        "recursos": ["Projetor", "Material Impresso", "Computadores"],
        "observacoes": "Turma interessada em meio ambiente"
    },
    {
        "nome": "Inclusão + Storytelling",
        "disciplina": "História",
        "ano_escolar": "5º ano - Ensino Fundamental",
        "tema": "Povos indígenas do Brasil",
        "duracao_aulas": 1,
        "metodologia": "Storytelling",
        "recursos": ["Quadro/Lousa", "Material Impresso"],
        "observacoes": "Turma com 2 alunos com TDAH e 1 com baixa visão"
    }
]


def criar_agentes():
    """Cria os 3 agentes de validação."""
    # Usando modelo menor para evitar rate limit do tier gratuito
    llm = "groq/llama-3.1-8b-instant"
    
    gerador = Agent(
        role="Professor Planejador",
        goal="Criar planos de aula de alta qualidade",
        backstory="Professor com 15 anos de experiência, domina BNCC e metodologias ativas.",
        llm=llm,
        verbose=False,
        max_iter=1
    )
    
    avaliador = Agent(
        role="Coordenador Pedagógico",
        goal="Avaliar planos de aula com rigor em 5 critérios",
        backstory="""Coordenador pedagógico experiente. Avalia:
        1. Alinhamento BNCC (25%)
        2. Clareza pedagógica (25%)
        3. Estrutura completa (20%)
        4. Coerência temporal (15%)
        5. Aplicabilidade (15%)
        Sempre justifica notas com exemplos específicos.""",
        llm=llm,
        verbose=False,
        max_iter=1
    )
    
    refinador = Agent(
        role="Engenheiro de Prompts",
        goal="Sugerir melhorias específicas e acionáveis no prompt",
        backstory="""Especialista em otimização de prompts para Llama.
        Foca em melhorias concretas: adicionar regras, exemplos, estruturas.
        Nunca sugere mudanças genéricas.""",
        llm=llm,
        verbose=False,
        max_iter=1
    )
    
    return gerador, avaliador, refinador


def executar_ciclo(cenario: dict, system_prompt: str, user_prompt: str):
    """Executa um ciclo completo de validação para um cenário."""
    
    console.print(f"\n[bold yellow]📝 Cenário: {cenario['nome']}[/]")
    console.print(f"   Disciplina: {cenario['disciplina']} | Ano: {cenario['ano_escolar']}")
    console.print(f"   Metodologia: {cenario.get('metodologia', 'Nenhuma')}")
    
    gerador, avaliador, refinador = criar_agentes()
    
    # Task 1: Gerar
    task_gerar = Task(
        description=f"""Use este SYSTEM PROMPT e USER PROMPT para gerar um plano de aula:

SYSTEM PROMPT:
{system_prompt}

USER PROMPT:
{user_prompt}

Gere o plano de aula completo seguindo o formato especificado.""",
        expected_output="Plano de aula completo em markdown",
        agent=gerador
    )
    
    # Task 2: Avaliar
    task_avaliar = Task(
        description="""Avalie o plano de aula gerado em 5 critérios (0-10):

1. **Alinhamento BNCC** (peso 25%): Código correto? Coerente com tema?
2. **Clareza Pedagógica** (peso 25%): Instruções claras para o professor?
3. **Estrutura Completa** (peso 20%): Todas as seções preenchidas?
4. **Coerência Temporal** (peso 15%): Tempos somam corretamente?
5. **Aplicabilidade** (peso 15%): Recursos realistas? Atividades viáveis?

Para cada critério dê NOTA e JUSTIFICATIVA.
Calcule a MÉDIA PONDERADA final.
Liste PONTOS FORTES e PONTOS A MELHORAR.""",
        expected_output="Avaliação com notas, justificativas e média ponderada",
        agent=avaliador,
        context=[task_gerar]
    )
    
    # Task 3: Refinar
    task_refinar = Task(
        description="""Analise a avaliação e sugira MELHORIAS ESPECÍFICAS no PROMPT (não no plano).

Foque em:
1. Quais critérios tiveram nota < 7?
2. Que REGRAS ou INSTRUÇÕES adicionar ao prompt para evitar esses problemas?
3. Precisa de EXEMPLOS no prompt?
4. O FORMATO de saída precisa de ajustes?

Dê sugestões CONCRETAS, com texto exato a adicionar/modificar no prompt.
NÃO sugira mudanças genéricas como "melhorar clareza".""",
        expected_output="Lista de sugestões específicas para melhorar o prompt",
        agent=refinador,
        context=[task_gerar, task_avaliar]
    )
    
    # Executar crew
    crew = Crew(
        agents=[gerador, avaliador, refinador],
        tasks=[task_gerar, task_avaliar, task_refinar],
        process=Process.sequential,
        verbose=False
    )
    
    console.print("   ⏳ Executando agentes...", style="dim")
    start = time.time()
    
    result = crew.kickoff()
    
    elapsed = time.time() - start
    console.print(f"   ✅ Concluído em {elapsed:.1f}s", style="green")
    
    return {
        "cenario": cenario["nome"],
        "plano": task_gerar.output.raw if task_gerar.output else "",
        "avaliacao": task_avaliar.output.raw if task_avaliar.output else "",
        "sugestoes": task_refinar.output.raw if task_refinar.output else "",
        "tempo": elapsed
    }


def main():
    console.print(Panel(
        "[bold yellow]🔄 CICLO DE MELHORIA DO PROMPT COM CREWAI[/]\n\n"
        "3 agentes vão avaliar o prompt e sugerir melhorias:\n"
        "1. 🧑‍🏫 Gerador - Cria planos\n"
        "2. 📊 Avaliador - Dá notas 0-10\n"
        "3. 🛠️ Refinador - Sugere melhorias",
        title="PlanBel 2.0"
    ))
    
    # Montar prompt atual
    system_prompt = montar_system_prompt()
    
    resultados = []
    
    for cenario in CENARIOS_TESTE:
        # Preparar contexto BNCC
        bncc_context = get_bncc_context(cenario["disciplina"], cenario["ano_escolar"])
        
        # Montar prompt do usuário
        user_prompt = build_prompt_modular(
            disciplina=cenario["disciplina"],
            ano_escolar=cenario["ano_escolar"],
            tema=cenario["tema"],
            duracao_aulas=cenario["duracao_aulas"],
            bncc_context=bncc_context,
            metodologia=cenario.get("metodologia"),
            recursos=cenario.get("recursos"),
            observacoes=cenario.get("observacoes")
        )
        
        # Executar ciclo
        resultado = executar_ciclo(cenario, system_prompt, user_prompt)
        resultados.append(resultado)
        
        # Rate limiting - esperar mais tempo para evitar erro 429
        console.print("   ⏸️ Aguardando 15s (rate limit Groq)...", style="dim")
        time.sleep(15)
    
    # Salvar resultados
    output_dir = "outputs/crewai_validacao"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_dir}/validacao_{timestamp}.md"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 📊 Resultado da Validação com CrewAI\n\n")
        f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
        
        for r in resultados:
            f.write(f"---\n\n## 📝 {r['cenario']}\n\n")
            f.write(f"### Plano Gerado\n\n{r['plano']}\n\n")
            f.write(f"### Avaliação\n\n{r['avaliacao']}\n\n")
            f.write(f"### Sugestões de Melhoria\n\n{r['sugestoes']}\n\n")
    
    console.print(f"\n[bold green]✅ Resultados salvos em: {output_file}[/]")
    
    # Mostrar resumo das sugestões
    console.print(Panel(
        "[bold]📋 RESUMO DAS SUGESTÕES DE MELHORIA[/]\n\n"
        "Veja o arquivo gerado para:\n"
        "• Notas detalhadas de cada critério\n"
        "• Sugestões específicas do agente Refinador\n"
        "• Textos exatos para adicionar ao prompt",
        title="Próximos Passos"
    ))


if __name__ == "__main__":
    main()
