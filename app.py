# Continuar desde la estructura madre
import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Lista inicial de formas de pago
formas_pago = ['transferencia', 'depósito', 'efectivo']

def agregar_forma_pago(pago):
    if pago not in formas_pago:
        formas_pago.append(pago)
        st.write(f"Forma de pago '{pago}' añadida a la lista.")
    else:
        st.write(f"La forma de pago '{pago}' ya está en la lista.")

# Funciones existentes (cargar CSV, registrar transacciones, etc.)
# ... (Mantener igual que en el código madre) ...

# Nueva función para realizar análisis de patrones y visualizaciones
def analizar_datos(df):
    st.title("Análisis de tus Finanzas")

    # Verificar que el dataframe no esté vacío
    if df.empty:
        st.warning("No hay datos disponibles para analizar.")
        return

    # Convertir columna de fecha a datetime si no lo está
    if not pd.api.types.is_datetime64_any_dtype(df['Fecha de transacción']):
        df['Fecha de transacción'] = pd.to_datetime(df['Fecha de transacción'])

    # Crear columna de mes
    df['Mes'] = df['Fecha de transacción'].dt.to_period('M')

    # Total de ingresos y gastos por mes
    resumen_mensual = df.groupby(['Mes', 'Tipo'])['Monto'].sum().unstack(fill_value=0)
    st.write("**Resumen Mensual (Ingresos vs Gastos):**")
    st.bar_chart(resumen_mensual)

    # Análisis de proporción ingresos/gastos
    st.write("**Proporción Ingresos vs Gastos:**")
    total_ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].sum()
    total_gastos = df[df['Tipo'] == 'Gasto']['Monto'].sum()
    proporciones = pd.DataFrame({
        'Categoría': ['Ingresos', 'Gastos'],
        'Monto': [total_ingresos, total_gastos]
    })
    fig, ax = plt.subplots()
    ax.pie(proporciones['Monto'], labels=proporciones['Categoría'], autopct='%1.1f%%', colors=['#6a1b9a', '#9c4dcc'])
    st.pyplot(fig)

    # Análisis de valoración de gastos
    if 'Valoración gasto' in df.columns:
        st.write("**Valoración promedio de gastos:**")
        valoracion_promedio = df[df['Tipo'] == 'Gasto']['Valoración gasto'].mean()
        st.metric("Valoración Promedio de Gastos", f"{valoracion_promedio:.2f} / 6")

# Actualizar función principal
def app():
    st.title("¿Qué deseas hacer?")
    opcion = st.radio("Selecciona una opción", ["Registrar Datos", "Analizar Finanzas"])

    if opcion == "Registrar Datos":
        transaccion = st.radio("¿Qué deseas registrar?", ["Ingreso", "Gasto"])
        registrar_transaccion(transaccion)
    elif opcion == "Analizar Finanzas":
        archivo = st.file_uploader("Carga tu archivo CSV para análisis", type=["csv"])
        if archivo:
            df = pd.read_csv(archivo)
            analizar_datos(df)

if __name__ == "__main__":
    app()
