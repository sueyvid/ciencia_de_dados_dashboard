# app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análise de Personalidade", layout="wide")

st.title("📊 Análise de Personalidade: Extrovertidos vs Introvertidos")

# Carrega os dados
@st.cache_data
def load_data():
    return pd.read_csv("personality_dataset.csv")

df = load_data()

# Verifica se a coluna de personalidade existe
if 'Personality' not in df.columns:
    st.error("A coluna 'Personality' não foi encontrada no dataset.")
    st.stop()

# Mostra dados brutos
with st.expander("🔍 Ver dados brutos"):
    st.dataframe(df)

# Lista de colunas numéricas (excluindo a coluna de personalidade)
caracteristicas = df.select_dtypes(include='number').columns.tolist()

if not caracteristicas:
    st.warning("Nenhuma característica numérica encontrada para análise.")
    st.stop()

# Seletor de característica
st.sidebar.header("🔧 Filtros")
carac = st.sidebar.selectbox("Selecione uma característica:", caracteristicas)

# Seletor de tipo de gráfico
grafico_tipo = st.sidebar.radio("Tipo de gráfico:", ["Boxplot", "Histograma"])

# Subtítulo
st.subheader(f"Comparação de {carac} entre Extrovertidos e Introvertidos")

# Gráfico
fig, ax = plt.subplots(figsize=(10, 5))

if grafico_tipo == "Boxplot":
    sns.boxplot(x='Personality', y=carac, data=df, ax=ax, palette="pastel")
    ax.set_title(f"Distribuição de {carac}")
else:
    for p in df['Personality'].unique():
        subset = df[df['Personality'] == p]
        sns.kdeplot(subset[carac], label=p, fill=True, ax=ax)
    ax.legend()
    ax.set_title(f"Distribuição de {carac} por Perfil")

st.pyplot(fig)

# Estatísticas descritivas
st.subheader("📈 Estatísticas Descritivas")
st.write(df.groupby('Personality')[carac].describe().T)

# Contagem de perfis
st.sidebar.markdown("### 📌 Distribuição de Perfis")
st.sidebar.bar_chart(df['Personality'].value_counts())
