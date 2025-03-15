import streamlit as st
import polars as pl
import matplotlib.pyplot as plt

# Cargar datos
df = pl.read_excel('depositos_oinks.xlsx')

# Convertir a pandas para Matplotlib
df_pd = df.to_pandas()

# Crear la figura
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df_pd["user_id"], df_pd["operation_value"], color="skyblue")
ax.set_xlabel("User ID")
ax.set_ylabel("Operation Value")
ax.set_title("Valor de Operaciones por Usuario")

# Mostrar en Streamlit
st.pyplot(fig)
