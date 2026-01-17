import os
from dotenv import load_dotenv
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
    load_dotenv()
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
INSERT INTO stock_fundamental_indicators (
    ticker_id, price, pe_ratio, pb_ratio, ps_ratio, dividend_yield, price_to_assets, price_to_working_capital, price_to_ebit, price_to_current_assets,
    ev_to_ebit, ev_to_ebitda, ebit_margin, net_margin, roic, roe, current_ratio, avg_liquidity_2_months,
    net_equity, gross_debt_to_equity, revenue_growth_5y, created_at, updated_at
)
SELECT
    :ticker_id, :price, :pe_ratio, :pb_ratio, :ps_ratio, :dividend_yield, :price_to_assets, :price_to_working_capital, :price_to_ebit, :price_to_current_assets,
    :ev_to_ebit, :ev_to_ebitda, :ebit_margin, :net_margin, :roic, :roe, :current_ratio, :avg_liquidity_2_months,
    :net_equity, :gross_debt_to_equity, :revenue_growth_5y, :created_at, :updated_at
WHERE NOT EXISTS (
    SELECT 1
    FROM (
        SELECT *
        FROM stock_fundamental_indicators
        WHERE ticker_id = :ticker_id
        ORDER BY created_at DESC
        LIMIT 1
    ) last
    WHERE
        last.price                      IS NOT DISTINCT FROM :price AND
        last.pe_ratio                   IS NOT DISTINCT FROM :pe_ratio AND
        last.pb_ratio                   IS NOT DISTINCT FROM :pb_ratio AND
        last.ps_ratio                   IS NOT DISTINCT FROM :ps_ratio AND
        last.dividend_yield             IS NOT DISTINCT FROM :dividend_yield AND
        last.price_to_assets            IS NOT DISTINCT FROM :price_to_assets AND
        last.price_to_working_capital   IS NOT DISTINCT FROM :price_to_working_capital AND
        last.price_to_ebit              IS NOT DISTINCT FROM :price_to_ebit AND
        last.price_to_current_assets    IS NOT DISTINCT FROM :price_to_current_assets AND
        last.ev_to_ebit                 IS NOT DISTINCT FROM :ev_to_ebit AND
        last.ev_to_ebitda               IS NOT DISTINCT FROM :ev_to_ebitda AND
        last.ebit_margin                IS NOT DISTINCT FROM :ebit_margin AND
        last.net_margin                 IS NOT DISTINCT FROM :net_margin AND
        last.roic                       IS NOT DISTINCT FROM :roic AND
        last.roe                        IS NOT DISTINCT FROM :roe AND
        last.current_ratio              IS NOT DISTINCT FROM :current_ratio AND
        last.avg_liquidity_2_months     IS NOT DISTINCT FROM :avg_liquidity_2_months AND
        last.net_equity                 IS NOT DISTINCT FROM :net_equity AND
        last.gross_debt_to_equity       IS NOT DISTINCT FROM :gross_debt_to_equity AND
        last.revenue_growth_5y          IS NOT DISTINCT FROM :revenue_growth_5y
);
""")

def sql_insert_fii():
    return text("""
INSERT INTO reit_fundamental_indicators (
    ticker_id, price, ffo_yield, dividend_yield, pb_ratio, market_value,
    liquidity, property_count, price_per_sqm, rent_per_sqm, cap_rate, avg_vacancy_rate,
    created_at, updated_at
)
SELECT
    :ticker_id, :price, :ffo_yield, :dividend_yield, :pb_ratio, :market_value,
    :liquidity, :property_count, :price_per_sqm, :rent_per_sqm, :cap_rate, :avg_vacancy_rate,
    :created_at, :updated_at
WHERE NOT EXISTS (
    SELECT 1
    FROM (
        SELECT *
        FROM reit_fundamental_indicators
        WHERE ticker_id = :ticker_id
        ORDER BY created_at DESC
        LIMIT 1
    ) last
    WHERE
        last.price    IS NOT DISTINCT FROM :price AND
        last.ffo_yield  IS NOT DISTINCT FROM :ffo_yield AND
        last.dividend_yield IS NOT DISTINCT FROM :dividend_yield AND
        last.pb_ratio        IS NOT DISTINCT FROM :pb_ratio AND
        last.market_value IS NOT DISTINCT FROM :market_value AND
        last.liquidity   IS NOT DISTINCT FROM :liquidity AND
        last.property_count IS NOT DISTINCT FROM :property_count AND
        last.price_per_sqm   IS NOT DISTINCT FROM :price_per_sqm AND
        last.rent_per_sqm IS NOT DISTINCT FROM :rent_per_sqm AND
        last.cap_rate   IS NOT DISTINCT FROM :cap_rate AND
        last.avg_vacancy_rate IS NOT DISTINCT FROM :avg_vacancy_rate
);
""")

def get_or_create_ticker_id(conn, ticker, segment=None):
    """
    Busca o ticker na tabela tickers; se não existir, insere e retorna o id.
    """
    ticker_query = text("SELECT id FROM tickers WHERE symbol = :ticker LIMIT 1")
    existing = conn.execute(ticker_query, {"ticker": ticker}).scalar()
    if existing:
        return existing

    if segment:
        insert_ticker_query = text("INSERT INTO tickers (symbol, segment, created_at, updated_at) VALUES (:ticker, :segment, NOW(), NOW()) RETURNING id")
    else:
        insert_ticker_query = text("INSERT INTO tickers (symbol, created_at, updated_at) VALUES (:ticker, NOW(), NOW()) RETURNING id")

    return conn.execute(insert_ticker_query, {"ticker": ticker, "segment": segment}).scalar()

def insert_data(conn, df, mode):
    """
    Insere dados no banco de dados
    Input:
        df: Series (uma linha) com os dados a serem inseridos
    Output:
        número de registros inseridos
    """
    data = df.to_dict()
    
    if mode == 'fii':
        return conn.execute(sql_insert_fii(), data)
    else:  # mode == 'acao'
        return conn.execute(sql_insert_acao(), data)