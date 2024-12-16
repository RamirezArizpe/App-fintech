import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
        if proporcion_gastos > 0.8:
            st.warning("🚨 Alerta: La proporción de tus gastos sobre ingresos es alta (>80%). Revisa tus gastos.")
        
        st.write(f"- **Balance Neto**: ${balance:.2f}")
        st.write(f"- **Promedio de Ingresos**: ${promedio_ingresos:.2f}")
        st.write(f"- **Promedio de Gastos**: ${promedio_gastos:.2f}")

        # Estadísticas de las formas de pago
        formas_pago_counts = df['Forma de pago'].value_counts()
        st.write("### Frecuencia de Formas de Pago:")
        st.write(formas_pago_counts)


# Cargar el CSV y ejecutar el análisis
def app():
    # Ejemplo de dataframe para pruebas
    df = pd.DataFrame({
        "Descripción": ["Ingreso 1", "Gasto 1", "Ingreso 2", "Gasto 2"],
        "Monto": [1000, 200, 1500, 100],
        "Forma de pago": ["transferencia", "efectivo", "depósito", "efectivo"],
        "Fecha de transacción": ["2024-12-16", "2024-12-16", "2024-12-17", "2024-12-17"],
        "Tipo": ["Ingreso", "Gasto", "Ingreso", "Gasto"]  # Columna Tipo para diferenciar
    })
    
    # Convertir la columna 'Fecha de transacción' a formato de fecha
    df['Fecha'] = pd.to_datetime(df['Fecha de transacción'])

    # Llamar a la función para mostrar análisis
    mostrar_analisis(df)
    
    st.write("Ejemplo de formato CSV para carga correcta: (no escribas acentos ni caractéres especiales)")
    st.write(ejemplo)
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
            background-color: #6a1b9a;  /* Morado */
            color: white;
            border-radius: 50px; /* Hacerlo "pill" */
            font-size: 16px;
            padding: 10px 20px;
            border: none;
        }
        .stButton > button:hover {
            background-color: #9c4dcc;  /* Morado más claro al pasar el ratón */
        }

        /* Cambiar el estilo del radio button */
        .stRadio > div {
            display: flex;
            flex-direction: row;
            justify-content: space-around;
        }

        /* Cambiar el estilo de las opciones del radio button a pills moradas */
        .stRadio label {
            background-color: #6a1b9a;
            color: white;
            border-radius: 50px;
            font-size: 16px;
            padding: 8px 20px;
        }

        .stRadio input:checked + label {
            background-color: #9c4dcc; /* Morado más claro cuando se selecciona */
        }

        /* Estilo de los radio buttons */
        .stRadio .st-bw {
            color: white; /* Color de texto blanco en los botones */
        }

        /* Sin fondo para la pregunta */
        .stTitle, .stSubheader, .stMarkdown {
            background: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Función para registrar un ingreso o un gasto
def registrar_transaccion(tipo):
    st.title(f"Registrar {tipo}")

    # Campos comunes para ingreso y gasto
    descripcion = st.text_input(f"Descripción del {tipo.lower()}")
    monto = st.number_input("Monto en pesos mexicanos", min_value=0.0)
    pago = st.selectbox("Forma de pago", formas_pago)
    fecha = st.date_input("Fecha de transacción", datetime.today())

    # Si es un gasto, añadir valoración de necesidad
    if tipo == "Gasto":
        valoracion = st.slider(
            "¿Qué tan necesario fue este gasto?", 
            min_value=1, 
            max_value=5, 
            value=3, 
            step=1,
            help="1 es 'muy necesario', 5 es 'no necesario en absoluto'."
        )

    if st.button(f"Guardar {tipo}"):
        # Aquí agregarías código para guardar la transacción
        st.success(f"{tipo} registrado con éxito.")
        st.write(f"Descripción: {descripcion}, Monto: ${monto}, Pago: {pago}, Fecha: {fecha}")


# Ejecutar la aplicación
app()
