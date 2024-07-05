import folium

#  CODICE DI PROVA!  

# Dati ricevuti dall'API
charging_stations = [
    {
        'name': 'Queenergy S.r.l.',
        'address': 'Viale Col di Lana 2, 20136 Milano',
        'lat': 45.452128,
        'lon': 9.181988,
        'connectors': [
            {'type': 'Chademo', 'power': 60},
            {'type': 'IEC62196Type2CableAttached', 'power': 41},
            {'type': 'IEC62196Type2Outlet', 'power': 21},
            {'type': 'IEC62196Type2CCS', 'power': 60}
        ]
    },
    # Aggiungi gli altri caricabatterie come dizionari qui...
]

# Crea una mappa centrata sulla posizione media dei caricabatterie
map_center = [45.4642, 9.19]
m = folium.Map(location=map_center, zoom_start=13)

# Aggiungi i marker per ciascun caricabatterie
for station in charging_stations:
    folium.Marker(
        location=[station['lat'], station['lon']],
        popup=(
            f"<strong>{station['name']}</strong><br>"
            f"{station['address']}<br>"
            f"Connectors:<br>"
            + "<br>".join([f"{c['type']}: {c['power']} kW" for c in station['connectors']])
        ),
        tooltip=station['name']
    ).add_to(m)

# Salva la mappa in un file HTML
m.save("charging_stations_map.html")
