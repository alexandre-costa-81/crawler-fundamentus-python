import requests
import pandas   as pd
import io
import time

"""

Example usage

acoes = get_resultado(mode='acao')

OR

fiis = get_resultado(mode='fii')

"""

def get_resultado(mode='acao'):
    if mode == 'acao':
        url = get_acao_url()
        columns = get_acoes_columns()
    elif mode == 'fii':
        url = get_fii_url()
        columns = get_fii_columns()
    else:
        raise ValueError("Invalid mode. Use 'acao' or 'fii'.")

    header = get_header()

    content = requests.get(url, headers=header)

    df = pd.read_html(io.StringIO(content.text), decimal=",", thousands='.')[0]
    
    if columns:
        df = df.rename(columns=columns)

    time.sleep(1)

    return df

def get_header():
    return {
        'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
        'Accept': 'text/html, text/plain, text/css, text/sgml, */*;q=0.01',
        'Accept-Encoding': 'gzip, deflate',
    }

def get_acao_url():
    return 'https://www.fundamentus.com.br/resultado.php'

def get_acoes_columns():
    return {
        'Papel': 'papel',
        'Cotação': 'cotacao',
        'P/L': 'pl',
        'P/VP': 'pvp',
        'PSR': 'psr',
        'Div.Yield': 'dy',
        'P/Ativo': 'pa',
        'P/Cap.Giro': 'pcg',
        'P/EBIT': 'pebit',
        'P/Ativ Circ.Liq': 'pacl',
        'EV/EBIT': 'evebit',
        'EV/EBITDA': 'evebitda',
        'Mrg Ebit': 'mrgebit',
        'Mrg. Líq.': 'mrgliq',
        'ROIC': 'roic',
        'ROE': 'roe',
        'Liq. Corr.': 'liqc',
        'Liq.2meses': 'liq2m',
        'Patrim. Líq': 'patrliq',
        'Dív.Brut/ Patrim.': 'divbpatr',
        'Cresc. Rec.5a': 'c5y'
    }

def get_fii_url():
    return 'https://www.fundamentus.com.br/fii_resultado.php'

def get_fii_columns():
    return {
        'Papel': 'papel',
        'Segmento': 'segmento',
        'Cotação': 'cotacao',
        'FFO Yield': 'ffo_yield',
        'Dividend Yield': 'dividend_yield',
        'P/VP': 'pvp',
        'Valor de Mercado': 'valor_mercado',
        'Liquidez': 'liquidez',
        'Qtd de imóveis': 'qtd_imoveis',
        'Preço do m2': 'preco_m2',
        'Aluguel por m2': 'aluguel_m2',
        'Cap Rate': 'cap_rate',
        'Vacância Média': 'vacancia_media'
    }
