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

    # Convertir la columna 'Fecha de transacción' a formato de fecha
    df['Fecha'] = pd.to_datetime(df['Fecha de transacción'])
    
    # Gráfico de Ingresos vs Gastos
    fig = plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Tipo', palette="Set2")
    plt.title("Distribución de Ingresos vs Gastos")
    st.pyplot(fig)
    
    # Apartado explicativo
    st.markdown("""
        ### ¿Qué significa este gráfico?
        Este gráfico muestra la distribución de los ingresos y los gastos en tus registros. 
        Cada barra representa la cantidad de transacciones de tipo 'Ingreso' o 'Gasto', lo que te permite ver cuántas veces has registrado cada tipo de transacción.
    """)

    # Gráfico de ingresos y gastos por mes
    df['Mes-Año'] = df['Fecha'].dt.to_period('M')
    ingresos_mes = df[df['Tipo'] == 'Ingreso'].groupby('Mes-Año')['Monto'].sum()
    gastos_mes = df[df['Tipo'] == 'Gasto'].groupby('Mes-Año')['Monto'].sum()

    fig = plt.figure(figsize=(10, 6))
    plt.plot(ingresos_mes.index.astype(str), ingresos_mes, label="Ingresos", marker='o')
    plt.plot(gastos_mes.index.astype(str), gastos_mes, label="Gastos", marker='o')
    plt.title("Ingresos y Gastos Mensuales")
    plt.xlabel("Mes")
    plt.ylabel("Monto en Pesos")
    plt.legend()
    st.pyplot(fig)

    # Apartado explicativo
    st.markdown("""
        ### ¿Qué significa este gráfico?
        Este gráfico muestra la evolución mensual de los ingresos y los gastos. 
        Permite comparar cómo varían tus ingresos y gastos a lo largo del tiempo, ayudándote a identificar tendencias y comportamientos financieros.
    """)

    # Gráfico interactivo de formas de pago (usando Plotly)
    fig = px.pie(df, names='Forma de pago', title='Distribución de Formas de Pago')
    st.plotly_chart(fig)

    # Apartado explicativo
    st.markdown("""
        ### ¿Qué significa este gráfico?
        Este gráfico circular muestra la distribución de las formas de pago utilizadas en tus transacciones. 
        Cada segmento representa el porcentaje de uso de cada forma de pago (transferencia, depósito, efectivo), dándote una visión general de cómo prefieres realizar tus pagos.
    """)

    # Insights de los datos
    st.write("### Insights:")
    
    total_ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].sum()
    total_gastos = df[df['Tipo'] == 'Gasto']['Monto'].sum()
    balance = total_ingresos - total_gastos
    promedio_ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].mean()
    promedio_gastos = df[df['Tipo'] == 'Gasto']['Monto'].mean()

    st.write(f"- **Total de Ingresos**: ${total_ingresos:.2f}")
    st.write(f"- **Total de Gastos**: ${total_gastos:.2f}")
    st.write(f"- **Balance Neto**: ${balance:.2f}")
    st.write(f"- **Promedio de Ingresos**: ${promedio_ingresos:.2f}")
    st.write(f"- **Promedio de Gastos**: ${promedio_gastos:.2f}")

    # Estadísticas de las formas de pago
    formas_pago_counts = df['Forma de pago'].value_counts()
    st.write("### Frecuencia de Formas de Pago:")
    st.write(formas_pago_counts)

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML
import math

# Configuración de estilo para gráficos
sns.set(style="whitegrid")

# Datos simulados (puedes cargar datos reales desde un CSV)
data = {
    'forma_pago': ['Efectivo', 'Tarjeta', 'Transferencia', 'Crédito', 'Otros'],
    'cantidad': [150, 300, 450, 75, 25],
}

# Convertir a DataFrame
df = pd.DataFrame(data)

# Total de transacciones
total_transacciones = df['cantidad'].sum()

# Calcular las proporciones
df['proporcion'] = df['cantidad'] / total_transacciones

# Intervalo de confianza para cada forma de pago
Z = 1.96  # Valor crítico para 95% de confianza

def calcular_ic(p, n):
    error_estandar = math.sqrt((p * (1 - p)) / n)
    intervalo_confianza = Z * error_estandar
    return p - intervalo_confianza, p + intervalo_confianza

# Aplicar cálculo de IC a cada forma de pago
df['IC_inferior'], df['IC_superior'] = zip(*df['proporcion'].apply(lambda p: calcular_ic(p, total_transacciones)))

