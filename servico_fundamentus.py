import requests
import pandas   as pd
import io
import time

from datetime import datetime

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
    
    if mode == 'acao':
        df['dividend_yield']    = perc_to_float(df['dividend_yield'])
        df['mrg_ebit']          = perc_to_float(df['mrg_ebit'])
        df['mrg_liq']           = perc_to_float(df['mrg_liq'])
        df['roic']              = perc_to_float(df['roic'])
        df['roe']               = perc_to_float(df['roe'])
        df['cresc_rec_5_a']     = perc_to_float(df['cresc_rec_5_a'])
    elif mode == 'fii':
        df['ffo_yield']         = perc_to_float(df['ffo_yield'])
        df['dividend_yield']    = perc_to_float(df['dividend_yield'])
        df['cap_rate']          = perc_to_float(df['cap_rate'])
        df['vacancia_media']    = perc_to_float(df['vacancia_media'])

    df['data_coleta'] = datetime.now()

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
        'Div.Yield': 'dividend_yield',
        'P/Ativo': 'p_ativo',
        'P/Cap.Giro': 'p_cap_giro',
        'P/EBIT': 'p_ebit',
        'P/Ativ Circ.Liq': 'p_ativ_circ_liqs',
        'EV/EBIT': 'ev_ebit',
        'EV/EBITDA': 'ev_ebitda',
        'Mrg Ebit': 'mrg_ebit',
        'Mrg. Líq.': 'mrg_liq',
        'ROIC': 'roic',
        'ROE': 'roe',
        'Liq. Corr.': 'liq_corr',
        'Liq.2meses': 'liq_2_meses',
        'Patrim. Líq': 'patrim_liq',
        'Dív.Brut/ Patrim.': 'div_brut_patrim',
        'Cresc. Rec.5a': 'cresc_rec_5_a'
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

def perc_to_float(val):
    """
    Percent to float
      - replace string in pt-br to float
      - from '45,56%' to 0.4556

    Input:
        (DataFrame, column_name)
    """

    res = val
    res = res.replace( to_replace=r'[%]', value='' , regex=True )
    res = res.replace( to_replace=r'[.]', value='' , regex=True )
    res = res.replace( to_replace=r'[,]', value='.', regex=True )
    res = res.astype(float) / 100

    return res
