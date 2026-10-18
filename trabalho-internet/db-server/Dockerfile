FROM postgres:16

# Instala o Python e as bibliotecas que o seu script usa (requests e bs4)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-requests \
    python3-bs4 \
    && rm -rf /var/lib/apt/lists/*

# Cria a pasta interna onde o seu script vai salvar os CSVs
RUN mkdir -p /db/dados
WORKDIR /db/dados

# Copia o seu script Python para dentro do Docker
COPY preparar_dados.py .

# A MÁGICA: Roda o seu script durante a construção!
# Ele vai baixar e limpar os arquivos direto na internet, sem tocar no seu Windows
RUN python3 preparar_dados.py

# Copia o script de criação das tabelas para o PostgreSQL executar na inicialização
COPY init.sql /docker-entrypoint-initdb.d/