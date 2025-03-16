import streamlit as st
import polars as pl  
import plotly.express as px
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

st.title("Análisis de Operaciones y Calificación de Usuarios")

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

# Verificar si "operation_value" es numérico y no tiene NaN
if "operation_value" in df_pd.columns:
    df_pd = df_pd[pd.to_numeric(df_pd["operation_value"], errors="coerce").notna()]
    df_pd["operation_value"] = df_pd["operation_value"].astype(float)
else:
    st.error("No se encontró la columna 'operation_value'. No se puede continuar.")
    st.stop()

# Normalizar "operation_value" para análisis temporal
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

# --- Calificación de Usuarios ---
st.subheader("Calificación de Usuarios")

# Verificar si la columna "user_id" existe
if "user_id" in df_pd.columns:
    df_pd = df_pd.dropna(subset=["user_id"])  # Eliminar usuarios nulos
    df_pd["user_id"] = df_pd["user_id"].astype(str)  # Convertir a string

    # Cálculo de métricas por usuario (sin normalizar)
    user_metrics = df_pd.groupby("user_id").agg(
        frequency=("operation_value", "count"),  # Número de transacciones
        avg_amount=("operation_value", "mean"),  # Monto promedio
        std_dev=("operation_value", "std"),  # Variabilidad en el monto
        activity_days=("operation_date", lambda x: (x.max() - x.min()).days),  # Días de actividad
    ).fillna(0)  # Llenar NaN con 0

    # Pesos de las métricas
    weights = {
        "frequency": 0.3,
        "avg_amount": 0.25,
        "std_dev": 0.2,
        "activity_days": 0.25,
    }

    # Calcular puntaje final sin normalización
    user_metrics["final_score"] = (
        user_metrics["frequency"] * weights["frequency"] +
        user_metrics["avg_amount"] * weights["avg_amount"] +
        (1 - user_metrics["std_dev"]) * weights["std_dev"] +  # Menos variabilidad es mejor
        user_metrics["activity_days"] * weights["activity_days"]
    )

    # Categorizar usuarios con nuevos umbrales (ajustados según los datos sin normalizar)
    def categorize(score):
        if score >= user_metrics["final_score"].quantile(0.75):
            return "Buen Usuario"
        elif score >= user_metrics["final_score"].quantile(0.5):
            return "Usuario Promedio"
        else:
            return "Usuario de Riesgo"

    user_metrics["category"] = user_metrics["final_score"].apply(categorize)

    # Mostrar tabla de métricas
    st.dataframe(user_metrics)

    # Mostrar distribución de puntajes
    st.subheader("Distribución de Puntajes")
    st.bar_chart(user_metrics["final_score"])
else:
    st.warning("No se encontró la columna 'user_id' en los datos. No se puede calcular la calificación de usuarios.")
