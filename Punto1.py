import streamlit as st
import polars as pl  
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

st.title("Análisis de Operaciones y Calificación de Usuarios")

# Cargar datos con Polars
df = pl.read_excel('depositos_oinks.xlsx')

# Mostrar tabla original
st.subheader("Vista previa de los datos originales")
st.dataframe(df.head(50))

# Convertir "operation_date" a formato datetime
df = df.with_columns(pl.col("operation_date").str.to_date("%Y-%m-%d"))

# Verificar si "operation_value" es numérico y limpiar NaN
if "operation_value" in df.columns:
    df = df.with_columns(
        pl.when(pl.col("operation_value").cast(pl.Float64, strict=False).is_not_null())
        .then(pl.col("operation_value").cast(pl.Float64))
        .otherwise(None)  # Si no es numérico, se convierte en NULL
    ).drop_nulls()  # Elimina filas con valores no numéricos en "operation_value"
else:
    st.error("No se encontró la columna 'operation_value'. No se puede continuar.")
    st.stop()

# Normalizar "operation_value"
min_val, max_val = df["operation_value"].min(), df["operation_value"].max()
df = df.with_columns(
    ((pl.col("operation_value") - min_val) / (max_val - min_val)).alias("normalized_operation_value")
)

# Agrupar por fecha y calcular promedio
df_grouped = df.groupby("operation_date").agg(
    pl.col("normalized_operation_value").mean()
).sort("operation_date")

# Mostrar datos normalizados
st.subheader("Datos Agrupados y Normalizados")
st.dataframe(df_grouped)

# Crear gráfico de tendencia por fecha
st.subheader("Gráfico de Tendencia por Fecha")
fig = px.line(df_grouped.to_pandas(), x="operation_date", y="normalized_operation_value",
              title="Tendencia Normalizada de Operaciones por Fecha",
              labels={"operation_date": "Fecha", "normalized_operation_value": "Valor Normalizado"})
st.plotly_chart(fig)

# --- Calificación de Usuarios ---
st.subheader("Calificación de Usuarios")

if "user_id" in df.columns:
    df = df.with_columns(pl.col("user_id").cast(pl.Utf8)).drop_nulls(subset=["user_id"])

    # Calcular métricas por usuario
    user_metrics = df.groupby("user_id").agg([
        pl.count("operation_value").alias("frequency"),
        pl.col("operation_value").mean().alias("avg_amount"),
        pl.col("operation_value").std().alias("std_dev"),
        (pl.col("operation_date").max() - pl.col("operation_date").min()).dt.days().alias("activity_days"),
    ]).fill_null(0)  # Reemplazar NaN con 0

    # Pesos de las métricas
    weights = {"frequency": 0.3, "avg_amount": 0.25, "std_dev": 0.2, "activity_days": 0.25}

    # Calcular puntaje final
    user_metrics = user_metrics.with_columns(
        (
            user_metrics["frequency"] * weights["frequency"]
            + user_metrics["avg_amount"] * weights["avg_amount"]
            + (1 - user_metrics["std_dev"]) * weights["std_dev"]  # Menos variabilidad es mejor
            + user_metrics["activity_days"] * weights["activity_days"]
        ).alias("final_score")
    )

    # Definir categorías basadas en cuantiles
    q75, q50 = user_metrics["final_score"].quantile(0.75), user_metrics["final_score"].quantile(0.5)

    user_metrics = user_metrics.with_columns(
        pl.when(pl.col("final_score") >= q75)
        .then("Buen Usuario")
        .when(pl.col("final_score") >= q50)
        .then("Usuario Promedio")
        .otherwise("Usuario de Riesgo")
        .alias("category")
    )

    # Mostrar tabla de usuarios
    st.dataframe(user_metrics)

    # Mostrar distribución de puntajes
    st.subheader("Distribución de Puntajes")
    st.bar_chart(user_metrics["final_score"])
else:
    st.warning("No se encontró la columna 'user_id' en los datos. No se puede calcular la calificación de usuarios.")
