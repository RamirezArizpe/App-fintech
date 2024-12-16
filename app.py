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
        valoracion = st.slider("¿Qué tan necesario fue este gasto?", 1, 6)

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

# Ejecutar la aplicación
if __name__ == "__main__":
    app()

