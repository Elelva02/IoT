import streamlit as st
import polars as pl  
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

st.title("Visualización de Ejemplo")

# Cargar datos
data = pl.read_excel('depositos_oinks.xlsx')
df = pl.DataFrame(data)

# Convertir a pandas para procesamiento
df_pd = df.to_pandas()

# Normalizar el campo "operation_value"
scaler = MinMaxScaler()
df_pd["normalized_operation_value"] = scaler.fit_transform(df_pd[["operation_value"]])

# Agrupar por user_id y calcular la media (si es necesario)
df_grouped = df_pd.groupby("user_id", as_index=False).mean()

st.subheader("Gráfico mejorado con Plotly")

# Crear gráfico de dispersión
fig = px.scatter(df_grouped, x="user_id", y="normalized_operation_value",
                 title="Valor Normalizado de Operaciones por Usuario",
                 labels={"user_id": "User ID", "normalized_operation_value": "Normalized Operation Value"})

st.plotly_chart(fig)
