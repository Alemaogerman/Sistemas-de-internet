
FROM postgres:16

RUN mkdir -p /dados

COPY db-server/init.sql /docker-entrypoint-initdb.d/01_init.sql

COPY APOSENTADOS_072026_limpo_com_cabecalho.csv /dados/APOSENTADOS_072026_limpo.csv
COPY CARREIRA_072026_limpo.csv /dados/CARREIRA_072026_limpo.csv
