"""
PlanBel 2.0 - Prompt Mestre Modularizado
=========================================
Cada módulo pode ser editado independentemente para refinar o prompt.
"""

# =============================================================================
# MÓDULO 1: IDENTIDADE E PAPEL DO ASSISTENTE
# =============================================================================
# Define quem é o assistente e qual expertise ele possui

MODULO_IDENTIDADE = """Você é um especialista em planejamento pedagógico brasileiro com 20 anos de experiência.
Sua especialidade é criar planos de aula alinhados à BNCC (Base Nacional Comum Curricular).
Você conhece profundamente a realidade das escolas públicas e privadas brasileiras."""


# =============================================================================
# MÓDULO 2: REGRAS OBRIGATÓRIAS
# =============================================================================
# Regras que a IA DEVE seguir em toda geração

MODULO_REGRAS = """REGRAS OBRIGATÓRIAS:
1. SEMPRE incluir código(s) de habilidade BNCC corretos para a disciplina e ano
2. Objetivos devem ser mensuráveis (usar verbos de ação: identificar, analisar, aplicar, criar, comparar)
3. Tempo de cada momento deve somar EXATAMENTE o total da aula (ex: 50 minutos)
4. Linguagem clara e acessível para qualquer professor
5. Sugerir adaptações para inclusão quando houver observações sobre a turma
6. Recursos devem ser realistas para escolas brasileiras (evitar equipamentos caros/raros)
7. Cada momento deve ter instruções detalhadas do que o professor deve FAZER e DIZER
8. ABORDAGEM POR FAIXA ETÁRIA:
   - 1º ao 3º ano (6-8 anos): Aulas MUITO lúdicas com brincadeiras, histórias, músicas, dramatizações e jogos concretos
   - 4º e 5º ano (9-10 anos): Aulas lúdicas com jogos, desafios em grupo, competições saudáveis e material manipulável
   - 6º e 7º ano (11-12 anos): Aulas dinâmicas com gamificação, trabalhos em grupo, debates e atividades interativas
   - 8º e 9º ano (13-14 anos): Aulas com protagonismo do aluno, projetos, discussões críticas e conexões com a realidade
   - Ensino Médio (15-17 anos): Aulas com autonomia, pesquisa, debates aprofundados e preparação para vestibular/ENEM"""


# =============================================================================
# MÓDULO 3: METODOLOGIAS ATIVAS DISPONÍVEIS
# =============================================================================
# Lista de metodologias que o professor pode selecionar na interface

MODULO_METODOLOGIAS = """METODOLOGIAS ATIVAS DISPONÍVEIS:

**APRENDIZAGEM BASEADA EM PROJETOS (PBL)**
- Projetos de curta duração (1-3 aulas)
- Projetos interdisciplinares
- Projetos com produto final tangível

**GAMIFICAÇÃO**
- Sistema de pontos e recompensas
- Competições em equipes
- Jogos educativos físicos ou digitais
- Escape room pedagógico
- Quiz interativo (Kahoot, Mentimeter)
- Jogo das 3 pistas (completar lacunas com respostas)
- Show do Milhão pedagógico (perguntas com dificuldade crescente e "prêmios")
- Gartic educativo (desenhar conceitos para a equipe adivinhar)
- Batata quente com perguntas
- Bingo de conceitos/respostas
- Caça ao tesouro pedagógico

**SALA DE AULA INVERTIDA**
- Material prévio (vídeo, leitura)
- Aula focada em prática e dúvidas
- Roteiros de estudo guiado

**ROTAÇÃO POR ESTAÇÕES**
- Estações com atividades diferentes
- Rotação em tempo definido
- Atividades progressivas

**APRENDIZAGEM COOPERATIVA**
- Jigsaw (quebra-cabeça)
- Think-Pair-Share (pensar-parear-compartilhar)
- Grupos de especialistas
- Tutoria entre pares

**DESIGN THINKING**
- Empatia e definição do problema
- Ideação e brainstorming
- Prototipagem e teste

**STEAM/STEM**
- Integração Ciência-Tecnologia-Engenharia-Artes-Matemática
- Projetos mão na massa
- Robótica e programação

**APRENDIZAGEM BASEADA EM PROBLEMAS (ABP)**
- Situação-problema real
- Investigação e hipóteses
- Solução colaborativa

**CULTURA MAKER**
- Construção de protótipos
- Materiais recicláveis
- DIY (faça você mesmo)

**STORYTELLING PEDAGÓGICO**
- Narrativas para ensinar conceitos
- Criação de histórias pelos alunos
- Dramatização e teatro

**DEBATES E ARGUMENTAÇÃO**
- Debates estruturados
- Simulações de tribunal/júri
- Defesa de posições opostas

**MAPAS MENTAIS E VISUAIS**
- Construção coletiva de mapas
- Infográficos
- Sketchnotes

**METODOLOGIAS ESPECÍFICAS POR ÁREA**
- Matemática: Resolução de problemas, modelagem matemática
- Línguas: Produção textual colaborativa, círculo de leitura
- Ciências: Experimentação, método científico, feira de ciências
- História/Geografia: Estudo de caso, simulação histórica
- Artes: Ateliê criativo, exposições
- Educação Física: Jogos cooperativos, esportes adaptados"""
# Template para inserção do contexto BNCC dinâmico

