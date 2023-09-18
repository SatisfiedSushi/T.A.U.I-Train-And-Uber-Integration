import googlemaps
from datetime import datetime

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

def get_lat_lng_from_address(address, api_key):
    geocode_api = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(geocode_api)
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        location = data['results'][0]['geometry']['location']
        return f"{location['lat']},{location['lng']}"
    else:
        return None

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

def get_place_id(address, api_key):
    location = get_lat_lng_from_address(address, api_key)
    if location is None:
        print("Unable to get location from address.")
        return

    gmaps_places_api = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius=10000&type=train_station&key={api_key}"
    response = requests.get(gmaps_places_api)
    data = response.json()

    if 'results' in data and len(data['results']) > 0:
        return data['results'][0]['place_id']
    else:
        return None

# print(get_place_id("5900 n keating", "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM"))

# returns CTA stop id for a given train station (returns it in a format that CTA api can use)
def get_CTA_station_id(lat, lng, api_key):
    places_api = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=1500&type=train_station&key={api_key}"
    response = requests.get(places_api)
    data = response.json()

    if 'results' in data and len(data['results']) > 0:
        return data['results'][0]['place_id']
    else:
        return None

# Example usage:
place_id = get_place_id(41.8781, -87.6298)
print(f"The place ID is {place_id}")

# uses cta api to get departure times for a given train station
def get_departure_times(train_station, api_key):
    place_id = get_CTA_station_id(train_station, api_key)
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

# get_departure_times("Schiller Park Train Station", "4a8cc4d9702a4087af064b1fc18f00d9")