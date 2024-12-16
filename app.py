def mostrar_analisis(df):
    st.title("Análisis Gráfico e Insights de tus Finanzas")

    # Convertir la columna 'Fecha de transacción' a formato de fecha
    df['Fecha'] = pd.to_datetime(df['Fecha de transacción'])
    
    # Gráfico de Ingresos vs Gastos
    fig = plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Tipo', palette="Set2")
    plt.title("Distribución de Ingresos vs Gastos")
    st.pyplot(fig)

    # Cálculo de la proporción de los ingresos que representan los gastos
    total_ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].sum()
    total_gastos = df[df['Tipo'] == 'Gasto']['Monto'].sum()
    
    if total_ingresos > 0:
        proporcion = total_gastos / total_ingresos
    else:
        proporcion = 0

    # Mostrar la proporción y su interpretación
    st.write(f"### Proporción de los ingresos que representan los gastos:")
    st.write(f"Los gastos representan el {proporcion*100:.2f}% de los ingresos.")
    
    # Explicación
    if proporcion < 0.5:
        st.write("Esto significa que tus ingresos son más altos que tus gastos, lo cual es una señal positiva para tu estabilidad financiera. Estás logrando mantener un balance favorable.")
    elif 0.5 <= proporcion < 1:
        st.write("Tus gastos están cerca de la mitad de tus ingresos. Esto es una situación aceptable, pero es importante seguir monitoreando tus finanzas para evitar que los gastos superen a los ingresos.")
    else:
        st.write("Tus gastos están acercándose o incluso superan a tus ingresos, lo que puede generar problemas financieros a largo plazo. Es recomendable revisar y reducir los gastos para evitar un posible déficit.")

    # Gráfico de ingresos y gastos por mes
    df['Mes-Año'] = df['Fecha'].dt.to_period('M')
    ingresos_mes = df[df['Tipo'] == 'Ingreso'].groupby('Mes-Año')['Monto'].sum()
    gastos_mes = df[df['Tipo'] == 'Gasto'].groupby('Mes-Año')['Monto'].sum()

    fig = plt.figure(figsize=(10, 6))
    plt.plot(ingresos_mes.index.astype(str), ingresos_mes, label="Ingresos", marker='o')
    plt.plot(gastos_mes.index.astype(str), gastos_mes, label="Gastos", marker='o')
    plt.title("Ingresos y Gastos Mensuales")
    plt.xlabel("Mes")
    plt.ylabel("Monto en Pesos")
    plt.legend()
    st.pyplot(fig)
    
    # Gráfico interactivo de formas de pago (usando Plotly)
    fig = px.pie(df, names='Forma de pago', title='Distribución de Formas de Pago')
    st.plotly_chart(fig)

    # Insights de los datos
    st.write("### Insights:")
    st.write(f"- **Total de Ingresos**: ${total_ingresos:.2f}")
    st.write(f"- **Total de Gastos**: ${total_gastos:.2f}")
    balance = total_ingresos - total_gastos
    st.write(f"- **Balance Neto**: ${balance:.2f}")
    promedio_ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].mean()
    promedio_gastos = df[df['Tipo'] == 'Gasto']['Monto'].mean()
    st.write(f"- **Promedio de Ingresos**: ${promedio_ingresos:.2f}")
    st.write(f"- **Promedio de Gastos**: ${promedio_gastos:.2f}")

    # Estadísticas de las formas de pago
    formas_pago_counts = df['Forma de pago'].value_counts()
    st.write("### Frecuencia de Formas de Pago:")
    st.write(formas_pago_counts)
