import os
from sqlalchemy import create_engine, text

def criar_engine():
    """
    Cria e retorna uma engine de conexão com o banco de dados
    Output:
        engine SQLAlchemy
    """
    # ==========================================================
    # Conexão com o banco (via variáveis de ambiente)
    # ==========================================================
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")

    if (not DB_HOST):
        raise ValueError("Database host variables are not fully set.")

    if (not DB_NAME):
        raise ValueError("Database name variables are not fully set.")

    if (not DB_USER):
        raise ValueError("Database user variables are not fully set.")

    if (not DB_PASS):
        raise ValueError("Database password variables are not fully set.")

    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )

    return engine

def sql_insert_acao():
    return text("""
INSERT INTO indicadores_fundamentalistas_acoes (
    papel, cotacao, pl, pvp, psr, dividend_yield, p_ativo, p_cap_giro, p_ebit, p_ativ_circ_liqs,
    ev_ebit, ev_ebitda, mrg_ebit, mrg_liq, roic, roe, liq_corr, liq_2_meses,
    patrim_liq, div_brut_patrim, cresc_rec_5_a, data_coleta
)
SELECT
    :papel, :cotacao, :pl, :pvp, :psr, :dividend_yield, :p_ativo, :p_cap_giro, :p_ebit, :p_ativ_circ_liqs,
    :ev_ebit, :ev_ebitda, :mrg_ebit, :mrg_liq, :roic, :roe, :liq_corr, :liq_2_meses,
    :patrim_liq, :div_brut_patrim, :cresc_rec_5_a, :data_coleta
WHERE NOT EXISTS (
    SELECT 1
    FROM (
        SELECT *
        FROM indicadores_fundamentalistas_acoes
        WHERE papel = :papel
        ORDER BY data_coleta DESC
        LIMIT 1
    ) last
    WHERE
        last.cotacao    IS NOT DISTINCT FROM :cotacao AND
        last.pl         IS NOT DISTINCT FROM :pl AND
        last.pvp        IS NOT DISTINCT FROM :pvp AND
        last.psr        IS NOT DISTINCT FROM :psr AND
        last.dividend_yield         IS NOT DISTINCT FROM :dividend_yield AND
        last.p_ativo         IS NOT DISTINCT FROM :p_ativo AND
        last.p_cap_giro        IS NOT DISTINCT FROM :p_cap_giro AND
        last.p_ebit      IS NOT DISTINCT FROM :p_ebit AND
        last.p_ativ_circ_liqs       IS NOT DISTINCT FROM :p_ativ_circ_liqs AND
        last.ev_ebit     IS NOT DISTINCT FROM :ev_ebit AND
        last.ev_ebitda   IS NOT DISTINCT FROM :ev_ebitda AND
        last.mrg_ebit    IS NOT DISTINCT FROM :mrg_ebit AND
        last.mrg_liq     IS NOT DISTINCT FROM :mrg_liq AND
        last.roic       IS NOT DISTINCT FROM :roic AND
        last.roe        IS NOT DISTINCT FROM :roe AND
        last.liq_corr       IS NOT DISTINCT FROM :liq_corr AND
        last.liq_2_meses      IS NOT DISTINCT FROM :liq_2_meses AND
        last.patrim_liq    IS NOT DISTINCT FROM :patrim_liq AND
        last.div_brut_patrim   IS NOT DISTINCT FROM :div_brut_patrim AND
        last.cresc_rec_5_a        IS NOT DISTINCT FROM :cresc_rec_5_a
);
""")

def sql_insert_fii():
    return text("""
INSERT INTO indicadores_fundamentalistas_fii (
    papel, cotacao, segmento, ffo_yield, dividend_yield, pvp, valor_mercado,
    liquidez, qtd_imoveis, preco_m2, aluguel_m2, cap_rate, vacancia_media,
    data_coleta
)
SELECT
    :papel, :cotacao, :segmento, :ffo_yield, :dividend_yield, :pvp, :valor_mercado,
    :liquidez, :qtd_imoveis, :preco_m2, :aluguel_m2, :cap_rate, :vacancia_media,
    :data_coleta
WHERE NOT EXISTS (
    SELECT 1
    FROM (
        SELECT *
        FROM indicadores_fundamentalistas_fii
        WHERE papel = :papel
        ORDER BY data_coleta DESC
        LIMIT 1
    ) last
    WHERE
        last.cotacao    IS NOT DISTINCT FROM :cotacao AND
        last.segmento   IS NOT DISTINCT FROM :segmento AND
        last.cotacao    IS NOT DISTINCT FROM :cotacao AND
        last.ffo_yield  IS NOT DISTINCT FROM :ffo_yield AND
        last.dividend_yield IS NOT DISTINCT FROM :dividend_yield AND
        last.pvp        IS NOT DISTINCT FROM :pvp AND
        last.valor_mercado IS NOT DISTINCT FROM :valor_mercado AND
        last.liquidez   IS NOT DISTINCT FROM :liquidez AND
        last.qtd_imoveis IS NOT DISTINCT FROM :qtd_imoveis AND
        last.preco_m2   IS NOT DISTINCT FROM :preco_m2 AND
        last.aluguel_m2 IS NOT DISTINCT FROM :aluguel_m2 AND
        last.cap_rate   IS NOT DISTINCT FROM :cap_rate AND
        last.vacancia_media IS NOT DISTINCT FROM :vacancia_media
);
""")

def insert_data(conn, df, mode):
    """
    Insere dados no banco de dados
    Input:
        df: DataFrame com os dados a serem inseridos
    Output:
        número de registros inseridos
    """
    if mode == 'fii':
        return conn.execute(sql_insert_fii(), df.to_dict())
    else:  # mode == 'acao'
        return conn.execute(sql_insert_acao(), df.to_dict())