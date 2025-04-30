import streamlit as st
import polars as pl
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Análisis de Depósitos y Consignaciones", layout="wide")
st.title("Análisis de Depósitos y Consignaciones")

# Cargar datos con Polars
df = pl.read_excel('depositos_oinks.xlsx')

# Transformar operation value a float
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

st.write("En la sección de Consignaciones de la aplicación Streamlit, el usuario puede interactuar con diferentes herramientas para visualizar y analizar los datos de consignaciones de manera clara y sencilla. Al ingresar a esta sección, el usuario encuentra en la barra lateral un filtro de rango de fechas que le permite seleccionar un periodo específico para el análisis. De manera predeterminada, el rango de fechas incluye todas las fechas disponibles en los datos, pero el usuario puede ajustarlo según sus necesidades. Dentro de la misma barra lateral, también se encuentra la opción de agrupar las consignaciones por día, mes o año. Dependiendo de la selección realizada, los datos se organizarán en diferentes niveles de detalle, permitiendo al usuario visualizar la información de manera más granular o resumida según lo requiera. Una vez definidos los filtros, en la sección principal de la aplicación se muestra una tabla con las consignaciones agrupadas según el periodo seleccionado. La tabla está compuesta por dos columnas: una que indica la fecha o periodo correspondiente (día, mes o año) y otra que muestra el total de consignaciones sumadas para ese periodo. Acompañando la tabla, se presenta un gráfico de barras interactivo que permite visualizar las consignaciones de manera más intuitiva. En el eje X del gráfico se encuentra la fecha o periodo seleccionado, mientras que en el eje Y se representa el total de consignaciones. Cada barra indica el total de consignaciones en un periodo específico, y al interactuar con el gráfico, el usuario puede ver detalles específicos como los valores exactos de cada consignación. El flujo de interacción del usuario en esta sección es sencillo y eficiente. Al abrir la aplicación, el usuario accede a la sección de Consignaciones y selecciona el rango de fechas deseado. Luego, elige el nivel de agrupación adecuado (día, mes o año). Inmediatamente, la aplicación actualiza la tabla con los datos filtrados y genera el gráfico correspondiente. Si el usuario desea realizar un análisis más detallado, puede modificar los filtros en cualquier momento y la aplicación actualizará la información de forma dinámica. Además, la interactividad del gráfico permite explorar los datos de una manera más visual y comprensible, facilitando la toma de decisiones basada en los patrones observados. En la interfaz, la barra lateral contiene las opciones de selección de rango de fechas y agrupación. La sección principal muestra primero la tabla con los datos y luego el gráfico de barras interactivo. Esta distribución permite que el usuario pueda analizar la información de manera estructurada, primero observando los valores en la tabla y luego validando las tendencias mediante la representación visual del gráfico."
)

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

st.write("En la sección de Usuarios con Más Depósitos de la aplicación Streamlit, el usuario puede visualizar de manera clara y ordenada a los usuarios que han realizado los mayores depósitos. La aplicación presenta inicialmente una tabla donde se listan los usuarios ordenados de mayor a menor según el total de sus depósitos. Esta tabla está compuesta por dos columnas: una que muestra el identificador único del usuario y otra con la suma total de los valores de depósitos realizados por cada usuario. Acompañando la tabla, se presenta un gráfico de barras interactivo que permite visualizar de manera intuitiva la distribución de los depósitos entre los principales usuarios. En el eje X del gráfico se encuentran los identificadores de usuario y en el eje Y se representa el total de depósitos. Cada barra indica el monto total de depósitos de un usuario, y al interactuar con el gráfico, el usuario puede ver detalles específicos, como el valor exacto de cada depósito. Para personalizar la información mostrada, la aplicación ofrece un filtro que permite seleccionar cuántos usuarios se desean visualizar en el ranking de los principales depositantes. A través de un control deslizante, el usuario puede elegir mostrar el top 5, 10, 20 o 50 usuarios con más depósitos. Una vez seleccionado el número de usuarios deseado, la aplicación actualiza la tabla y el gráfico de manera dinámica, mostrando solo la información relevante según la configuración elegida. El flujo de interacción del usuario en esta sección es simple y eficiente. Al acceder a la aplicación, se muestra la tabla con todos los usuarios y sus depósitos totales, junto con un gráfico de barras que representa estos datos visualmente. Si el usuario desea enfocarse en un grupo específico de usuarios, puede ajustar el control deslizante para filtrar la información y visualizar solo los usuarios que se encuentran en el top seleccionado. La actualización inmediata de la tabla y el gráfico permite un análisis rápido y preciso de los patrones de depósitos. La interfaz está diseñada para facilitar la exploración de los datos, con la tabla de depósitos ubicada en la sección principal y el gráfico interactivo justo debajo para complementar la información de manera visual. El control deslizante se encuentra en una posición accesible, permitiendo modificar rápidamente la selección sin interrumpir el flujo de análisis.")
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