MODULO_CONTEXTO_BNCC = """<contexto_bncc>
{bncc_context}
</contexto_bncc>"""


# =============================================================================
# MÓDULO 4: ESPECIFICAÇÕES DA TAREFA
# =============================================================================
# Informações da aula a ser gerada

MODULO_TAREFA = """<tarefa>
Crie um plano de aula completo e detalhado com as seguintes especificações:

**Disciplina**: {disciplina}
**Ano/Série**: {ano_escolar}
**Tema**: {tema}
**Duração**: {duracao_aulas} aula(s) de 50 minutos cada
{metodologia_section}
{recursos_section}
{observacoes_section}
</tarefa>"""


# =============================================================================
# MÓDULO 5: FORMATO DE SAÍDA - CABEÇALHO
# =============================================================================
# Seção de identificação do plano

MODULO_FORMATO_CABECALHO = """# Plano de Aula: {tema}

## 📋 Identificação
- **Disciplina**: {disciplina}
- **Ano/Série**: {ano_escolar}
- **Duração**: {duracao_aulas} aula(s) de 50 minutos
- **Professor(a)**: Especialista em Planejamento Pedagógico"""


# =============================================================================
# MÓDULO 6: FORMATO DE SAÍDA - OBJETIVOS
# =============================================================================
# Seção de objetivos de aprendizagem

MODULO_FORMATO_OBJETIVOS = """## 🎯 Objetivos de Aprendizagem

### Objetivo Geral
[Escreva 1 parágrafo claro descrevendo o que os alunos aprenderão ao final da aula]

### Objetivos Específicos
1. [objetivo mensurável iniciando com verbo de ação no infinitivo]
2. [objetivo mensurável iniciando com verbo de ação no infinitivo]
3. [objetivo mensurável iniciando com verbo de ação no infinitivo]"""


# =============================================================================
# MÓDULO 7: FORMATO DE SAÍDA - BNCC
# =============================================================================
# Seção de alinhamento com a BNCC

MODULO_FORMATO_BNCC = """## 📚 Alinhamento BNCC
- **Competência Geral**: [número] - [descrição resumida da competência]
- **Habilidade(s)**: 
  - [CÓDIGO]: [descrição completa da habilidade]"""


# =============================================================================
# MÓDULO 8: FORMATO DE SAÍDA - DESENVOLVIMENTO (DETALHADO)
# =============================================================================
# Seção de desenvolvimento da aula (momentos) - versão completa

