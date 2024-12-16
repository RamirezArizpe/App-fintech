# Función para análisis matemático de finanzas personales
def analisis_finanzas_personal(df):
    """
    Transforma análisis matemático en insights financieros útiles
    """
    st.header("🔍 Análisis Inteligente de tus Finanzas")

    # 1. Patrones de Gasto
    st.write("### Patrones de Gasto")
    # Filtrar los gastos por tipo de pago para identificar patrones
    gastos_por_categoria = df[df['Tipo'] == 'Gasto'].groupby('Forma de pago')['Monto'].sum().reset_index()
    gastos_por_categoria = gastos_por_categoria.sort_values(by='Monto', ascending=False)
    st.write(gastos_por_categoria)

    # 2. Gasto por mes
    st.write("### Gasto Mensual Total")
    gastos_mensuales = df[df['Tipo'] == 'Gasto'].groupby(df['Fecha'].dt.to_period('M'))['Monto'].sum()
    st.write(gastos_mensuales)

    # 3. Análisis de tendencias de gasto
    st.write("### Tendencias de Gasto")
    tendencias_gasto = df[df['Tipo'] == 'Gasto'].groupby(df['Fecha'].dt.to_period('M'))['Monto'].sum()
    fig_tendencias = plt.figure(figsize=(8, 5))
    plt.plot(tendencias_gasto.index.astype(str), tendencias_gasto, label='Gastos', color='red', marker='o')
    plt.xlabel("Mes")
    plt.ylabel("Monto en Pesos")
    plt.title("Tendencia de Gasto Mensual")
    plt.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig_tendencias)

    # 4. Comparación de ingresos y gastos
    st.write("### Comparación de Ingresos vs Gastos")
    ingresos_total = df[df['Tipo'] == 'Ingreso']['Monto'].sum()
    gastos_total = df[df['Tipo'] == 'Gasto']['Monto'].sum()
    st.write(f"- **Total de Ingresos**: ${ingresos_total:.2f}")
    st.write(f"- **Total de Gastos**: ${gastos_total:.2f}")
    balance = ingresos_total - gastos_total
    st.write(f"- **Balance Neto**: ${balance:.2f}")
    if balance < 0:
        st.warning("⚠️ ¡Alerta! Tus gastos superan tus ingresos. Considera revisar tu presupuesto.")

# Incluir llamada a la nueva función `analisis_finanzas_personal` en el flujo principal
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
        
        # Llamar a la función de análisis inteligente de finanzas
        analisis_finanzas_personal(df)

# Llamar a la función de análisis en el flujo principal
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

# Ejecutar la aplicación
if __name__ == "__main__":
    app()
