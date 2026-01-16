"""
PlanBel 2.0 - API de Geração de Planos de Aula
===============================================
Servidor Flask que conecta a interface HTML com o prompt modular.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
import logging
from typing import Dict, Tuple

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from src.prompts.prompt_modular import montar_system_prompt, build_prompt_modular
from src.bncc import get_bncc_context

load_dotenv()

app = Flask(__name__)
CORS(app)  # Permitir chamadas do HTML local

# Configuração Gemini
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("ERRO: Chave de API do Gemini não encontrada no .env (GEMINI_API_KEY ou GOOGLE_API_KEY)")
else:
    genai.configure(api_key=api_key)

# Modelo padrão (gemini-3-pro solicitado pelo usuário)
# Modelo padrão
model_name = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")


@app.route('/')
def index():
    """Serve a interface HTML."""
    return send_from_directory('.', 'teste_interface.html')


@app.route('/api/gerar-plano', methods=['POST'])
def gerar_plano():
    """
    Gera um plano de aula usando o prompt modular completo.
    
    Body esperado:
    {
        "disciplina": "Matemática",
        "ano_escolar": "3º ano - Ensino Fundamental",
        "tema": "Multiplicação",
        "duracao_aulas": 1,
        "metodologia": "Gamificação",
        "recursos": ["Quadro/Lousa", "Material Manipulável"],
        "observacoes": "Turma com 25 alunos"
    }
    """
    try:
        data = request.json
        
        # Validar campos obrigatórios
        required = ['disciplina', 'ano_escolar', 'tema']
        for field in required:
            if not data.get(field):
                return jsonify({"error": f"Campo obrigatório: {field}"}), 400
        
        # Extrair parâmetros
        disciplina = data['disciplina']
        ano_escolar = data['ano_escolar']
        tema = data['tema']
        duracao_aulas = data.get('duracao_aulas', 1)
        metodologia = data.get('metodologia')
        recursos = data.get('recursos', [])
        observacoes = data.get('observacoes')
        
        # Buscar contexto BNCC
        bncc_context = get_bncc_context(disciplina, ano_escolar)
        
        # Montar prompts
        system_prompt = montar_system_prompt()
        user_prompt = build_prompt_modular(
            disciplina=disciplina,
            ano_escolar=ano_escolar,
            tema=tema,
            duracao_aulas=duracao_aulas,
            bncc_context=bncc_context,
            metodologia=metodologia,
            recursos=recursos if recursos else None,
            observacoes=observacoes
        )
        
        # Chamar Gemini
        # Instanciar modelo com a system prompt específica desta chamada
        gemini_model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt
        )
        
        response = gemini_model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=6000
            )
        )
        
        plano = response.text
        tokens = response.usage_metadata.total_token_count if response.usage_metadata else 0
        
        return jsonify({
            "success": True,
            "plano": plano,
            "tokens": tokens
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/health')
def health():
    """Endpoint de verificação de saúde."""
    return jsonify({
        "status": "ok",
        "model": model_name,
        "api_key_set": bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    })


@app.route('/api/gerar-plano-estruturado', methods=['POST'])
def gerar_plano_estruturado():
    """
    Gera um plano de aula em formato JSON estruturado para o frontend Lovable.
    Usa o prompt modular completo para máxima qualidade.
    """
    import json
    import uuid
    
    try:
        data = request.json
        
        # Extrair parâmetros com fallbacks
        # Adaptação para múltiplas disciplinas
        disciplinas_list = data.get('disciplinas', [])
        if disciplinas_list and isinstance(disciplinas_list, list):
            disciplina_nomes = [d.get('nome') for d in disciplinas_list if isinstance(d, dict) and d.get('nome')]
            # Se a lista de objetos falhar, tenta pegar strings diretas (caso o frontend mude formato)
            if not disciplina_nomes: 
                 disciplina_nomes = [d for d in disciplinas_list if isinstance(d, str)]
            
            if disciplina_nomes:
                disciplina = ', '.join(disciplina_nomes)
            else:
                disciplina = data.get('disciplina', 'Matemática')
        else:
            disciplina = data.get('disciplina', 'Matemática')
        ano_escolar = data.get('ano_escolar', '3º ano - Ensino Fundamental')
        tema = data.get('tema', 'Tema geral')
        duracao = data.get('duracao', '50')
        duracao_aulas = max(1, int(duracao) // 50) if duracao else 1
        
        # Novos campos do wizard
        segmento = data.get('segmento', 'fundamental1')
        objetivos = data.get('objetivos', '')
        dinamicas = data.get('dinamicas', [])
        avaliacoes = data.get('avaliacoes', [])
        metodologias = data.get('metodologias', [])
        metodologia = data.get('metodologia') or ', '.join(metodologias) if metodologias else None
        recursos = data.get('recursos', [])
        materiais_disponiveis = data.get('materiais_disponiveis', [])
        materiais_custom = data.get('materiais_custom', '')
        permitir_extras = data.get('permitir_extras', False)
        observacoes = data.get('observacoes', '')
        gerar_material_impresso = data.get('gerar_material_impresso', False)
        detalhes_gamificacao = data.get('detalhes_gamificacao')
        print(f"DEBUG: Recebido gerar_material_impresso = {gerar_material_impresso}")
        
        # Incorporar detalhes da gamificação no texto da metodologia
        if detalhes_gamificacao and ('Gamificação' in (metodologia or '') or 'gamificacao' in metodologias):
            metodologia_texto = f"Gamificação (Foco: {detalhes_gamificacao})" 
            if metodologia:
                metodologia += f", usando {detalhes_gamificacao}"
        else:
            metodologia_texto = metodologia or ', '.join(metodologias) if metodologias else None
        
        # Combinar todos os materiais
        todos_materiais = recursos + materiais_disponiveis
        if materiais_custom:
            todos_materiais.append(materiais_custom)
        
        # Buscar contexto BNCC real
        bncc_context = get_bncc_context(disciplina, ano_escolar)
        
        # Usar o system prompt modular completo
        system_prompt = montar_system_prompt()
        
        # Adicionar instrução de JSON ao system prompt
        system_prompt += """

