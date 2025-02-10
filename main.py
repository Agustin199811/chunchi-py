import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import re
import locale

# Cargar datos
df = pd.read_csv("output_data.csv")


# Configurar el idioma a español
#locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")  # Para sistemas Linux/macOS
locale.setlocale(locale.LC_TIME, "Spanish_Spain.1252")  # Para Windows

# Limpiar la columna de fechas
df["Fecha y Hora de actualización"] = df["Fecha y Hora de actualización"].apply(
    lambda x: re.sub(r"^\w+, ", "", str(x))  # Elimina "viernes, ", "lunes, " etc.
)
df["Fecha y Hora de actualización"] = df["Fecha y Hora de actualización"].str.replace("–", "-")  # Normaliza separador
# Eliminar cualquier texto adicional como "Informe No. 10"
df["Fecha y Hora de actualización"] = df["Fecha y Hora de actualización"].apply(
    lambda x: re.sub(r"Informe No\. \d+", "", str(x)).strip()
)

# Intentar convertir con formato en español
df["Fecha y Hora de actualización"] = pd.to_datetime(
    df["Fecha y Hora de actualización"], 
    format="%d de %B de %Y - %H:%M:%S",  
    errors="coerce"
)
# Intentar convertir con formato en español
df["Fecha y Hora de actualización"] = pd.to_datetime(
    df["Fecha y Hora de actualización"], 
    format="%d de %B de %Y - %H:%M:%S",  
    errors="coerce"
)

print(df["Fecha y Hora de actualización"].head(10))  # Verificar si ya se convierte correctamente

# Título del dashboard con estilo personalizado
st.markdown(
    """
    <h1 style='text-align: center; color: #2c3e50; font-family: Arial, sans-serif; font-size: 36px;'>
        📊 Dashboard del Deslave en Chunchi
    </h1>
    <hr style='border: 2px solid #2c3e50;'>
    """,
    unsafe_allow_html=True
)

# Ordenar datos por fecha
df = df.sort_values("Fecha y Hora de actualización")

# Línea de tiempo
timeline_fig = px.scatter(
    df, 
    x="Fecha y Hora de actualización", 
    y=[1] * len(df),  # Todos los puntos en y=1
    title="Línea de Tiempo del Deslave: Eventos Registrados",  # Título mejorado
    labels={"x": "Fecha y Hora de Actualización", "y": ""},  # Etiquetas más claras
    text=df["Archivo"]  # Mostrar el nombre del archivo como texto
)

# Personalizar la línea de tiempo
timeline_fig.update_traces(
    mode="lines+markers",  # Mostrar líneas y puntos
    marker=dict(size=12, color="blue", symbol="circle"),  # Tamaño, color y forma del punto
    line=dict(color="blue", width=2),  # Color y grosor de la línea
    textposition="top center"  # Posición del texto
)

# Ocultar líneas de fondo y eje Y
timeline_fig.update_layout(
    showlegend=False,  # Ocultar leyenda
    xaxis_title="Fecha y Hora de Actualización",  # Título del eje X
    yaxis_title="",  # Ocultar título del eje Y
    yaxis_showticklabels=False,  # Ocultar etiquetas del eje Y
    plot_bgcolor="white",  # Fondo blanco
    xaxis=dict(showgrid=False),  # Ocultar cuadrícula del eje X
    yaxis=dict(showgrid=False, zeroline=False),  # Ocultar cuadrícula y línea cero del eje Y
    title={
        "text": "Línea de Tiempo del Deslave: Eventos Registrados",
        "y": 0.95,  # Posición vertical del título
        "x": 0.5,   # Posición horizontal del título (centrado)
        "xanchor": "center",  # Anclaje del título
        "yanchor": "top",     # Anclaje vertical
        "font": {"size": 20, "family": "Arial", "color": "#2c3e50"}  # Estilo de fuente
    }
)

# Mostrar la línea de tiempo
st.plotly_chart(timeline_fig)



