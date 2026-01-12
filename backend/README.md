# PlanBel 2.0 - SAAS para Professores

> Gerador de Planos de Aula com IA alinhado à BNCC

## 🚀 Setup

### 1. Criar ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente
```bash
copy .env.example .env
# Editar .env com sua GROQ_API_KEY
```

### 4. Executar validação de prompts
```bash
python src/crew_validation.py
```

## 📁 Estrutura

```
backend/
├── src/
│   ├── agents/       # Agentes CrewAI
│   ├── prompts/      # Templates de prompts
│   ├── bncc/         # Dados da BNCC
│   └── utils/        # Utilitários
├── tests/            # Testes de validação
├── outputs/          # Planos gerados
└── BNCC.pdf          # Documento original
```

## 🔑 API Keys

Obtenha sua key gratuita em: https://console.groq.com/keys
