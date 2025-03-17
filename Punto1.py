import streamlit as st
import polars as pl
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Análisis de Depósitos y Consignaciones", layout="wide")
st.title("Análisis de Depósitos y Consignaciones")

# Cargar datos con Polars
try:
    df = pl.read_excel('depositos_oinks.xlsx')
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
    st.stop()

# Verificar y corregir el tipo de dato de operation_value
st.write("Valores únicos en operation_value:", df["operation_value"].unique())
df = df.with_columns(
    pl.col("operation_value").cast(pl.Float64, strict=False).fill_null(0)
)

# Verificar que la columna operation_date existe
if 'operation_date' not in df.columns:
    st.error("La columna 'operation_date' no existe en el archivo.")
    st.stop()

# Convertir operation_date a tipo fecha (si no lo está)
df = df.with_columns(
    pl.col("operation_date").cast(pl.Date)
)

# Sidebar para filtros
st.sidebar.header("Filtros")

# Filtro de rango de fechas
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
fig_consignaciones = px.bar(
    df_agrupado.to_pandas(),  # Convertir a Pandas para Plotly
    x="operation_date",
    y="total_consignaciones",
    title=titulo_grafico,
    labels={"operation_date": "Fecha", "total_consignaciones": "Total de Consignaciones"},
    text="total_consignaciones"
)
fig_consignaciones.update_traces(textposition='outside')
st.plotly_chart(fig_consignaciones, use_container_width=True)

# Separador visual
st.markdown("---")

# Análisis de usuarios con más depósitos
st.header("Usuarios con Más Depósitos")

# Agrupar por user_id y sumar operation_value
usuarios_depositos = df_filtrado.group_by("user_id").agg(
    pl.col("operation_value").sum().alias("total_depositos")
).sort("total_depositos", descending=True)

# Filtrar usuarios con total_depositos mayor a 1,000,000
usuarios_depositos_filtrados = usuarios_depositos.filter(
    pl.col("total_depositos") > 1_000_000
)

# Mostrar los usuarios con más depósitos (filtrados)
st.subheader("Top Usuarios con Más Depósitos (Mayores a 1,000,000)")
st.dataframe(usuarios_depositos_filtrados)

# Gráfico de barras: Top usuarios con más depósitos (filtrados)
fig_usuarios_filtrados = px.bar(
    usuarios_depositos_filtrados.to_pandas(),  # Convertir a Pandas para Plotly
    x="user_id",
    y="total_depositos",
    title="Top Usuarios con Más Depósitos (Mayores a 1,000,000)",
    labels={"user_id": "Usuario", "total_depositos": "Total de Depósitos"},
    text="total_depositos"
)
fig_usuarios_filtrados.update_traces(textposition='outside')
st.plotly_chart(fig_usuarios_filtrados, use_container_width=True)

# Filtro para mostrar el top N de usuarios
top_n = st.slider("Selecciona el número de usuarios top a mostrar", min_value=5, max_value=50, value=10)

# Mostrar el top N de usuarios
st.subheader(f"Top {top_n} Usuarios con Más Depósitos")
top_usuarios = usuarios_depositos.head(top_n)
st.dataframe(top_usuarios)

# Gráfico de barras para el top N de usuarios
fig_top_n = px.bar(
    top_usuarios.to_pandas(),  # Convertir a Pandas para Plotly
    x="user_id",
    y="total_depositos",
    title=f"Top {top_n} Usuarios con Más Depósitos",
    labels={"user_id": "Usuario", "total_depositos": "Total de Depósitos"},
    text="total_depositos"
)
fig_top_n.update_traces(textposition='outside')
st.plotly_chart(fig_top_n, use_container_width=True)