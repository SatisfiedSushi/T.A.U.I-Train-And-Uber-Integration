# defunct, kept for reference
# initial attempt at a backend, read at your own risk

import pandas as pd
import pprint

import requests
import datetime
from fuzzywuzzy import fuzz

origin_stop = ""
destination_stop = ""

df = pd.read_excel('CTA train addresses.xlsx')
station_names = df['station name'].tolist()
cta_station_IDs = df['cta station id'].tolist()

# convert to dict
cta_to_gmaps_ID_mapping = dict(zip(station_names, cta_station_IDs))
user_location_lat_lng = None
# Gets directions from one location to another

# gmaps = googlemaps.Client(key='AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM')

def get_address_from_place_ID(place_id, api_key):
    gmaps_places_api = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_address&key={api_key}"
    response = requests.get(gmaps_places_api)
    data = response.json()
    if 'result' in data:
        return data['result']['formatted_address']
    else:
        return None

def find_closest_matching_string_with_fuzzywuzzy(string, list_of_strings):
    highest_score = 0
    closest_match = None
    for str in list_of_strings:
        score = fuzz.ratio(string, str)
        if score > highest_score:
            highest_score = score
            closest_match = str
    return closest_match, highest_score

# print(f'Closest string: {find_closest_matching_string_with_fuzzywuzzy("Jackson & Austin Terminal, Northeastbound, Bus Terminal", cta_to_gmaps_ID_mapping.keys())}')


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


def convert_miles_to_meters(miles):
    return miles * 1609.34

def get_cta_data_of_Station(station_id, api_key):
    api_url = f"http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={api_key}&mapid={station_id}&outputType=JSON"
    response = requests.get(api_url)
    data = response.json()
    # print(data)
    trains = []

    # print all child stations and their ids and arrivals
    if 'ctatt' in data and 'eta' in data['ctatt']:
        for i, eta in enumerate(data['ctatt']['eta']):
            '''print(f"Train {i + 1}:")
            print(f"  stpId: {eta['stpId']}")
            print(f"  Direction: {'Northbound' if eta['trDr'] == '1' else 'Southbound'}")
            print(f"  Destination: {eta['destNm']}")
            print(f"  Arrival Time: {eta['arrT']}")
            print(f"  Run Number: {eta['rn']}")'''
            trains.append({'stpId': eta['stpId'], 'Direction': 'Northbound' if eta['trDr'] == '1' else 'Southbound', 'Destination': eta['destNm'], 'Arrival Time': eta['arrT'], 'Run Number': eta['rn']})

        print(trains)
        return trains

def get_common_run_number(origin_station_id, destination_station_id, direction, api_key):
    origin_trains = get_cta_data_of_Station(origin_station_id, api_key) # list of trains
    destination_trains = get_cta_data_of_Station(destination_station_id, api_key) # list of trains
    common_trains = []
    print(f'Origin station id: {origin_station_id}')
    print(f'Destination station id: {destination_station_id}')
    print(f'Origin trains: {origin_trains}')
    print(f'Destination trains: {destination_trains}')
    if origin_trains is None or destination_trains is None:
        print("No common trains found.")
        return
    for origin_train in origin_trains:
        for destination_train in destination_trains:
            if origin_train['Run Number'] == destination_train['Run Number']:
                common_trains.append(origin_train)

    if len(common_trains) == 0:
        print("No common trains found.")
        return
    else:
        print(f"Common trains: {common_trains}")
        fastest_train = common_trains[0]
        fastest_time = datetime.datetime.max
        for train in common_trains:
            print(train)
            if train['Direction'] == direction:
                arrival_time = datetime.datetime.strptime(train['Arrival Time'], "%Y-%m-%dT%H:%M:%S")
                if arrival_time < fastest_time:
                    fastest_time = arrival_time
                    fastest_train = train
        print(f"Fastest train: {fastest_train}")
        print(f"Fastest time: {fastest_time}")
        return fastest_train

# print(f'common run number{get_common_run_number(40370, 41330, "Southbound", "4a8cc4d9702a4087af064b1fc18f00d9")}')

'''print(get_cta_data_of_Station(41330, "4a8cc4d9702a4087af064b1fc18f00d9"))
print(get_cta_data_of_Station(40370, "4a8cc4d9702a4087af064b1fc18f00d9"))'''

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

