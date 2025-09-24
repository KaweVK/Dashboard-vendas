import pandas as pd
import streamlit as st
import plotly as plt
import requests as req 

st.title("Sales Dashboard :shopping_cart:")

url = "https://labdados.com/produtos"
response = req.get(url)
dados = pd.DataFrame.from_dict(response.json())

st.dataframe(dados)