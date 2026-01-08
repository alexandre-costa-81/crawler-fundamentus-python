from servico_fundamentus import get_resultado
from servico_bd import criar_engine, insert_data

acoes = get_resultado(mode='acao')
engine = criar_engine()
inseridos = 0

with engine.begin() as conn:
    for _, acao in acoes.iterrows():
        result = insert_data(conn, acao)
        inseridos += result.rowcount


# # ==========================================================
# # Conexão com o banco (via variáveis de ambiente)
# # ==========================================================
# DB_HOST = os.getenv("DB_HOST")
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")

# engine = create_engine(
#     f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
# )

# # ==========================================================
# # Coleta dos dados
# # ==========================================================
# df = fd.get_resultado()

# # 🔑 ESSENCIAL: o ticker vem como índice
# df = df.reset_index()

# # ==========================================================
# # Normalização e limpeza
# # ==========================================================
# df['data_coleta'] = datetime.now()

# campos = [
#     'papel', 'cotacao', 'pl', 'pvp', 'psr', 'dy', 'pa', 'pcg',
#     'pebit', 'pacl', 'evebit', 'evebitda', 'mrgebit', 'mrgliq',
#     'roic', 'roe', 'liqc', 'liq2m', 'patrliq', 'divbpatr', 'c5y',
#     'data_coleta'
# ]

# df = df.reindex(columns=campos)

# # Remove registros inválidos
# df = df[df['papel'].notna() & (df['papel'] != '')]

# # ==========================================================
# # SQL: insere SOMENTE se algum campo mudou
# # ==========================================================
# SQL_INSERT_IF_CHANGED = text("""
# INSERT INTO indicadores_fundamentalistas (
#     papel, cotacao, pl, pvp, psr, dy, pa, pcg, pebit, pacl,
#     evebit, evebitda, mrgebit, mrgliq, roic, roe, liqc, liq2m,
#     patrliq, divbpatr, c5y, data_coleta
# )
# SELECT
#     :papel, :cotacao, :pl, :pvp, :psr, :dy, :pa, :pcg, :pebit, :pacl,
#     :evebit, :evebitda, :mrgebit, :mrgliq, :roic, :roe, :liqc, :liq2m,
#     :patrliq, :divbpatr, :c5y, :data_coleta
# WHERE NOT EXISTS (
#     SELECT 1
#     FROM (
#         SELECT *
#         FROM indicadores_fundamentalistas
#         WHERE papel = :papel
#         ORDER BY data_coleta DESC
#         LIMIT 1
#     ) last
#     WHERE
#         last.cotacao    IS NOT DISTINCT FROM :cotacao AND
#         last.pl         IS NOT DISTINCT FROM :pl AND
#         last.pvp        IS NOT DISTINCT FROM :pvp AND
#         last.psr        IS NOT DISTINCT FROM :psr AND
#         last.dy         IS NOT DISTINCT FROM :dy AND
#         last.pa         IS NOT DISTINCT FROM :pa AND
#         last.pcg        IS NOT DISTINCT FROM :pcg AND
#         last.pebit      IS NOT DISTINCT FROM :pebit AND
#         last.pacl       IS NOT DISTINCT FROM :pacl AND
#         last.evebit     IS NOT DISTINCT FROM :evebit AND
#         last.evebitda   IS NOT DISTINCT FROM :evebitda AND
#         last.mrgebit    IS NOT DISTINCT FROM :mrgebit AND
#         last.mrgliq     IS NOT DISTINCT FROM :mrgliq AND
#         last.roic       IS NOT DISTINCT FROM :roic AND
#         last.roe        IS NOT DISTINCT FROM :roe AND
#         last.liqc       IS NOT DISTINCT FROM :liqc AND
#         last.liq2m      IS NOT DISTINCT FROM :liq2m AND
#         last.patrliq    IS NOT DISTINCT FROM :patrliq AND
#         last.divbpatr   IS NOT DISTINCT FROM :divbpatr AND
#         last.c5y        IS NOT DISTINCT FROM :c5y
# );
# """)

# # ==========================================================
# # Execução
# # ==========================================================
# inseridos = 0

# with engine.begin() as conn:
#     for _, row in df.iterrows():
#         result = conn.execute(SQL_INSERT_IF_CHANGED, row.to_dict())
#         if result.rowcount == 1:
#             inseridos += 1

# print(
#     f"✅ Coleta finalizada | "
#     f"Papeis processados: {df['papel'].nunique()} | "
#     f"Novos registros (mudança detectada): {inseridos} | "
#     f"Horário: {datetime.now()}"
# )
