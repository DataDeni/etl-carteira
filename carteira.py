
import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import requests

st.set_page_config(page_title="Histórico de Ativos", layout="wide")
st.title("📊 Histórico de Ações, Metais, Criptomoedas e Moedas")

# Cria abas
abas = st.tabs([
    "🏦 BBDC3",
    "🥇 Ouro",
    "🥈 Prata",
    "₿ Bitcoin",
    "Ξ Ethereum",
    "💵 Dólar",
    "💶 Euro"
])

# ----------- Aba BBDC3 -----------


with abas[0]:
    st.subheader("📈 Ação BBDC3 (Bradesco)")

    hoje = datetime.datetime.today().strftime('%Y-%m-%d')
    bbdc3 = yf.Ticker("BBDC3.SA")
    df_bbdc3 = bbdc3.history(start="2010-01-01", end=hoje).reset_index()

    df_bbdc3 = df_bbdc3.drop(columns=['Dividends', 'Stock Splits'])
    df_bbdc3.columns = ["Data", "Abertura", "Máxima", "Mínima", "Fechamento", "Volume"]
    df_bbdc3['Variação (%)'] = df_bbdc3['Fechamento'].pct_change().mul(100).round(2)

    df_bbdc3['Data'] = pd.to_datetime(df_bbdc3['Data'])
    df_bbdc3 = df_bbdc3.sort_values('Data', ascending=False).reset_index(drop=True)
    df_bbdc3['Data'] = df_bbdc3['Data'].dt.strftime('%d/%m/%Y')

    st.write("📅 Última data retornada:", df_bbdc3.loc[0, 'Data'])
    st.table(df_bbdc3)

  
# ----------- Aba Ouro -----------
with abas[1]:
    st.subheader("🥇 Ouro (GC=F)")

    hoje = datetime.datetime.today().strftime('%Y-%m-%d')
    ouro = yf.Ticker("GC=F")
    df_ouro = ouro.history(start="2010-01-01", end=hoje).reset_index()
    df_ouro = df_ouro.drop(columns=['Dividends', 'Stock Splits'])
    df_ouro.columns = ["Data", "Abertura", "Máxima", "Mínima", "Fechamento", "Volume"]
    df_ouro['Variação (%)'] = df_ouro['Fechamento'].pct_change().mul(100).round(2)
    df_ouro = df_ouro[::-1].reset_index(drop=True)
    df_ouro['Data'] = df_ouro['Data'].dt.strftime('%d/%m/%Y')
    st.dataframe(df_ouro)

# ----------- Aba Prata -----------
with abas[2]:
    st.subheader("🥈 Prata (SI=F)")

    hoje = datetime.datetime.today().strftime('%Y-%m-%d')
    prata = yf.Ticker("SI=F")
    df_prata = prata.history(start="2010-01-01", end=hoje).reset_index()
    df_prata = df_prata.drop(columns=['Dividends', 'Stock Splits'])
    df_prata.columns = ["Data","Abertura","Máxima","Mínima","Fechamento","Volume"]
    df_prata['Variação (%)'] = df_prata['Fechamento'].pct_change().mul(100).round(2)
    df_prata = df_prata[::-1].reset_index(drop=True)
    df_prata['Data'] = df_prata['Data'].dt.strftime('%d/%m/%Y')
    st.dataframe(df_prata)

# ----------- Aba Bitcoin -----------
with abas[3]:
    st.subheader("₿ Bitcoin (BTC/BRL)")

    url = 'https://min-api.cryptocompare.com/data/v2/histoday'
    api = '37acf552f80fe45daae9c8cb8904d98e0ee288704e6e16a0def95dbb850d4687'
    params = {
        'fsym': 'BTC',
        'tsym': 'BRL',
        'limit': 2000,
        'api_key': api  # substitua pela sua chave válida
    }

    response = requests.get(url, params=params)
    dados = response.json()

    if 'Data' in dados and 'Data' in dados['Data']:
        df_bitcoin = pd.DataFrame(dados['Data']['Data'])
        df_bitcoin = df_bitcoin.drop(columns=['volumeto', 'conversionType', 'conversionSymbol'], errors='ignore')
        df_bitcoin = df_bitcoin[['time', 'open', 'high', 'low', 'close', 'volumefrom']]
        df_bitcoin.columns = ["Data", "Abertura", "Máxima", "Mínima", "Fechamento", "Volume"]
        df_bitcoin['Variação (%)'] = df_bitcoin['Fechamento'].pct_change().mul(100).round(2)
        df_bitcoin['Data'] = pd.to_datetime(df_bitcoin['Data'], unit='s').dt.strftime('%d/%m/%Y')
        df_bitcoin = df_bitcoin[::-1].reset_index(drop=True)
        st.dataframe(df_bitcoin)
    else:
        st.error("Erro ao obter os dados do Bitcoin. Verifique a API key ou tente novamente mais tarde.")

