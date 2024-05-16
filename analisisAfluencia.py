import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("Analisis de datos afluencia metro CDMX")
    df = pd.read_csv('afluenciastc_simple_02_2024.csv', sep=',')
    columns = df.columns
    columsExclude = ['fecha', 'afluencia']
    dataType = df.dtypes
    # print(dataType)

    dUniqueValues = {}

    for column in columns:
        if column not in columsExclude:
            dUniqueValues[column] = df[column].unique()

    print("Valores únicos por columna:")
    for column, uniqueValues in dUniqueValues.items():
        print(f"{column}: {uniqueValues}")

    """ Analisis """
    # Cantidad de pasajeros anual en cada mes por cada linea
    # meses = dUniqueValues['mes']
    # anios = dUniqueValues['anio']
    # lineas = dUniqueValues['linea']
    # estaciones = dUniqueValues['estacion']

    mes = 'Enero'
    anio = 2020
    linea = '3'

    # Filtro
    dfFiltrado = df[(df['anio'] == anio) & (df['mes'] == mes) & (df['linea'] == linea)]
    sumaAfluenciaEstacion = dfFiltrado.groupby('estacion')['afluencia'].sum()

    # Imprimir resultados (Serie de pandas)
    print(sumaAfluenciaEstacion)
    
    # Graficar los datos
    etiquetas = sumaAfluenciaEstacion.index.to_list()
    alturas = sumaAfluenciaEstacion.values.tolist()

    plt.figure(figsize=(14, 8))
    bars = plt.bar(etiquetas, alturas)
    plt.bar(etiquetas, alturas)
    plt.xlabel('Estaciones')
    plt.ylabel('Afluencia')
    plt.ticklabel_format(style='plain', axis='y')
    plt.xticks(rotation='vertical')
    plt.title(f'Afluencia metro CDMX {mes} {anio} {linea}')

    # Agregar los valores de Y a cada barra
    for bar, altura in zip(bars, alturas):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), altura, ha='center', va='bottom')

    plt.show()


