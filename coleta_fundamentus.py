from servico_fundamentus import get_resultado
from servico_bd import criar_engine, insert_data, get_or_create_ticker_id
from datetime import datetime

modalidades = ['acao', 'fii']
# modalidades = ['acao']

for modalidade in modalidades:
    df = get_resultado(mode=modalidade)
    engine = criar_engine()
    inseridos = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            if modalidade == 'fii':
                row['ticker_id'] = get_or_create_ticker_id(conn, row['ticker'], segment=row['segment'])
            else:
                row['ticker_id'] = get_or_create_ticker_id(conn, row['ticker'])
            result = insert_data(conn, row, mode=modalidade)
            inseridos += result.rowcount

    print(
        f"✅ Coleta finalizada | "
        f"Papeis processados: {df['ticker'].nunique()} | "
        f"Novos registros (mudança detectada): {inseridos} | "
        f"Horário: {datetime.now()}"
    )
