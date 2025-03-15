import streamlit as st
import polars as pl  
import plotly.express as px
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

st.title("Visualización de Ejemplo")

# Cargar datos con Polars
data = pl.read_excel('depositos_oinks.xlsx')
df = pl.DataFrame(data)

# Convertir a Pandas
df_pd = df.to_pandas()

# Convertir "operation_date" a formato datetime en Pandas
df_pd["operation_date"] = pd.to_datetime(df_pd["operation_date"], errors='coerce')

# Normalizar "operation_value"
scaler = MinMaxScaler()
df_pd["normalized_operation_value"] = scaler.fit_transform(df_pd[["operation_value"]])

# Agrupar por fecha
df_grouped = df_pd.groupby("operation_date", as_index=False)[["normalized_operation_value"]].mean()

# Ordenar por fecha
df_grouped = df_grouped.sort_values(by="operation_date")

st.subheader("Gráfico de Tendencia por Fecha")

# Crear gráfico de líneas
fig = px.line(df_grouped, x="operation_date", y="normalized_operation_value",
              title="Tendencia Normalizada de Operaciones por Fecha",
              labels={"operation_date": "Fecha", "normalized_operation_value": "Valor Normalizado"})

st.plotly_chart(fig)