# Mostrar datos con intervalos de confianza
display(HTML("<h2 style='color: #1DB954;'>Tus Formas de Pago Más Populares</h2>"))
display(df[['forma_pago', 'proporcion', 'IC_inferior', 'IC_superior']])

# Graficar la proporción de cada forma de pago
plt.figure(figsize=(10, 6))
sns.barplot(x='proporcion', y='forma_pago', data=df, palette="viridis")

# Añadir intervalos de confianza como barras
for i, row in df.iterrows():
    plt.plot([row['IC_inferior'], row['IC_superior']], [i, i], color='black', lw=2)

plt.title('Proporción de Formas de Pago con Intervalos de Confianza al 95%', fontsize=14, weight='bold')
plt.xlabel('Proporción de Uso (%)')
plt.ylabel('Forma de Pago')

# Personalización estética
plt.grid(False)
plt.show()

# Mensajes impactantes (basados en insights)
mensaje = f"""
<h3 style='color: #1DB954;'>🔮 Insights Impactantes:</h3>
<ul>
    <li><strong>{df['forma_pago'][df['proporcion'].idxmax()]}</strong> es la forma de pago más utilizada, con un {df['proporcion'].max()*100:.2f}% de las transacciones.</li>
    <li>¡Te sorprendería saber que más del {df['IC_superior'].max()*100:.2f}% de tus transacciones futuras serán probablemente pagadas con la forma más popular!</li>
    <li><strong>La forma de pago menos utilizada</strong> es <strong>{df['forma_pago'][df['proporcion'].idxmin()]}</strong>, con solo un {df['proporcion'].min()*100:.2f}% de las transacciones. ¡Podrías explorar más opciones!</li>
</ul>
"""
display(HTML(mensaje))


# Función para mostrar un ejemplo de archivo CSV
def mostrar_ejemplo_csv():
    # Ejemplo con columna "Tipo" para indicar si es un Ingreso o Gasto
    ejemplo = pd.DataFrame({
        "Descripción": ["Ingreso 1", "Gasto 1", "Ingreso 2", "Gasto 2"],
        "Monto": [1000, 200, 1500, 100],
        "Forma de pago": ["transferencia", "efectivo", "depósito", "efectivo"],
        "Fecha de transacción": ["2024-12-16", "2024-12-16", "2024-12-17", "2024-12-17"],
        "Valoración gasto": [None, 3, None, 4],  # Valoración sólo para gastos
        "Tipo": ["Ingreso", "Gasto", "Ingreso", "Gasto"]  # Columna Tipo para diferenciar
    })
    
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
            max_value=6, 
            step=1
        )
        st.markdown("""
            <style>
                /* Estilo para el texto explicativo */
                .stSlider + .stText {
                    font-size: 14px;
                    color: #333;
                    font-style: italic;
                }
            </style>
            <p style="font-size: 14px; color: #333; font-style: italic;">1 = Totalmente innecesario, 6 = Totalmente necesario</p>
        """, unsafe_allow_html=True)

    if st.button(f"Registrar {tipo}"):
        # Convertir la fecha en formato adecuado
        fecha_str = fecha.strftime('%Y-%m-%d')

        if tipo == "Ingreso":
            st.write(f"Ingreso registrado: Descripción: {descripcion}, Monto: {monto}, Forma de pago: {pago}, Fecha: {fecha_str}")
        elif tipo == "Gasto":
            st.write(f"Gasto registrado: Descripción: {descripcion}, Monto: {monto}, Forma de pago: {pago}, Fecha: {fecha_str}, Valoración: {valoracion}")

# Función principal que permite elegir entre ingresar manualmente o cargar CSV
def app():
    # Añadir la pregunta antes de las opciones
    st.title("¿Qué deseas registrar?")
    
    # Botón para elegir entre "Ingreso Manual" o "Carga desde CSV"
    opcion = st.radio("Selecciona cómo deseas registrar tus datos", ["Ingreso Manual", "Carga desde CSV"])

    if opcion == "Ingreso Manual":
        # Subopciones para elegir entre Ingreso o Gasto
        transaccion = st.radio("¿Qué deseas registrar?", ["Ingreso", "Gasto"])

        # Mostrar el formulario según la selección
        registrar_transaccion(transaccion)
    
    elif opcion == "Carga desde CSV":
        mostrar_ejemplo_csv()
        cargar_csv()

# Ejecutar la aplicación
if __name__ == "__main__":
    app()