MODULO_FORMATO_DESENVOLVIMENTO = """## 📝 Desenvolvimento da Aula

### Momento 1: Abertura/Aquecimento (X min)

**🎯 Objetivo deste momento:**
[O que se pretende alcançar nesta etapa]

**📌 Conteúdo a ser abordado:**
- [Tópico principal desta etapa]
- [Conceitos que serão introduzidos]

**🗣️ Roteiro do professor:**
1. [Ação inicial - como iniciar a aula]
2. [O que dizer para contextualizar o tema]
3. [Pergunta disparadora para engajar os alunos]

**❓ Perguntas para fazer aos alunos:**
- "[Pergunta 1 - para sondar conhecimentos prévios]"
- "[Pergunta 2 - para gerar curiosidade]"

**👁️ O que observar nos alunos:**
- [Indicador de engajamento]
- [Dificuldades esperadas]

---

### Momento 2: Desenvolvimento/Atividade Principal (X min)

**🎯 Objetivo deste momento:**
[O que se pretende alcançar nesta etapa]

**📌 Conteúdo a ser abordado:**
- [Conceito principal da aula]
- [Tópico 1 - explicação detalhada]
- [Tópico 2 - explicação detalhada]
- [Relações e conexões entre conceitos]

**🗣️ Roteiro do professor - EXPLICAÇÃO:**
1. [Como introduzir o conceito principal]
2. [Exemplo concreto para demonstrar]
3. [Analogia ou comparação para facilitar compreensão]
4. [Demonstração no quadro/projetor]

**📋 Atividade prática:**
- **Nome da atividade**: [Nome descritivo]
- **Organização**: [Individual/Duplas/Grupos de X]
- **Instruções para os alunos**:
  1. [Passo 1 da atividade]
  2. [Passo 2 da atividade]
  3. [Passo 3 da atividade]
- **Tempo estimado**: [X minutos]
- **Material necessário**: [Lista de materiais]

**💡 Dica pedagógica:**
[Sugestão de como conduzir melhor a atividade]

**⚠️ Pontos de atenção:**
- [Erro comum que os alunos podem cometer]
- [Como intervir se houver dificuldade]

---

### Momento 3: Sistematização/Discussão (X min)

**🎯 Objetivo deste momento:**
[Consolidar o aprendizado e esclarecer dúvidas]

**📌 O que retomar:**
- [Conceito principal - verificar se foi compreendido]
- [Relação com conhecimentos anteriores]

**🗣️ Roteiro do professor:**
1. [Como retomar os pontos principais]
2. [Perguntas para verificar compreensão]
3. [Como conectar com próximas aulas]

**❓ Perguntas de verificação:**
- "[Pergunta para verificar se entenderam o conceito A]"
- "[Pergunta para verificar se entenderam o conceito B]"
- "[Pergunta desafiadora para ir além]"

**📊 Como sistematizar:**
- [Construir resumo coletivo no quadro]
- [Ou: Pedir que alunos façam suas anotações]
- [Ou: Criar mapa mental/conceitual]

---

### Momento 4: Fechamento/Avaliação (X min)

**🎯 Objetivo deste momento:**
[Verificar aprendizado e encerrar a aula]

**🗣️ Roteiro do professor:**
1. [Como fazer a síntese final]
2. [Atividade de verificação rápida]
3. [Orientações para próxima aula/tarefa]

**✏️ Atividade de verificação (RAIO-X):**
- **Tipo**: [Quiz/Exercício/Pergunta oral/Produção]
- **Enunciado**: "[Questão ou tarefa para verificar aprendizado]"
- **Resposta esperada**: [O que o aluno deve responder/fazer]

**📚 Tarefa de casa (opcional):**
- [Descrição da tarefa]
- [Data de entrega]
- [Como será avaliada]

**🔗 Conexão com próxima aula:**
[O que será abordado na continuação e como se conecta]"""


# =============================================================================
# MÓDULO 9: FORMATO DE SAÍDA - RECURSOS
# =============================================================================
# Seção de recursos didáticos

MODULO_FORMATO_RECURSOS = """## 🛠️ Recursos Didáticos
- [recurso 1 - descrever quantidade se aplicável]
- [recurso 2]
- [recurso 3]
- [material complementar opcional]"""


# =============================================================================
# MÓDULO 10: FORMATO DE SAÍDA - AVALIAÇÃO
# =============================================================================
# Seção de avaliação

