import tkinter as tk
from tkinter import ttk
import requests
import json
import webbrowser
import os

class TomTomNearbySearch:
    def __init__(self, api_key, latitude, longitude, radius=10000):
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.data = None

    #... (rest of the class remains the same)
    
    def make_request(self):
        url = f"https://api.tomtom.com/search/2/nearbySearch/.json?key={self.api_key}&lat={self.latitude}&lon={self.longitude}&radius={self.radius}&categorySet=7309&connectorSet=IEC62196Type2CableAttached&minPowerKW=22.2&maxPowerKW=43.2"
        response = requests.get(url)
        if response.status_code == 200:
            self.data = response.json()
            return True
        else:
            print(f"Request failed with status code {response.status_code}")
            return False
    
    def save_to_json_file(self, filename):
        if self.data:
            with open(filename, 'w') as file:
                json.dump(self.data, file, indent=4)
            print(f"Dizionario scritto nel file {filename} in modo formattato.")
        else:
            print("Nessun dato da salvare. Esegui prima la richiesta.")
    
    def extract_google_maps_urls(self):
        if self.data:
            results = self.data.get('results', [])
            google_maps_urls = []
            for result in results:
                position = result.get('position', {})
                latitude = position.get('lat', '')
                longitude = position.get('lon', '')
                google_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
                google_maps_urls.append(google_maps_url)
            return google_maps_urls
        else:
            print("Nessun dato disponibile per estrarre gli URL di Google Maps.")
            return []

    def generate_html_output(self, filename):
        if self.data and 'results' in self.data:
            html_content = '''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>EV Chargers GeoFind</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #333;
                            color: #fff;
                            margin: 0;
                            padding: 0;
                            background-image: url('images/map_wallpaper.jpg'); /* Aggiungi qui il percorso della tua immagine */
                            background-size: cover; /* Adatta l'immagine per coprire l'intera pagina */
                            background-repeat: no-repeat; /* Evita la ripetizione dell'immagine */
                            background-position: center; /* Centra l'immagine */
                        }
                        h1 {
                            background-color: #222;
                            padding: 10px;
                            text-align: center;
                        }
                        ul {
                            list-style-type: none;
                            padding: 0;
                            text-align: center;
                        }
                        li {
                            padding: 10px;
                            display: inline-block;
                            background-color: #444;
                            margin: 5px;
                        }
                        a {
                            color: #fff;
                            text-decoration: none;
                        }
                        a:hover {
                            text-decoration: underline;
                        }
                    </style>
                </head>
                <body>
                    <h1>EV Chargers vicini:</h1>
                    <ul>
            '''

            for result in self.data['results']:
                name = result.get('poi').get('name', 'N/A')
                address = result.get('address').get('freeformAddress', 'N/A')
                phone = result.get('poi').get('phone', 'N/A')
                postal_code = result.get('address').get('postalCode', 'N/A')
                distance = result.get('dist')
                distance_km = float(distance/1000)
                latitude = result.get('position').get('lat')
                longitude = result.get('position').get('lon')
                google_maps_url = f'https://www.google.com/maps/search/?api=1&query={latitude},{longitude}'

                html_content += f'''
                    <li>
                        <strong>Name:</strong> {name}<br>
                        <strong>Address:</strong> {address}<br>
                        <strong>Phone:</strong> {phone}<br>
                        <strong>Postal Code:</strong> {postal_code}<br>
                        <strong>ATCF Distance (linea d'aria):</strong> {distance_km} Km<br>
                        <a href="{google_maps_url}" target="_blank">View on Google Maps</a><br>
                    </li>
                '''

            html_content += '''
                    </ul>
                </body>
                </html>
            '''

            with open(filename, 'w') as file:
                file.write(html_content)

            print(f"HTML output generated: {filename}")
        else:
            print("No data available to generate HTML.")

    def generate_html_output_old(self, filename):
        google_maps_urls = self.extract_google_maps_urls()
        if google_maps_urls:
            html_content = f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>EV Chargers</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #333;
                            color: #fff;
                            margin: 0;
                            padding: 0;
                        }}
                        h1 {{
                            background-color: #222;
                            padding: 10px;
                            text-align: center;
                        }}
                        ul {{
                            list-style-type: none;
                            padding: 0;
                            text-align: center; /* Allinea il testo al centro */
                        }}
                        li {{
                            padding: 10px;
                            display: inline-block; /* Rende gli elementi lista in linea */
                        }}
                        li:nth-child(odd) {{
                            background-color: #444;
                        }}
                        a {{
                            color: #fff;
                            text-decoration: none;
                        }}
                        a:hover {{
                            text-decoration: underline;
                        }}
                    </style>
                </head>
                <body>
                    <h1>EV Chargers vicini:</h1>
                    <ul>
            '''
            
            for url in google_maps_urls:
                html_content += f'<li><a href="{url}" target="_blank">{url}</a></li>\n'
            
            html_content += '''
                    </ul>
                </body>
                </html>
            '''

            with open(filename, 'w') as file:
                file.write(html_content)
            
            print(f"File HTML generato con successo: {filename}")
        else:
            print("Nessun URL di Google Maps disponibile per generare l'HTML.")

    def open_html_in_browser(self, filename):
        if os.path.exists(filename):
            webbrowser.open(filename)
        else:
            print(f"Errore: il file {filename} non esiste.")
            
            
            
#*************************************************************************************************************************************************************************     
#*************************************************************************************************************************************************************************           
      

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("TomTom Nearby Search")

        # API Key entry
        self.api_key_label = tk.Label(master, text="API Key:")
        self.api_key_label.pack()
        self.api_key_entry = tk.Entry(master, width=40)
        self.api_key_entry.pack()

        # Map selection
        self.map_label = tk.Label(master, text="Select location:")
        self.map_label.pack()
        self.map_frame = tk.Frame(master)
        self.map_frame.pack()
        self.map_lat_label = tk.Label(self.map_frame, text="Latitude:")
        self.map_lat_label.pack(side=tk.LEFT)
        self.map_lat_entry = tk.Entry(self.map_frame, width=20)
        self.map_lat_entry.pack(side=tk.LEFT)
        self.map_lon_label = tk.Label(self.map_frame, text="Longitude:")
        self.map_lon_label.pack(side=tk.LEFT)
        self.map_lon_entry = tk.Entry(self.map_frame, width=20)
        self.map_lon_entry.pack(side=tk.LEFT)
        self.map_button = tk.Button(self.map_frame, text="Select on map", command=self.select_on_map)
        self.map_button.pack(side=tk.LEFT)

        # Radius selection
        self.radius_label = tk.Label(master, text="Radius (meters):")
        self.radius_label.pack()
        self.radius_entry = tk.Entry(master, width=20)
        self.radius_entry.pack()

        # Search button
        self.search_button = tk.Button(master, text="Search", command=self.search)
        self.search_button.pack()

    def select_on_map(self):
        # Open a new window with a map (e.g. Google Maps)
        # Allow user to select a location and get the latitude and longitude
        # Update the entries with the selected location
        pass  # TO DO: implement map selection

    def search(self):
        api_key = self.api_key_entry.get()
        latitude = float(self.map_lat_entry.get())
        longitude = float(self.map_lon_entry.get())
        radius = int(self.radius_entry.get())

        search = TomTomNearbySearch(api_key, latitude, longitude, radius)
        if search.make_request():
            search.save_to_json_file('response.json')
            search.generate_html_output('output.html')
            search.open_html_in_browser('output.html')

root = tk.Tk()
gui = GUI(root)
root.mainloop()
