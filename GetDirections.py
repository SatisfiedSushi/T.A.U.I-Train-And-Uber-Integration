import googlemaps
from datetime import datetime
import polyline
import requests

api_key = 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM'

gmaps = googlemaps.Client(key=api_key)


def map_inputs(lat, long):
    # Generate markers for location
    label = 'P'
    marker_color = 'green'
    marker = f'markers=color:{marker_color}|label:{label}|{lat},{long}&'

    return marker


def get_address_from_lat_lng(latitude, longitude, api_key):
    # Define the Google Maps Geocoding API endpoint
    geocode_api = "https://maps.googleapis.com/maps/api/geocode/json"
    # Prepare the parameters
    params = {
        "latlng": f"{latitude},{longitude}",
        "key": api_key,  # Replace with your Google Maps API key
    }
    # Send a GET request to the Geocoding API
    response = requests.get(geocode_api, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK" and len(data["results"]) > 0:
            # Extract the formatted address from the first result
            formatted_address = data["results"][0]["formatted_address"]
            return formatted_address
        else:
            return "Address not found"
    else:
        return "Error fetching address"

def get_transit_directions(start, end):
    transit_directions = gmaps.directions(
        start,
        end,
        mode="transit",
        departure_time=datetime.now(),
        transit_mode="bus|rail",  # Specify transit modes (e.g., bus and subway)
    )
    return transit_directions

def get_driving_directions(start, end):
    driving_directions = gmaps.directions(
        start,
        end,
        mode="driving",
        departure_time=datetime.now(),
    )
    return driving_directions

def combine_directions(transit_directions, driving_directions, end_point):
    # Get driving directions from the last transit stop to the final destination
    last_transit_stop = None
    for step in reversed(transit_directions[0]['legs'][0]['steps']):
        if step['travel_mode'] == 'TRANSIT':
            last_transit_stop = step.get('transit_details', {}).get('arrival_stop', {}).get('name')
            if last_transit_stop:
                break

    if last_transit_stop:
        last_transit_stop_location = f"{last_transit_stop}, Chicago, IL"
        final_driving_directions = gmaps.directions(
            last_transit_stop_location,
            end_point,
            mode="driving",
            departure_time=datetime.now(),
        )
        combined_directions = driving_directions + final_driving_directions
    else:
        combined_directions = driving_directions

    return combined_directions

def calculate_total_time(directions):
    total_time = 0
    for step in directions:
        if 'duration' in step:
            total_time += step['duration']['value']
    return total_time

def calculate_total_distance(directions):
    total_distance = 0
    for step in directions:
        if 'distance' in step:
            total_distance += step['distance']['value']
    return total_distance

# Get driving directions for transit and final leg
def get_driving_directions_for_transit_steps(transit_steps, start_point):
    driving_directions = []
    for step in transit_steps:
        if step['travel_mode'] == 'TRANSIT':
            station_name = step.get('transit_details', {}).get('arrival_stop', {}).get('name')
            if station_name:
                station_location = f"{station_name}, Chicago, IL"
                driving_direction = get_driving_directions(start_point, station_location)
                driving_directions.extend(driving_direction)
        elif step['travel_mode'] == 'WALKING' or step['travel_mode'] == 'DRIVING':
            driving_directions.append(step)
    return driving_directions

def get_transit_stops(transit_steps):
    transit_stops = []
    for step in transit_steps:
        if step['travel_mode'] == 'TRANSIT':
            transit_stops.append(step.get('transit_details', {}).get('arrival_stop', {}).get('name'))
    return transit_stops

def extract_transit_steps(directions):
    transit_steps = []

    for step in directions[0]['legs'][0]['steps']:
        if step['travel_mode'] == 'TRANSIT':
            transit_steps.append(step)

    return transit_steps

def get_chosen_route_data(start, end):
    transit_directions = get_transit_directions(start, end)
    driving_directions = get_driving_directions(start, end)

    transit_time = calculate_total_time(transit_directions)
    driving_time = calculate_total_time(driving_directions)

    transit_steps = extract_transit_steps(transit_directions)
    transit_stops = get_transit_stops(transit_steps)

    if transit_stops:
        chosen_directions = transit_directions
        chosen_mode = "Transit"
    else:
        chosen_directions = driving_directions
        chosen_mode = "Driving"

    # Calculate distance and time for the chosen route
    chosen_distance = calculate_total_distance(chosen_directions)
    chosen_time = calculate_total_time(chosen_directions)

    transit_steps = transit_directions[0]['legs'][0]['steps']
    transit_stops = []
    for step in transit_steps:
        if step['travel_mode'] == 'TRANSIT':
            stop_name = step['transit_details']['arrival_stop']['name']
            stop_location = step['transit_details']['arrival_stop']['location']
            transit_stops.append({"name": stop_name, "location": stop_location})

    return {
        "mode": chosen_mode,
        "distance": chosen_distance,
        "time": chosen_time,
        "departure_time": transit_directions[0]['legs'][0]['departure_time']['text'],
        "arrival_time": transit_directions[0]['legs'][0]['arrival_time']['text'],
        "directions": chosen_directions,
        "transit_stops": transit_stops
    }

# Function to decode polyline points
def decode_polyline(polyline_str):
    return polyline.decode(polyline_str)
def extract_polyline(directions):
    # Extract the path from the directions response
    path = []
    for step in directions[0]['legs'][0]['steps']:
        path.extend(decode_polyline(step['polyline']['points']))

    # Generate the path as a string for the static map
    path_color = '0x0000ff'
    path_weight = 5
    path_string = f'color:{path_color}|weight:{path_weight}|'
    path_string += '|'.join([f"{lat},{lng}" for lat, lng in path])

    return path_string
