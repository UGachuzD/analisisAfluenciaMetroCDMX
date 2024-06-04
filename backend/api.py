from flask import Flask, request, render_template_string
import folium
import json
import pandas as pd

app = Flask(__name__)

class Estacion:
    def __init__(self, nombre, linea, latitud, longitud):
        self.nombre = nombre
        self.linea = linea
        self.latitud = latitud
        self.longitud = longitud

def obtenerAfluenciaMesAnioLinea(df, linea, mes, anio):
    dfFiltrado = df[(df['anio'] == anio) & (df['mes'] == mes) & (df['linea'] == linea)]
    sumaAfluenciaEstacion = dfFiltrado.groupby('estacion')['afluencia'].sum()
    return sumaAfluenciaEstacion

@app.route('/map')
def map():
    mes = request.args.get('mes')
    anio = request.args.get('anio')

    if not mes or not anio:
        return folium.Map(location=[19.4163340855965, -99.0747357270116], zoom_start=12, tiles='CartoDB positron')._repr_html_()

    anio = int(anio)

    df = pd.read_csv('afluenciastc_simple_02_2024.csv', sep=',')
    df['linea'] = df['linea'].apply(lambda x: x.replace('Linea ', ''))

    with open('STC_Metro_estaciones.geojson', encoding='utf-8') as f:
        data = json.load(f)

    mapa = folium.Map(location=[19.4163340855965, -99.0747357270116], zoom_start=12, tiles='CartoDB positron')

    lineas = {}
    dEstaciones = {}

    lineasColores = {
        "1": "#E30A45",
        "2": "#0000FF",
        "3": "#808000",
        "4": "#00FFFF",
        "5": "#FFFF00",
        "6": "#FF0000",
        "7": "#FFA500",
        "8": "#008000",
        "9": "#A52A2A",
        "A": "#800080",
        "B": "#696969",
        "12": "#FFD700",
    }

    for feature in data['features']:
        nombre = feature['properties']['NOMBRE']
        linea = feature['properties']['LINEA']
        latitud, longitud = feature['geometry']['coordinates'][::-1]
        if linea not in lineas:
            lineas[linea] = []
        lineas[linea].append((latitud, longitud))
        dEstaciones[nombre] = Estacion(nombre, linea, latitud, longitud)

        folium.CircleMarker(
            location=(latitud, longitud),
            radius=5,
            color=lineasColores.get(linea, '#000000'),
            fill=True,
            fill_color=lineasColores.get(linea, '#000000'),
            fill_opacity=0.7,
            popup=nombre
        ).add_to(mapa)

    for estacion in dEstaciones.values():
        lineaAfluencia = obtenerAfluenciaMesAnioLinea(df, estacion.linea, mes, anio)
        if estacion.nombre in lineaAfluencia:
            afluencia = lineaAfluencia[estacion.nombre]
            folium.Marker(
                location=(estacion.latitud, estacion.longitud),
                popup=f"{estacion.nombre} ({estacion.linea}): {afluencia}",
            ).add_to(mapa)

    for linea, estaciones in lineas.items():
        color = lineasColores.get(linea, '#000000')
        folium.PolyLine(estaciones, color=color, weight=2.5, opacity=1, popup=linea).add_to(mapa)

    return mapa._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)