# ----------- Aba Ethereum -----------
with abas[4]:
    st.subheader("Ξ Ethereum (ETH/BRL)")

    url = 'https://min-api.cryptocompare.com/data/v2/histoday'
    api = '37acf552f80fe45daae9c8cb8904d98e0ee288704e6e16a0def95dbb850d4687'
    params = {
        'fsym': 'ETH',
        'tsym': 'BRL',
        'limit': 2000,
        'api_key': api
    }

    response = requests.get(url, params=params)
    dados = response.json()

    if 'Data' in dados and 'Data' in dados['Data']:
        df_ethereum = pd.DataFrame(dados['Data']['Data'])
        df_ethereum = df_ethereum.drop(columns=['volumeto', 'conversionType', 'conversionSymbol'], errors='ignore')
        df_ethereum = df_ethereum[['time', 'open', 'high', 'low', 'close', 'volumefrom']]
        df_ethereum.columns = ["Data", "Abertura", "Máxima", "Mínima", "Fechamento", "Volume"]
        df_ethereum['Variação (%)'] = df_ethereum['Fechamento'].pct_change().mul(100).round(2)
        df_ethereum['Data'] = pd.to_datetime(df_ethereum['Data'], unit='s').dt.strftime('%d/%m/%Y')
        df_ethereum = df_ethereum[::-1].reset_index(drop=True)
        st.dataframe(df_ethereum)
    else:
        st.error("Erro ao obter os dados do Ethereum. Verifique a API ou tente novamente.")

# ----------- Aba Dólar -----------
with abas[5]:
    st.subheader("💵 Dólar (USD/BRL)")

    url = 'https://www.alphavantage.co/query'
    api = 'XUVYGH7HQ1CATKYS'
    params = {
        'function': 'FX_DAILY',
        'from_symbol': 'USD',
        'to_symbol': 'BRL',
        'outputsize': 'full',
        'apikey': api
    }

    response = requests.get(url, params=params)
    dados = response.json()

    if 'Time Series FX (Daily)' in dados:
        precos = dados['Time Series FX (Daily)']
        df_dolar = pd.DataFrame.from_dict(precos, orient='index').reset_index()
        df_dolar.columns = ['Data', 'Abertura', 'Máxima', 'Mínima', 'Fechamento']
        colunas = ['Abertura', 'Máxima', 'Mínima', 'Fechamento']
        df_dolar[colunas] = df_dolar[colunas].astype(float)

        df_dolar['Data'] = pd.to_datetime(df_dolar['Data'])
        df_dolar = df_dolar.sort_values('Data').reset_index(drop=True)

        df_dolar['Variação (%)'] = df_dolar['Fechamento'].pct_change().mul(100).round(2)
        df_dolar = df_dolar[::-1].reset_index(drop=True)
        df_dolar['Data'] = df_dolar['Data'].dt.strftime('%d/%m/%Y')

        st.dataframe(df_dolar)
    else:
        st.error("Erro ao obter os dados do dólar. Verifique a chave da API ou limite de requisições.")

# ----------- Aba Euro -----------
    with abas[6]:
         st.subheader("💶 Euro (EUR/BRL)")

         url = 'https://www.alphavantage.co/query'
         api = 'XUVYGH7HQ1CATKYS'
         params = {
             'function': 'FX_DAILY',
             'from_symbol': 'EUR',
             'to_symbol': 'BRL',
             'outputsize': 'full',
             'apikey': api
         }

         response = requests.get(url, params=params)
         dados = response.json()

         if 'Time Series FX (Daily)' in dados:
         precos = dados['Time Series FX (Daily)']
         df_euro = pd.DataFrame.from_dict(precos, orient='index').reset_index()
         df_euro.columns = ['Data', 'Abertura', 'Máxima', 'Mínima', 'Fechamento']

         colunas = ['Abertura', 'Máxima', 'Mínima', 'Fechamento']
         df_euro[colunas] = df_euro[colunas].astype(float)

         df_euro['Data'] = pd.to_datetime(df_euro['Data'])
         df_euro = df_euro.sort_values('Data').reset_index(drop=True)

         df_euro['Variação (%)'] = df_euro['Fechamento'].pct_change().mul(100).round(2)
         df_euro = df_euro[::-1].reset_index(drop=True)
         df_euro['Data'] = df_euro['Data'].dt.strftime('%d/%m/%Y')

         st.dataframe(df_euro)
     else:
         st.error("Erro ao obter os dados do euro. Verifique a chave da API ou tente novamente mais tarde")
