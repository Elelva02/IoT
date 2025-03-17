import streamlit as st
import polars as pl  
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

st.title("Análisis de Operaciones y Calificación de Usuarios")

# Cargar datos con Polars
df = pl.read_excel('depositos_oinks.xlsx')

# Mostrar tabla

st.dataframe(df.head(50))