FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia requirements PRIMEIRO (cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia código
COPY ./app ./app

# Expoe porta
EXPOSE 8000

# Comando Railway/Render
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $${PORT:-8000}"]
