import streamlit as st
import polars as pl  

st.title("Verificación de Tipos en Polars")

# Cargar datos con Polars
df = pl.read_excel('depositos_oinks.xlsx')

# Mostrar esquema de columnas
st.write("Esquema del DataFrame:", df.schema)
