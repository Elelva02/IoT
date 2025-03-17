import streamlit as st
import polars as pl
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Usuarios con Más Depósitos", layout="wide")
st.title("Usuarios con Más Depósitos")

# Cargar datos con Polars
df = pl.read_excel('depositos_oinks.xlsx')

st.write("Valores únicos en operation_value:", df["operation_value"].unique())
# Corregir el tipo de dato de la columna operation_value
df = df.with_columns(
    pl.col("operation_value").cast(pl.Float64, strict=False)
    )


# Agrupar por user_id y sumar operation_value
usuarios_depositos = df.group_by("user_id").agg(
    pl.col("operation_value").sum().alias("total_depositos")
).sort("total_depositos", descending=True)

# Mostrar los usuarios con más depósitos
st.subheader("Top Usuarios con Más Depósitos")
st.dataframe(usuarios_depositos)

# Gráfico de barras: Top usuarios con más depósitos
st.subheader("Gráfico de Usuarios con Más Depósitos")
fig = px.bar(
    usuarios_depositos,
    x="user_id",
    y="total_depositos",
    title="Top Usuarios con Más Depósitos",
    labels={"user_id": "Usuario", "total_depositos": "Total de Depósitos"},
    text="total_depositos"
)
fig.update_traces(textposition='outside')
st.plotly_chart(fig, use_container_width=True)

# Filtro para mostrar el top N de usuarios
top_n = st.slider("Selecciona el número de usuarios top a mostrar", min_value=5, max_value=50, value=10)

# Mostrar el top N de usuarios
st.subheader(f"Top {top_n} Usuarios con Más Depósitos")
top_usuarios = usuarios_depositos.head(top_n)
st.dataframe(top_usuarios)

# Gráfico de barras para el top N de usuarios
fig_top_n = px.bar(
    top_usuarios,
    x="user_id",
    y="total_depositos",
    title=f"Top {top_n} Usuarios con Más Depósitos",
    labels={"user_id": "Usuario", "total_depositos": "Total de Depósitos"},
    text="total_depositos"
)
fig_top_n.update_traces(textposition='outside')
st.plotly_chart(fig_top_n, use_container_width=True)