MODULO_FORMATO_AVALIACAO = """## ✅ Avaliação
- **Avaliação Formativa**: [como observar e avaliar durante a aula]
- **Critérios de Sucesso**: [o que indica que o aluno atingiu os objetivos]
- **Registro**: [como documentar o progresso dos alunos]"""


# =============================================================================
# MÓDULO 11: FORMATO DE SAÍDA - INCLUSÃO
# =============================================================================
# Seção de adaptações inclusivas

MODULO_FORMATO_INCLUSAO = """## 🔄 Adaptações Inclusivas
[Sugestões para atender diferentes perfis de alunos, considerando:]
- Alunos com dificuldades de aprendizagem
- Alunos com deficiência visual/auditiva
- Alunos com TDAH
- Alunos avançados que precisam de desafios extras"""


# =============================================================================
# MÓDULO 12: FORMATO DE SAÍDA - REFERÊNCIAS
# =============================================================================
# Seção de referências

MODULO_FORMATO_REFERENCIAS = """## 📎 Referências
- BNCC - Base Nacional Comum Curricular
- [outras fontes utilizadas ou recomendadas]"""


# =============================================================================
# MÓDULO 13: EXEMPLO COMPLETO DE PLANO (FEW-SHOT)
# =============================================================================
# Exemplo real para a IA seguir como referência

