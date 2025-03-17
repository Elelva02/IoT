import streamlit as st
import polars as pl
import plotly.express as px

# Cargar datos con Polars
try:
    df = pl.read_excel('depositos_oinks.xlsx')
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
    st.stop()

# Verificar que la columna operation_date existe
if 'operation_date' not in df.columns:
    st.error("La columna 'operation_date' no existe en el archivo.")
    st.stop()

# Convertir operation_date a tipo fecha (si no lo está)
df = df.with_columns(
    pl.col("operation_date").cast(pl.Date)
)

# Agregar filtro de rango de fechas
st.sidebar.header("Filtros")
min_date = df["operation_date"].min()
max_date = df["operation_date"].max()
date_range = st.sidebar.date_input(
    "Selecciona el rango de fechas",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Filtrar datos por el rango de fechas seleccionado
df_filtrado = df.filter(
    (pl.col("operation_date") >= date_range[0]) &
    (pl.col("operation_date") <= date_range[1])
)

# Agrupar consignaciones por día, mes o año
st.sidebar.subheader("Agrupar por")
agrupar_por = st.sidebar.radio(
    "Selecciona el período",
    ["Día", "Mes", "Año"]
)

if agrupar_por == "Día":
    df_agrupado = df_filtrado.group_by(pl.col("operation_date")).agg(
        pl.col("operation_value").sum().alias("total_consignaciones")
    ).sort("operation_date")
    titulo_grafico = "Consignaciones por Día"
elif agrupar_por == "Mes":
    df_agrupado = df_filtrado.group_by(pl.col("operation_date").dt.strftime("%Y-%m")).agg(
        pl.col("operation_value").sum().alias("total_consignaciones")
    ).sort("operation_date")
    titulo_grafico = "Consignaciones por Mes"
else:  # Año
    df_agrupado = df_filtrado.group_by(pl.col("operation_date").dt.strftime("%Y")).agg(
        pl.col("operation_value").sum().alias("total_consignaciones")
    ).sort("operation_date")
    titulo_grafico = "Consignaciones por Año"

# Mostrar datos agrupados
st.subheader(f"{titulo_grafico}")
st.dataframe(df_agrupado)

# Crear histograma con Plotly
fig = px.bar(
    df_agrupado,
    x="operation_date",
    y="total_consignaciones",
    title=titulo_grafico,
    labels={"operation_date": "Fecha", "total_consignaciones": "Total de Consignaciones"},
    text="total_consignaciones"
)
fig.update_traces(textposition='outside')
st.plotly_chart(fig, use_container_width=True)