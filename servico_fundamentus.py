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
        df['ebit_margin']       = perc_to_float(df['ebit_margin'])
        df['net_margin']        = perc_to_float(df['net_margin'])
        df['roic']              = perc_to_float(df['roic'])
        df['roe']               = perc_to_float(df['roe'])
        df['revenue_growth_5y'] = perc_to_float(df['revenue_growth_5y'])
    elif mode == 'fii':
        df['ffo_yield']         = perc_to_float(df['ffo_yield'])
        df['dividend_yield']    = perc_to_float(df['dividend_yield'])
        df['cap_rate']          = perc_to_float(df['cap_rate'])
        df['avg_vacancy_rate']  = perc_to_float(df['avg_vacancy_rate'])

    df['created_at'] = datetime.now()
    df['updated_at'] = datetime.now()

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
        'Papel': 'ticker',
        'Cotação': 'price',
        'P/L': 'pe_ratio',
        'P/VP': 'pb_ratio',
        'PSR': 'ps_ratio',
        'Div.Yield': 'dividend_yield',
        'P/Ativo': 'price_to_assets',
        'P/Cap.Giro': 'price_to_working_capital',
        'P/EBIT': 'price_to_ebit',
        'P/Ativ Circ.Liq': 'price_to_current_assets',
        'EV/EBIT': 'ev_to_ebit',
        'EV/EBITDA': 'ev_to_ebitda',
        'Mrg Ebit': 'ebit_margin',
        'Mrg. Líq.': 'net_margin',
        'ROIC': 'roic',
        'ROE': 'roe',
        'Liq. Corr.': 'current_ratio',
        'Liq.2meses': 'avg_liquidity_2_months',
        'Patrim. Líq': 'net_equity',
        'Dív.Brut/ Patrim.': 'gross_debt_to_equity',
        'Cresc. Rec.5a': 'revenue_growth_5y'
    }

def get_fii_url():
    return 'https://www.fundamentus.com.br/fii_resultado.php'

def get_fii_columns():
    return {
        'Papel': 'ticker',
        'Segmento': 'segment',
        'Cotação': 'price',
        'FFO Yield': 'ffo_yield',
        'Dividend Yield': 'dividend_yield',
        'P/VP': 'pb_ratio',
        'Valor de Mercado': 'market_value',
        'Liquidez': 'liquidity',
        'Qtd de imóveis': 'property_count',
        'Preço do m2': 'price_per_sqm',
        'Aluguel por m2': 'rent_per_sqm',
        'Cap Rate': 'cap_rate',
        'Vacância Média': 'avg_vacancy_rate'
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
    
    # Arredondar para 8 casas decimais para evitar imprecisão de ponto flutuante
    res = res.round(8)

    return res
