pip install plotly
import streamlit as st
import pandas as pd
import os

# Agregar el logo al encabezado
st.image("https://raw.githubusercontent.com/RamirezArizpe/App-fintech/main/encabezado%20app.jpg", width=400)

# Ruta para guardar los datos
DATA_PATH = 'finanzas_personales.csv'

# Función para cargar los datos desde el archivo CSV si existe
def cargar_datos():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        df['Fecha de registro'] = pd.to_datetime(df['Fecha de registro'])
        return df
    else:
        return pd.DataFrame(columns=['Tipo', 'Descripción', 'Monto', 'Fecha de registro', 'Forma de pago', 'Valoración'])

# Función para guardar los datos en el archivo CSV
def guardar_datos(df):
    df.to_csv(DATA_PATH, index=False)

# Cargar los datos al inicio
df_finanzas = cargar_datos()

# Función para registrar un movimiento (ingreso o gasto)
def registrar_movimiento(tipo, descripcion, monto, forma_pago, valoracion, fecha):
    global df_finanzas
    nuevo_movimiento = {'Tipo': tipo, 'Descripción': descripcion, 'Monto': monto, 'Fecha de registro': fecha, 'Forma de pago': forma_pago, 'Valoración': valoracion}
    df_finanzas = df_finanzas.append(nuevo_movimiento, ignore_index=True)
    guardar_datos(df_finanzas)
    st.success(f"{tipo.capitalize()} registrado exitosamente.")

# Función para mostrar el balance
def mostrar_balance():
    df_ingresos = df_finanzas[df_finanzas['Tipo'] == 'ingreso']
    df_gastos = df_finanzas[df_finanzas['Tipo'] == 'gasto']

    df_ingresos['Mes'] = df_ingresos['Fecha de registro'].dt.strftime('%Y-%m')
    df_gastos['Mes'] = df_gastos['Fecha de registro'].dt.strftime('%Y-%m')

    resumen_ingresos = df_ingresos.groupby('Mes').agg({'Monto': 'sum'}).rename(columns={'Monto': 'Ingresos'})
    resumen_gastos = df_gastos.groupby('Mes').agg({'Monto': 'sum'}).rename(columns={'Monto': 'Gastos'})

    resumen_mensual = pd.merge(resumen_ingresos, resumen_gastos, on='Mes', how='outer').fillna(0)
    resumen_mensual['Balance'] = resumen_mensual['Ingresos'] - resumen_mensual['Gastos']

    st.write("Resumen mensual de ingresos, gastos y balance:")
    st.dataframe(resumen_mensual)

# Interfaz de usuario
st.title("App de Finanzas Personales")

# Selección del tipo de entrada: manual o desde CSV
opcion_entrada = st.radio("¿Cómo desea registrar los datos?", ["Ingreso manual", "Cargar desde archivo CSV"], horizontal=True)

if opcion_entrada == "Ingreso manual":
    # Selección de tipo de movimiento
    tipo = st.selectbox("¿Qué desea registrar?", ["Ingreso", "Gasto"])

    # Entradas según el tipo de movimiento
    descripcion = st.text_input("Descripción")
    monto = st.number_input("Monto", min_value=0.01, format="%.2f")
    forma_pago = st.selectbox("Forma de pago", ["Efectivo", "Tarjeta de crédito", "Tarjeta de débito", "Transferencia", "Otros"])

    if tipo == "Gasto":
        valoracion = st.slider("Valoración del gasto (1-6)", 1, 6, 3)
    else:
        valoracion = None  # Los ingresos no tienen valoración

    fecha = st.date_input("Fecha de registro")

    # Botón para registrar
    if st.button(f"Registrar {tipo.lower()}"):
        if descripcion and monto > 0 and forma_pago:
            registrar_movimiento(tipo.lower(), descripcion, monto, forma_pago, valoracion, fecha)
        else:
            st.error("Por favor, complete todos los campos.")
elif opcion_entrada == "Cargar desde archivo CSV":
    # Cargar archivo CSV
    archivo = st.file_uploader("Suba un archivo CSV", type="csv")

    if archivo:
        try:
            df_cargado = pd.read_csv(archivo)
            df_cargado['Fecha de registro'] = pd.to_datetime(df_cargado['Fecha de registro'])
            st.write("Datos cargados desde el archivo:")
            st.dataframe(df_cargado)
            # Registrar datos cargados en el DataFrame principal
            for _, row in df_cargado.iterrows():
                registrar_movimiento(row['Tipo'], row['Descripción'], row['Monto'], row['Forma de pago'], row.get('Valoración', None), row['Fecha de registro'])
        except Exception as e:
            st.error(f"Hubo un error al cargar el archivo: {e}")

# Mostrar balance mensual
if st.checkbox("Ver balance mensual"):
    mostrar_balance()

# Mostrar los registros actuales
if st.checkbox("Ver registros actuales"):
    st.write(df_finanzas)

import plotly.express as px

# Crear gráfico de barras
data = {'Categoría': ['A', 'B', 'C', 'D'], 'Valor': [10, 20, 30, 40]}
df = pd.DataFrame(data)

fig = px.bar(df, x='Categoría', y='Valor', title="Gráfico de Barras Interactivo")
st.plotly_chart(fig)

