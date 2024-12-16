import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Función para mostrar gráficos y análisis visual
def mostrar_analisis(df):
    st.title("Análisis Gráfico e Insights de tus Finanzas")

    # Convertir la columna 'Fecha de transacción' a formato de fecha
    df['Fecha'] = pd.to_datetime(df['Fecha de transacción'])

    # Filtro para seleccionar mes o total
    opcion_mes = st.selectbox("Selecciona un mes o Total", ["Total"] + list(df['Fecha'].dt.to_period('M').unique().astype(str)))

    # Análisis de ingresos vs gastos
    if opcion_mes == "Total":
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

    # Análisis de necesidad de los gastos
    st.write("### Análisis de Necesidad de los Gastos")
    gastos_necesarios = df[(df['Tipo'] == 'Gasto') & (df['Valoración'] <= 3)]  # Valoración ≤ 3
    total_gastos_necesarios = gastos_necesarios['Monto'].sum()
    st.write(f"- **Total de Gastos Innecesarios (Valoración ≤ 3)**: ${total_gastos_necesarios:.2f}")

    # Potencial de ahorro
    st.write(f"- **Potencial de Ahorro**: ${total_gastos_necesarios:.2f}")

    # Mostrar detalles de los gastos innecesarios
    if not gastos_necesarios.empty:
        st.write("#### Detalle de los Gastos Innecesarios:")
        st.write(gastos_necesarios[['Descripción', 'Monto', 'Valoración']])

    # Tendencia de Ingresos y Gastos
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

# Modificar la función para registrar un gasto y su valoración de necesidad
def registrar_transaccion(tipo):
    st.title(f"Registrar {tipo}")

    # Campos comunes para ingreso y gasto
    descripcion = st.text_input(f"Descripción del {tipo.lower()}")
    monto = st.number_input("Monto en pesos mexicanos", min_value=0.0)
    pago = st.selectbox("Forma de pago", ['transferencia', 'depósito', 'efectivo'])
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
    st.title("¿Qué deseas registrar?")
    
    # Botón para elegir entre "Ingreso Manual" o "Carga desde CSV"
    opcion = st.radio("Selecciona cómo deseas registrar tus datos", ["Ingreso Manual", "Carga desde CSV"])

    if opcion == "Ingreso Manual":
        # Subopciones para elegir entre Ingreso o Gasto
        transaccion = st.radio("¿Qué deseas registrar?", ["Ingreso", "Gasto"])
        registrar_transaccion(transaccion)
    
    elif opcion == "Carga desde CSV":
        cargar_csv()

# Ejecutar la aplicación
if __name__ == "__main__":
    app()
