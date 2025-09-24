import pandas as pd
import streamlit as st
import plotly.express as px
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

## Tabelas 
receita_estados = dados.groupby('Local da compra')[['Preço']].sum()
receita_estados = dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on='Local da compra', right_index=True).sort_values('Preço', ascending=False)

# Graficos
fig_mapa_receita = px.scatter_geo(receita_estados,
                                   lat = 'lat',
                                   lon = 'lon',
                                   scope='south america',
                                   size = 'Preço',
                                   template = 'seaborn',
                                   hover_name = 'Local da compra',
                                   hover_data = {'lat':False, 'lon':False},
                                   title = 'Receita por Estado',)

## Visualizações
col1, col2 = st.columns(2)
with col1:
  st.metric("Receita das Vendas", formatar_valor(dados['Preço'].sum(), "R$"), border= True) 
  st.plotly_chart(fig_mapa_receita)
with col2: 
   st.metric("Quantidade de Vendas", formatar_valor(dados.shape[0]))

st.dataframe(dados)
