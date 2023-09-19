import googlemaps
from datetime import datetime
import pandas as pd
import time

# Gets directions from one location to another

# gmaps = googlemaps.Client(key='AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM')

'''
#define locations
start = "4419 N Lamon Ave, Chicago, IL 60630"
end = "Jefferson Park Blue Line Station, Chicago, IL"

# Get directions
directions_result = None
try:
    directions_result = gmaps.directions(start, end, mode="transit", departure_time=datetime.now())

    # The result is a list of directions
    for direction in directions_result:
        for step in direction['legs'][0]['steps']:
            print(step['html_instructions'])
except:
    print("Error: Invalid location(s)")'''

# Gets distance matrix between two locations

'''def compute_routes_matrix(start, end, mode_="transit"):
    try:
        directions_result = gmaps.distance_matrix(start, end, mode=mode_, departure_time=datetime.now())
        return directions_result
    except:
        print("Error: Invalid location(s)")
        return None

print(compute_routes_matrix("4419 N Lamon Ave, Chicago, IL 60630", "Jefferson Park Blue Line Station, Chicago, IL", "transit"))'''

import requests
import datetime

def convert_miles_to_meters(miles):
    return miles * 1609.34

def get_routes(origin, destination, api_key):
    gmaps_directions_api = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&alternatives=true&key={api_key}"
    response = requests.get(gmaps_directions_api)
    data = response.json()
    if 'routes' in data:
        for i, route in enumerate(data['routes']):
            print(f"Route {i + 1}:")
            for leg in route['legs']:
                print(f"  Distance: {leg['distance']['text']}")
                print(f"  Duration: {leg['duration']['text']}")
    else:
        print("No routes found.")

# get_routes("5024 w argyle", "5900 n keating", "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM")

def get_address_from_name(name, api_key):
    gmaps_places_api = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={name}&inputtype=textquery&fields=formatted_address&key={api_key}"
    response = requests.get(gmaps_places_api)
    data = response.json()
    if 'candidates' in data and len(data['candidates']) > 0:
        return data['candidates'][0]['formatted_address']
    else:
        return None

# get_address_from_name("Northside College Preparatory Highschool",'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM')

def get_lat_lng_from_address(address, api_key):
    geocode_api = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(geocode_api)
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        location = data['results'][0]['geometry']['location']
        return f"{location['lat']},{location['lng']}"
    else:
        return None

#get_lat_lng_from_address(get_address_from_name("Jackson & Austin Terminal, Northeastbound, Bus Terminal", "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM"), "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM")

def get_nearest_trains_in_radius(radius, address, api_key):
    radius = convert_miles_to_meters(radius)
    location = get_lat_lng_from_address(address, api_key)
    if location is None:
        print("Unable to get location from address.")
        return

    gmaps_places_api = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type=train_station&key={api_key}"
    response = requests.get(gmaps_places_api)
    data = response.json()

    print(data)

    if 'results' in data:
        for i, result in enumerate(data['results']):
            print(f"Train Station {i + 1}:")
            print(f"  Name: {result['name']}")
            print(f"  Location: {result['geometry']['location']}")
    else:
        print("No train stations found.")

# get_nearest_trains_in_radius(10,"5900 n keating", "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM")

def get_place_id(address, api_key, type="Train Station"):
    '''old_address = address
    address = f'{address} {type}'
    print(address)'''
    location = get_lat_lng_from_address("19 N. Dearborn St., Chicago, IL 60602", api_key)
    if location is None:
        '''if type == "Train Station":
            return get_place_id(old_address, api_key, "Subway Station")
        if type == "Subway Station":
            return get_place_id(old_address, api_key, "Station")
        if type == "Station":
            return get_place_id(old_address, api_key, "CTA Train Station")
        if type == "CTA Train Station":
            return get_place_id(old_address, api_key, "CTA Subway Station")'''
        print("Unable to get location from address.")
        return

    gmaps_places_api = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius=10000&type=train_station&key={api_key}"
    response = requests.get(gmaps_places_api)
    data = response.json()

    if 'results' in data and len(data['results']) > 0:
        return data['results'][0]['place_id']
    else:
        return None


# print(get_place_id(f'Lake', "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM"))

# print(get_place_id("5900 n keating", "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM"))

# uses CTA api to get trainstations in a radius and their arrival times
def get_nearby_train_stations(location, radius, google_api_key):
    lat, lng = get_lat_lng_from_address(location, google_api_key).split(',')
    places_api = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type=train_station&key={google_api_key}"
    response = requests.get(places_api)
    data = response.json()

    if 'results' in data:
        return [result['name'] for result in data['results']]
    else:
        return []

def get_train_arrivals(cta_api_key, stpid):
    api_url = f"http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={cta_api_key}&stpid={stpid}&outputType=JSON"
    response = requests.get(api_url)
    data = response.json()

    if 'ctatt' in data and 'eta' in data['ctatt']:
        return [eta['arrT'] for eta in data['ctatt']['eta']]
    else:
        return []

# Example usage:
'''stations = get_nearby_train_stations("5024 w argyle", 1000000, "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM")
for station in stations:
    arrivals = get_train_arrivals("4a8cc4d9702a4087af064b1fc18f00d9", station)
    print(f"Station: {station}")
    print(f"Arrivals: {arrivals}")
place_id = get_place_id(41.8781, -87.6298)
print(f"The place ID is {place_id}")'''

# uses cta api to get departure times for a given train station
def get_departure_times(train_line, api_key):
    place_id = None
        #get_CTA_train_stations(train_line, api_key)
    cta_api = f"http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={api_key}&mapid={place_id}&outputType=JSON"
    response = requests.get(cta_api)
    data = response.json()
    if 'ctatt' in data and 'eta' in data['ctatt']:
        for i, eta in enumerate(data['ctatt']['eta']):
            print(f"Train {i + 1}:")
            print(f"  Destination: {eta['destNm']}")
            print(f"  Arrival Time: {eta['arrT']}")
    else:
        print("No departure times found.")

def map_station_cta2googlemaps(excel_path, api_key):
    df = pd.read_excel(excel_path)
    df['googlemaps'] = df.apply(lambda row: get_place_id(f'{row.iloc[0]}', api_key), axis=1)
    df.to_excel('CTA train addresses.xlsx')

# map_station_cta2googlemaps('CTA train stpids.xlsx', 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM') # DONT EVER RUN THIS UN LESS YOU UNDERSTAND IT

# get_departure_times("blue", "4a8cc4d9702a4087af064b1fc18f00d9")


