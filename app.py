import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px

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
            
            # Mostrar análisis gráfico e insights
            mostrar_analisis(df)
            
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

# Función para mostrar gráficos y análisis visual
def mostrar_analisis(df):
    st.title("Análisis Gráfico e Insights de tus Finanzas")

    # Crear un contenedor con dos columnas: una para las gráficas y otra para el texto
    col1, col2 = st.columns([2, 1])

    with col1:
        # Convertir la columna 'Fecha de transacción' a formato de fecha
        df['Fecha'] = pd.to_datetime(df['Fecha de transacción'])

        # Filtro para seleccionar mes o total
        opcion_mes = st.selectbox("Selecciona un mes o Total", ["Total"] + list(df['Fecha'].dt.to_period('M').unique().astype(str)))

        if opcion_mes == "Total":
            # Gráfico de Ingresos vs Gastos total
            ingresos_total = df[df['Tipo'] == 'Ingreso']['Monto'].sum()
            gastos_total = df[df['Tipo'] == 'Gasto']['Monto'].sum()
            labels = ['Ingresos', 'Gastos']
            values = [ingresos_total, gastos_total]
            fig = plt.figure(figsize=(6, 4))
            plt.bar(labels, values, color=['green', 'red'])
            plt.title("Ingresos vs Gastos Total")
            plt.ylabel("Monto en Pesos")
            st.pyplot(fig)
        else:
            # Filtro dinámico por mes
            df_mes = df[df['Fecha'].dt.to_period('M').astype(str) == opcion_mes]
            ingresos_mes = df_mes[df_mes['Tipo'] == 'Ingreso']['Monto'].sum()
            gastos_mes = df_mes[df_mes['Tipo'] == 'Gasto']['Monto'].sum()
            labels = ['Ingresos', 'Gastos']
            values = [ingresos_mes, gastos_mes]
            fig = plt.figure(figsize=(6, 4))
            plt.bar(labels, values, color=['green', 'red'])
            plt.title(f"Ingresos vs Gastos - {opcion_mes}")
            plt.ylabel("Monto en Pesos")
            st.pyplot(fig)

        # Gráfico de tendencias de ingresos y gastos
        st.write("### Tendencias de Ingresos y Gastos a lo largo del tiempo")
        # Agrupar los datos por mes y año
        df['Mes'] = df['Fecha'].dt.to_period('M')
        ingresos_tendencia = df[df['Tipo'] == 'Ingreso'].groupby('Mes')['Monto'].sum()
        gastos_tendencia = df[df['Tipo'] == 'Gasto'].groupby('Mes')['Monto'].sum()

        fig_tendencia = plt.figure(figsize=(8, 5))
        plt.plot(ingresos_tendencia.index.astype(str), ingresos_tendencia, label='Ingresos', color='green', marker='o')
        plt.plot(gastos_tendencia.index.astype(str), gastos_tendencia, label='Gastos', color='red', marker='o')
        plt.xlabel("Mes")
        plt.ylabel("Monto en Pesos")
        plt.title("Tendencia de Ingresos y Gastos")
        plt.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig_tendencia)

    with col2:
        # Mostrar insights de los datos
        st.write("### Insights:")
        
        total_ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].sum()
        total_gastos = df[df['Tipo'] == 'Gasto']['Monto'].sum()
        balance = total_ingresos - total_gastos
        promedio_ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].mean()
        promedio_gastos = df[df['Tipo'] == 'Gasto']['Monto'].mean()

        st.write(f"- **Total de Ingresos**: ${total_ingresos:.2f}")
        st.write(f"- **Total de Gastos**: ${total_gastos:.2f}")

        # Calcular la proporción de gastos sobre ingresos
        if total_ingresos > 0:
            proporcion_gastos = total_gastos / total_ingresos
        else:
            proporcion_gastos = 0  # Si no hay ingresos, la proporción será 0

        st.write(f"- **Proporción de Gastos sobre Ingresos**: {proporcion_gastos:.2%}")

        # Alertas si la proporción de gastos es alta
        if proporcion_gastos > 0.7:
            st.warning("🚨 Alerta: La proporción de tus gastos sobre ingresos es alta (>70%). Revisa tus gastos.")
        
        st.write(f"- **Balance Neto**: ${balance:.2f}")
        st.write(f"- **Promedio de Ingresos**: ${promedio_ingresos:.2f}")
        st.write(f"- **Promedio de Gastos**: ${promedio_gastos:.2f}")

        # Estadísticas de las formas de pago
        formas_pago_counts = df['Forma de pago'].value_counts()
        st.write("### Frecuencia de Formas de Pago:")
        st.write(formas_pago_counts)

