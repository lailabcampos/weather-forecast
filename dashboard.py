import streamlit as st

from conexao_api import Conexao_API
from database import Database
from datetime import date, timedelta

st.set_page_config(page_title="Weather Forecast", page_icon="🌤️", layout="centered")

previsao_icones = {
    "chuva leve": "🌦️",
    "chuva moderada": "🌧️",
    "chuva forte": "⛈️",
    "nublado": "☁️",
    "céu limpo": "🌞",
    "nuvens dispersas": "🌤️",
    "algumas nuvens": "🌥️",
}


def capitalize(string):
    return f"{string[0].upper()}{string[1:]}"


st.sidebar.markdown("# 🌤️ Previsão do Tempo")

cidade = st.sidebar.text_input("Região", value="Recife")
data = st.sidebar.date_input(
    "Data",
    value=date.today(),
    min_value=date.today(),
    max_value=date.today() + timedelta(days=5),
)
grafico = st.sidebar.checkbox("Plotar gráfico de resultados", value=False)

# Inicialização da API e Busca pela cidade
dados = Conexao_API(cidade)

if not dados.coord:
    st.error("Região não encontrada! Favor inserir outro local.")
    st.stop()

# Seleção do período de tempo a ser consultado
database = Database(data, dados)

relatorio = database.database()
st.markdown(f"#### Relatório de Previsão do tempo (Data: {database.str_data})")
st.dataframe(relatorio, use_container_width=True)

st.markdown(
    f"O clima é predominantemente **{capitalize(database.previsao)}** {previsao_icones.get(database.previsao, '')}"
)

if grafico:
    fig = database.graficos()
    st.plotly_chart(fig)
