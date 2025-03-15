import streamlit as st
import polars as pl  # Usamos polars
import matplotlib.pyplot as plt
import plotly.graph_objects as go  # Mejor que plotly.express para listas puras

st.title("Visualización de Punto 1")

#st.subheader("Subtítulo")

# Leer archivo Excel con polars
df = pl.read_excel('depositos_oinks.xlsx')

# Mostrar el DataFrame en Streamlit (como tabla de diccionarios)
st.write(df)

# O convertirlo a lista de dicts para que se vea mejor en streamlit
st.dataframe(df.to_dicts())

# ---------------------------------
st.subheader("Gráfico sencillo con Matplotlib")

# Extraer columnas como listas
user_ids = df["user_id"].to_list()
operation_values = df["operation_value"].to_list()

# Crear figura y eje
fig, ax = plt.subplots()
ax.plot(user_ids, operation_values, marker="o", linestyle="-", color="b")
ax.set_xlabel("user_id")
ax.set_ylabel("operation_value")
ax.set_title("Gráfico de Líneas con Matplotlib")

# Mostrar gráfico en Streamlit
st.pyplot(fig)

# ---------------------------------
st.subheader("Gráfico interactivo con Plotly")

# Crear gráfico con listas, usando go.Figure
fig_plotly = go.Figure(data=[
    go.Bar(x=user_ids, y=operation_values)
])
fig_plotly.update_layout(title="Gráfico de Barras con Plotly")

# Mostrar gráfico en Streamlit
st.plotly_chart(fig_plotly)

# ---------------------------------
st.subheader("Gráfico de Barras con Matplotlib")

fig_bar, ax_bar = plt.subplots()
ax_bar.bar(user_ids, operation_values, color="skyblue")
ax_bar.set_xlabel("user_id")
ax_bar.set_ylabel("operation_value")
ax_bar.set_title("Gráfico de Barras con Matplotlib")

st.pyplot(fig_bar)
