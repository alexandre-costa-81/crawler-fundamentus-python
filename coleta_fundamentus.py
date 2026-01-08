from servico_fundamentus import get_resultado
from servico_bd import criar_engine, insert_data
from datetime import datetime

modalidades = ['acao', 'fii']

for modalidade in modalidades:
    df = get_resultado(mode=modalidade)
    engine = criar_engine()
    inseridos = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            result = insert_data(conn, row, mode=modalidade)
            inseridos += result.rowcount

    print(
        f"✅ Coleta finalizada | "
        f"Papeis processados: {df['papel'].nunique()} | "
        f"Novos registros (mudança detectada): {inseridos} | "
        f"Horário: {datetime.now()}"
    )
