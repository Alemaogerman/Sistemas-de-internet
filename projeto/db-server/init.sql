CREATE TABLE aposentados (
    nome TEXT,
    cpf TEXT,
    matricula_servidor TEXT,
    nome_orgao TEXT,
    sigla_orgao TEXT,
    codigo_orgao_superior TEXT,
    cargo TEXT,
    classe TEXT,
    padrao TEXT,
    referencia TEXT,
    nivel TEXT,
    tipo_aposentadoria TEXT,
    fundamentacao_inatividade TEXT,
    nome_diploma_legal TEXT,
    data_publicacao_diploma_legal DATE,
    ocorrencia_ingresso_servico_publico TEXT,
    data_ingresso_servico_publico DATE,
    valor_rendimento_liquido NUMERIC(15,2)
);


CREATE TABLE carreira (
    nome TEXT,
    cpf TEXT,
    codigo_carreira TEXT,
    descricao_cargo_emprego TEXT,
    uf_upag_vinculacao TEXT,
    denominacao_orgao_atuacao TEXT,
    mes_referencia TEXT,
    valor_remuneracao NUMERIC(15,2)
);


CREATE EXTENSION IF NOT EXISTS pg_trgm;

COPY aposentados
FROM '/dados/APOSENTADOS_072026_limpo.csv'
WITH (
    FORMAT csv,
    DELIMITER ';',
    ENCODING 'WIN1252'
);

COPY carreira
FROM '/dados/CARREIRA_072026_limpo.csv'
WITH (
    FORMAT csv,
    DELIMITER ';',
    ENCODING 'WIN1252'
);


CREATE INDEX idx_aposentados_nome
ON aposentados USING gin (nome gin_trgm_ops);

CREATE INDEX idx_aposentados_cargo
ON aposentados USING gin (cargo gin_trgm_ops);

CREATE INDEX idx_aposentados_orgao
ON aposentados USING gin (nome_orgao gin_trgm_ops);


CREATE INDEX idx_carreira_nome
ON carreira USING gin (nome gin_trgm_ops);

CREATE INDEX idx_carreira_cargo
ON carreira USING gin (descricao_cargo_emprego gin_trgm_ops);

CREATE INDEX idx_carreira_uf
ON carreira USING gin (uf_upag_vinculacao gin_trgm_ops);

CREATE INDEX idx_carreira_orgao
ON carreira USING gin (denominacao_orgao_atuacao gin_trgm_ops);
