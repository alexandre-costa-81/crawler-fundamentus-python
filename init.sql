CREATE TABLE IF NOT EXISTS indicadores_fundamentalistas_acoes (
    id SERIAL PRIMARY KEY,
    papel TEXT,
    cotacao NUMERIC,
    pl NUMERIC,
    pvp NUMERIC,
    psr NUMERIC,
    dividend_yield NUMERIC,
    p_ativo NUMERIC,
    p_cap_giro NUMERIC,
    p_ebit NUMERIC,
    p_ativ_circ_liqs NUMERIC,
    ev_ebit NUMERIC,
    ev_ebitda NUMERIC,
    mrg_ebit NUMERIC,
    mrg_liq NUMERIC,
    roic NUMERIC,
    roe NUMERIC,
    liq_corr NUMERIC,
    liq_2_meses NUMERIC,
    patrim_liq NUMERIC,
    div_brut_patrim NUMERIC,
    cresc_rec_5_a NUMERIC,
    data_coleta TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_fund_papel_data
ON indicadores_fundamentalistas_acoes (papel, data_coleta);

CREATE TABLE IF NOT EXISTS indicadores_fundamentalistas_fii (
    id SERIAL PRIMARY KEY,
    papel TEXT,
    segmento TEXT,
    cotacao NUMERIC,
    ffo_yield NUMERIC,
    dividend_yield NUMERIC,
    pvp NUMERIC,
    valor_mercado NUMERIC,
    liquidez NUMERIC,
    qtd_imoveis INTEGER,
    preco_m2 NUMERIC,
    aluguel_m2 NUMERIC,
    cap_rate NUMERIC,
    vacancia_media NUMERIC,
    data_coleta TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_fund_papel_data
ON indicadores_fundamentalistas_fii (papel, data_coleta);
