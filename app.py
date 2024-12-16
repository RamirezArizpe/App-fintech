import streamlit as st
import pandas as pd

# Agregar el logo al encabezado
st.image(https://drive.google.com/file/d/1kD9ibgHAIaxX3xHxuPnw241Fucj8URLD/view?usp=sharing, width=200) 

# Configuración inicial de la aplicación
st.title("Formulario de Datos y Análisis")
st.write("Introduce tus datos manualmente o carga un archivo CSV para comenzar.")

# Entrada manual de datos
st.subheader("Entrada Manual")
nombre = st.text_input("Nombre")
edad = st.number_input("Edad", min_value=0, step=1)
ingreso_mensual = st.number_input("Ingreso Mensual", min_value=0.0, step=100.0)

# Botón para añadir manualmente al DataFrame
if st.button("Añadir Datos Manuales"):
    st.write("Datos añadidos:")
    st.write(f"Nombre: {nombre}, Edad: {edad}, Ingreso Mensual: {ingreso_mensual}")

# Cargar datos desde un archivo CSV
st.subheader("Carga de Archivo CSV")
archivo_cargado = st.file_uploader("Selecciona un archivo CSV", type=["csv"])

if archivo_cargado is not None:
    datos = pd.read_csv(archivo_cargado)
    st.write("Datos cargados:")
    st.dataframe(datos)
