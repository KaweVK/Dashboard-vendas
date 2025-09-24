import pandas as pd
import streamlit as st
import plotly as plt
import requests as req 

st.title("Sales Dashboard :shopping_cart:")

url = "https://labdados.com/produtos"
response = req.get(url)
dados = pd.DataFrame.from_dict(response.json())

col1, col2 = st.columns(2)
with col1:
  st.metric("Soma das Vendas", dados['Preço'].sum(), "R$", border= True) 
with col2: 
   st.metric("Quantidade de Vendas", dados.shape[0])

st.dataframe(dados)
