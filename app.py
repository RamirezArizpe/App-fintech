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
import pandas as pd
import streamlit as st
import io

# Crear un CSV de ejemplo para ingresos y gastos
def crear_csv_ejemplo():
    # Crear un DataFrame de ejemplo
    data_ingresos = {
        "Descripción": ["Ingreso Ejemplo 1", "Ingreso Ejemplo 2"],
        "Monto": [500, 1000],
        "Fecha de registro": ["2023-12-15", "2023-12-16"],
        "Forma de pago": ["Efectivo", "Tarjeta"]
    }
    data_gastos = {
        "Descripción": ["Gasto Ejemplo 1", "Gasto Ejemplo 2"],
        "Monto": [200, 150],
        "Fecha de registro": ["2023-12-15", "2023-12-16"],
        "Forma de pago": ["Efectivo", "Transferencia"],
        "Valoración": [4, 5]
    }

    # Crear DataFrames
    df_ingresos = pd.DataFrame(data_ingresos)
    df_gastos = pd.DataFrame(data_gastos)

    # Guardar ambos DataFrames como CSV en un archivo temporal
    csv_ingresos = df_ingresos.to_csv(index=False)
    csv_gastos = df_gastos.to_csv(index=False)

    # Combinar ambos CSV en un solo archivo (puedes ofrecer dos archivos separados si lo prefieres)
    combined_csv = csv_ingresos + "\n\n" + csv_gastos

    return combined_csv

# Función para descargar el archivo de ejemplo
def descargar_csv_ejemplo():
    # Crear el CSV de ejemplo
    csv_ejemplo = crear_csv_ejemplo()

    # Crear un buffer en memoria para poder descargar el archivo
    buffer = io.StringIO(csv_ejemplo)

    # Botón para descargar el archivo
    st.download_button(
        label="Descargar ejemplo CSV",
        data=buffer.getvalue(),
        file_name="ejemplo_finanzas.csv",
        mime="text/csv"
    )

# Mostrar opciones para elegir si manual o CSV
opcion = st.radio("Selecciona cómo ingresar los datos", ["Manual", "CSV"], horizontal=True)

if opcion == "CSV":
    descargar_csv_ejemplo()
elif opcion == "Manual":
    # Aquí puedes colocar el resto de tu código de registro manual
    st.write("Registrando datos manualmente...")

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

def registrar_gasto_con_slider():
    descripcion = st.text_input("Descripción del gasto:", key="descripcion_gasto")
    monto = st.number_input("Monto del gasto:", min_value=0.0, key="monto_gasto")
    forma_pago = st.selectbox("Forma de pago:", ["Efectivo", "Tarjeta", "Transferencia"], key="forma_pago")
    fecha_mov = st.date_input("Fecha de registro", key="fecha_gasto")

    # Mostrar la barra deslizadora solo si es un gasto
    if monto > 0:
        valoracion = st.slider("¿Qué tan necesario fue este gasto?", 1, 6, 3, key="valoracion_gasto")
        if st.button("Registrar Gasto", key="registrar_gasto"):
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
