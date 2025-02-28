import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px  # Corrección en la importación

st.title("Visualización de Ejemplo")

st.subheader("Subtítulo")

data = {
    "Categoria": ["A", "B", "C", "D", "E"],
    "Valores": [10, 20, 30, 40, 15]
}

df = pd.DataFrame(data)
st.dataframe(df)  # Mostrar tabla

st.subheader("Gráfico sencillo con Matplotlib")

# Crear figura y eje
fig, ax = plt.subplots()
ax.plot(df["Categoria"], df["Valores"], marker="o", linestyle="-", color="b")
ax.set_xlabel("Categoría")
ax.set_ylabel("Valores")
ax.set_title("Gráfico de Líneas con Matplotlib")

# Mostrar gráfico en Streamlit
st.pyplot(fig)

st.subheader("Gráfico interactivo con Plotly")

# Crear gráfico con Plotly
fig_plotly = px.bar(df, x="Categoria", y="Valores", title="Gráfico de Barras con Plotly")

# Mostrar gráfico en Streamlit
st.plotly_chart(fig_plotly)

# Gráfico de barras con Matplotlib
st.subheader("Gráfico de Barras con Matplotlib")

fig_bar, ax_bar = plt.subplots()
ax_bar.bar(df["Categoria"], df["Valores"], color="skyblue")
ax_bar.set_xlabel("Categoría")
ax_bar.set_ylabel("Valores")
ax_bar.set_title("Gráfico de Barras")