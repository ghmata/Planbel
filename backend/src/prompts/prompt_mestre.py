"""
PlanBel 2.0 - Prompt Mestre para Geração de Planos de Aula
Otimizado para Groq/Llama 3.3 70B
"""

SYSTEM_PROMPT = """Você é um especialista em planejamento pedagógico brasileiro com 20 anos de experiência.
Sua especialidade é criar planos de aula alinhados à BNCC (Base Nacional Comum Curricular).

REGRAS OBRIGATÓRIAS:
1. SEMPRE incluir código(s) de habilidade BNCC corretos
2. Objetivos devem ser mensuráveis (verbos de ação: identificar, analisar, aplicar, criar)
3. Tempo de cada momento deve somar o total da aula
4. Linguagem clara, acessível para qualquer professor
5. Sugerir adaptações para inclusão quando relevante
6. Recursos devem ser realistas para escolas brasileiras"""

PROMPT_TEMPLATE = """<contexto_bncc>
{bncc_context}
</contexto_bncc>

<tarefa>
Crie um plano de aula completo com as seguintes especificações:

**Disciplina**: {disciplina}
**Ano/Série**: {ano_escolar}
**Tema**: {tema}
**Duração**: {duracao_aulas} aula(s) de 50 minutos
{metodologia_section}
{recursos_section}
{observacoes_section}
</tarefa>

<formato_saida>
Use EXATAMENTE o formato abaixo, preenchendo cada seção:

# Plano de Aula: {tema}

## 📋 Identificação
- **Disciplina**: {disciplina}
- **Ano/Série**: {ano_escolar}
- **Duração**: {duracao_aulas} aula(s) de 50 minutos
- **Professor(a)**: [A definir]

## 🎯 Objetivos de Aprendizagem

### Objetivo Geral
[1 parágrafo descrevendo o objetivo principal]

### Objetivos Específicos
1. [objetivo mensurável com verbo de ação]
2. [objetivo mensurável com verbo de ação]
3. [objetivo mensurável com verbo de ação]

## 📚 Alinhamento BNCC
- **Competência Geral**: [número e descrição resumida]
- **Habilidade(s)**: [código(s) e descrição da habilidade]

## 📝 Desenvolvimento da Aula

### Momento 1: Abertura (X min)
[descrição detalhada do que o professor deve fazer]

### Momento 2: Desenvolvimento (X min)
[descrição detalhada com atividades práticas]

### Momento 3: Fechamento (X min)
[descrição de como encerrar e verificar aprendizagem]

## 🛠️ Recursos Didáticos
- [recurso 1]
- [recurso 2]
- [recurso 3]

## ✅ Avaliação
- **Formativa**: [como avaliar durante a aula]
- **Critérios**: [o que será observado nos alunos]

## 🔄 Adaptações Inclusivas
[sugestões para atender diferentes perfis de alunos]

## 📎 Referências
[fontes e materiais de apoio utilizados]
</formato_saida>"""


def build_prompt(
    disciplina: str,
    ano_escolar: str,
    tema: str,
    duracao_aulas: int = 1,
    bncc_context: str = "",
    metodologia: str | None = None,
    recursos: list[str] | None = None,
    observacoes: str | None = None
) -> str:
    """
    Constrói o prompt completo para geração de plano de aula.
    
    Args:
        disciplina: Nome da disciplina (ex: "Matemática")
        ano_escolar: Ano/série (ex: "7º ano - Ensino Fundamental")
        tema: Tema da aula (ex: "Frações e operações")
        duracao_aulas: Número de aulas de 50 minutos
        bncc_context: Contexto BNCC relevante (habilidades filtradas)
        metodologia: Metodologia preferida (opcional)
        recursos: Lista de recursos disponíveis (opcional)
        observacoes: Observações sobre a turma (opcional)
    
    Returns:
        Prompt formatado pronto para envio ao LLM
    """
    # Seções opcionais
    metodologia_section = ""
    if metodologia:
        metodologia_section = f"\n**Metodologia preferida**: {metodologia}"
    
    recursos_section = ""
    if recursos:
        recursos_section = f"\n**Recursos disponíveis**: {', '.join(recursos)}"
    
    observacoes_section = ""
    if observacoes:
        observacoes_section = f"\n**Observações da turma**: {observacoes}"
    
    return PROMPT_TEMPLATE.format(
        disciplina=disciplina,
        ano_escolar=ano_escolar,
        tema=tema,
        duracao_aulas=duracao_aulas,
        bncc_context=bncc_context or "Utilize as habilidades BNCC apropriadas para o ano e disciplina.",
        metodologia_section=metodologia_section,
        recursos_section=recursos_section,
        observacoes_section=observacoes_section
    )


# Cenários de teste para validação
TEST_SCENARIOS = [
    {
        "nome": "Anos Iniciais - Matemática",
        "disciplina": "Matemática",
        "ano_escolar": "3º ano - Ensino Fundamental",
        "tema": "Adição e subtração com agrupamento",
        "duracao_aulas": 1
    },
    {
        "nome": "Anos Finais - Português",
        "disciplina": "Língua Portuguesa",
        "ano_escolar": "7º ano - Ensino Fundamental",
        "tema": "Tipos de narrador e ponto de vista narrativo",
        "duracao_aulas": 2
    },
    {
        "nome": "Ensino Médio - Biologia",
        "disciplina": "Biologia",
        "ano_escolar": "2º ano - Ensino Médio",
        "tema": "Divisão celular: mitose e meiose",
        "duracao_aulas": 2
    },
    {
        "nome": "Inclusão - História",
        "disciplina": "História",
        "ano_escolar": "6º ano - Ensino Fundamental",
        "tema": "Civilizações antigas da Mesopotâmia",
        "duracao_aulas": 1,
        "observacoes": "Turma com 2 alunos com TDAH e 1 aluno com baixa visão"
    },
    {
        "nome": "Recursos Limitados - Ciências",
        "disciplina": "Ciências",
        "ano_escolar": "5º ano - Ensino Fundamental",
        "tema": "Ciclo da água",
        "duracao_aulas": 1,
        "recursos": ["quadro branco", "livro didático"],
        "observacoes": "Escola sem laboratório ou projetor"
    }
]
