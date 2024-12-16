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

# Función para cargar datos desde un archivo CSV
def cargar_csv():
    archivo = st.file_uploader("Cargar archivo CSV", type=["csv"])
    if archivo:
        try:
            df = pd.read_csv(archivo)
            st.write("Datos cargados exitosamente:")
            st.write(df)
            return df
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")
    return None

# Función para mostrar gráficos y análisis visual
def mostrar_analisis(df, periodo):
    st.title("Análisis Gráfico e Insights de tus Finanzas")

    # Filtrar los datos según el período seleccionado
    if periodo != 'Total':
        df['Fecha'] = pd.to_datetime(df['Fecha de transacción'])
        df_filtrado = df[df['Fecha'].dt.to_period('M') == periodo]
    else:
        df_filtrado = df
    
    # Gráfico de Ingresos vs Gastos por mes
    fig = plt.figure(figsize=(10, 6))
    sns.countplot(data=df_filtrado, x='Tipo', palette="Set2")
    plt.title(f"Distribución de Ingresos vs Gastos - {periodo}")
    st.pyplot(fig)

    # Gráfico de ingresos y gastos por mes
    df_filtrado['Mes-Año'] = df_filtrado['Fecha'].dt.to_period('M')
    ingresos_mes = df_filtrado[df_filtrado['Tipo'] == 'Ingreso'].groupby('Mes-Año')['Monto'].sum()
    gastos_mes = df_filtrado[df_filtrado['Tipo'] == 'Gasto'].groupby('Mes-Año')['Monto'].sum()

    fig = plt.figure(figsize=(10, 6))
    plt.plot(ingresos_mes.index.astype(str), ingresos_mes, label="Ingresos", marker='o')
    plt.plot(gastos_mes.index.astype(str), gastos_mes, label="Gastos", marker='o')
    plt.title(f"Ingresos y Gastos Mensuales - {periodo}")
    plt.xlabel("Mes")
    plt.ylabel("Monto en Pesos")
    plt.legend()
    st.pyplot(fig)
    
    # Gráfico interactivo de formas de pago (usando Plotly)
    fig = px.pie(df_filtrado, names='Forma de pago', title=f'Distribución de Formas de Pago - {periodo}')
    st.plotly_chart(fig)

    # Insights de los datos
    st.write("### Insights:")
    total_ingresos = df_filtrado[df_filtrado['Tipo'] == 'Ingreso']['Monto'].sum()
    total_gastos = df_filtrado[df_filtrado['Tipo'] == 'Gasto']['Monto'].sum()
    balance = total_ingresos - total_gastos
    promedio_ingresos = df_filtrado[df_filtrado['Tipo'] == 'Ingreso']['Monto'].mean()
    promedio_gastos = df_filtrado[df_filtrado['Tipo'] == 'Gasto']['Monto'].mean()

    st.write(f"- **Total de Ingresos**: ${total_ingresos:.2f}")
    st.write(f"- **Total de Gastos**: ${total_gastos:.2f}")
    st.write(f"- **Balance Neto**: ${balance:.2f}")
    st.write(f"- **Promedio de Ingresos**: ${promedio_ingresos:.2f}")
    st.write(f"- **Promedio de Gastos**: ${promedio_gastos:.2f}")

    # Estadísticas de las formas de pago
    formas_pago_counts = df_filtrado['Forma de pago'].value_counts()
    st.write("### Frecuencia de Formas de Pago:")
    st.write(formas_pago_counts)

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

# Función principal que permite elegir entre ingresar manualmente o cargar CSV
def app():
    # Añadir la pregunta antes de las opciones
    st.title("¿Qué deseas registrar?")
    
    # Botón para elegir entre "Ingreso Manual" o "Carga desde CSV"
    opcion = st.radio("Selecciona cómo deseas registrar tus datos", ["Ingreso Manual", "Carga desde CSV"])

    if opcion == "Ingreso Manual":
        # Subopciones para elegir entre Ingreso o Gasto
        transaccion = st.radio("¿Qué deseas registrar?", ["Ingreso", "Gasto"])
        registrar_transaccion(transaccion)
    
    elif opcion == "Carga desde CSV":
        df = cargar_csv()
        if df is not None:
            # Filtro para seleccionar mes o total
            periodo = st.selectbox("Selecciona un periodo", ['Total'] + sorted(df['Fecha de transacción'].apply(lambda x: x[:7]).unique().tolist()))
            mostrar_analisis(df, periodo)

# Ejecutar la aplicación
if __name__ == "__main__":
    app()
