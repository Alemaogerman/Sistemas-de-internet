FROM postgres:18

RUN mkdir /dados

COPY init.sql /docker-entrypoint-initdb.d/01_init.sql

COPY APOSENTADOS_072026_limpo_com_cabecalho.csv /dados/APOSENTADOS_072026_limpo.csv
COPY CARREIRA_072026_limpo.csv /dados/CARREIRA_072026_limpo.csv