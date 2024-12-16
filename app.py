import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Agregar el logo al encabezado
st.image("https://raw.githubusercontent.com/RamirezArizpe/App-fintech/main/encabezado%20app.jpg", width=4000)

# Lista inicial de formas de pago
formas_pago = ['transferencia', 'depósito', 'efectivo']

# Función para agregar forma de pago si no está en la lista
def agregar_forma_pago(pago):
    if pago not in formas_pago:
        formas_pago.append(pago)
        st.write(f"Forma de pago '{pago}' añadida a la lista.")
    else:
        st.write(f"La forma de pago '{pago}' ya está en la lista.")

# Función para cargar datos desde un archivo CSV
def cargar_csv():
    archivo = st.file_uploader("Cargar archivo CSV", type=["csv"])
    if archivo:
        try:
            df = pd.read_csv(archivo)
            st.write("Datos cargados exitosamente:")
            st.write(df)
            mostrar_analisis(df)
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

# Función para mostrar gráficos y análisis visual
def mostrar_analisis(df):
    st.title("Análisis Gráfico e Insights de tus Finanzas")
    # Convertir la columna 'Fecha de transacción' a formato de fecha
    df['Fecha'] = pd.to_datetime(df['Fecha de transacción'])

    # Selección de mes o total
    opcion_mes = st.selectbox("Selecciona un mes o Total", ["Total"] + list(df['Fecha'].dt.to_period('M').unique().astype(str)))

    col1, col2 = st.columns([2, 1])

    with col1:
        # Gráfico de Ingresos vs Gastos
        if opcion_mes == "Total":
            ingresos_total = df[df['Tipo'] == 'Ingreso']['Monto'].sum()
            gastos_total = df[df['Tipo'] == 'Gasto']['Monto'].sum()
        else:
            df_mes = df[df['Fecha'].dt.to_period('M').astype(str) == opcion_mes]
            ingresos_total = df_mes[df_mes['Tipo'] == 'Ingreso']['Monto'].sum()
            gastos_total = df_mes[df_mes['Tipo'] == 'Gasto']['Monto'].sum()

        labels = ['Ingresos', 'Gastos']
        values = [ingresos_total, gastos_total]
        fig = plt.figure(figsize=(6, 4))
        plt.bar(labels, values, color=['green', 'red'])
        plt.title(f"Ingresos vs Gastos - {opcion_mes}")
        plt.ylabel("Monto en Pesos")
        st.pyplot(fig)

        # Gráfico de tendencias de ingresos y gastos
        st.write("### Tendencias de Ingresos y Gastos a lo largo del tiempo")
        df['Mes'] = df['Fecha'].dt.to_period('M')
        ingresos_tendencia = df[df['Tipo'] == 'Ingreso'].groupby('Mes')['Monto'].sum()
        gastos_tendencia = df[df['Tipo'] == 'Gasto'].groupby('Mes')['Monto'].sum()

        fig_tendencia = plt.figure(figsize=(8, 5))
        plt.plot(ingresos_tendencia.index.astype(str), ingresos_tendencia, label='Ingresos', color='green', marker='o')
        plt.plot(gastos_tendencia.index.astype(str), gastos_tendencia, label='Gastos', color='red', marker='o')
        plt.xlabel("Mes")
        plt.ylabel("Monto en Pesos")
        plt.title("Tendencia de Ingresos y Gastos")
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig_tendencia)

    with col2:
        # Insights de los datos
        total_ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].sum()
        total_gastos = df[df['Tipo'] == 'Gasto']['Monto'].sum()
        balance = total_ingresos - total_gastos
        promedio_ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].mean()
        promedio_gastos = df[df['Tipo'] == 'Gasto']['Monto'].mean()

        st.write(f"- **Total de Ingresos**: ${total_ingresos:.2f}")
        st.write(f"- **Total de Gastos**: ${total_gastos:.2f}")
        proporcion_gastos = total_gastos / total_ingresos if total_ingresos > 0 else 0
        st.write(f"- **Proporción de Gastos sobre Ingresos**: {proporcion_gastos:.2%}")
        if proporcion_gastos > 0.7:
            st.warning("🚨 Alerta: La proporción de tus gastos sobre ingresos es alta (>70%). Revisa tus gastos.")
        st.write(f"- **Balance Neto**: ${balance:.2f}")
        st.write(f"- **Promedio de Ingresos**: ${promedio_ingresos:.2f}")
        st.write(f"- **Promedio de Gastos**: ${promedio_gastos:.2f}")
        
        formas_pago_counts = df['Forma de pago'].value_counts()
        st.write("### Frecuencia de Formas de Pago:")
        st.write(formas_pago_counts)

        # Inicializar listas en el estado de la sesión si no existen
