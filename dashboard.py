import pandas as pd
import streamlit as st
import plotly as plt
import requests as req 

def formatar_valor(valor, prefixo = ""):
   for unidade in ['', 'mil', 'milhões']:
        if valor < 1000:
            return f"{prefixo}{valor:.2f} {unidade}"
        valor /= 1000

st.title("Sales Dashboard :shopping_cart:")

url = "https://labdados.com/produtos"
response = req.get(url)
dados = pd.DataFrame.from_dict(response.json())

col1, col2 = st.columns(2)
with col1:
  st.metric("Receita das Vendas", formatar_valor(dados['Preço'].sum(), "R$"), border= True) 
with col2: 
   st.metric("Quantidade de Vendas", formatar_valor(dados.shape[0]))

st.dataframe(dados)
