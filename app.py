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

# Función para mostrar glosario de términos financieros
def mostrar_glosario():
    st.write("### Glosario de términos financieros")
    st.write("- **Ingreso**: Dinero que recibes regularmente o de una sola vez.")
    st.write("- **Gasto**: Dinero que se destina a pagar por bienes o servicios.")
    st.write("- **Saldo**: La cantidad de dinero que tienes disponible después de registrar tus ingresos y gastos.")
    st.write("- **Forma de pago**: Método utilizado para realizar el pago (ej. transferencia, efectivo).")

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
    
    # Incluir el glosario para los nuevos usuarios
    mostrar_glosario()

    # Convertir la columna 'Fecha de transacción' a formato de fecha
    df['Fecha'] = pd.to_datetime(df['Fecha de transacción'])
    
    # Gráfico de Ingresos vs Gastos
    fig = plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Tipo', palette="Set2")
    plt.title("Distribución de Ingresos vs Gastos")
    st.pyplot(fig)

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
    
    # Gráfico interactivo de formas de pago (usando Plotly)
    fig = px.pie(df, names='Forma de pago', title='Distribución de Formas de Pago')
    st.plotly_chart(fig)

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

    # Sugerencias para mejorar la situación financiera
    if balance < 0:
        st.write("⚠️ **¡Atención!** Tu balance es negativo. Considera reducir tus gastos o aumentar tus ingresos.")
    elif balance < 1000:
        st.write("💡 Podrías mejorar tu balance incrementando tus ahorros o buscando maneras de reducir gastos innecesarios.")
    else:
        st.write("🎉 ¡Buen trabajo! Tienes un balance positivo. Sigue ahorrando y controlando tus gastos.")

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
        st.markdown("""<p style="font-size: 14px; color: #333; font-style: italic;">1 = Totalmente innecesario, 6 = Totalmente necesario</p>""", unsafe_allow_html=True)

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
