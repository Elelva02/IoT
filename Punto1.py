import streamlit as st
import polars as pl  # Cambiamos pandas por polars
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd  # Asegurar compatibilidad con Pandas
from sklearn.preprocessing import MinMaxScaler

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

# Asegurar que 'operation_value' es numérico
df_pd["operation_value"] = pd.to_numeric(df_pd["operation_value"], errors="coerce")

# Agrupar por 'user_id' y calcular la media solo para 'operation_value'
df_grouped = df_pd.groupby("user_id", as_index=False)["operation_value"].mean()

# Normalizar los valores de 'operation_value'
scaler = MinMaxScaler()
df_grouped["operation_value"] = scaler.fit_transform(df_grouped[["operation_value"]])

# Graficar con Matplotlib
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(df_grouped["user_id"], df_grouped["operation_value"], color="skyblue")
ax.set_xlabel("User ID")
ax.set_ylabel("Normalized Operation Value")
ax.set_title("Valor Normalizado de Operaciones por Usuario")
ax.tick_params(axis='x', rotation=90)  # Rotar etiquetas para mejor visibilidad

# Mostrar en Streamlit
st.pyplot(fig)
