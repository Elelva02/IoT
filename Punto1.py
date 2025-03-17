import streamlit as st
import polars as pl  
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

st.title("Análisis de Operaciones y Calificación de Usuarios")

# Cargar datos con Polars
df = pl.read_excel('depositos_oinks.xlsx')

# Verificar y convertir la columna operation_date a tipo Date
df = df.with_columns(pl.col("operation_date").cast(pl.Date))

# Eliminar valores nulos en operation_date
df = df.drop_nulls
