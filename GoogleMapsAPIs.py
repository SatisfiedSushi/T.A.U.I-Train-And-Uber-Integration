import googlemaps
from datetime import datetime

# Gets directions from one location to another

gmaps = googlemaps.Client(key='AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM')

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
import json

def get_directions(origin, destination, api_key):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&alternatives=true&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'routes' in data:
        for i, route in enumerate(data['routes']):
            print(f"Route {i + 1}:")
            for leg in route['legs']:
                print(f"  Distance: {leg['distance']['text']}")
                print(f"  Duration: {leg['duration']['text']}")
    else:
        print("No routes found.")

get_directions("5024 w argyle", "5900 n keating", "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM")

