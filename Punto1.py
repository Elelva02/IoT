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

# Agrupar por usuario y calcular el promedio de operation_value
df_grouped = df_pd.groupby("user_id", as_index=False).mean()

# Graficar con Matplotlib
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(df_grouped["user_id"], df_grouped["operation_value"], color="skyblue")
ax.set_xlabel("User ID")
ax.set_ylabel("Average Operation Value")
ax.set_title("Promedio del Valor de Operaciones por Usuario")
ax.tick_params(axis='x', rotation=90)  # Rotar etiquetas para mejor visibilidad

# Mostrar en Streamlit
st.pyplot(fig)
