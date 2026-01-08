CREATE TABLE IF NOT EXISTS indicadores_fundamentalistas_acoes (
    id SERIAL PRIMARY KEY,
    papel TEXT,
    cotacao NUMERIC,
    pl NUMERIC,
    pvp NUMERIC,
    psr NUMERIC,
    dy NUMERIC,
    pa NUMERIC,
    pcg NUMERIC,
    pebit NUMERIC,
    pacl NUMERIC,
    evebit NUMERIC,
    evebitda NUMERIC,
    mrgebit NUMERIC,
    mrgliq NUMERIC,
    roic NUMERIC,
    roe NUMERIC,
    liqc NUMERIC,
    liq2m NUMERIC,
    patrliq NUMERIC,
    divbpatr NUMERIC,
    c5y NUMERIC,
    data_coleta TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_fund_papel_data
ON indicadores_fundamentalistas_acoes (papel, data_coleta);