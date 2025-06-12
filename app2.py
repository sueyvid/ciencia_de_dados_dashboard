
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análise de Personalidade", layout="wide")

st.title("📊 Análise de Personalidade: Extrovertidos vs Introvertidos")

@st.cache_data
def load_data():
    # Assuming the processed data is saved as 'processed_personality_data.csv'
    # If not, you'll need to save the processed 'data' DataFrame to a CSV file first
    try:
        df = pd.read_csv("personality_dataset.csv")
    except FileNotFoundError:
        st.error("Processed data file not found. Please ensure 'personality_dataset.csv' exists.")
        st.stop()
    return df

df = load_data()

if 'Personality' not in df.columns:
    st.error("A coluna 'Personality' não foi encontrada no dataset.")
    st.stop()

# Map encoded Personality back to original labels for better readability in the dashboard
personality_map = {0: 'Extrovert', 1: 'Introvert'}
df['Personality'] = df['Personality'].map(personality_map)


with st.expander("🔍 Ver dados brutos"):
    st.dataframe(df)

# Identify numeric and boolean columns for plotting
numeric_columns = df.select_dtypes(include=['number', 'float64', 'int64']).columns.tolist()
boolean_columns = df.select_dtypes(include=['bool']).columns.tolist()

st.sidebar.header("🔧 Filtros e Configurações de Gráfico")

# Select feature to plot
all_features = numeric_columns + boolean_columns
if not all_features:
    st.warning("Nenhuma característica numérica ou booleana encontrada para plotar.")
    st.stop()

selected_feature = st.sidebar.selectbox("Selecione uma característica para analisar:", all_features)

# Select chart type based on the selected feature type
if selected_feature in numeric_columns:
    grafico_tipo = st.sidebar.radio("Tipo de gráfico para variáveis numéricas:", ["Boxplot", "Histograma", "Violin Plot"])
elif selected_feature in boolean_columns:
     grafico_tipo = st.sidebar.radio("Tipo de gráfico para variáveis booleanas:", ["Countplot"])


st.subheader(f"Comparação de {selected_feature} entre Extrovertidos e Introvertidos")

# Create plots based on selected chart type and feature type
fig, ax = plt.subplots(figsize=(10, 6))

if selected_feature in numeric_columns:
    if grafico_tipo == "Boxplot":
        sns.boxplot(x='Personality', y=selected_feature, data=df, ax=ax, palette="pastel")
        ax.set_title(f"Boxplot de {selected_feature} por Personalidade")
        ax.set_xlabel("Personalidade")
        ax.set_ylabel(selected_feature)
    elif grafico_tipo == "Histograma":
        for p in df['Personality'].unique():
            subset = df[df['Personality'] == p]
            sns.histplot(subset[selected_feature], label=p, fill=True, ax=ax, kde=True)
        ax.legend(title="Personalidade")
        ax.set_title(f"Histograma de {selected_feature} por Personalidade")
        ax.set_xlabel(selected_feature)
        ax.set_ylabel("Frequência")
    elif grafico_tipo == "Violin Plot":
        sns.violinplot(x='Personality', y=selected_feature, data=df, ax=ax, palette="pastel", inner='quartile')
        ax.set_title(f"Violin Plot de {selected_feature} por Personalidade")
        ax.set_xlabel("Personalidade")
        ax.set_ylabel(selected_feature)

elif selected_feature in boolean_columns:
    if grafico_tipo == "Countplot":
        sns.countplot(x=selected_feature, hue='Personality', data=df, ax=ax, palette="pastel")
        ax.set_title(f"Contagem de {selected_feature} por Personalidade")
        ax.set_xlabel(selected_feature)
        ax.set_ylabel("Contagem")
        ax.legend(title="Personalidade")


plt.tight_layout()
st.pyplot(fig)

st.subheader(f"📈 Estatísticas Descritivas para {selected_feature}")
if selected_feature in numeric_columns:
    st.write(df.groupby('Personality')[selected_feature].describe().T)
elif selected_feature in boolean_columns:
    st.write(df.groupby('Personality')[selected_feature].value_counts(normalize=True).unstack().fillna(0).T)


st.sidebar.markdown("---")
st.sidebar.subheader("📊 Distribuição Geral de Personalidade")
personality_counts = df['Personality'].value_counts()
st.sidebar.bar_chart(personality_counts)
