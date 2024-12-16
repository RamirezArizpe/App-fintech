import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

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
    return None

# Análisis de ingresos y gastos
def analizar_ingresos_gastos(df):
    st.header("Análisis de Ingresos y Gastos")

    ingresos = df[df["Tipo"] == "Ingreso"]["Monto"].sum()
    gastos = df[df["Tipo"] == "Gasto"]["Monto"].sum()

    st.write(f"**Total de Ingresos:** ${ingresos:.2f}")
    st.write(f"**Total de Gastos:** ${gastos:.2f}")
    
    # Gráfico de barras comparativo
    fig, ax = plt.subplots()
    ax.bar(["Ingresos", "Gastos"], [ingresos, gastos], color=["green", "red"])
    ax.set_ylabel("Monto ($)")
    ax.set_title("Ingresos vs. Gastos")
    st.pyplot(fig)

    # Distribución de gastos por categoría
    if "Forma de pago" in df.columns:
        gastos_categoria = df[df["Tipo"] == "Gasto"].groupby("Forma de pago")["Monto"].sum()
        fig, ax = plt.subplots()
        gastos_categoria.plot(kind="pie", autopct="%1.1f%%", ax=ax, startangle=90, colors=plt.cm.Paired.colors)
        ax.set_ylabel("")
        ax.set_title("Distribución de Gastos por Forma de Pago")
        st.pyplot(fig)

# Clasificación de gastos por necesidad
def clasificar_gastos(df):
    st.header("Clasificación de Gastos por Necesidad")

    if "Valoración gasto" in df.columns:
        gastos = df[df["Tipo"] == "Gasto"]
        innecesarios = gastos[gastos["Valoración gasto"] <= 3]
        st.write("### Gastos menos necesarios:")
        st.write(innecesarios.sort_values(by="Valoración gasto", ascending=True))

# Cálculo de ahorro mensual
def calcular_ahorro(df):
    st.header("Cálculo de Ahorros")

    ingresos_totales = df[df["Tipo"] == "Ingreso"].groupby("Fecha de transacción")["Monto"].sum()
    gastos_totales = df[df["Tipo"] == "Gasto"].groupby("Fecha de transacción")["Monto"].sum()

    ahorro_mensual = ingresos_totales - gastos_totales

    st.write("### Ahorro por mes:")
    st.write(ahorro_mensual)

    # Gráfico de ahorro
    fig, ax = plt.subplots()
    ahorro_mensual.plot(kind="bar", ax=ax, color="blue")
    ax.set_ylabel("Ahorro ($)")
    ax.set_title("Ahorro Mensual")
    st.pyplot(fig)

# Predicción básica de ahorros
def predecir_ahorros(df):
    st.header("Predicción de Ahorros")

    if "Fecha de transacción" in df.columns:
        df["Fecha de transacción"] = pd.to_datetime(df["Fecha de transacción"])
        ingresos_totales = df[df["Tipo"] == "Ingreso"].groupby("Fecha de transacción")["Monto"].sum()
        gastos_totales = df[df["Tipo"] == "Gasto"].groupby("Fecha de transacción")["Monto"].sum()

        ahorro_mensual = (ingresos_totales - gastos_totales).resample("M").sum()

        # Promedio móvil simple para predicción
        ahorro_mensual["Predicción"] = ahorro_mensual.rolling(window=3).mean()

        st.write("### Predicción de ahorro basado en promedio móvil:")
        st.line_chart(ahorro_mensual)

# Aplicación principal
def app():
    st.title("Gestión de Finanzas Personales")

    df = cargar_csv()

    if df is not None:
        analizar_ingresos_gastos(df)
        clasificar_gastos(df)
        calcular_ahorro(df)
        predecir_ahorros(df)

if __name__ == "__main__":
    app()

