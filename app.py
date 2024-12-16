import streamlit as st
import pandas as pd
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
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

# Función para mostrar un ejemplo de archivo CSV
def mostrar_ejemplo_csv():
    ejemplo = pd.DataFrame({
        "Descripción": ["Ingreso 1", "Gasto 1"],
        "Monto": [1000, 200],
        "Forma de pago": ["transferencia", "efectivo"],
        "Fecha de transacción": ["2024-12-16", "2024-12-16"],
        "Valoración gasto": [None, 3]
    })
    st.write("Ejemplo de formato CSV para carga correcta:")
    st.write(ejemplo)
    # Opción para descargar el ejemplo como CSV
    st.download_button(
        label="Descargar archivo ejemplo",
        data=ejemplo.to_csv(index=False),
        file_name="ejemplo_finanzas_personales.csv",
        mime="text/csv"
    )

# Función para agregar un ingreso
def agregar_ingreso():
    st.title("Agregar Ingreso")

    # Campos para ingresar datos
    descripcion = st.text_input("Descripción del ingreso")
    monto = st.number_input("Monto en pesos mexicanos", min_value=0.0)
    pago = st.selectbox("Forma de pago", formas_pago)
    fecha = st.date_input("Fecha de transacción", datetime.today())

    if st.button("Registrar Ingreso"):
        # Convertir la fecha en formato adecuado
        fecha_str = fecha.strftime('%Y-%m-%d')
        st.write(f"Ingreso registrado: Descripción: {descripcion}, Monto: {monto}, Forma de pago: {pago}, Fecha: {fecha_str}")

# Función para agregar un gasto
def agregar_gasto():
    st.title("Agregar Gasto")

    # Campos para ingresar datos
    descripcion = st.text_input("Descripción del gasto")
    monto = st.number_input("Monto en pesos mexicanos", min_value=0.0)
    pago = st.selectbox("Forma de pago", formas_pago)
    fecha = st.date_input("Fecha de transacción", datetime.today())
    valoracion = st.slider("¿Qué tan necesario fue este gasto?", 1, 6)

    if st.button("Registrar Gasto"):
        # Convertir la fecha en formato adecuado
        fecha_str = fecha.strftime('%Y-%m-%d')
        st.write(f"Gasto registrado: Descripción: {descripcion}, Monto: {monto}, Forma de pago: {pago}, Fecha: {fecha_str}, Valoración: {valoracion}")

# Función principal que permite elegir entre ingresar manualmente o cargar CSV
def app():
    st.sidebar.title("Menú de Finanzas Personales")
    opcion = st.sidebar.radio("Selecciona una opción", ["Agregar Ingreso", "Agregar Gasto", "Cargar Datos desde CSV", "Ver Ejemplo CSV"])

    if opcion == "Agregar Ingreso":
        agregar_ingreso()
    elif opcion == "Agregar Gasto":
        agregar_gasto()
    elif opcion == "Cargar Datos desde CSV":
        cargar_csv()
    elif opcion == "Ver Ejemplo CSV":
        mostrar_ejemplo_csv()

# Ejecutar la aplicación
if __name__ == "__main__":
    app()