class AnalisisFinanciero:
    def __init__(self, df):
        # Convertir a datetime y asegurar tipos de datos
        self.df = df.copy()
        self.df['Fecha'] = pd.to_datetime(self.df['Fecha de transacción'])
        self.df['Monto'] = pd.to_numeric(self.df['Monto'])
        
    def preparar_matriz(self):
        """Convertir DataFrame a matriz numérica"""
        # Seleccionar características para análisis
        caracteristicas = ['Monto']
        matriz_numerica = self.df[caracteristicas].values
        return matriz_numerica
    
    def analisis_pca(self):
        """Realizar Análisis de Componentes Principales"""
        # Preparar datos
        X = self.df[['Monto']]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Realizar PCA
        pca = PCA(n_components=1)
        X_pca = pca.fit_transform(X_scaled)
        
        print("Análisis de Componentes Principales (PCA):")
        print("Varianza explicada:", pca.explained_variance_ratio_)
        print("Componente principal:", pca.components_)
        
        # Visualización de PCA
        plt.figure(figsize=(10, 6))
        plt.scatter(range(len(X_pca)), X_pca, c=X_pca, cmap='viridis')
        plt.title('Proyección de Datos Financieros en Componente Principal')
        plt.xlabel('Índice de Transacción')
        plt.ylabel('Valor en Componente Principal')
        plt.colorbar(label='Magnitud')
        plt.tight_layout()
        plt.show()
        
        return X_pca
    
    def matriz_covarianza(self):
        """Calcular matriz de covarianza"""
        # Incluir múltiples características si están disponibles
        caracteristicas = ['Monto']
        matriz_cov = np.cov(self.df[caracteristicas].T)
        
        print("\nMatriz de Covarianza:")
        print(matriz_cov)
        
        # Visualización de la matriz de covarianza
        plt.figure(figsize=(8, 6))
        sns.heatmap(matriz_cov, annot=True, cmap='coolwarm', center=0)
        plt.title('Matriz de Covarianza de Características Financieras')
        plt.tight_layout()
        plt.show()
        
        return matriz_cov
    
    def clustering_kmeans(self):
        """Realizar clustering de transacciones"""
        # Preparar datos para clustering
        X = self.df[['Monto']]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Realizar K-means clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        
        # Añadir información de clusters al DataFrame
        self.df['Cluster'] = clusters
        
        print("\nAnálisis de Clustering:")
        # Estadísticas por cluster
        print(self.df.groupby('Cluster').agg({
            'Monto': ['mean', 'count'],
            'Tipo': lambda x: x.value_counts().index[0]
        }))
        
        # Visualización de clusters
        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(
            range(len(X_scaled)), 
            X_scaled, 
            c=clusters, 
            cmap='viridis'
        )
        plt.title('Clustering de Transacciones Financieras')
        plt.xlabel('Índice de Transacción')
        plt.ylabel('Monto Normalizado')
        plt.colorbar(scatter, label='Cluster')
        plt.tight_layout()
        plt.show()
        
        return clusters
    
    def analisis_vectorial(self):
        """Análisis vectorial de transacciones"""
        # Separar ingresos y gastos
        ingresos = self.df[self.df['Tipo'] == 'Ingreso']['Monto']
        gastos = self.df[self.df['Tipo'] == 'Gasto']['Monto']
        
        # Calcular vectores de tendencia
        vector_ingresos = np.array(ingresos)
        vector_gastos = np.array(gastos)
        
        # Calcular ángulo entre vectores de ingresos y gastos
        producto_punto = np.dot(vector_ingresos, vector_gastos)
        magnitud_ingresos = np.linalg.norm(vector_ingresos)
        magnitud_gastos = np.linalg.norm(vector_gastos)
        
        # Calcular ángulo
        try:
            coseno_angulo = producto_punto / (magnitud_ingresos * magnitud_gastos)
            angulo = np.arccos(np.clip(coseno_angulo, -1.0, 1.0))
            angulo_grados = np.degrees(angulo)
            
            print("\nAnálisis Vectorial:")
            print(f"Magnitud de Ingresos: {magnitud_ingresos}")
            print(f"Magnitud de Gastos: {magnitud_gastos}")
            print(f"Ángulo entre vectores de Ingresos y Gastos: {angulo_grados:.2f} grados")
        except Exception as e:
            print("Error en cálculo vectorial:", e)

def main():
    # Crear DataFrame de ejemplo
    df = pd.DataFrame({
        "Descripción": ["Ingreso 1", "Gasto 1", "Ingreso 2", "Gasto 2", "Ingreso 3", "Gasto 3"],
        "Monto": [1000, 200, 1500, 100, 2000, 300],
        "Forma de pago": ["transferencia", "efectivo", "depósito", "efectivo", "transferencia", "efectivo"],
        "Fecha de transacción": [
            "2024-01-16", "2024-01-16", 
            "2024-02-17", "2024-02-17", 
            "2024-03-18", "2024-03-18"
        ],
        "Tipo": ["Ingreso", "Gasto", "Ingreso", "Gasto", "Ingreso", "Gasto"]
    })
    
    # Crear instancia de análisis
    analisis = AnalisisFinanciero(df)
    
    # Ejecutar diversos análisis
    print("Matriz Original:")
    print(analisis.preparar_matriz())
    
    # PCA
    analisis.analisis_pca()
    
    # Matriz de Covarianza
    analisis.matriz_covarianza()
    
    # Clustering
    analisis.clustering_kmeans()
    
    # Análisis Vectorial
    analisis.analisis_vectorial()

