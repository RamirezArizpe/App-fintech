import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px

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
            
            # Mostrar análisis gráfico e insights
            mostrar_analisis(df)
            
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

# Función para mostrar gráficos y análisis visual
def mostrar_analisis(df):
    st.title("Análisis Gráfico e Insights de tus Finanzas")

    # Crear un contenedor con dos columnas: una para las gráficas y otra para el texto
    col1, col2 = st.columns([2, 1])

    with col1:
        # Convertir la columna 'Fecha de transacción' a formato de fecha
        df['Fecha'] = pd.to_datetime(df['Fecha de transacción'])

        # Filtro para seleccionar mes o total
        opcion_mes = st.selectbox("Selecciona un mes o Total", ["Total"] + list(df['Fecha'].dt.to_period('M').unique().astype(str)))

        if opcion_mes == "Total":
            # Gráfico de Ingresos vs Gastos total
            ingresos_total = df[df['Tipo'] == 'Ingreso']['Monto'].sum()
            gastos_total = df[df['Tipo'] == 'Gasto']['Monto'].sum()
            labels = ['Ingresos', 'Gastos']
            values = [ingresos_total, gastos_total]
            fig = plt.figure(figsize=(6, 4))
            plt.bar(labels, values, color=['green', 'red'])
            plt.title("Ingresos vs Gastos Total")
            plt.ylabel("Monto en Pesos")
            st.pyplot(fig)
        else:
            # Filtro dinámico por mes
            df_mes = df[df['Fecha'].dt.to_period('M').astype(str) == opcion_mes]
            ingresos_mes = df_mes[df_mes['Tipo'] == 'Ingreso']['Monto'].sum()
            gastos_mes = df_mes[df_mes['Tipo'] == 'Gasto']['Monto'].sum()
            labels = ['Ingresos', 'Gastos']
            values = [ingresos_mes, gastos_mes]
            fig = plt.figure(figsize=(6, 4))
            plt.bar(labels, values, color=['green', 'red'])
            plt.title(f"Ingresos vs Gastos - {opcion_mes}")
            plt.ylabel("Monto en Pesos")
            st.pyplot(fig)

        # Gráfico de tendencias de ingresos y gastos
        st.write("### Tendencias de Ingresos y Gastos a lo largo del tiempo")
        # Agrupar los datos por mes y año
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
        # Mostrar insights de los datos
        st.write("### Insights:")
        
        total_ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].sum()
        total_gastos = df[df['Tipo'] == 'Gasto']['Monto'].sum()
        balance = total_ingresos - total_gastos
        promedio_ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].mean()
        promedio_gastos = df[df['Tipo'] == 'Gasto']['Monto'].mean()

        st.write(f"- **Total de Ingresos**: ${total_ingresos:.2f}")
        st.write(f"- **Total de Gastos**: ${total_gastos:.2f}")

        # Calcular la proporción de gastos sobre ingresos
        if total_ingresos > 0:
            proporcion_gastos = total_gastos / total_ingresos
        else:
            proporcion_gastos = 0  # Si no hay ingresos, la proporción será 0

        st.write(f"- **Proporción de Gastos sobre Ingresos**: {proporcion_gastos:.2%}")

        # Alertas si la proporción de gastos es alta
        if proporcion_gastos > 0.7:
            st.warning("🚨 Alerta: La proporción de tus gastos sobre ingresos es alta (>70%). Revisa tus gastos.")
        
        st.write(f"- **Balance Neto**: ${balance:.2f}")
        st.write(f"- **Promedio de Ingresos**: ${promedio_ingresos:.2f}")
        st.write(f"- **Promedio de Gastos**: ${promedio_gastos:.2f}")

        # Estadísticas de las formas de pago
        formas_pago_counts = df['Forma de pago'].value_counts()
        st.write("### Frecuencia de Formas de Pago:")
        st.write(formas_pago_counts)

