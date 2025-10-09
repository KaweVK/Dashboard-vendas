import pandas as pd
import streamlit as st
import plotly.express as px
import requests as req 

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

def formatar_valor(valor, prefixo = ""):
   for unidade in ['', 'mil', 'milhões']:
        if valor < 1000:
            return f"{prefixo}{valor:.2f} {unidade}"
        valor /= 1000

st.title("Sales Dashboard :shopping_cart:")

url = "https://labdados.com/produtos"
response = req.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')


## Tabelas 
# Receita por Estado
receita_estados = dados.groupby('Local da compra')[['Preço']].sum()
receita_estados = dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on='Local da compra', right_index=True).sort_values('Preço', ascending=False)

# Receita Mensal
receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Preço'].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mês'] = receita_mensal['Data da Compra'].dt.month_name().str.slice(stop=3)

# Receita Categoria
receita_categoria = dados.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending=False)

# Quantidade de Vendas por Estado
qtd_vendas_estado = dados.groupby('Local da compra')[['Preço']].count()
qtd_vendas_estado = dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(qtd_vendas_estado, left_on='Local da compra', right_index=True).sort_values('Preço', ascending=False)
qtd_vendas_estado = qtd_vendas_estado.rename(columns={'Preço':'Quantidade de Vendas'})

# Quantidade de Vendas por Mês
qtd_vendas_mensais = dados.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Preço'].count().reset_index()
qtd_vendas_mensais['Ano'] = qtd_vendas_mensais['Data da Compra'].dt.year
qtd_vendas_mensais['Mês'] = qtd_vendas_mensais['Data da Compra'].dt.month_name().str.slice(stop=3)
qtd_vendas_mensais = qtd_vendas_mensais.rename(columns={'Preço':'Quantidade de Vendas'})

# Quantidade de Vendas por Categoria
qtd_vendas_categoria = dados.groupby('Categoria do Produto')[['Preço']].count().sort_values('Preço', ascending=False)

## Graficos
fig_mapa_receita = px.scatter_geo(receita_estados,
                                   lat = 'lat',
                                   lon = 'lon',
                                   scope='south america',
                                   size = 'Preço',
                                   template = 'seaborn',
                                   hover_name = 'Local da compra',
                                   hover_data = {'lat':False, 'lon':False},
                                   title = 'Receita por Estado')

fig_receita_mensal = px.line(receita_mensal,
                             x = 'Mês',
                             y = 'Preço',
                             markers = True,
                             range_y = (0, receita_mensal.max()),
                             color = 'Ano',
                             line_dash = 'Ano',
                             title = 'Receita Mensal')

fig_receita_mensal.update_layout(xaxis_title = 'Mês', 
                                 yaxis_title = 'Receita')

fig_receita_estados = px.bar(receita_estados.head(),
                             x = 'Local da compra',
                             y = 'Preço',
                             text_auto = True,
                             title = 'Top 5 Estados - Receita')                             

fig_receita_estados.update_layout(xaxis_title = 'Estado', 
                                 yaxis_title = 'Receita')

fig_receita_categoria = px.bar(receita_categoria,
                               text_auto = True,
                               title = 'Receita por Categoria')

fig_receita_categoria.update_layout(yaxis_title = 'Receita')

fig_mapa_vendas_estado = px.scatter_geo(qtd_vendas_estado,
                                   lat = 'lat',
                                   lon = 'lon',
                                   scope='south america',
                                   size = 'Quantidade de Vendas',
                                   template = 'seaborn',
                                   hover_name = 'Local da compra',
                                   hover_data = {'lat':False, 'lon':False},
                                   title = 'Quantidade de Vendas por Estado')

fig_vendas_mensais = px.line(qtd_vendas_mensais,
                             x = 'Mês',
                             y = 'Quantidade de Vendas',
                             markers = True,
                             range_y = (0, qtd_vendas_mensais.max()),
                             color = 'Ano',
                             line_dash = 'Ano',
                             title = 'Quantidade de Vendas Mensal')

fig_vendas_estado = px.bar(qtd_vendas_estado.head(),
                           x = 'Local da compra',
                           y = 'Quantidade de Vendas',
                           text_auto = True,
                           title = 'Top 5 Estados - Quantidade de Vendas')

fig_vendas_estado.update_layout(xaxis_title = 'Estado')

fig_vendas_categorias = px.bar(qtd_vendas_categoria, text_auto = True, title = 'Quantidade de Vendas por Categoria')

## Visualizações no streamlit
aba1, aba2, aba3 = st.tabs(['Receita', 'Vendas', 'Vendedores'])

with aba1:
   st.subheader("Análise da Receita")
   col1, col2 = st.columns(2)
   with col1:
      st.metric("Receita das Vendas", formatar_valor(dados['Preço'].sum(), "R$"), border= True) 
      st.plotly_chart(fig_mapa_receita, use_container_width=True)
      st.plotly_chart(fig_receita_estados, use_container_width=True)
   with col2: 
      st.metric("Quantidade de Vendas", formatar_valor(dados.shape[0]), border= True)
      st.plotly_chart(fig_receita_mensal, use_container_width=True) 
      st.plotly_chart(fig_receita_categoria, use_container_width=True)
   st.dataframe(dados)

with aba2:
   st.subheader("Análise da Vendas")
   col1, col2 = st.columns(2)
   with col1:
      st.metric("Receita das Vendas", formatar_valor(dados['Preço'].sum(), "R$"), border= True) 
      st.plotly_chart(fig_mapa_vendas_estado, use_container_width=True)
      st.plotly_chart(fig_vendas_estado, use_container_width=True)
   with col2: 
      st.metric("Quantidade de Vendas", formatar_valor(dados.shape[0]), border= True)
      st.plotly_chart(fig_vendas_mensais, use_container_width=True)
      st.plotly_chart(fig_vendas_categorias, use_container_width=True)
   st.dataframe(qtd_vendas_estado)
   st.dataframe(qtd_vendas_mensais)

with aba3:
   st.subheader("Análise da Vendas")
   col1, col2 = st.columns(2)
   with col1:
      st.metric("Receita das Vendas", formatar_valor(dados['Preço'].sum(), "R$"), border= True) 
   with col2: 
      st.metric("Quantidade de Vendas", formatar_valor(dados.shape[0]), border= True)

## source .venv/Scripts/activate
## python.exe -m pip install --upgrade pip
## pip install -r requirements.txt 
## .venv/Scripts/activate
## streamlit run dashboard.py 