if __name__ == "__main__":
    main()

# Cargar el CSV y ejecutar el análisis
def app():
    # Ejemplo de dataframe para pruebas
    df = pd.DataFrame({
        "Descripción": ["Ingreso 1", "Gasto 1", "Ingreso 2", "Gasto 2"],
        "Monto": [1000, 200, 1500, 100],
        "Forma de pago": ["transferencia", "efectivo", "depósito", "efectivo"],
        "Fecha de transacción": ["2024-12-16", "2024-12-16", "2024-12-17", "2024-12-17"],
        "Tipo": ["Ingreso", "Gasto", "Ingreso", "Gasto"]  # Columna Tipo para diferenciar
    })
    
    # Convertir la columna 'Fecha de transacción' a formato de fecha
    df['Fecha'] = pd.to_datetime(df['Fecha de transacción'])

    # Llamar a la función para mostrar análisis
    mostrar_analisis(df)
    
    st.write("Ejemplo de formato CSV para carga correcta: (no escribas acentos ni caractéres especiales)")
    st.write(ejemplo)
    # Opción para descargar el ejemplo como CSV
    st.download_button(
        label="Descargar archivo ejemplo",
        data=ejemplo.to_csv(index=False),
        file_name="ejemplo_finanzas_personales.csv",
        mime="text/csv"
    )

# Inyectar CSS personalizado para cambiar el color y el grosor del slider y el estilo de los botones
st.markdown("""
    <style>
        /* Cambiar color y grosor del slider */
        .stSlider .st-bw {
            width: 100%;
            height: 12px; /* Hacer el slider más grueso */
            background-color: #001f3d; /* Azul marino */
        }
        .stSlider .st-bw .st-cb {
            background-color: #FFFFFF; /* Color blanco para el botón del slider */
        }

        /* Cambiar estilo de los botones a pills moradas */
        .stButton > button {
            background-color: #6a1b9a;  /* Morado */
            color: white;
            border-radius: 50px; /* Hacerlo "pill" */
            font-size: 16px;
            padding: 10px 20px;
            border: none;
        }
        .stButton > button:hover {
            background-color: #9c4dcc;  /* Morado más claro al pasar el ratón */
        }

        /* Cambiar el estilo del radio button */
        .stRadio > div {
            display: flex;
            flex-direction: row;
            justify-content: space-around;
        }

        /* Cambiar el estilo de las opciones del radio button a pills moradas */
        .stRadio label {
            background-color: #6a1b9a;
            color: white;
            border-radius: 50px;
            font-size: 16px;
            padding: 8px 20px;
        }

        .stRadio input:checked + label {
            background-color: #9c4dcc; /* Morado más claro cuando se selecciona */
        }

        /* Estilo de los radio buttons */
        .stRadio .st-bw {
            color: white; /* Color de texto blanco en los botones */
        }

        /* Sin fondo para la pregunta */
        .stTitle, .stSubheader, .stMarkdown {
            background: none !important;
        }
    </style>
""", unsafe_allow_html=True)

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
        valoracion = st.slider(
            "¿Qué tan necesario fue este gasto?", 
            min_value=1, 
            max_value=6, 
            step=1
        )
        st.markdown("""
            <style>
                /* Estilo para el texto explicativo */
                .stSlider + .stText {
                    font-size: 14px;
                    color: #333;
                    font-style: italic;
                }
            </style>
            <p style="font-size: 14px; color: #333; font-style: italic;">1 = Totalmente innecesario, 6 = Totalmente necesario</p>
        """, unsafe_allow_html=True)

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
def mostrar_ejemplo_csv():
    # Ejemplo de cómo debería verse el CSV
    ejemplo = pd.DataFrame({
        "Descripción": ["Ingreso 1", "Gasto 1", "Ingreso 2", "Gasto 2"],
        "Monto": [1000, 200, 1500, 100],
        "Forma de pago": ["transferencia", "efectivo", "depósito", "efectivo"],
        "Fecha de transacción": ["2024-12-16", "2024-12-16", "2024-12-17", "2024-12-17"],
        "Tipo": ["Ingreso", "Gasto", "Ingreso", "Gasto"]
    })
    st.write("Ejemplo de formato CSV para carga correcta: (no escribas acentos ni caracteres especiales)")
    st.write(ejemplo)

# Ejecutar la aplicación
if __name__ == "__main__":
    app()
