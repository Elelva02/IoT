import streamlit as st
import polars as pl  
import plotly.express as px

st.set_page_config(page_title="Ranking de Usuarios", layout="wide")

st.title("🏆 Mejores Usuarios por Monto Depositado")

# Leer el archivo directamente (asegúrate de tener el archivo en el mismo directorio)
df = pl.read_excel('depositos_oinks.xlsx')

# Agrupar por user_id y sumar los montos depositados
ranking_df = df.groupby("user_id").agg([
    pl.col("operation_value").sum().alias("total_depositado"),
    pl.count().alias("cantidad_operaciones")
]).sort("total_depositado", descending=True)

# Mostrar el ranking en tabla
st.subheader("Top 10 Usuarios que Más Han Depositado")
st.dataframe(ranking_df.head(10))

# Gráfico de barras para los 10 mejores usuarios
top_usuarios = ranking_df.head(10).to_pandas()

fig = px.bar(top_usuarios,
             x="user_id",
             y="total_depositado",
             title="Top 10 Usuarios por Total Depositado",
             labels={"user_id": "Usuario", "total_depositado": "Monto Total"},
             text="total_depositado")

fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

st.plotly_chart(fig, use_container_width=True)