def get_place_id(address, api_key, type="Train Station"):
    old_address = address
    address = f'{address} {type}'
    print(address)
    location = get_lat_lng_from_address(address, api_key)
    if location is None:
        if type == "Train Station":
            return get_place_id(old_address, api_key, "Subway Station")
        if type == "Subway Station":
            return get_place_id(old_address, api_key, "Station")
        if type == "Station":
            return get_place_id(old_address, api_key, "CTA Train Station")
        if type == "CTA Train Station":
            return get_place_id(old_address, api_key, "CTA Subway Station")
        print("Unable to get location from address.")
        return

    gmaps_places_api = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius=10000&type=train_station&key={api_key}"
    response = requests.get(gmaps_places_api)
    data = response.json()

    if 'results' in data and len(data['results']) > 0:
        return data['results'][0]['place_id']
    else:
        return None

def get_lat_lng_from_address(address, api_key, type="Train Station"):
    old_address = address
    address = f'{address} {type}' if type != 'place' else address
    geocode_api = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(geocode_api)
    data = response.json()

    print(address)
    print(data)
    if 'results' in data and len(data['results']) > 0:
        location = data['results'][0]['geometry']['location']

        if location is None:
            if type == "Train Station":
                return get_lat_lng_from_address(old_address, api_key, "Subway Station")
            if type == "Subway Station":
                return get_lat_lng_from_address(old_address, api_key, "Station")
            if type == "Station":
                return get_lat_lng_from_address(old_address, api_key, "CTA Train Station")
            if type == "CTA Train Station":
                return get_lat_lng_from_address(old_address, api_key, "CTA Subway Station")
            print("Unable to get location from address.")
            return
        return f"{location['lat']},{location['lng']}"
    else:
        return None