# Función para mostrar análisis de necesidad de gastos y potencial de ahorro
def analizar_gastos(df):
    st.title("Análisis de Necesidad de Gastos y Potencial de Ahorro")

    # Filtrar los gastos con valoraciones de 1 a 3 (innecesarios)
    gastos_innecesarios = df[(df['Tipo'] == 'Gasto') & (df['Valoración'] <= 3)]
    
    # Calcular el total de los gastos innecesarios
    total_gastos_innecesarios = gastos_innecesarios['Monto'].sum()
    
    # Calcular el total de todos los gastos
    total_gastos = df[df['Tipo'] == 'Gasto']['Monto'].sum()

    # Mostrar los resultados
    st.write(f"- **Total de Gastos**: ${total_gastos:.2f}")
    st.write(f"- **Total de Gastos Innecesarios**: ${total_gastos_innecesarios:.2f}")
    st.write(f"- **Potencial de Ahorro**: ${total_gastos_innecesarios:.2f}")
    
    # Porcentaje de ahorro potencial
    if total_gastos > 0:
        porcentaje_ahorro = (total_gastos_innecesarios / total_gastos) * 100
    else:
        porcentaje_ahorro = 0
    
    st.write(f"- **Porcentaje del Ahorro Potencial sobre el Total de Gastos**: {porcentaje_ahorro:.2f}%")

    # Alerta si el ahorro potencial es alto
    if porcentaje_ahorro > 20:
        st.warning("🚨 Alerta: Más del 20% de tus gastos podrían ser innecesarios. Revisa tus hábitos de gasto.")

# Ejemplo de formato CSV para carga correcta
ejemplo = pd.DataFrame({
    "Descripción": ["Ingreso 1", "Gasto 1", "Ingreso 2", "Gasto 2"],
    "Monto": [1000, 200, 1500, 100],
    "Forma de pago": ["transferencia", "efectivo", "depósito", "efectivo"],
    "Fecha de transacción": ["2024-12-16", "2024-12-16", "2024-12-17", "2024-12-17"],
    "Tipo": ["Ingreso", "Gasto", "Ingreso", "Gasto"]
})

# Opción para descargar el ejemplo como CSV
st.download_button(
    label="Descargar archivo ejemplo",
    data=ejemplo.to_csv(index=False),
    file_name="ejemplo_finanzas_personales.csv",
    mime="text/csv"
)

# Inyectar CSS personalizado para cambiar el color y el grosor del slider y el estilo de los botones
st.markdown("""
    <style>
        /* Cambiar color y grosor del slider */
        .stSlider .st-bw {
            width: 100%;
            height: 12px; /* Hacer el slider más grueso */
            background-color: #001f3d; /* Azul marino */
        }
        .stSlider .st-bw .st-cb {
            background-color: #FFFFFF; /* Color blanco para el botón del slider */
        }

        /* Cambiar estilo de los botones a pills moradas */
        .stButton > button {
            background-color: #6a0dad; /* Morado */
            color: white;
            border-radius: 20px;
            font-size: 18px;
        }
        .stButton > button:hover {
            background-color: #5a009d; /* Morado más oscuro */
        }
    </style>
""", unsafe_allow_html=True)

# Interfaz de entrada para agregar datos
st.title("Registro de Movimiento Financiero")
opcion = st.selectbox("Selecciona una opción", ["Cargar archivo CSV", "Ingresar datos manualmente"])

if opcion == "Cargar archivo CSV":
    cargar_csv()
else:
    # Ingreso manual de datos
    descripcion = st.text_input("Descripción")
    monto = st.number_input("Monto", min_value=0.01, step=0.01)
    forma_pago = st.selectbox("Forma de pago", formas_pago)
    tipo = st.radio("Tipo de Movimiento", ("Ingreso", "Gasto"))
    fecha_transaccion = st.date_input("Fecha de transacción", min_value=datetime(2000, 1, 1), max_value=datetime.today())
    valoracion = st.slider("Valoración de la Necesidad (1: Muy innecesario, 5: Muy necesario)", 1, 5, 3)

    if st.button("Registrar movimiento"):
        # Crear un DataFrame para agregar los datos
        nuevo_registro = pd.DataFrame({
            "Descripción": [descripcion],
            "Monto": [monto],
            "Forma de pago": [forma_pago],
            "Fecha de transacción": [fecha_transaccion],
            "Tipo": [tipo],
            "Valoración": [valoracion]
        })

        # Guardar el nuevo registro en un archivo CSV (actualiza el archivo existente)
        nuevo_registro.to_csv("finanzas_personales.csv", mode='a', header=False, index=False)
        st.success("Movimiento registrado exitosamente!")
