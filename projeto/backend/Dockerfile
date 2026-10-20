
FROM python:3.11-slim

WORKDIR /app/Backend

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do backend
COPY . .

EXPOSE 5000

# Inicia o Gunicorn usando a configuração existente
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]
