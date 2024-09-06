import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


st.set_page_config(layout="wide", page_title="Dashboard PISA", page_icon=":factory:")

COLOR_AZUL = "#3498db"
COLOR_VERDE = "#2ecc71"
COLOR_NARANJA = "#e67e22"
COLOR_ROJO = "#e74c3c"
COLOR_GRIS = "#95a5a6"

@st.cache_data
def cargar_datos():
    clientes_df = pd.read_csv('/Users/claudiogonzalezarriaga/Documents/Progra_Tec/QuintoSemestre/Optimizacion Estocastica/Reto pisa markov/Markov_chain_prediction_model/csv_clientes.csv')
    materiales_df = pd.read_csv('/Users/claudiogonzalezarriaga/Documents/Progra_Tec/QuintoSemestre/Optimizacion Estocastica/Reto pisa markov/Markov_chain_prediction_model/csv_materiales.csv')
    return clientes_df, materiales_df

clientes_df, materiales_df = cargar_datos()

# Función para crear gráfico de matriz de transición
def grafico_matriz_transicion(matriz):
    labels = ['Activo', 'Inactivo']
    valores = [matriz[0][0], matriz[0][1]]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=valores, hole=.3, marker_colors=[COLOR_AZUL, COLOR_NARANJA])])
    fig.update_layout(
        title_text="Probabilidades de Transición",
        annotations=[dict(text='Transición', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    return fig

# visualizacion del tiempo medio de recurrencia (mu_j)
def grafico_tiempo_recurrencia(mu_j):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = mu_j,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Tiempo Medio de Recurrencia (mu_j)"},
        gauge = {
            'axis': {'range': [1, 5], 'tickwidth': 1},
            'bar': {'color': COLOR_AZUL},
            'steps': [
                {'range': [1, 2], 'color': COLOR_VERDE},
                {'range': [2, 3], 'color': COLOR_NARANJA},
                {'range': [3, 5], 'color': COLOR_ROJO}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': mu_j}}))
    fig.update_layout(height=400)
    return fig

# Estilo CSS personalizado
st.markdown(f"""
    <style>
    .main {{
        background-color: #151d26;
    }}
    .stApp {{
        max-width: 1200px;
        margin: 0 auto;
    }}
    .dataframe {{
        font-size: 12px;
    }}
    .st-emotion-cache-1wivap2 {{
        background-color: {COLOR_AZUL};
    }}
    .st-emotion-cache-1wivap2:hover {{
        background-color: {COLOR_VERDE};
    }}
    .info-box {{
        background-color: #0d1a1f;
        border-left: 5px solid {COLOR_AZUL};
        padding: 10px;
        margin-bottom: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# Encabezado
st.title('🏭 Dashboard de Análisis de Datos PISA')
st.markdown('---')

# Barra lateral
st.sidebar.title('Búsqueda')
opcion_busqueda = st.sidebar.radio("Buscar por:", ('Material', 'ID de Cliente'))

if opcion_busqueda == 'Material':
    nombre_material = st.sidebar.text_input("Ingrese el Nombre del Material:")
    if nombre_material:
        datos_material = materiales_df[materiales_df['Material'] == nombre_material]
        if not datos_material.empty:
            st.header(f"Datos del Material: {nombre_material}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Información General")
                fig = go.Figure(data=[go.Table(
                    header=dict(values=list(datos_material.columns),
                                fill_color=COLOR_AZUL,
                                align='left',
                                font=dict(color='black', size=12)),
                    cells=dict(values=[datos_material[col] for col in datos_material.columns],
                               fill_color='black',
                               align='left'))
                ])
                fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if 'Tabla_Transiciones' in datos_material.columns:
                    st.subheader("Matriz de Transición")
                    st.markdown('<div class="info-box">La matriz de transición muestra la probabilidad de que un material pase de un estado a otro (activo a inactivo o viceversa) en el próximo período.</div>', unsafe_allow_html=True)
                    matriz_transicion = eval(datos_material['Tabla_Transiciones'].values[0])
                    fig = grafico_matriz_transicion(matriz_transicion)
                    st.plotly_chart(fig, use_container_width=True)
            
            if 'Claudio (Prob Est.)' in datos_material.columns:
                st.subheader("Probabilidades Estacionarias")
                st.markdown('<div class="info-box">Las probabilidades estacionarias indican la proporción de tiempo que el material pasa en cada estado (activo o inactivo) a largo plazo.</div>', unsafe_allow_html=True)
                prob_estacionarias = eval(datos_material['Claudio (Prob Est.)'].values[0])
                fig = go.Figure(data=[
                    go.Bar(name='Activo', x=['Probabilidad'], y=[prob_estacionarias[0]], marker_color=COLOR_AZUL),
                    go.Bar(name='Inactivo', x=['Probabilidad'], y=[prob_estacionarias[1]], marker_color=COLOR_NARANJA)
                ])
                fig.update_layout(barmode='group')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Material no encontrado.")

elif opcion_busqueda == 'ID de Cliente':
    id_cliente = st.sidebar.text_input("Ingrese el ID del Cliente:")
    if id_cliente:
        datos_cliente = clientes_df[clientes_df['id_cliente'] == int(id_cliente)]
        if not datos_cliente.empty:
            st.header(f"Datos del Cliente: {id_cliente}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Información General")
                fig = go.Figure(data=[go.Table(
                    header=dict(values=list(datos_cliente.columns),
                                fill_color=COLOR_AZUL,
                                align='left',
                                font=dict(color='black', size=12)),
                    cells=dict(values=[datos_cliente[col] for col in datos_cliente.columns],
                               fill_color='black',
                               align='left'))
                ])
                fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if 'CLV' in datos_cliente.columns:
                    clv = datos_cliente['CLV'].values[0]
                    st.subheader("Valor de Vida del Cliente (CLV)")
                    st.markdown('<div class="info-box">El CLV (Customer Lifetime Value) es una estimación del valor total que un cliente generará para la empresa durante toda su relación comercial. Un CLV más alto indica un cliente más valioso para PISA.</div>', unsafe_allow_html=True)
                    st.metric("CLV", f"${clv:.2f}")
                    
                    if clv > 500000:
                        st.success("Este es un cliente de alto valor para PISA.")
                    elif clv > 100000:
                        st.info("Este es un cliente de valor medio para PISA.")
                    else:
                        st.warning("Este es un cliente de valor bajo para PISA.")
                    
                    # Gráfico de gauge para CLV
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = clv,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "CLV"},
                        gauge = {
                            'axis': {'range': [0, 1000000], 'tickwidth': 1},
                            'bar': {'color': COLOR_AZUL},
                            'steps': [
                                {'range': [0, 100000], 'color': COLOR_GRIS},
                                {'range': [100000, 500000], 'color': COLOR_NARANJA},
                                {'range': [500000, 1000000], 'color': COLOR_VERDE}],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': clv}}))
                    st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Tiempo Medio de Recurrencia (mu_j)")
            st.markdown('<div class="info-box">El tiempo medio de recurrencia (mu_j) indica el tiempo promedio que transcurre entre compras de un cliente. Un valor más bajo sugiere compras más frecuentes, lo cual es generalmente mejor para el negocio.</div>', unsafe_allow_html=True)
            if 'mu_j' in datos_cliente.columns:
                mu_j = datos_cliente['mu_j'].values[0]
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    st.metric("mu_j", f"{mu_j:.2f}")
                    fig = grafico_tiempo_recurrencia(mu_j)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    if mu_j < 2:
                        st.success("Este cliente tiene una alta frecuencia de compra.")
                    elif mu_j < 3:
                        st.info("Este cliente tiene una frecuencia de compra moderada.")
                    else:
                        st.warning("Este cliente tiene una baja frecuencia de compra.")
        else:
            st.warning("ID de Cliente no encontrado.")

st.sidebar.info("Ingrese un Nombre de Material o ID de Cliente en la barra lateral para ver los datos correspondientes.")

# Pie de página
st.markdown('---')
st.markdown('Desarrollado por EBU Inc para PiSA® Farmacéutica  | Todos los derechos reservados © 2024')