# Gráfico de barras: Viviendas, Personas, Damnificados y Animales afectados
fig_barras = px.bar(
    df, 
    x="Fecha y Hora de actualización", 
    y=["Viviendas afectadas", "Personas afectadas", "Personas damnificadas", 
       "Animales con afectación", "Animales muertos"],
    title="Impacto del Deslave en Viviendas, Personas y Animales a lo Largo del Tiempo",  # Título mejorado
    labels={"value": "Cantidad", "variable": "Categoría"},
    barmode="group"
)

# Personalizar el diseño del gráfico de barras
fig_barras.update_layout(
    title={
        "text": "Impacto del Deslave en Viviendas, Personas y Animales a lo Largo del Tiempo",
        "y": 0.95,  # Posición vertical del título
        "x": 0.5,   # Posición horizontal del título (centrado)
        "xanchor": "center",  # Anclaje del título
        "yanchor": "top",     # Anclaje vertical
        "font": {"size": 17, "family": "Arial", "color": "#2c3e50"}  # Estilo de fuente
    },
    xaxis_title="Fecha y Hora de Actualización",  # Título del eje X
    yaxis_title="Cantidad",  # Título del eje Y
    plot_bgcolor="white",  # Fondo blanco
    xaxis=dict(showgrid=False),  # Ocultar cuadrícula del eje X
    yaxis=dict(showgrid=False)  # Ocultar cuadrícula del eje Y
)

# Mostrar el gráfico de barras
st.plotly_chart(fig_barras)

# Reemplazar valores NaN por 0 para evitar que falten datos en el gráfico y la tabla
df = df.fillna(0)


# Gráfico de área: Viviendas afectadas y destruidas
fig_viviendas = px.area(
    df,
    x="Fecha y Hora de actualización",
    y=["Viviendas afectadas", "Viviendas destruidas"],
    title="Evolución de Viviendas Afectadas y Destruidas por el Deslave",  # Título mejorado
    labels={"value": "Cantidad", "variable": "Categoría"},
    color_discrete_sequence=["#2ca02c", "#d62728"]  # Colores personalizados
)

# Personalizar el diseño del título
fig_viviendas.update_layout(
    title={
        "text": "Evolución de Viviendas Afectadas y Destruidas por el Deslave",
        "y": 0.95,  # Posición vertical del título
        "x": 0.5,   # Posición horizontal del título (centrado)
        "xanchor": "center",  # Anclaje del título
        "yanchor": "top",     # Anclaje vertical
        "font": {"size": 20, "family": "Arial", "color": "#2c3e50"}  # Estilo de fuente
    }
)

# Mostrar el gráfico
st.plotly_chart(fig_viviendas)

# Calcular el total de animales afectados y muertos
total_afectacion = df["Animales con afectación"].sum()
total_muertos = df["Animales muertos"].sum()

# Obtener el valor más reciente de "Animales con afectación" y "Animales muertos"
total_afectacion = df["Animales con afectación"].dropna().iloc[-1]  # Último valor no nulo
total_muertos = df["Animales muertos"].dropna().iloc[-1]  # Último valor no nulo

# Gráfico de torta: Distribución de animales afectados y muertos
fig_animales = px.pie(
    names=["Animales Afectados", "Animales Muertos"],
    values=[total_afectacion, total_muertos],
    title="Impacto en la Fauna: Animales Afectados vs. Muertos",  # Título mejorado
    color_discrete_sequence=["#17becf", "#e377c2"],  # Colores personalizados
    labels={"value": "Cantidad", "names": "Categoría"}  # Etiquetas más claras
)

# Personalizar el diseño del título
fig_animales.update_layout(
    title={
        "text": "Impacto en la Fauna: Animales Afectados vs. Muertos",
        "y": 0.95,  # Posición vertical del título
        "x": 0.5,   # Posición horizontal del título (centrado)
        "xanchor": "center",  # Anclaje del título
        "yanchor": "top",     # Anclaje vertical
        "font": {"size": 20, "family": "Arial", "color": "#2c3e50"}  # Estilo de fuente
    }
)

# Mostrar el gráfico
st.plotly_chart(fig_animales)

