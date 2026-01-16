
# Usar imagem oficial do Python
FROM python:3.10-slim

# Definir diretório de trabalho
WORKDIR /app

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY . .

# Criar usuário não-root (boa prática/necessário no HF)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Expor a porta 7860 (Padrão Hugging Face)
EXPOSE 7860

# Comando de execução (Timeout alto para Gemini)
CMD ["gunicorn", "servidor:app", "--bind", "0.0.0.0:7860", "--timeout", "120", "--keep-alive", "5", "--log-level", "info"]
