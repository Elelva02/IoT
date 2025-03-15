import streamlit as st
import polars as pl
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

st.title("Tendencia de Operaciones por Fecha")

# Cargar el DataFrame desde el archivo Excel
df = pl.read_excel('depositos_oinks.xlsx')

# Convertir a pandas y asegurarse de que operation_date sea tipo fecha
df_pd = df.to_pandas()
df_pd["operation_date"] = pd.to_datetime(df_pd["operation_date"], errors="coerce")

# Agrupar por fecha y calcular la media de operation_value
df_grouped = df_pd.groupby("operation_date", as_index=False)["operation_value"].mean()

# Verificar si hay datos antes de normalizar
if not df_grouped.empty:
    # Normalizar los valores de operación
    scaler = MinMaxScaler()
    df_grouped["normalized_operation_value"] = scaler.fit_transform(df_grouped[["operation_value"]])

    # Crear el gráfico con Plotly
    fig = px.line(df_grouped, x="operation_date", y="normalized_operation_value",
                  title="Tendencia Normalizada de Operaciones por Fecha",
                  labels={"operation_date": "Fecha", "normalized_operation_value": "Valor Normalizado"})

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True, key="tendencia_fecha")
else:
    st.warning("No hay datos disponibles para graficar.")
