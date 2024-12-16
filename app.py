import streamlit as st
import pandas as pd

# Agregar el logo al encabezado
st.image("https://raw.githubusercontent.com/RamirezArizpe/App-fintech/main/encabezado%20app.jpg", width=4000)

from IPython.display import display

# Crear DataFrames vacíos para ingresos y gastos
df_ingresos = pd.DataFrame(columns=['Descripción', 'Monto', 'Fecha de registro', 'Forma de pago'])
df_gastos = pd.DataFrame(columns=['Descripción', 'Monto', 'Fecha de registro', 'Forma de pago', 'Valoración'])

# Función para registrar un ingreso
def registrar_ingreso(descripcion, monto, forma_pago, fecha):
    global df_ingresos
    nuevo_ingreso = {'Descripción': descripcion, 'Monto': monto, 'Fecha de registro': fecha, 'Forma de pago': forma_pago}
    df_ingresos = pd.concat([df_ingresos, pd.DataFrame([nuevo_ingreso])], ignore_index=True)

# Función para registrar un gasto
def registrar_gasto(descripcion, monto, forma_pago, valoracion, fecha):
    global df_gastos
    nuevo_gasto = {'Descripción': descripcion, 'Monto': monto, 'Fecha de registro': fecha, 'Forma de pago': forma_pago, 'Valoración': valoracion}
    df_gastos = pd.concat([df_gastos, pd.DataFrame([nuevo_gasto])], ignore_index=True)

# Función para solicitar datos del usuario y registrar movimientos
def solicitar_datos():
    tipo = input("¿Desea registrar un ingreso o un gasto? (ingreso/gasto/salir): ").strip().lower()
    if tipo == 'ingreso':
        descripcion = input("Descripción del ingreso: ")
        monto = float(input("Monto del ingreso: "))
        forma_pago = input("Forma de pago: ")
        fecha_mov = date_input('Fecha de registro')

        def on_button_clicked(b):
            fecha = fecha_mov.value.strftime('%d/%m/%Y')
            registrar_ingreso(descripcion, monto, forma_pago, fecha)
            print(f"Ingreso registrado: {descripcion}, {monto}, {forma_pago}, {fecha}")
            button.close()  # Cerrar el botón después de un clic

        button.on_click(on_button_clicked)

    elif tipo == 'gasto':
        descripcion = input("Descripción del gasto: ")
        monto = float(input("Monto del gasto: "))
        forma_pago = input("Forma de pago: ")
        valoracion = int(input("Valoración del gasto (1-6): "))
        fecha_mov = date_input('Fecha de registro')

        def on_button_clicked(b):
            fecha = fecha_mov.value.strftime('%d/%m/%Y')
            registrar_gasto(descripcion, monto, forma_pago, valoracion, fecha)
            print(f"Gasto registrado: {descripcion}, {monto}, {forma_pago}, {valoracion}, {fecha}")
            button.close()  # Cerrar el botón después de un clic

        button.on_click(on_button_clicked)

    elif tipo == 'salir':
        return
    else:
        print("Opción no válida. Por favor, intente de nuevo.")
        solicitar_datos()


# Función para calcular y mostrar el balance
def calcular_balance():
    # Calcular el balance general del mes (Ingresos - Gastos)
    df_ingresos['Fecha'] = pd.to_datetime(df_ingresos['Fecha de registro'], format='%d/%m/%Y')
    df_gastos['Fecha'] = pd.to_datetime(df_gastos['Fecha de registro'], format='%d/%m/%Y')

    # Agrupar por mes y calcular totales
    df_ingresos['Mes'] = df_ingresos['Fecha'].dt.strftime('%Y-%m')
    df_gastos['Mes'] = df_gastos['Fecha'].dt.strftime('%Y-%m')

    resumen_ingresos = df_ingresos.groupby('Mes').agg({'Monto': 'sum'}).rename(columns={'Monto': 'Ingresos'})
    resumen_gastos = df_gastos.groupby('Mes').agg({'Monto': 'sum'}).rename(columns={'Monto': 'Gastos'})

    # Unir los resúmenes de ingresos y gastos
    resumen_mensual = pd.merge(resumen_ingresos, resumen_gastos, on='Mes', how='outer').fillna(0)
    resumen_mensual['Balance'] = resumen_mensual['Ingresos'] - resumen_mensual['Gastos']

    # Mostrar resultados
    print("\nDataFrame de Ingresos:")
    print(df_ingresos)
    print("\nDataFrame de Gastos:")
    print(df_gastos)
    print("\nResumen mensual:")
    print(resumen_mensual)
