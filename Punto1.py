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

# Mostrar la tabla original
st.subheader("Vista previa de los datos originales")
st.dataframe(df_pd.head(50))  # Muestra las primeras 50 filas

# Convertir "operation_date" a formato datetime en Pandas
df_pd["operation_date"] = pd.to_datetime(df_pd["operation_date"], errors='coerce')

# Normalizar "operation_value"
scaler = MinMaxScaler()
df_pd["normalized_operation_value"] = scaler.fit_transform(df_pd[["operation_value"]])

# Agrupar por fecha
df_grouped = df_pd.groupby("operation_date", as_index=False)[["normalized_operation_value"]].mean()

# Ordenar por fecha
df_grouped = df_grouped.sort_values(by="operation_date")

# Mostrar la tabla agrupada
st.subheader("Datos Agrupados y Normalizados")
st.dataframe(df_grouped)

st.subheader("Gráfico de Tendencia por Fecha")

# Crear gráfico de líneas
fig = px.line(df_grouped, x="operation_date", y="normalized_operation_value",
              title="Tendencia Normalizada de Operaciones por Fecha",
              labels={"operation_date": "Fecha", "normalized_operation_value": "Valor Normalizado"})

st.plotly_chart(fig)

# Calcular métricas de usuarios
user_metrics = df_pd.groupby("user_id").agg(
    transaction_count=("operation_value", "count"),
    avg_transaction_value=("operation_value", "mean"),
    max_transaction_value=("operation_value", "max"),
    total_value=("operation_value", "sum")
)

# Normalizar valores
scaler = MinMaxScaler()
user_metrics_normalized = scaler.fit_transform(user_metrics)
user_metrics["final_score"] = user_metrics_normalized.mean(axis=1)

# Mostrar solo los 20 mejores usuarios
top_users = user_metrics.nlargest(20, "final_score")

st.subheader("Top 20 Mejores Usuarios")
fig_top = px.bar(
    top_users,
    x=top_users.index,
    y="final_score",
    title="Top 20 Usuarios con Mejor Puntaje",
    labels={"x": "User ID", "final_score": "Puntaje Final"},
    text_auto=True
)
fig_top.update_layout(xaxis_tickangle=-45)  # Rotar etiquetas para mejor visualización
st.plotly_chart(fig_top)