print(get_lat_lng_from_address(get_address_from_name('Seafood City Supermarket', 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM'), 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM', 'place'))

#get_lat_lng_from_address(get_address_from_name("Jackson & Austin Terminal, Northeastbound, Bus Terminal", "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM"), "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM")

def get_nearest_trains_in_radius(radius, address, api_key):
    radius = convert_miles_to_meters(radius)
    location = get_lat_lng_from_address(address, api_key, 'place')
    nearest_stations = []

    if location is None:
        print("Unable to get location from address.")
        return None

    gmaps_places_api = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type=train_station&key={api_key}"
    response = requests.get(gmaps_places_api)
    data = response.json()

    if 'results' in data:
        for i, result in enumerate(data['results']):
            if find_closest_matching_string_with_fuzzywuzzy(result['name'], cta_to_gmaps_ID_mapping.keys())[1] > 70:
                print(f"Train Station {i + 1}:")
                print(f"  Name: {result['name']}")
                print(f"  Place ID: {result['place_id']}")
                #print(f"  Station ID: {cta_to_gmaps_ID_mapping[result['place_id']]}")
                nearest_stations.append((find_closest_matching_string_with_fuzzywuzzy(result['name'], cta_to_gmaps_ID_mapping.keys())[0], result['place_id'], cta_to_gmaps_ID_mapping[find_closest_matching_string_with_fuzzywuzzy(result['name'], cta_to_gmaps_ID_mapping.keys())[0]]))
            else:
                continue

        print(f'Nearest stations: {nearest_stations}')
        return nearest_stations
    else:
        print("No train stations found.")
        return None

# uses get_nearest_trains_in_radius and loops get_common_run_number to find the common train/run/line between two locations
def get_common_train_between_two_stations(origin, destination, api_key):
    radius = 2
    origin_stations = get_nearest_trains_in_radius(radius, origin, api_key)
    destination_stations = get_nearest_trains_in_radius(radius, destination, api_key)

    if len(origin_stations) == 0 or len(destination_stations) == 0:
        radius += 2
        origin_stations = get_nearest_trains_in_radius(radius, origin, api_key)
        destination_stations = get_nearest_trains_in_radius(radius, destination, api_key)


    fastest_origin_station = origin_stations[0]
    fastest_destination_station = destination_stations[0]
    fastest_time = datetime.datetime.max
    direction = 'None'
     #set direction to northbound or southbound deppending on if the origin or the destination is higher up on the map
    if float(get_lat_lng_from_address(get_address_from_name(origin, api_key), api_key, 'place').split(',')[0]) > float(get_lat_lng_from_address(get_address_from_name(destination, api_key), api_key, 'place').split(',')[0]):
        direction = 'Southbound'
    else:
        direction = 'Northbound'

    while radius < 20:
        for origin_station in origin_stations:
            for destination_station in destination_stations:
                if origin_station != destination_station:
                    print(f'Origin station[2]: {origin_station[2]}')
                    run_number = get_common_run_number(origin_station[2], destination_station[2], direction, "4a8cc4d9702a4087af064b1fc18f00d9")
                    if run_number is not None:
                        arrival_time = datetime.datetime.strptime(run_number['Arrival Time'], "%Y-%m-%dT%H:%M:%S")
                        if arrival_time < fastest_time:
                            fastest_time = arrival_time
                            fastest_origin_station = origin_station
                            fastest_destination_station = destination_station
                            '''print(f'New fastest time: {fastest_time}')
                            print(f'New fastest origin station: {fastest_origin_station}')
                            print(f'New fastest destination station: {fastest_destination_station}')'''

        if fastest_time != datetime.datetime.max:
            break
        else:
            radius += 2
            origin_stations = get_nearest_trains_in_radius(radius, origin, api_key)
            destination_stations = get_nearest_trains_in_radius(radius, destination, api_key)

    print(f"Fastest origin station: {fastest_origin_station}")
    print(f"Fastest destination station: {fastest_destination_station}")
    print(f"Fastest time: {fastest_time}")
    print(f'First Uber pickup location: {get_address_from_name(origin, api_key)}')
    print(f'First Uber dropoff location: {get_address_from_place_ID(fastest_origin_station[1], api_key)}')
    print(f'Second Uber pickup location: {get_address_from_place_ID(fastest_destination_station[1], api_key)}')
    print(f'Second Uber dropoff location: {get_address_from_name(destination, api_key)}')

    return fastest_origin_station, fastest_destination_station, fastest_time

origin, destination, time =  get_common_train_between_two_stations(get_address_from_name(origin_stop, "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM"), get_address_from_name(destination_stop, "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM"), "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM")
get_routes(origin, destination, "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM")


# get_nearest_trains_in_radius(10,"5900 n keating", "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM")

def get_place_id(address, api_key, type="Train Station"):
    old_address = address
    address = f'{address} {type}'
    print(address)
    location = get_lat_lng_from_address(address, api_key)
    if location is None:
        if type == "Train Station":
            return get_place_id(old_address, api_key, "Subway Station")
        if type == "Subway Station":
            return get_place_id(old_address, api_key, "Station")
        if type == "Station":
            return get_place_id(old_address, api_key, "CTA Train Station")
        if type == "CTA Train Station":
            return get_place_id(old_address, api_key, "CTA Subway Station")
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

# print(get_train_arrivals("4a8cc4d9702a4087af064b1fc18f00d9", 40680))

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

# gets the fastest common train station between two locations and in their radii
def get_fastest_common_train(origin, destination, api_key):
    origin_stations = get_nearest_trains_in_radius(1,origin,  api_key)
    destination_stations = get_nearest_trains_in_radius(1, destination, api_key)
    common_stations = list(set(origin_stations) & set(destination_stations))
    if len(common_stations) == 0:
        print("No common stations found.")
        return
    else:
        print(f"Common stations: {common_stations}")
        fastest_station = common_stations[0]
        fastest_time = datetime.datetime.max
        for station in common_stations:
            arrivals = get_train_arrivals("4a8cc4d9702a4087af064b1fc18f00d9", station)
            if len(arrivals) > 0:
                arrival_time = datetime.datetime.strptime(arrivals[0], "%Y-%m-%dT%H:%M:%S")
                if arrival_time < fastest_time:
                    fastest_time = arrival_time
                    fastest_station = station
        print(f"Fastest station: {fastest_station}")
        print(f"Fastest time: {fastest_time}")



# get_fastest_common_train("5024 w argyle", "5900 n keating", "AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM")

def map_station_cta2googlemaps(excel_path, api_key):
    df = pd.read_excel(excel_path)
    df['googlemaps'] = df.apply(lambda row: get_place_id(f'{row.iloc[0]}', api_key), axis=1)
    df.to_excel('CTA train addresses.xlsx')

# map_station_cta2googlemaps('CTA train stpids.xlsx', 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM') # DONT EVER RUN THIS UN LESS YOU UNDERSTAND IT

# get_departure_times("blue", "4a8cc4d9702a4087af064b1fc18f00d9")


