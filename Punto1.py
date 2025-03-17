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
df = df.drop_nulls("operation_date")

# Convertir operation_value a numérico
df = df.with_columns(pl.col("operation_value").cast(pl.Float64))

# Normalizar operation_value
scaler = MinMaxScaler()
df = df.with_columns(
    pl.Series("normalized_operation_value", scaler.fit_transform(df["operation_value"].to_numpy().reshape(-1, 1)).flatten())
)

# 🚀 SOLUCIÓN 1: Usar groupby con operación correcta
df_grouped = df.groupby("operation_date").agg(
    pl.col("normalized_operation_value").mean().alias("avg_normalized_value")
)

# 🚀 SOLUCIÓN 2: Si sigue fallando, usar groupby_dynamic()
# df_grouped = df.groupby_dynamic("operation_date", every="1d").agg(
#     pl.col("normalized_operation_value").mean().alias("avg_normalized_value")
# )

# Mostrar datos agrupados
st.subheader("Datos Agrupados y Normalizados")
st.dataframe(df_grouped)

st.subheader("Gráfico de Tendencia por Fecha")

# Crear gráfico de líneas
fig = px.line(df_grouped.to_pandas(), x="operation_date", y="avg_normalized_value",
              title="Tendencia Normalizada de Operaciones por Fecha",
              labels={"operation_date": "Fecha", "avg_normalized_value": "Valor Normalizado"})

st.plotly_chart(fig)
