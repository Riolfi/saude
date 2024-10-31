import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configurações da Página
st.set_page_config(page_title="Relatórios Analíticos de Saúde Comunitária", layout="wide")

# Título do App
st.title("Relatórios Analíticos de Saúde Comunitária")
st.subheader("Análise de dados de saúde para identificação de comorbidades e apoio ao planejamento preventivo")

# Sidebar para navegação entre páginas
st.sidebar.title("Navegação")
pagina_selecionada = st.sidebar.selectbox("Selecione a página:", ["Visão Geral", "Análise de Comorbidades", "Relatórios Personalizados"])

# Carregar os dados
@st.cache_data
def carregar_dados():
    return pd.read_csv('dados_saude_comunidade.csv')

dados = carregar_dados()

# Página 1: Visão Geral
if pagina_selecionada == "Visão Geral":
    st.title("Visão Geral")
    st.write("Bem-vindo ao painel de relatórios de saúde comunitária.")
    st.write("Nesta seção, você verá uma visão geral dos dados, como o total de pacientes, comorbidades mais comuns, entre outras métricas.")
    
    # Exemplo de métrica
    st.write("**Total de Pacientes:**", len(dados))
    comorbidade_comum = dados['comorbidade'].value_counts().idxmax()
    st.write("**Comorbidade Mais Comum:**", comorbidade_comum)

# Página 2: Análise de Comorbidades
elif pagina_selecionada == "Análise de Comorbidades":
    st.title("Análise de Comorbidades")
    st.write("Nesta seção, você pode explorar as comorbidades dos pacientes e suas distribuições.")
    
    # Filtros e gráficos para analisar comorbidades
    comorbidades = dados['comorbidade'].value_counts()
    st.bar_chart(comorbidades)

# Página 3: Relatórios Personalizados
elif pagina_selecionada == "Relatórios Personalizados":
    st.title("Relatórios Personalizados")
    st.write("Aqui você pode personalizar relatórios com filtros e exportá-los conforme necessário.")
    
    # Filtros de idade e sexo
    idade_min, idade_max = st.slider(
        "Filtrar por faixa etária", 
        min_value=int(dados['idade'].min()), 
        max_value=int(dados['idade'].max()), 
        value=(0, 60)
    )
    sexo = st.selectbox("Filtrar por sexo", ["Todos", "Masculino", "Feminino"])
    
    # Filtro de comorbidade
    comorbidades_unicas = sorted(dados['comorbidade'].str.split(", ").explode().unique())  # Obter lista única de comorbidades
    comorbidades_selecionadas = st.multiselect("Filtrar por comorbidade", comorbidades_unicas, default=comorbidades_unicas)
    
    # Aplicar filtros aos dados
    dados_filtrados = dados[(dados['idade'] >= idade_min) & (dados['idade'] <= idade_max)]
    if sexo != "Todos":
        dados_filtrados = dados_filtrados[dados_filtrados['sexo'] == sexo]
    if comorbidades_selecionadas:
        dados_filtrados = dados_filtrados[dados_filtrados['comorbidade'].apply(lambda x: any(comorb in x for comorb in comorbidades_selecionadas))]

    # Exibir dados filtrados
    st.write("Dados filtrados:", dados_filtrados)
    
    # Opção para exportar dados filtrados
    csv = dados_filtrados.to_csv(index=False)
    st.download_button(label="Baixar Relatório CSV", data=csv, file_name="relatorio_filtrado.csv", mime="text/csv")