INSTRUÇÃO CRÍTICA DE FORMATO:
Você DEVE responder SOMENTE com um objeto JSON válido.
NÃO inclua texto antes ou depois do JSON.
NÃO use blocos de código markdown (```).
Apenas o JSON puro."""

        # Montar o prompt modular completo
        from src.prompts.prompt_modular import MODULO_METODOLOGIAS, MODULO_EXEMPLO
        
        # Formatar dinâmicas de interação
        dinamicas_texto = ', '.join(dinamicas) if dinamicas else 'A critério do professor'
        
        # Formatar tipos de avaliação
        avaliacoes_texto = ', '.join(avaliacoes) if avaliacoes else 'Observação direta'
        
        # Instrução condicional para material impresso
        if gerar_material_impresso:
            material_impresso_json = ''',
  
  "materialImpresso": "📋 SUGESTÃO DE ATIVIDADE IMPRESSA\\n\\n📝 Título da Atividade: [Nome criativo]\\n\\n🎯 Objetivo: [O que o aluno deve demonstrar]\\n\\n📄 ATIVIDADE COMPLETA:\\n\\n[Crie uma atividade detalhada pronta para imprimir com:]\\n- Cabeçalho: Nome do aluno, Data, Turma\\n- Enunciado claro e objetivo\\n- Questões numeradas (mínimo 5 questões)\\n- Espaços/linhas para respostas\\n\\n📝 GABARITO (para o professor):\\n[Respostas de cada questão]\\n\\n⚠️ AVISO: Sugestão gerada por IA. Revise antes de usar."'''
            material_impresso_instrucao = "- INCLUA o campo 'materialImpresso' com uma atividade COMPLETA pronta para imprimir"
        else:
            material_impresso_json = ""
            material_impresso_instrucao = "- NÃO inclua o campo 'materialImpresso'"
        
        # User prompt combinando o prompt modular com pedido de JSON
        user_prompt = f"""
<contexto_bncc>
{bncc_context}
</contexto_bncc>

<tarefa>
Crie um plano de aula COMPLETO e DETALHADO com as seguintes especificações:

**Disciplina**: {disciplina}
**Ano/Série**: {ano_escolar}
**Segmento**: {segmento.replace('fundamental1', 'Ensino Fundamental I').replace('fundamental2', 'Ensino Fundamental II').replace('medio', 'Ensino Médio')}
**Tema/Conteúdo**: {tema}
**Duração**: {duracao_aulas} aula(s) de 50 minutos cada ({duracao} min total)

**OBJETIVOS DE APRENDIZAGEM DEFINIDOS PELO PROFESSOR**:
{objetivos or 'O professor deseja que os alunos compreendam e apliquem os conceitos do tema.'}

**Dinâmicas de Interação**: {dinamicas_texto}
**Tipos de Avaliação a usar**: {avaliacoes_texto}
**Metodologias ativas preferidas**: {metodologia or 'Gamificação, atividades práticas'} {f"(Detalhes: {detalhes_gamificacao})" if detalhes_gamificacao else ""}
**Recursos disponíveis**: {', '.join(todos_materiais) if todos_materiais else 'Quadro, material impresso, materiais básicos'}
**Permitir materiais extras**: {'Sim, pode sugerir materiais adicionais' if permitir_extras else 'Não, usar apenas os materiais listados'}
**Observações da turma**: {observacoes or 'Turma regular, sem observações específicas'}
</tarefa>

<metodologias_disponiveis>
{MODULO_METODOLOGIAS}
</metodologias_disponiveis>

<regras_obrigatorias>
1. SEMPRE incluir código(s) de habilidade BNCC corretos para a disciplina e ano
2. Objetivos devem ser mensuráveis (usar verbos de ação: identificar, analisar, aplicar, criar, comparar)
3. Tempo de cada momento deve somar EXATAMENTE {duracao} minutos
4. Linguagem clara e acessível para qualquer professor
5. Sugerir adaptações para inclusão quando houver observações sobre a turma
6. Recursos devem ser realistas para escolas brasileiras
7. Cada momento deve ter instruções detalhadas do que o professor deve FAZER e DIZER
8. ABORDAGEM POR FAIXA ETÁRIA:
   - 1º ao 3º ano (6-8 anos): Aulas MUITO lúdicas com brincadeiras, histórias, músicas
   - 4º e 5º ano (9-10 anos): Aulas lúdicas com jogos, desafios em grupo
   - 6º e 7º ano (11-12 anos): Aulas dinâmicas com gamificação, trabalhos em grupo
   - 8º e 9º ano (13-14 anos): Aulas com protagonismo do aluno, projetos, discussões críticas
   - Ensino Médio (15-17 anos): Aulas com autonomia, pesquisa, debates aprofundados
</regras_obrigatorias>

<formato_resposta>
Responda APENAS com este JSON (sem texto adicional, sem markdown):
{{
  "titulo": "Título criativo e descritivo do plano de aula",
  
  "introducao": "ESCREVA UM TEXTO RICO COM NO MÍNIMO 250 PALAVRAS contendo:\\n\\n🎯 Objetivo deste momento: [explicar]\\n\\n📌 Conteúdo a ser abordado: [listar]\\n\\n🗣️ Roteiro do professor:\\n1. [instrução exata do que fazer]\\n2. [o que DIZER aos alunos entre aspas]\\n3. [como conduzir]\\n\\n❓ Perguntas para fazer aos alunos:\\n- [pergunta específica 1]\\n- [pergunta específica 2]\\n\\n👁️ O que observar nos alunos: [descrever]",
  
  "desenvolvimento": "ESCREVA UM TEXTO RICO COM NO MÍNIMO 500 PALAVRAS contendo:\\n\\n🎯 Objetivo deste momento: [explicar]\\n\\n📌 Conteúdo a ser abordado com detalhes: [listar pontos]\\n\\n🗣️ Roteiro do professor - EXPLICAÇÃO:\\n1. [passo a passo de como explicar]\\n2. [o que DIZER entre aspas]\\n3. [exemplos para usar]\\n\\n📋 ATIVIDADE PRÁTICA:\\n- Nome da atividade: [nome criativo]\\n- Organização: [individual/duplas/grupos]\\n- Instruções detalhadas para os alunos:\\n  1. [passo 1]\\n  2. [passo 2]\\n  3. [passo 3]\\n- Tempo estimado: [X minutos]\\n- Material necessário: [listar]\\n\\n💡 Dica pedagógica: [dica específica]\\n\\n⚠️ Pontos de atenção: [dificuldades comuns e como intervir]",
  
  "fechamento": "ESCREVA UM TEXTO RICO COM NO MÍNIMO 200 PALAVRAS contendo:\\n\\n🎯 Objetivo deste momento: [explicar]\\n\\n🗣️ Roteiro do professor:\\n1. [como retomar os pontos principais]\\n2. [o que DIZER para consolidar]\\n\\n❓ Perguntas de verificação:\\n- [pergunta 1]\\n- [resposta esperada]\\n- [pergunta 2]\\n- [resposta esperada]\\n\\n✏️ Atividade RAIO-X (verificação individual):\\n- Tipo: [exercício/quiz/etc]\\n- Enunciado: [enunciado completo]\\n- Resposta esperada: [resposta]\\n\\n📚 Tarefa de casa (opcional): [descrever]\\n\\n🔗 Conexão com próxima aula: [explicar]",
  
  "cronograma": [
    {{"etapa": "Abertura/Aquecimento", "tempo": "X min", "descricao": "DETALHADO: O que o professor faz, o que diz, como organiza a sala"}},
    {{"etapa": "Desenvolvimento/Explicação", "tempo": "X min", "descricao": "DETALHADO: Passo a passo da explicação com exemplos"}},
    {{"etapa": "Atividade Prática", "tempo": "X min", "descricao": "DETALHADO: Nome da atividade, como organizar alunos, instruções"}},
    {{"etapa": "Sistematização/Discussão", "tempo": "X min", "descricao": "DETALHADO: Como retomar, perguntas para fazer, como consolidar"}},
    {{"etapa": "Fechamento/Avaliação", "tempo": "X min", "descricao": "DETALHADO: Atividade RAIO-X, verificação, encerramento"}}
  ],
  "competenciasBNCC": [
    "EF01MA14 - Identificar e nomear figuras planas (círculo, quadrado, retângulo e triângulo)",
    "EF01MA15 - Comparar comprimentos utilizando termos como mais alto, mais baixo"
  ],
  "materiaisNecessarios": ["Material 1 com quantidade", "Material 2", "Material 3"]{material_impresso_json}
}}
</formato_resposta>

<exemplo_referencia>
{MODULO_EXEMPLO}
</exemplo_referencia>

IMPORTANTE: 
- Use o exemplo acima como REFERÊNCIA de qualidade e detalhamento
- Seja ESPECÍFICO e PRÁTICO nas descrições
- Inclua o que o professor deve DIZER aos alunos
- Inclua perguntas para fazer aos alunos
- O cronograma DEVE somar exatamente {duracao} minutos
- COMPETÊNCIAS BNCC: Liste TODOS os códigos relevantes para a aula (não há limite)
- Cada código BNCC deve estar no formato: "CÓDIGO - Descrição completa da habilidade"
- Use códigos BNCC REAIS e CORRETOS para {disciplina} do {ano_escolar}
- Adapte as atividades para a faixa etária do {ano_escolar}
- Se houver dinâmicas específicas ({dinamicas_texto}), organize as atividades de acordo
- Se houver observações da turma, sugira adaptações inclusivas
{material_impresso_instrucao}
"""

        # Chamar Gemini com prompt rico
        gemini_model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt
        )
        
        response = gemini_model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=8000,
                response_mime_type="application/json" # Forçar JSON mode se suportado
            )
        )
        
        content = response.text
        tokens = response.usage_metadata.total_token_count if response.usage_metadata else 0
        
        # Tentar parsear JSON da resposta
        try:
            # Remover possíveis blocos de código markdown
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0]
            elif '```' in content:
                content = content.split('```')[1].split('```')[0]
            
            plan_data = json.loads(content.strip())
        except json.JSONDecodeError:
            # Se falhar, tentar extrair JSON com regex
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                plan_data = json.loads(json_match.group())
            else:
                return jsonify({
                    "success": False,
                    "error": "Não foi possível processar a resposta da IA",
                    "raw": content[:500]
                }), 500
        
        # Adicionar metadados
        plan_data['id'] = str(uuid.uuid4())
        plan_data['serie'] = ano_escolar
        plan_data['duracao'] = duracao
        plan_data['disciplinas'] = [disciplina]
        plan_data['status'] = 'gerado'
        plan_data['createdAt'] = __import__('datetime').datetime.now().isoformat()
        plan_data['gerarMaterialImpresso'] = gerar_material_impresso
        plan_data['metodologia'] = metodologia
        plan_data['detalhesGamificacao'] = detalhes_gamificacao
        print(f"DEBUG: Dados finais do plano: {plan_data.get('gerarMaterialImpresso')}")
        
        return jsonify({
            "success": True,
            "plan": plan_data,
            "tokens": tokens
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@app.route('/api/gerar-material', methods=['POST'])
def gerar_material_impresso():
    """
    Gera material impresso em HTML baseado no plano de aula.
    
    Body esperado:
    {
        "plano": { ... plano de aula completo ... }
    }
    
    Retorna:
    {
        "success": true,
        "html": "<html>...</html>",
        "titulo": "Nome do material"
    }
    """
    try:
        data = request.json
        plano = data.get('plano', {})
        
        if not plano:
            return jsonify({"error": "Plano de aula não fornecido"}), 400
        
        # Extrair informações do plano
        titulo = plano.get('titulo', 'Atividade')
        disciplina = plano.get('disciplinas', [''])[0] if plano.get('disciplinas') else ''
        serie = plano.get('serie', '')
        desenvolvimento = plano.get('desenvolvimento', '')
        fechamento = plano.get('fechamento', '')
        
        # Prompt para Apostila/Workbook
        system_prompt = """Você é um DESIGNER PEDAGÓGICO ESPECIALISTA em materiais didáticos impressos de alta qualidade.


Sua missão: criar WORKBOOKS profissionais prontos para impressão, com excelência visual e pedagógica.

# ESPECIFICAÇÕES TÉCNICAS

## 1. ESTRUTURA HTML
- Documento HTML5 completo e válido
- CSS incorporado no <head> (sem folhas externas)
- Sem dependências de bibliotecas externas
- Compatível com impressão direta (Ctrl+P)

## 2. DESIGN SYSTEM

### Paleta de Cores
- **Primária**: #2563eb (Azul educacional)
- **Secundária**: #0891b2 (Cyan vibrante)
- **Texto principal**: #1e293b (Slate 800)
- **Texto secundário**: #64748b (Slate 500)
- **Backgrounds**: #f8fafc (Neutro claro), #ffffff (Branco)
- **Bordas**: #cbd5e1 (Slate 300)
- **Destaque**: #fbbf24 (Âmbar para avisos)

### Tipografia
```css
body {
  font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif;
  font-size: 11pt;
  line-height: 1.6;
  color: #1e293b;
}

h1 { font-size: 18pt; font-weight: 700; color: #1e293b; margin-bottom: 8px; }
h2 { font-size: 14pt; font-weight: 600; color: #334155; margin: 16px 0 8px; }
h3 { font-size: 12pt; font-weight: 600; color: #475569; }
```

### Formato de Página
```css
.page {
  width: 210mm;
  min-height: 297mm;
  padding: 20mm;
  margin: 20px auto;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  position: relative;
}

@media print {
  body { margin: 0; background: white; }
  .page { 
    margin: 0; 
    box-shadow: none; 
    padding: 15mm;
    page-break-after: always;
  }
  .no-print { display: none; }
}
```

## 3. COMPONENTES OBRIGATÓRIOS

### A. CABEÇALHO INSTITUCIONAL
```html
<div style="border: 3px double #2563eb; padding: 16px; background: linear-gradient(to right, #f8fafc, #ffffff); border-radius: 8px; margin-bottom: 24px;">
  <div style="text-align: center; margin-bottom: 12px;">
    <div style="font-size: 10pt; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">Instituição de Ensino</div>
    <div style="border-bottom: 1px solid #1e293b; width: 70%; margin: 8px auto; padding-bottom: 4px;"></div>
  </div>
  <div style="display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 12px; font-size: 10pt;">
    <div>
      <span style="font-weight: 600;">Aluno(a):</span>
      <span style="border-bottom: 1px dotted #64748b; display: inline-block; width: calc(100% - 60px); margin-left: 4px;"></span>
    </div>
    <div>
      <span style="font-weight: 600;">Data:</span>
      <span style="border-bottom: 1px dotted #64748b; display: inline-block; width: 80px; margin-left: 4px;"></span>
    </div>
    <div>
      <span style="font-weight: 600;">Turma:</span>
      <span style="border-bottom: 1px dotted #64748b; display: inline-block; width: 60px; margin-left: 4px;"></span>
    </div>
  </div>
</div>
```

### B. NUMERAÇÃO DE QUESTÕES
```html
<div style="display: flex; align-items: start; margin: 16px 0;">
  <span style="
    background: linear-gradient(135deg, #2563eb, #0891b2);
    color: white;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 13pt;
    flex-shrink: 0;
    margin-right: 12px;
    box-shadow: 0 2px 4px rgba(37,99,235,0.3);
  ">1</span>
  <div style="flex: 1;">
    <p style="margin: 0; font-weight: 500;">Enunciado da questão...</p>
  </div>
</div>
```

### C. ÁREAS DE RESPOSTA

#### Linhas de Caderno
```html
<div style="
  background-image: repeating-linear-gradient(
    transparent,
    transparent 31px,
    #cbd5e1 31px,
    #cbd5e1 32px
  );
  min-height: 128px;
  padding: 8px 0;
  margin: 12px 0;
  border-left: 3px solid #f87171;
  padding-left: 12px;
"></div>
```

#### Caixa de Desenho/Resposta Curta
```html
<div style="
  border: 2px dashed #cbd5e1;
  border-radius: 8px;
  min-height: 100px;
  background: #fafafa;
  margin: 12px 0;
  padding: 12px;
"></div>
```

### D. BOXES DE DESTAQUE

#### Dica/Atenção
```html
<div style="
  background: linear-gradient(to right, #fef3c7, #fef9e6);
  border-left: 4px solid #fbbf24;
  padding: 12px 16px;
  border-radius: 4px;
  margin: 16px 0;
">
  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
    <span style="font-weight: 700; color: #92400e;">💡 Dica:</span>
  </div>
  <p style="margin: 0; color: #78350f; font-size: 10pt;">Conteúdo da dica...</p>
</div>
```

#### Desafio
```html
<div style="
  background: linear-gradient(135deg, #dbeafe, #e0f2fe);
  border: 2px solid #2563eb;
  border-radius: 8px;
  padding: 16px;
  margin: 20px 0;
">
  <h3 style="color: #1e40af; margin: 0 0 8px 0;">🎯 Desafio Extra</h3>
  <p style="margin: 0;">Conteúdo do desafio...</p>
</div>
```

### E. AUTOAVALIAÇÃO (Rodapé da Atividade)
```html
<div style="
  margin-top: 32px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
">
  <p style="font-weight: 600; margin: 0 0 8px 0; font-size: 10pt;">Como você se sentiu fazendo esta atividade?</p>
  <div style="display: flex; gap: 24px; justify-content: center;">
    <div style="text-align: center;">
      <div style="width: 40px; height: 40px; border: 2px solid #cbd5e1; border-radius: 50%; margin: 0 auto 4px;"></div>
      <span style="font-size: 9pt; color: #64748b;">Fácil</span>
    </div>
    <div style="text-align: center;">
      <div style="width: 40px; height: 40px; border: 2px solid #cbd5e1; border-radius: 50%; margin: 0 auto 4px;"></div>
      <span style="font-size: 9pt; color: #64748b;">Médio</span>
    </div>
    <div style="text-align: center;">
      <div style="width: 40px; height: 40px; border: 2px solid #cbd5e1; border-radius: 50%; margin: 0 auto 4px;"></div>
      <span style="font-size: 9pt; color: #64748b;">Difícil</span>
    </div>
  </div>
</div>
```

### F. RODAPÉ EM TODAS AS PÁGINAS
```html
<div style="
  position: absolute;
  bottom: 10mm;
  left: 20mm;
  right: 20mm;
  text-align: center;
  font-size: 8pt;
  color: #94a3b8;
  border-top: 1px solid #e2e8f0;
  padding-top: 8px;
">
  Material didático gerado por IA • Revisão pedagógica recomendada
</div>
```

### G. SEPARADOR PARA GABARITO
```html
<div style="page-break-before: always;"></div>
<div style="
  background: #1e293b;
  color: white;
  padding: 16px;
  text-align: center;
  font-weight: 700;
  font-size: 14pt;
  margin-bottom: 24px;
  border-radius: 8px;
">
  📋 GABARITO PARA O PROFESSOR
</div>
```

## 4. ESTRUTURA PEDAGÓGICA

O material deve conter exatamente estas seções, nesta ordem:

1. **Cabeçalho Institucional** (componente A)
2. **Título da Atividade** (h1 centralizado)
3. **Informações da Aula** (Disciplina, Série, Objetivo - em grid)
4. **Aquecimento** (1-2 questões leves, lúdicas) - 10% do conteúdo
5. **Atividade Principal** (4-6 questões de desenvolvimento) - 70% do conteúdo
6. **Desafio** (1 questão complexa ou interdisciplinar) - 15% do conteúdo
7. **Autoavaliação** (componente E)
8. **Nova página: Gabarito** (respostas detalhadas + orientações ao professor)

## 5. BOAS PRÁTICAS

### Pedagógicas
- Questões progressivas (do simples ao complexo)
- Diversificar tipos: múltipla escolha, dissertativa, V/F, completar, desenho
- Contextualizar com situações reais
- Incluir pelo menos 1 questão interdisciplinar
- Gabarito com comentários pedagógicos, não apenas respostas

### Visuais
- Máximo de 1 elemento visual decorativo por página
- Espaçamento generoso entre questões (16-20px)
- Contraste suficiente para impressão P&B
- Evitar blocos de texto maiores que 5 linhas
- Use negrito APENAS para destacar termos-chave

### Técnicas
- `-webkit-print-color-adjust: exact;` para preservar cores na impressão
- `orphans: 3; widows: 3;` para evitar linhas órfãs
- IDs únicos se precisar de âncoras
- Comentários HTML para facilitar edições: `<!-- Seção: Aquecimento -->`

## 6. VALIDAÇÃO FINAL

Antes de retornar, verifique:
- [ ] HTML válido (DOCTYPE, head, body fechados)
- [ ] Todos os estilos inline ou no <style>
- [ ] Rodapé presente em TODAS as páginas
- [ ] Gabarito em página separada
- [ ] Mínimo de 5 questões variadas
- [ ] Espaços adequados para respostas
- [ ] Compatibilidade com impressão

# OUTPUT

Retorne APENAS o código HTML completo.
NÃO inclua:
- Blocos de markdown (```)
- Explicações antes ou depois do código
- Comentários fora do HTML

O código deve começar com `<!DOCTYPE html>` e terminar com `</html>`."""

        user_prompt = f"""DADOS DO PLANO DE AULA:

📚 Título: {titulo}
🎓 Disciplina: {disciplina}
👥 Série/Ano: {serie}

DESENVOLVIMENTO:
{desenvolvimento}

FECHAMENTO:
{fechamento}

---

TAREFA: Criar um WORKBOOK completo em HTML seguindo rigorosamente as especificações do system_prompt.

REQUISITOS ESPECÍFICOS:
1. Analise o conteúdo do plano e identifique 5-7 objetivos de aprendizagem
2. Crie questões que avaliem esses objetivos de forma progressiva
3. Inclua pelo menos:
   - 2 questões de múltipla escolha
   - 2 questões dissertativas
   - 1 questão de aplicação prática
   - 1 desafio interdisciplinar
4. O gabarito deve incluir:
   - Respostas corretas
   - Explicação breve de cada resposta
   - Sugestões de critérios de avaliação
   - Habilidades BNCC trabalhadas (se aplicável)

IMPORTANTE:
- Adapte a linguagem à faixa etária da série
- Use espaçamentos adequados para a escrita manual
- Garanta que o material seja imprimível em impressoras comuns
- O visual deve ser profissional, limpo e convidativo

Retorne APENAS o HTML completo, começando com <!DOCTYPE html>"""


        # Chamar Gemini
        gemini_model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt
        )
        
        response = gemini_model.generate_content(
            user_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=10500
            )
        )
        
        html_content = response.text
        
        # Limpar possíveis blocos de código markdown
        if '```html' in html_content:
            html_content = html_content.split('```html')[1].split('```')[0]
        elif '```' in html_content:
            html_content = html_content.split('```')[1].split('```')[0]
        
        html_content = html_content.strip()
        
        return jsonify({
            "success": True,
            "html": html_content,
            "titulo": f"Material - {titulo}"
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500



# ============================================
# CONFIGURAÇÃO DOS TIPOS DE JOGOS
# ============================================

TIPOS_JOGOS_DETALHADOS = {
    "pontos_recompensas": {
        "nome": "Sistema de Pontos e Recompensas",
        "componentes": ["tabela_pontuacao", "cartoes_recompensa", "tracker_progresso"],
        "descricao": "Sistema de gamificação com pontos e badges"
    },
    "competicao_equipes": {
        "nome": "Competições em Equipes",
        "componentes": ["placar_equipes", "cartas_desafio", "regras_competicao"],
        "descricao": "Dinâmica competitiva entre grupos"
    },
    "jogos_educativos": {
        "nome": "Jogos Educativos Físicos ou Digitais",
        "componentes": ["tabuleiro", "cartas", "pecas", "regras"],
        "descricao": "Jogo de tabuleiro ou cartas educativo"
    },
    "escape_room": {
        "nome": "Escape Room Pedagógico",
        "componentes": ["enigmas", "pistas", "chaves", "mapa_progresso"],
        "descricao": "Sala de fuga com desafios educacionais"
    },
    "quiz_interativo": {
        "nome": "Quiz Interativo",
        "componentes": ["lista_perguntas", "gabarito", "placar"],
        "descricao": "Quiz dinâmico com perguntas e respostas"
    },
    "tres_pistas": {
        "nome": "Jogo das 3 Pistas",
        "componentes": ["cartas_pistas", "cartas_resposta", "tabela_pontos"],
        "descricao": "Adivinhar conceitos com 3 dicas progressivas"
    },
    "show_milhao": {
        "nome": "Show do Milhão Pedagógico",
        "componentes": ["cartas_perguntas", "niveis_dificuldade", "ajudas", "placar"],
        "descricao": "Perguntas progressivas inspiradas no programa"
    },
    "gartic_educativo": {
        "nome": "Gartic Educativo",
        "componentes": ["cartas_conceitos", "regras", "folhas_desenho"],
        "descricao": "Desenhar e adivinhar conceitos pedagógicos"
    },
    "batata_quente": {
        "nome": "Batata Quente com Perguntas",
        "componentes": ["cartas_perguntas", "regras", "cronometro_sugestao"],
        "descricao": "Dinâmica rápida de perguntas"
    },
    "bingo": {
        "nome": "Bingo de Conceitos",
        "componentes": ["cartelas_bingo", "lista_chamada", "marcadores"],
        "descricao": "Bingo educativo temático"
    },
    "caca_tesouro": {
        "nome": "Caça ao Tesouro Pedagógico",
        "componentes": ["pistas", "mapa", "desafios", "tesouro"],
        "descricao": "Busca por pistas com desafios educacionais"
    },
    "outro": {
        "nome": "Jogo Educativo Customizado",
        "componentes": ["componentes_personalizados"],
        "descricao": "Jogo criativo baseado nas observações"
    }
}


def gerar_material_impresso(plano: Dict) -> Tuple[dict, int]:
    """
    Gera material didático imprimível (exercícios, texto de apoio, etc).
    """
    try:
        titulo = plano.get('titulo', 'Atividade')
        serie = plano.get('serie', '')
        disciplina = plano.get('disciplina', '')
        conteudo = plano.get('desenvolvimento', '')
        objetivos = plano.get('objetivos', '')
        
        logger.info(f"Gerando material impresso: {titulo}")
        
        system_prompt = """Você é um ESPECIALISTA em design de materiais didáticos imprimíveis.
MISSÃO: Criar uma folha de atividades/exercícios completa baseada no plano de aula.
FORMATO: HTML puro, pronto para impressão (A4).

ESTRUTURA:
1. Cabeçalho (Escola, Nome, Data, Turma)
2. Título da Atividade
3. Texto de Apoio (Contextualização breve)
4. 4-5 Questões/Atividades diversificadas (Múltipla escolha, Dissertativa, Relacione, etc)
5. Espaço para respostas
6. Gabarito (em página separada ou no final, estilo 'Professor')

ESTILO:
- Fontes claras (Arial/Verdana)
- Preto e branco (economizar tinta)
- Espaçamento adequado para escrita
- Use CSS @media print para quebras de página

RETORNE APENAS O HTML. Sem markdown."""

        user_prompt = f"""Crie o material para esta aula:
Título: {titulo}
Série: {serie}
Disciplina: {disciplina}
Objetivos: {objetivos}
Conteúdo da Aula: {conteudo}

Gere agora."""

        config = {"temperature": 0.7, "max_output_tokens": 4000}
        model = genai.GenerativeModel(model_name=model_name, system_instruction=system_prompt, generation_config=config)
        
        response = model.generate_content(user_prompt)
        
        if not response or not response.text:
             return jsonify({"success": False, "error": "Sem resposta da IA"}), 500
             
        html = _limpar_html(response.text)
        
        return jsonify({
            "success": True, 
            "html": html,
            "titulo": f"Atividade - {titulo}"
        }), 200

    except Exception as e:
        logger.exception("Erro ao gerar material")
        return jsonify({"success": False, "error": str(e)}), 500


def gerar_jogo_educativo(plano: Dict) -> Tuple[dict, int]:
    """
    Função principal: gera jogo educativo imprimível.
    
    Args:
        plano: Dados do plano de aula
        
    Returns:
        (response_json, status_code)
    """
    try:
        # Adaptação de campos (Frontend envia 'disciplinas' array, Backend usa 'disciplina' string)
        if not plano.get('disciplina') and plano.get('disciplinas'):
             plano['disciplina'] = plano['disciplinas'][0]

        # Validação
        campos_obrigatorios = ['titulo', 'serie', 'disciplina', 'desenvolvimento']
        campos_faltantes = [c for c in campos_obrigatorios if not plano.get(c)]
        
        if campos_faltantes:
            logger.error(f"Campos faltando: {campos_faltantes}")
            return jsonify({
                "success": False,
                "error": f"Campos faltantes: {', '.join(campos_faltantes)}"
            }), 400
        
        # Extração
        titulo = plano.get('titulo', 'Jogo Educativo')
        serie = plano.get('serie', 'Não especificada')
        disciplina = plano.get('disciplina', 'Geral')
        desenvolvimento = plano.get('desenvolvimento', '')
        objetivos = plano.get('objetivos', '')
        detalhes_gamificacao = plano.get('detalhesGamificacao', '').strip()
        observacoes = plano.get('observacoes', '')
        
        # Identificar tipo
        tipo_key, tipo_info = _identificar_tipo_jogo(detalhes_gamificacao)
        
        logger.info(f"Gerando: {tipo_info['nome']} | {disciplina} | {serie}")
        
        # Construir prompts
        system_prompt = _construir_system_prompt(tipo_key, tipo_info)
        user_prompt = _construir_user_prompt(
            titulo, serie, disciplina, desenvolvimento,
            objetivos, tipo_key, tipo_info,
            detalhes_gamificacao, observacoes
        )
        
        # Configuração do modelo
        config = {
            "temperature": 0.9,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 4000,
        }
        
        safety = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        
        model = genai.GenerativeModel(
            model_name=model_name, # Usando variável global para consistência
            system_instruction=system_prompt,
            generation_config=config,
            safety_settings=safety
        )
        
        logger.info("Chamando Gemini...")
        response = model.generate_content(user_prompt)
        
        if not response or not response.text:
            logger.error("Resposta vazia")
            return jsonify({
                "success": False,
                "error": "IA não gerou resposta. Tente novamente."
            }), 500
        
        html_content = _limpar_html(response.text)
        _validar_html_basico(html_content)
        
        logger.info(f"Sucesso: {len(html_content)} caracteres")
        
        return jsonify({
            "success": True,
            "html": html_content,
            "titulo": f"{tipo_info['nome']} - {titulo}",
            "tipo_jogo": tipo_info['nome'],
            "tipo_jogo_key": tipo_key,
            "componentes": tipo_info['componentes']
        }), 200
        
    except Exception as e:
        logger.exception("Erro ao gerar jogo")
        import traceback
        return jsonify({
            "success": False,
            "error": "Erro interno",
            "detalhes": str(e),
            "traceback": traceback.format_exc() if logger.level == logging.DEBUG else None
        }), 500


def _identificar_tipo_jogo(detalhes: str) -> Tuple[str, Dict]:
    """Identifica tipo de jogo pelo texto do frontend."""
    if not detalhes:
        return ("jogos_educativos", TIPOS_JOGOS_DETALHADOS["jogos_educativos"])
    
    d = detalhes.lower().strip()
    
    mapeamento = {
        "sistema de pontos": "pontos_recompensas",
        "pontos e recompensas": "pontos_recompensas",
        "competições em equipes": "competicao_equipes",
        "competição": "competicao_equipes",
        "jogos educativos": "jogos_educativos",
        "escape room": "escape_room",
        "quiz interativo": "quiz_interativo",
        "kahoot": "quiz_interativo",
        "mentimeter": "quiz_interativo",
        "3 pistas": "tres_pistas",
        "três pistas": "tres_pistas",
        "show do milhão": "show_milhao",
        "gartic": "gartic_educativo",
        "desenho e adivinhação": "gartic_educativo",
        "batata quente": "batata_quente",
        "bingo": "bingo",
        "caça ao tesouro": "caca_tesouro",
        "outro": "outro",
    }
    
    for chave, tipo in mapeamento.items():
        if chave in d:
            return (tipo, TIPOS_JOGOS_DETALHADOS[tipo])
    
    logger.warning(f"Tipo não reconhecido: {detalhes}")
    return ("outro", TIPOS_JOGOS_DETALHADOS["outro"])


def _construir_system_prompt(tipo_key: str, tipo_info: Dict) -> str:
    """Constrói system prompt otimizado."""
    nome = tipo_info['nome']
    comps = ", ".join(tipo_info['componentes'])
    
    instrucoes_tipo = _get_instrucoes_especificas(tipo_key)
    
    return f"""Você é um GAME DESIGNER EDUCACIONAL especialista em jogos pedagógicos imprimíveis.

MISSÃO: Criar um **{nome}** completo para impressão em A4.

ESPECIFICAÇÕES TÉCNICAS:

1. HTML5 válido, CSS embutido, @media print configurado
2. Cores printer-friendly (evite fundos escuros)
3. Fontes: Arial/Helvetica, mín 10pt
4. Contraste: mín 4.5:1
5. Quebras de página: page-break-after
6. Componentes: {comps}

ESTRUTURA OBRIGATÓRIA:
- Página 1: Capa (título, info do jogo)
- Página 2: Regras completas
- Páginas 3+: Componentes imprimíveis

LAYOUT DE CARTAS:
- Pequenas (6×9cm): 6 por folha (2×3)
- Médias (7×10cm): 4 por folha (2×2)
- Grandes (9×13cm): 2 por folha (1×2)

{instrucoes_tipo}

RETORNE APENAS HTML PURO:
- Sem ```html, sem explicações
- Começar com <!DOCTYPE html>
- Terminar com </html>
- Zero placeholders ou "..."
- Mínimo 3 páginas completas"""


def _construir_user_prompt(
    titulo: str, serie: str, disciplina: str, 
    desenvolvimento: str, objetivos: str,
    tipo_key: str, tipo_info: Dict,
    detalhes_gamificacao: str, observacoes: str
) -> str:
    """Constrói user prompt com dados da aula."""
    
    obs_extra = ""
    if tipo_key == "outro" and observacoes:
        obs_extra = f"\n\n⚠️ JOGO CUSTOMIZADO:\n{observacoes}\n"
    
    requisitos = _get_requisitos_quantidade(tipo_key)
    
    return f"""DADOS DA AULA:

Título: {titulo}
Série: {serie}
Disciplina: {disciplina}

Objetivos:
{objetivos or 'Aprendizagem lúdica e engajadora'}

Conteúdo:
{desenvolvimento}
{obs_extra}

TIPO DE JOGO: {tipo_info['nome']}
Componentes: {', '.join(tipo_info['componentes'])}

REQUISITOS:
{requisitos}

- Fidelidade ao conteúdo da aula
- Apropriado para {serie}
- Zero placeholders
- Pronto para imprimir e jogar

Crie o jogo completo em HTML!"""


def _get_instrucoes_especificas(tipo_key: str) -> str:
    """Instruções específicas por tipo de jogo."""
    
    instrucoes = {
        "tres_pistas": """
JOGO DAS 3 PISTAS:
- 25-30 cartas (7×10cm)
- Cada carta: conceito + 3 pistas progressivas
- Pista 1 (difícil) = 3pts, Pista 2 (média) = 2pts, Pista 3 (fácil) = 1pt
- Frente: pistas | Verso: resposta
""",
        "bingo": """
BINGO:
- 12 cartelas únicas (5×5 ou 4×4)
- Lista de chamada com 40-50 itens do conteúdo
- Marcadores para recortar
- Variações: linha, coluna, diagonal, cartela cheia
""",
        "quiz_interativo": """
QUIZ:
- 40-50 perguntas categorizadas
- 4 níveis de dificuldade
- Gabarito completo
- Placar de pontuação
- Formato: pergunta + 4 alternativas
""",
        "show_milhao": """
SHOW DO MILHÃO:
- 15 perguntas progressivas
- 5 níveis (R$1.000 a R$1.000.000)
- 3 ajudas (Cartas, Pular, Universitários)
- Múltipla escolha com 4 alternativas
""",
        "escape_room": """
ESCAPE ROOM:
- 5-7 enigmas sequenciais
- Mapa de progresso
- Pistas opcionais
- Códigos/chaves para cada fase
- Tempo sugerido: 40 min
""",
        "batata_quente": """
BATATA QUENTE:
- 30-40 cartas de pergunta rápida
- Níveis variados
- Cronômetro sugerido (30 seg)
- Penalidades para erro
""",
        "gartic_educativo": """
GARTIC:
- 30-40 cartas de conceitos
- Dificuldade variada
- Folhas de desenho (templates)
- Regras de pontuação
- Tempo por rodada: 60 seg
""",
        "caca_tesouro": """
CAÇA AO TESOURO:
- Mapa ilustrado
- 8-10 pistas sequenciais
- Desafios em cada estação
- "Tesouro" = conhecimento final
""",
        "competicao_equipes": """
COMPETIÇÃO:
- Placar para 4-6 equipes
- 24-30 cartas de desafio
- 3 níveis (10pts, 20pts, 30pts)
- Bônus de equipe
""",
        "pontos_recompensas": """
PONTOS E RECOMPENSAS:
- Tabela de pontuação clara
- 12-16 cartões de recompensa
- Trackers individuais
- 3 níveis: Bronze, Prata, Ouro
""",
        "jogos_educativos": """
JOGO DE TABULEIRO:
- Tabuleiro com 30-50 casas
- 20 cartas de desafio
- 4 peões coloridos
- Dado (template)
- Tipos de casas: normal, desafio, especial
"""
    }
    
    return instrucoes.get(tipo_key, "")


def _get_requisitos_quantidade(tipo_key: str) -> str:
    """Requisitos de quantidade por tipo."""
    
    requisitos = {
        "tres_pistas": "- Mínimo 25 cartas de pistas",
        "bingo": "- 12 cartelas + 40 itens de chamada",
        "quiz_interativo": "- 40-50 perguntas categorizadas",
        "show_milhao": "- 15 perguntas em 5 níveis",
        "escape_room": "- 5-7 enigmas completos",
        "batata_quente": "- 30-40 perguntas rápidas",
        "gartic_educativo": "- 30-40 conceitos + templates",
        "caca_tesouro": "- 8-10 pistas + mapa",
        "competicao_equipes": "- 24-30 cartas de desafio",
        "pontos_recompensas": "- Tabela + 12-16 recompensas",
        "jogos_educativos": "- Tabuleiro + 20 cartas + peças"
    }
    
    return requisitos.get(tipo_key, "- Componentes completos")


def _limpar_html(html_bruto: str) -> str:
    """Remove markdown e formatação desnecessária."""
    html = html_bruto.strip()
    
    # Remover blocos markdown
    if '```html' in html:
        html = html.split('```html')[1].split('```')[0]
    elif '```' in html:
        html = html.split('```')[1].split('```')[0]
    
    html = html.strip()

    # Fallback para HTML truncado (auto-fechamento)
    if not html.endswith('</html>'):
        logger.warning("HTML truncado detectado. Tentando reparar...")
        if '</body>' not in html[-20:]: # Se não fechou o body
            html += "\n</body>"
        html += "\n</html>"
    
    if not html.lower().startswith('<!doctype'):
        logger.warning("HTML sem DOCTYPE")
    
    return html


def _validar_html_basico(html: str) -> bool:
    """Valida estrutura básica do HTML."""
    validacoes = [
        ('<!doctype' in html.lower(), "Falta DOCTYPE"),
        ('<html' in html.lower(), "Falta <html>"),
        ('<head>' in html.lower(), "Falta <head>"),
        ('<body>' in html.lower(), "Falta <body>"),
        ('</html>' in html.lower(), "Falta </html>"),
        ('<style>' in html.lower(), "Falta CSS"),
    ]
    
    todas_validas = True
    for valido, msg in validacoes:
        if not valido:
            logger.warning(f"Validação: {msg}")
            todas_validas = False
    
    return todas_validas


@app.route('/api/gerar-material', methods=['POST'])
def gerar_material():
    """Endpoint para gerar material impresso."""
    data = request.json
    plano = data.get('plano', {})
    return gerar_material_impresso(plano)


@app.route('/api/gerar-jogo', methods=['POST'])
def gerar_jogo():
    """Endpoint wrapper para o gerador de jogos modular."""
    data = request.json
    plano = data.get('plano', {})
    return gerar_jogo_educativo(plano)


if __name__ == '__main__':

    print("\n" + "="*60)
    print("🚀 PlanBel 2.0 - Servidor de API")
    print("="*60)
    port = int(os.getenv("PORT", 7860))
    print(f"📍 Interface: http://localhost:{port}")
    print(f"🔗 API: http://localhost:{port}/api/gerar-plano")
    print(f"🤖 Modelo: {model_name} (Gemini)")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)

