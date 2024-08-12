import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para usar o layout em largura total
st.set_page_config(layout="wide")

# Estilos personalizados com CSS
st.markdown("""
    <style>
    :root {
        --primary-color: #007bff;
        --secondary-color: #6c757d;
        --bg-color: #f2f2f2;
        --text-color: #333;
    }
    
    body {
        font-family: 'Roboto', sans-serif;
        color: var(--text-color);
        background-color: var(--bg-color);
    }

    .stSlider > div {
        padding: 16px 0;
        border-radius: 10px;
        background-color: #fff;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .css-1cpxqw2, .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .css-1cpxqw2 {
        background-color: #fff;
    }

    .stDataFrame th, .stDataFrame td {
        padding: 12px 16px;
    }

    .stButton > button {
        background-color: var(--primary-color);
        color: #fff;
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
        font-size: 16px;
        cursor: pointer;
    }

    .stButton > button:hover {
        background-color: #0056b3;
    }
    </style>
    """, unsafe_allow_html=True)

# Carregando datasets
df_reviews = pd.read_csv("datasets/customer reviews.csv")
df_top100_books = pd.read_csv("datasets/Top-100 Trending Books.csv")

# Calculando o preço máximo e mínimo dos livros
price_max = df_top100_books["book price"].max()
price_min = df_top100_books["book price"].min()

# Obtendo a lista de gêneros
genres = df_top100_books["genre"].unique()

# Layout de colunas
col1, col2 = st.columns([1, 3])

# Controles na primeira coluna
with col1:
    st.write("### Filtros")
    
    # Filtro de preço
    st.write("#### Faixa de Preço")
    price_range = st.slider("Preço", price_min, price_max, (price_min, price_max), step=0.01)

    # Filtro de gênero
    st.write("#### Gênero")
    selected_genre = st.selectbox("Selecione o gênero", ["Todos"] + list(genres))

    # Botões de seleção de tabela
    st.write("### Escolha a tabela:")
    if st.button("Avaliações de Clientes"):
        table_choice = "Avaliações de Clientes"
    if st.button("Top 100 Livros em Alta"):
        table_choice = "Top 100 Livros em Alta"

# Aplicar filtros
if 'table_choice' in locals():
    if table_choice == "Top 100 Livros em Alta":
        if selected_genre == "Todos":
            filtered_books = df_top100_books[(df_top100_books["book price"] >= price_range[0]) & 
                                             (df_top100_books["book price"] <= price_range[1])]
        else:
            filtered_books = df_top100_books[(df_top100_books["book price"] >= price_range[0]) & 
                                             (df_top100_books["book price"] <= price_range[1]) &
                                             (df_top100_books["genre"] == selected_genre)]

# Exibir a tabela selecionada na segunda coluna
with col2:
    if 'table_choice' in locals():
        if table_choice == "Avaliações de Clientes":
            st.write("### Avaliações de Clientes")
            st.dataframe(df_reviews)
        elif table_choice == "Top 100 Livros em Alta":
            st.write("### Top 100 Livros em Alta")
            st.dataframe(filtered_books)

            # Adicionar gráfico de avaliações por autor
            st.write("### Gráfico de Avaliações Médias por Autor")
            avg_rating_per_author = filtered_books.groupby('author')['rating'].mean().reset_index()
            fig = px.bar(avg_rating_per_author, x='author', y='rating', title="Avaliações Médias por Autor", labels={'rating':'Média de Avaliações', 'author':'Autor'})
            st.plotly_chart(fig)
