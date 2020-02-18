import folium
from geopy.geocoders import Nominatim

import data_base
import provider

def build_map(loc, capital, year, latitude, longitude, preference, coords='city_coordinates.tsv'):
    '''
    Builds a map and saves it in a HTML file
    depending whether you are willing to use maps provider or database file
    '''

    map = folium.Map(location=[latitude, longitude],
                    zoom_start=10)

    fg_cm = folium.FeatureGroup(name='Close Filmed Movies')

    if preference == 'provider':
        method = provider.prepare_movies_map(loc, year, latitude, longitude)
    elif preference == 'database':
        method = data_base.prepare_movies_map(loc, coords, year, latitude, longitude)

    for movie, lat, lng in method:
        fg_cm.add_child(folium.CircleMarker(location=[lat, lng],
                                            radius=10,
                                            popup=movie,
                                            fill_color='green',
                                            color='red',
                                            fill_opacity=0.5))

    fg_capitals = folium.FeatureGroup(name='World Capitals')

    for country, city, lat, lng in data_base.read_capitals(capital):
        fg_capitals.add_child(folium.CircleMarker(location=[lat, lng],
                                                  radius=10,
                                                  popup=f"{country}'s capital is {city}!",
                                                  fill_color='yellow',
                                                  color='blue',
                                                  fill_opacity=0.5))

    map.add_child(fg_cm)
    map.add_child(fg_capitals)
    map.add_child(folium.LayerControl())
    map.save(f"{str(year)}_movies_map.html")


def run():
    '''
    Runs and operates the program
    '''
    year = int(input('Please enter the year you would like to have a map for: '))
    location = str(input('Please enter your location (format: lat, long): '))
    print()
    print('Please enter the preference to be used for the map to be generated with')
    print('NOTE: database searches for broader locations, if closer not found; while provider just in your region!')
    mode = str(input('Enter: database/provider: '))
    latitude, longitude = location.split(',')
    latitude, longitude = float(latitude), float(longitude)
    print('Map is generating...')
    print('Please wait...')
    build_map('locations.list', 'capitals.csv', year, latitude, longitude, mode)
    print(f"Finished. Please have look at the map {str(year)}_movies_map.html")

run()