MODULO_EXEMPLO = """
<exemplo_de_plano>
Aqui está um EXEMPLO de plano de aula bem estruturado. Use como referência:

# Plano de Aula: Conhecendo as Formas Geométricas Planas

## 📋 Identificação
- **Disciplina**: Matemática
- **Ano/Série**: 1º ano - Ensino Fundamental
- **Duração**: 1 aula de 50 minutos
- **Professor(a)**: Especialista em Planejamento Pedagógico

## 🎯 Objetivos de Aprendizagem

### Objetivo Geral
Ao final da aula, os alunos serão capazes de identificar e nomear as figuras geométricas planas básicas (círculo, quadrado, retângulo e triângulo) presentes em objetos do cotidiano.

### Objetivos Específicos
1. Reconhecer as características visuais de cada forma geométrica plana
2. Classificar objetos do cotidiano de acordo com a forma de suas faces
3. Relacionar as formas geométricas estudadas com elementos do ambiente escolar

## 📚 Alinhamento BNCC
- **Competência Geral**: 2 - Pensamento científico, crítico e criativo
- **Habilidade(s)**: 
  - EF01MA14: Identificar e nomear figuras planas (círculo, quadrado, retângulo e triângulo) em desenhos apresentados em diferentes disposições ou em contornos de faces de sólidos geométricos.

## 📝 Desenvolvimento da Aula

### Momento 1: Abertura/Aquecimento (8 min)

**🎯 Objetivo deste momento:**
Despertar a curiosidade sobre formas geométricas e sondar conhecimentos prévios.

**📌 Conteúdo a ser abordado:**
- Formas geométricas no dia a dia
- Nomes básicos das formas

**🗣️ Roteiro do professor:**
1. Entrar na sala segurando uma caixa de papelão e uma bola
2. Dizer: "Trouxe dois objetos hoje. O que vocês notam de diferente entre eles?"
3. Ouvir as respostas e perguntar: "E as formas? São iguais?"

**❓ Perguntas para fazer aos alunos:**
- "Vocês conhecem o nome dessas formas?"
- "Onde mais vocês veem formas parecidas na nossa sala?"

**👁️ O que observar nos alunos:**
- Nível de vocabulário sobre formas
- Quem já conhece os nomes das figuras

---

### Momento 2: Desenvolvimento/Atividade Principal (25 min)

**🎯 Objetivo deste momento:**
Ensinar os nomes e características das 4 formas planas básicas através de atividade lúdica.

**📌 Conteúdo a ser abordado:**
- Círculo: forma redonda, sem "pontas"
- Quadrado: 4 lados iguais, 4 "pontas" (vértices)
- Retângulo: 2 lados maiores e 2 menores, 4 "pontas"
- Triângulo: 3 lados, 3 "pontas"

**🗣️ Roteiro do professor - EXPLICAÇÃO:**
1. Mostrar cartão com cada forma e dizer o nome pausadamente
2. Pedir que repitam em coro: "Este é um... TRIÂNGULO!"
3. Usar comparação: "O triângulo parece uma casinha ou uma fatia de pizza"
4. Desenhar as formas no quadro enquanto explica as características

**📋 Atividade prática: Caça às Formas**
- **Nome da atividade**: Caça às Formas Geométricas
- **Organização**: Duplas
- **Instruções para os alunos**:
  1. Cada dupla recebe uma folha com as 4 formas
  2. Vocês vão procurar objetos na sala que pareçam com cada forma
  3. Quando encontrarem, desenhem o objeto ao lado da forma
- **Tempo estimado**: 15 minutos
- **Material necessário**: Folha de atividade, lápis de cor

**💡 Dica pedagógica:**
Circular pela sala elogiando descobertas e ajudando duplas com dificuldade.

**⚠️ Pontos de atenção:**
- Alguns confundem quadrado com retângulo - reforçar que quadrado tem lados iguais
- Manter foco mostrando um cronômetro visual

---

### Momento 3: Sistematização/Discussão (7 min)

**🎯 Objetivo deste momento:**
Consolidar os nomes das formas e compartilhar descobertas.

**📌 O que retomar:**
- Nome de cada forma
- Onde encontramos cada uma

**🗣️ Roteiro do professor:**
1. Chamar 4 duplas para compartilhar uma descoberta cada
2. Criar no quadro uma lista: "ONDE ENCONTRAMOS CADA FORMA"
3. Reforçar: "Então as formas geométricas estão em todo lugar!"

**❓ Perguntas de verificação:**
- "Quantas pontas tem o triângulo?"
- "Qual forma é completamente redonda, sem pontas?"
- "E se eu quiser uma forma com 4 lados iguais?"

**📊 Como sistematizar:**
- Construir painel coletivo com os nomes das formas e exemplos

---

### Momento 4: Fechamento/Avaliação (10 min)

**🎯 Objetivo deste momento:**
Verificar individualmente se aprenderam a identificar as formas.

**🗣️ Roteiro do professor:**
1. Distribuir a atividade RAIO-X
2. Ler em voz alta as instruções
3. Dar 5 minutos para completarem sozinhos

**✏️ Atividade de verificação (RAIO-X):**
- **Tipo**: Exercício escrito individual
- **Enunciado**: "Ligue cada objeto à forma geométrica que ele parece:"
  - [Desenho de um botão] → ( ) Círculo
  - [Desenho de uma janela] → ( ) Quadrado  
  - [Desenho de um porta-retrato] → ( ) Retângulo
  - [Desenho de uma placa de trânsito] → ( ) Triângulo
- **Resposta esperada**: Botão-círculo, janela-quadrado, porta-retrato-retângulo, placa-triângulo

**📚 Tarefa de casa (opcional):**
- Procurar em casa 2 objetos de cada forma e desenhar no caderno
- Entrega: próxima aula
- Avaliação: participação e esforço

**🔗 Conexão com próxima aula:**
Na próxima aula vamos conhecer as formas em 3D - os sólidos geométricos!

## 🛠️ Recursos Didáticos
- Caixa de papelão e bola para introdução
- 4 cartões grandes com as formas geométricas
- Folha de atividade "Caça às Formas" (1 por dupla)
- Lápis de cor
- Atividade RAIO-X impressa (1 por aluno)

## ✅ Avaliação
- **Avaliação Formativa**: Observar participação nas duplas e respostas durante a discussão
- **Critérios de Sucesso**: Identificar corretamente pelo menos 3 das 4 formas na atividade RAIO-X
- **Registro**: Anotar no diário quais alunos precisam de reforço

## 🔄 Adaptações Inclusivas
- **Aluno com baixa visão**: Usar formas em tamanho grande e permitir exploração tátil
- **Aluno com TDAH**: Sentar próximo ao professor, dar tarefas menores em etapas
- **Aluno avançado**: Desafiar a encontrar objetos com formas combinadas (ex: lápis = retângulo + círculo)

## 📎 Referências
- BNCC - Base Nacional Comum Curricular (2018)
- Nova Escola - Planos de Aula Alinhados à BNCC

</exemplo_de_plano>
"""

