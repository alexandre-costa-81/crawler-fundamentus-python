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
    papel, cotacao, pl, pvp, psr, dy, pa, pcg, pebit, pacl,
    evebit, evebitda, mrgebit, mrgliq, roic, roe, liqc, liq2m,
    patrliq, divbpatr, c5y, data_coleta
)
SELECT
    :papel, :cotacao, :pl, :pvp, :psr, :dy, :pa, :pcg, :pebit, :pacl,
    :evebit, :evebitda, :mrgebit, :mrgliq, :roic, :roe, :liqc, :liq2m,
    :patrliq, :divbpatr, :c5y, :data_coleta
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
        last.dy         IS NOT DISTINCT FROM :dy AND
        last.pa         IS NOT DISTINCT FROM :pa AND
        last.pcg        IS NOT DISTINCT FROM :pcg AND
        last.pebit      IS NOT DISTINCT FROM :pebit AND
        last.pacl       IS NOT DISTINCT FROM :pacl AND
        last.evebit     IS NOT DISTINCT FROM :evebit AND
        last.evebitda   IS NOT DISTINCT FROM :evebitda AND
        last.mrgebit    IS NOT DISTINCT FROM :mrgebit AND
        last.mrgliq     IS NOT DISTINCT FROM :mrgliq AND
        last.roic       IS NOT DISTINCT FROM :roic AND
        last.roe        IS NOT DISTINCT FROM :roe AND
        last.liqc       IS NOT DISTINCT FROM :liqc AND
        last.liq2m      IS NOT DISTINCT FROM :liq2m AND
        last.patrliq    IS NOT DISTINCT FROM :patrliq AND
        last.divbpatr   IS NOT DISTINCT FROM :divbpatr AND
        last.c5y        IS NOT DISTINCT FROM :c5y
);
""")

def insert_data(conn, df):
    """
    Insere dados no banco de dados
    Input:
        df: DataFrame com os dados a serem inseridos
    Output:
        número de registros inseridos
    """
    return conn.execute(sql_insert_acao(), df.to_dict())
