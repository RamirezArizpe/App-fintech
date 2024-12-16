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

# Mostrar balance mensual
if st.checkbox("Ver balance mensual"):
    mostrar_balance()

# Mostrar los registros actuales
if st.checkbox("Ver registros actuales"):
    st.write(df_finanzas)
