import streamlit as st
import polars as pl  
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

st.title("Análisis de Operaciones y Calificación de Usuarios")

# Cargar datos con Polars
df = pl.read_excel('depositos_oinks.xlsx')

# Convertir operation_value a numérico
df = df.with_columns(pl.col("operation_value").cast(pl.Float64))

# Convertir operation_date a tipo Date (sin horas)
df = df.with_columns(pl.col("operation_date").cast(pl.Date))

# Normalizar "operation_value"
scaler = MinMaxScaler()
df = df.with_columns(
    pl.Series("normalized_operation_value", scaler.fit_transform(df["operation_value"].to_numpy().reshape(-1, 1)).flatten())
)

# Agrupar por fecha
df_grouped = df.groupby("operation_date").agg(
    pl.col("normalized_operation_value").mean().alias("avg_normalized_value")
)

# Mostrar datos agrupados
st.subheader("Datos Agrupados y Normalizados")
st.dataframe(df_grouped)

st.subheader("Gráfico de Tendencia por Fecha")

# Crear gráfico de líneas
fig = px.line(df_grouped.to_pandas(), x="operation_date", y="avg_normalized_value",
              title="Tendencia Normalizada de Operaciones por Fecha",
              labels={"operation_date": "Fecha", "avg_normalized_value": "Valor Normalizado"})

st.plotly_chart(fig)