if 'transacciones_ingresos' not in st.session_state:
    st.session_state['transacciones_ingresos'] = []
if 'transacciones_gastos' not in st.session_state:
    st.session_state['transacciones_gastos'] = []
if 'formas_pago' not in st.session_state:
    st.session_state['formas_pago'] = ['Efectivo', 'Tarjeta', 'Transferencia']
# Convertir listas a DataFrames
df_ingresos = pd.DataFrame(st.session_state['transacciones_ingresos'])
df_gastos = pd.DataFrame(st.session_state['transacciones_gastos'])
# Función para registrar un ingreso o gasto

# Graficar Gastos por Categoría
st.subheader('Gastos por Categoría')
fig, ax = plt.subplots()
if not df_gastos.empty:
    df_gastos.groupby('Descripción')['Monto'].sum().plot(kind='bar', ax=ax)
ax.set_title('Gastos por Categoría')
ax.set_xlabel('Categoría')
ax.set_ylabel('Monto')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

# Graficar Ingresos por Categoría
st.subheader('Ingresos por Categoría')
fig, ax = plt.subplots()
if not df_ingresos.empty:
    df_ingresos.groupby('Descripción')['Monto'].sum().plot(kind='bar', color="purple", ax=ax)
ax.set_title('Ingresos por Categoría')
ax.set_xlabel('Categoría')
ax.set_ylabel('Monto')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

def registrar_transaccion(tipo):
    st.title(f"Registrar {tipo}")
    descripcion = st.text_input(f"Descripción del {tipo.lower()}")
    monto = st.number_input("Monto en pesos mexicanos", min_value=0.0)
    pago = st.selectbox("Forma de pago", formas_pago)
    fecha = st.date_input("Fecha de transacción", datetime.today())

    if tipo == "Gasto":
        valoracion = st.slider("¿Qué tan necesario fue este gasto?", min_value=1, max_value=6, step=1)
        st.markdown("""<p style="font-size: 14px; color: #333; font-style: italic;">1 = Totalmente innecesario, 6 = Totalmente necesario</p>""", unsafe_allow_html=True)

    if st.button(f"Registrar {tipo}"):
        fecha_str = fecha.strftime('%Y-%m-%d')
        if tipo == "Ingreso":
            st.write(f"Ingreso registrado: Descripción: {descripcion}, Monto: {monto}, Forma de pago: {pago}, Fecha: {fecha_str}")
        elif tipo == "Gasto":
            st.write(f"Gasto registrado: Descripción: {descripcion}, Monto: {monto}, Forma de pago: {pago}, Fecha: {fecha_str}, Valoración: {valoracion}")

# Función principal que permite elegir entre ingresar manualmente o cargar CSV
def app():
    st.title("¿Qué deseas registrar?")
    opcion = st.radio("Selecciona cómo deseas registrar tus datos", ["Ingreso Manual", "Carga desde CSV"])

    if opcion == "Ingreso Manual":
        transaccion = st.radio("¿Qué deseas registrar?", ["Ingreso", "Gasto"])
        registrar_transaccion(transaccion)
    
    elif opcion == "Carga desde CSV":
        cargar_csv()

# Inyectar CSS personalizado para cambiar el estilo de los elementos
st.markdown("""
    <style>
        .stSlider .st-bw {
            width: 100%;
            height: 12px;
            background-color: #001f3d;
        }
        .stSlider .st-bw .st-cb {
            background-color: #FFFFFF;
        }
        .stButton > button {
            background-color: #6a1b9a;
            color: white;
            border-radius: 50px;
            font-size: 16px;
            padding: 10px 20px;
            border: none;
        }
        .stButton > button:hover {
            background-color: #9c4dcc;
        }
        .stRadio label {
            background-color: #6a1b9a;
            color: white;
            border-radius: 50px;
            font-size: 16px;
            padding: 8px 20px;
        }
    </style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    app()
