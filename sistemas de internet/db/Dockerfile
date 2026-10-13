FROM postgres:17

# Cria a pasta interna onde o Postgres vai ler os CSVs mapeados pelo Compose
RUN mkdir -p /db/dados && chown -R postgres:postgres /db/dados

# Copia apenas o arquivo SQL de inicialização leve
COPY init.sql /docker-entrypoint-initdb.d/01_init.sql