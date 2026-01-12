"""
PlanBel 2.0 - Agentes CrewAI para Validação de Prompts
"""

from crewai import Agent, Task, Crew, Process
import os
from dotenv import load_dotenv

load_dotenv()


def create_validation_agents():
    """Cria os 3 agentes para validação de prompts."""
    
    # Configuração do LLM via Groq
    llm_config = f"groq/{os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')}"
    
    # Agente 1: Gerador de Planos
    gerador = Agent(
        role="Professor Planejador Experiente",
        goal="Criar planos de aula de alta qualidade usando o prompt fornecido",
        backstory="""Você é um professor com 15 anos de experiência no ensino básico brasileiro.
        Domina a BNCC e sabe criar planos de aula práticos e aplicáveis.
        Seu foco é gerar planos que outros professores consigam executar facilmente.""",
        llm=llm_config,
        verbose=True,
        allow_delegation=False,
        max_iter=1
    )
    
    # Agente 2: Avaliador Pedagógico
    avaliador = Agent(
        role="Coordenador Pedagógico",
        goal="Avaliar planos de aula em 5 critérios específicos com notas de 0 a 10",
        backstory="""Você é um coordenador pedagógico com expertise em BNCC e metodologias ativas.
        Avalia planos de aula há 10 anos e tem critérios rigorosos mas justos.
        Sempre justifica suas notas com exemplos específicos do plano analisado.""",
        llm=llm_config,
        verbose=True,
        allow_delegation=False,
        max_iter=1
    )
    
    # Agente 3: Refinador de Prompts
    refinador = Agent(
        role="Engenheiro de Prompts Especialista",
        goal="Analisar avaliações e sugerir melhorias específicas no prompt",
        backstory="""Você é um especialista em engenharia de prompts para LLMs.
        Entende como modelos como Llama respondem a diferentes estruturas de prompt.
        Sempre sugere melhorias concretas e testáveis, nunca genéricas.""",
        llm=llm_config,
        verbose=True,
        allow_delegation=False,
        max_iter=1
    )
    
    return gerador, avaliador, refinador


def create_validation_tasks(gerador, avaliador, refinador, prompt: str, scenario: dict):
    """Cria as tasks de validação para um cenário específico."""
    
    # Task 1: Gerar plano de aula
    task_gerar = Task(
        description=f"""Usando o prompt abaixo, gere um plano de aula completo.

PROMPT A USAR:
{prompt}

CENÁRIO:
- Disciplina: {scenario.get('disciplina')}
- Ano: {scenario.get('ano_escolar')}
- Tema: {scenario.get('tema')}
- Duração: {scenario.get('duracao_aulas', 1)} aula(s)
{f"- Observações: {scenario.get('observacoes')}" if scenario.get('observacoes') else ""}
{f"- Recursos: {scenario.get('recursos')}" if scenario.get('recursos') else ""}

Gere o plano de aula seguindo EXATAMENTE o formato especificado no prompt.""",
        expected_output="Plano de aula completo no formato markdown especificado",
        agent=gerador
    )
    
    # Task 2: Avaliar plano gerado
    task_avaliar = Task(
        description="""Avalie o plano de aula gerado em 5 critérios:

1. **Alinhamento BNCC (0-10)**: O código de habilidade está correto? É coerente com o tema?
2. **Clareza Pedagógica (0-10)**: As instruções são claras para o professor executar?
3. **Estrutura Completa (0-10)**: Todas as seções foram preenchidas adequadamente?
4. **Coerência Temporal (0-10)**: Os tempos de cada momento somam corretamente?
5. **Aplicabilidade (0-10)**: Os recursos são realistas? As atividades são viáveis?

Para cada critério:
- Dê uma nota de 0 a 10
- Justifique brevemente com exemplo do plano

No final, calcule a MÉDIA PONDERADA:
- Alinhamento BNCC: peso 25%
- Clareza Pedagógica: peso 25%
- Estrutura Completa: peso 20%
- Coerência Temporal: peso 15%
- Aplicabilidade: peso 15%""",
        expected_output="""Avaliação estruturada com:
- Nota e justificativa para cada critério
- Média ponderada final (0-10)
- Principais pontos fortes
- Principais pontos a melhorar""",
        agent=avaliador,
        context=[task_gerar]
    )
    
    # Task 3: Sugerir refinamentos no prompt
    task_refinar = Task(
        description="""Analise a avaliação do plano de aula e sugira melhorias no PROMPT original.

Foque em:
1. Quais critérios tiveram nota < 7?
2. Que instruções poderiam ser adicionadas ao prompt para melhorar esses pontos?
3. O formato de saída precisa de ajustes?
4. Faltam exemplos ou regras mais específicas?

NÃO sugira mudanças no plano gerado - sugira mudanças no PROMPT que evitariam os problemas identificados.""",
        expected_output="""Lista de sugestões específicas para melhorar o prompt:
- Problemas identificados
- Sugestões de alteração
- Trecho específico do prompt a modificar (se aplicável)""",
        agent=refinador,
        context=[task_gerar, task_avaliar]
    )
    
    return [task_gerar, task_avaliar, task_refinar]


def run_validation_crew(prompt: str, scenario: dict) -> dict:
    """
    Executa uma validação completa para um cenário.
    
    Args:
        prompt: Prompt a ser testado
        scenario: Dicionário com dados do cenário
        
    Returns:
        Resultados da validação incluindo outputs de cada agente
    """
    gerador, avaliador, refinador = create_validation_agents()
    tasks = create_validation_tasks(gerador, avaliador, refinador, prompt, scenario)
    
    crew = Crew(
        agents=[gerador, avaliador, refinador],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    result = crew.kickoff()
    
    return {
        "scenario": scenario.get("nome", "Unknown"),
        "result": result,
        "tasks_output": [task.output for task in tasks if hasattr(task, 'output')]
    }
