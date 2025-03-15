import streamlit as st
import polars as pl  # Cambiamos pandas por polars
import matplotlib.pyplot as plt
import plotly.express as px

st.title("Visualización de Ejemplo")

st.subheader("Subtítulo")

# Creamos el DataFrame con polars
data = pl.read_excel('depositos_oinks.xlsx')

df = pl.DataFrame(data)

# Mostrar el DataFrame en Streamlit (convertido a pandas para st.dataframe)
st.dataframe(df.to_pandas())

st.subheader("Gráfico sencillo con Matplotlib")

# Convertimos a pandas para usar con Matplotlib
df_pd = df.to_pandas()