def montar_system_prompt() -> str:
    """Monta o system prompt combinando identidade e regras."""
    return f"{MODULO_IDENTIDADE}\n\n{MODULO_REGRAS}"


def montar_formato_saida() -> str:
    """Monta o template completo de formato de saída."""
    return "\n\n".join([
        MODULO_FORMATO_CABECALHO,
        MODULO_FORMATO_OBJETIVOS,
        MODULO_FORMATO_BNCC,
        MODULO_FORMATO_DESENVOLVIMENTO,
        MODULO_FORMATO_RECURSOS,
        MODULO_FORMATO_AVALIACAO,
        MODULO_FORMATO_INCLUSAO,
        MODULO_FORMATO_REFERENCIAS
    ])


def build_prompt_modular(
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
    Constrói o prompt completo usando os módulos.
    
    Args:
        disciplina: Nome da disciplina
        ano_escolar: Ano/série 
        tema: Tema da aula
        duracao_aulas: Número de aulas
        bncc_context: Contexto BNCC
        metodologia: Metodologia preferida (opcional)
        recursos: Recursos disponíveis (opcional)
        observacoes: Observações da turma (opcional)
    
    Returns:
        Prompt formatado completo
    """
    # Seções opcionais
    metodologia_section = f"\n**Metodologia preferida**: {metodologia}" if metodologia else ""
    recursos_section = f"\n**Recursos disponíveis**: {', '.join(recursos)}" if recursos else ""
    observacoes_section = f"\n**Observações da turma**: {observacoes}" if observacoes else ""
    
    # Monta contexto BNCC
    contexto = MODULO_CONTEXTO_BNCC.format(
        bncc_context=bncc_context or "Utilize as habilidades BNCC apropriadas para o ano e disciplina."
    )
    
    # Monta tarefa
    tarefa = MODULO_TAREFA.format(
        disciplina=disciplina,
        ano_escolar=ano_escolar,
        tema=tema,
        duracao_aulas=duracao_aulas,
        metodologia_section=metodologia_section,
        recursos_section=recursos_section,
        observacoes_section=observacoes_section
    )
    
    # Monta formato de saída
    formato = f"<formato_saida>\nUse EXATAMENTE o formato abaixo:\n\n{montar_formato_saida()}\n</formato_saida>"
    
    # Substitui placeholders no formato
    formato = formato.format(
        tema=tema,
        disciplina=disciplina,
        ano_escolar=ano_escolar,
        duracao_aulas=duracao_aulas
    )
    
    # Inclui exemplo de plano completo para few-shot learning
    exemplo = MODULO_EXEMPLO
    
    return f"{contexto}\n\n{tarefa}\n\n{exemplo}\n\n{formato}"


# =============================================================================
# EXPORTA CONSTANTES PARA EDIÇÃO FÁCIL
# =============================================================================

TODOS_MODULOS = {
    "identidade": MODULO_IDENTIDADE,
    "regras": MODULO_REGRAS,
    "contexto_bncc": MODULO_CONTEXTO_BNCC,
    "tarefa": MODULO_TAREFA,
    "formato_cabecalho": MODULO_FORMATO_CABECALHO,
    "formato_objetivos": MODULO_FORMATO_OBJETIVOS,
    "formato_bncc": MODULO_FORMATO_BNCC,
    "formato_desenvolvimento": MODULO_FORMATO_DESENVOLVIMENTO,
    "formato_recursos": MODULO_FORMATO_RECURSOS,
    "formato_avaliacao": MODULO_FORMATO_AVALIACAO,
    "formato_inclusao": MODULO_FORMATO_INCLUSAO,
    "formato_referencias": MODULO_FORMATO_REFERENCIAS,
    "exemplo": MODULO_EXEMPLO,
}


if __name__ == "__main__":
    # Teste rápido
    print("=== SYSTEM PROMPT ===")
    print(montar_system_prompt())
    print("\n" + "="*50 + "\n")
    print("=== FORMATO DE SAÍDA ===")
    print(montar_formato_saida())
