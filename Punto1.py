import streamlit as st
import polars as pl  # Cambiamos pandas por polars
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

st.title("Visualización de Ejemplo")

st.subheader("Subtítulo")

# Creamos el DataFrame con polars
data =pl.read_excel('depositos_oinks.xlsx')


df = pl.DataFrame(data)

# Mostrar el DataFrame en Streamlit (convertido a polars para st.dataframe)
st.dataframe(df.to_polars())

st.subheader("Gráfico sencillo con Matplotlib")

# Convertimos a polars para usar con Matplotlib
df_pl = df.to_polars()

# Crear figura y eje
fig, ax = plt.subplots()
ax.plot(df_pl["user_id"], df_pl["operation_value"], marker="o", linestyle="-", color="b")
ax.set_xlabel("user_id")
ax.set_ylabel("operation_value")
ax.set_title("Gráfico de Líneas con Matplotlib")

# Mostrar gráfico en Streamlit
st.pyplot(fig)

st.subheader("Gráfico interactivo con Plotly")

# Crear gráfico con Plotly (usando pandas para mayor compatibilidad)
fig_plotly = px.bar(df_pl, x="", y="peration_value", title="Gráfico de Barras con Plotly")

# Mostrar gráfico en Streamlit
st.plotly_chart(fig_plotly)

st.subheader("Gráfico de Barras con Matplotlib")

fig_bar, ax_bar = plt.subplots()
ax_bar.bar(df_pl["Categoria"], df_pl["Valores"], color="skyblue")
ax_bar.set_xlabel("Categoría")
ax_bar.set_ylabel("Valores")
ax_bar.set_title("Gráfico de Barras")

st.pyplot(fig_bar)
