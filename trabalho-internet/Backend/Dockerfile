FROM python:3.11-slim

# Define a pasta de trabalho do backend
WORKDIR /app/Backend

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia os requirements e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do backend (o frontend será injetado pelo docker-compose)
COPY . .

EXPOSE 5000

# Usamos o servidor Flask padrão para evitar a queda de conexão do Gunicorn
CMD ["flask", "run", "--host=0.0.0.0"]