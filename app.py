import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configurações da Página
st.set_page_config(page_title="Relatórios Analíticos de Saúde Comunitária", layout="wide")

# Título do App
st.title("Relatórios Analíticos de Saúde Comunitária")
st.subheader("Análise de dados de saúde para identificação de comorbidades e apoio ao planejamento preventivo")

# Carregar os dados (substitua 'dados_saude.csv' pelo caminho real do arquivo)
@st.cache_data
def carregar_dados():
    return pd.read_csv('dados_saude_comunidade.csv')

# Função para exibir os dados carregados
dados = carregar_dados()
st.write("Dados carregados:", dados.head())

# Visualização das Comorbidades
st.subheader("Distribuição das Comorbidades")
comorbidades = dados['comorbidade'].value_counts()
st.bar_chart(comorbidades)

# Tendência ao longo do tempo (exemplo: novos casos por mês)
st.subheader("Tendência de Casos ao Longo do Tempo")
dados['data'] = pd.to_datetime(dados['data'])  # Converter a coluna de datas
dados['mes'] = dados['data'].dt.to_period("M")
tendencia = dados.groupby('mes').size()
st.line_chart(tendencia)

# Identificar Grupos de Risco
st.subheader("Análise de Grupos de Risco")
idade_risco = dados.groupby('idade').size()
st.area_chart(idade_risco)

# Insights com métricas
st.write("Total de Pacientes:", len(dados))
st.write("Total de Casos com Comorbidades:", comorbidades.sum())
st.write("Comorbidade Mais Comum:", comorbidades.idxmax())

# Filtros e interação
idade_min, idade_max = st.slider("Filtrar por faixa etária", min_value=int(dados['idade'].min()), max_value=int(dados['idade'].max()), value=(20, 60))
dados_filtrados = dados[(dados['idade'] >= idade_min) & (dados['idade'] <= idade_max)]
st.write("Dados filtrados por faixa etária:", dados_filtrados.head())
