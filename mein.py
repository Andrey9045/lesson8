import os
import json

from geopy import distance
import requests
import folium
from dotenv import load_dotenv


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def nearest_coffee_shops(b):
    return b['distance']


def main():
    a = input('Где вы находитесь?')
    load_dotenv()
    apikey = os.getenv("TOKEN")
    with open("coffee.json", "r", encoding='cp1251') as my_file:
        file_contents = my_file.read()
    coffee_shops = json.loads(file_contents)
    coffee_coordination = []
    coords = fetch_coordinates(apikey, a)
    new_coords = coords[::-1]

    for shops in coffee_shops:
        coordination = {}
        coords_coffee = shops['geoData']['coordinates']
        new_coords_coffee = coords_coffee[::-1]
        coordination['title'] = shops['Name']
        coordination['distance'] = (distance.distance(
                                        new_coords,
                                        new_coords_coffee
                                        ).km)
        coordination['coor'] = new_coords_coffee
        coffee_coordination.append(coordination)
    coffee_house = sorted(coffee_coordination, key=nearest_coffee_shops)
    five_coffee_house = coffee_house[:5]

    m = folium.Map(new_coords, zoom_start=12)
    for one_coffee_house in five_coffee_house:
        folium.Marker(
            location=one_coffee_house['coor'],
            tooltip="Click me!",
            popup=one_coffee_house['title'],
            icon=folium.Icon(color="green"),
        ).add_to(m)
    m.save("index.html")


if __name__ == '__main__':
    main()
