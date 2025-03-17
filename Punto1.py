import streamlit as st
import polars as pl  
import plotly.express as px

st.title("Análisis de Operaciones y Calificación de Usuarios")

# Cargar datos con Polars
df = pl.read_excel('depositos_oinks.xlsx')

# Verificar los tipos de columnas
st.write("Tipos de columnas:", df.schema)

# Verificar y convertir operation_date a Date si es necesario
if df.schema["operation_date"] == pl.Utf8:
    df = df.with_columns(pl.col("operation_date").str.to_date("%Y-%m-%d"))
elif df.schema["operation_date"] == pl.Int64:
    df = df.with_columns(pl.col("operation_date").cast(pl.Date))
elif df.schema["operation_date"] == pl.Float64:
    df = df.with_columns(pl.col("operation_date").cast(pl.Date))
else:
    st.error("El tipo de 'operation_date' no es compatible.")
    st.stop()

# Mostrar tabla original
st.subheader("Vista previa de los datos originales")
st.dataframe(df.head(50))
