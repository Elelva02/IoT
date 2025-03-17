import streamlit as st
import polars as pl  
import plotly.express as px

st.title("Análisis de Operaciones y Calificación de Usuarios")

# Cargar datos con Polars
df = pl.read_excel('depositos_oinks.xlsx')

# Verificar el tipo de la columna 'operation_date'
column_types = df.schema  # Muestra los tipos de las columnas
st.write("Tipos de columnas:", column_types)

# Si operation_date no es Date o Datetime, convertir a string y luego a Date
if df.schema["operation_date"] not in [pl.Date, pl.Datetime]:
    df = df.with_columns(pl.col("operation_date").cast(pl.Utf8))

# Convertir a fecha
df = df.with_columns(pl.col("operation_date").str.to_date("%Y-%m-%d"))

# Mostrar tabla original
st.subheader("Vista previa de los datos originales")
st.dataframe(df.head(50))
