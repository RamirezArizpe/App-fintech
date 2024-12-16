import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Agregar el logo al encabezado
st.image("https://raw.githubusercontent.com/RamirezArizpe/App-fintech/main/encabezado%20app.jpg", width=4000)

# Crear DataFrames vacíos para ingresos y gastos
df_ingresos = pd.DataFrame(columns=['Descripción', 'Monto', 'Fecha de registro', 'Forma de pago'])
df_gastos = pd.DataFrame(columns=['Descripción', 'Monto', 'Fecha de registro', 'Forma de pago', 'Valoración'])

# Función para cargar CSV
def cargar_csv():
    archivo_subido = st.file_uploader("Sube tu archivo CSV", type=["csv"])
    if archivo_subido is not None:
        df = pd.read_csv(archivo_subido)
        df['Fecha de registro'] = pd.to_datetime(df['Fecha de registro'], format='%d/%m/%Y')
        
        # Separar los ingresos y los gastos según la columna 'Tipo'
        df_ingresos = df[df['Tipo'] == 'Ingreso']
        df_gastos = df[df['Tipo'] == 'Gasto']
        
        # Mostrar los DataFrames separados
        st.write("Ingresos:", df_ingresos)
        st.write("Gastos:", df_gastos)

        return df_ingresos, df_gastos
    return None, None

# Opción para elegir entre ingresar manualmente o cargar CSV
opcion = st.radio("¿Cómo deseas ingresar los datos?", ("Manual", "Desde archivo CSV"))

# Si el usuario selecciona "Desde archivo CSV", cargamos el CSV
if opcion == "Desde archivo CSV":
    df_ingresos, df_gastos = cargar_csv()

# Función para registrar un ingreso manualmente
def registrar_ingreso_manual():
    descripcion = st.text_input("Descripción del ingreso:")
    monto = st.number_input("Monto del ingreso:", min_value=0.0)
    forma_pago = st.selectbox("Forma de pago:", ["Efectivo", "Tarjeta", "Transferencia"])
    fecha_mov = st.date_input("Fecha de registro")

    if st.button("Registrar Ingreso"):
        nuevo_ingreso = {
            'Descripción': descripcion,
            'Monto': monto,
            'Fecha de registro': str(fecha_mov),
            'Forma de pago': forma_pago
        }
        df_ingresos.loc[len(df_ingresos)] = nuevo_ingreso
        st.success(f"Ingreso registrado: {descripcion}, {monto}, {forma_pago}, {fecha_mov}")

# Función para registrar un gasto manualmente
def registrar_gasto_con_slider():
    descripcion = st.text_input("Descripción del gasto:")
    monto = st.number_input("Monto del gasto:", min_value=0.0)
    forma_pago = st.selectbox("Forma de pago:", ["Efectivo", "Tarjeta", "Transferencia"])
    fecha_mov = st.date_input("Fecha de registro")

    # Mostrar la barra deslizadora solo si es un gasto
    if monto > 0:
        valoracion = st.slider("¿Qué tan necesario fue este gasto?", 1, 6, 3)
        if st.button("Registrar Gasto"):
            # Aquí puedes guardar el gasto en el DataFrame correspondiente
            nuevo_gasto = {
                'Descripción': descripcion,
                'Monto': monto,
                'Fecha de registro': str(fecha_mov),
                'Forma de pago': forma_pago,
                'Valoración': valoracion
            }
            df_gastos.loc[len(df_gastos)] = nuevo_gasto
            st.success(f"Gasto registrado: {descripcion}, {monto}, {forma_pago}, {valoracion}, {fecha_mov}")

    # Graficar DataFrame de ingresos vs DataFrame de gastos
    plt.figure(figsize=(10, 6))
    plt.plot(df_ingresos['Fecha de registro'], df_ingresos['Monto'], marker='o', label='Ingresos')
    plt.plot(df_gastos['Fecha de registro'], df_gastos['Monto'], marker='o', label='Gastos')
    plt.xlabel('Fecha')
    plt.ylabel('Monto')
    plt.title('Ingresos vs Gastos')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    # Graficar los gastos por categoría (Descripción)
    plt.figure(figsize=(10, 6))
    df_gastos.groupby('Descripción')['Monto'].sum().plot(kind='bar')
    plt.title('Gastos por Categoría')
    plt.xlabel('Categoría')
    plt.ylabel('Monto')
    plt.xticks(rotation=45)
    st.pyplot(plt)

# Si el usuario eligió "Manual", mostrar opciones para ingresar ingresos y gastos manualmente
if opcion == "Manual":
    # Registrar ingreso manual
    registrar_ingreso_manual()
    # Registrar gasto manual con slider
    registrar_gasto_con_slider()
