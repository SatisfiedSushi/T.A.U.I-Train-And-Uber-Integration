import googlemaps
from datetime import datetime
import polyline
import requests

api_key = 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM'

gmaps = googlemaps.Client(key=api_key)


def map_inputs(lat, long):
    '''The function "map_inputs" generates markers for a given latitude and longitude.
    
    Parameters
    ----------
    lat
        The `lat` parameter represents the latitude of a location. Latitude is a geographic coordinate that
    specifies the north-south position of a point on the Earth's surface.
    long
        The "long" parameter represents the longitude coordinate of a location.
    
    Returns
    -------
        a string that represents a marker for a specific location on a map. The marker includes the
    latitude and longitude coordinates, as well as a label and marker color.
    
    '''
    # Generate markers for location
    label = 'P'
    marker_color = 'green'
    marker = f'markers=color:{marker_color}|label:{label}|{lat},{long}&'

    return marker


def get_address_from_lat_lng(latitude, longitude, api_key):
    '''The function `get_address_from_lat_lng` takes latitude, longitude, and an API key as input and
    returns the formatted address corresponding to the given coordinates using the Google Maps Geocoding
    API.
    
    Parameters
    ----------
    latitude
        The latitude of the location you want to get the address for.
    longitude
        The longitude parameter is the geographic coordinate that specifies the east-west position of a
    point on the Earth's surface. It is measured in degrees, with values ranging from -180 to 180.
    api_key
        The `api_key` parameter is the API key that you need to obtain from the Google Cloud Platform
    Console in order to use the Google Maps Geocoding API. This key is used to authenticate your
    requests and track your API usage.
    
    Returns
    -------
        The function `get_address_from_lat_lng` returns the formatted address corresponding to the given
    latitude and longitude coordinates. If the address is found, it returns the formatted address as a
    string. If the address is not found or if there is an error fetching the address, it returns an
    appropriate error message as a string.
    
    '''
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
    '''The function `get_transit_directions` uses the Google Maps API to retrieve transit directions
    between a start and end location.
    
    Parameters
    ----------
    start
        The starting location for the transit directions.
    end
        The end parameter is the destination address or location for which you want to get transit
    directions.
    
    Returns
    -------
        the transit directions from the start location to the end location.
    
    '''
    transit_directions = gmaps.directions(
        start,
        end,
        mode="transit",
        departure_time=datetime.now(),
        transit_mode="bus|rail",  # Specify transit modes (e.g., bus and subway)
    )

    if not transit_directions:
        return "Error fetching transit directions"

    return transit_directions

def get_driving_directions(start, end):
    '''The function `get_driving_directions` uses the Google Maps API to retrieve driving directions from a
    starting location to an end location.
    
    Parameters
    ----------
    start
        The starting location for the driving directions.
    end
        The "end" parameter is the destination or the address where you want to get driving directions to.
    
    Returns
    -------
        the driving directions from the start location to the end location.
    
    '''
    driving_directions = gmaps.directions(
        start,
        end,
        mode="driving",
        departure_time=datetime.now(),
    )
    return driving_directions

def combine_directions(transit_directions, driving_directions, end_point):
    '''The function combines transit directions and driving directions, including the final driving
    directions from the last transit stop to the final destination if applicable.
    
    Parameters
    ----------
    transit_directions
        The transit_directions parameter is a list containing the directions for the transit portion of the
    journey. It is assumed to be in the format returned by the Google Maps Directions API.
    driving_directions
        The `driving_directions` parameter is a list of directions for driving from the starting point to
    the last transit stop. Each direction is represented as a dictionary with information such as the
    travel mode, distance, duration, and steps for each leg of the journey.
    end_point
        The `end_point` parameter is the final destination or the address where the user wants to go.
    
    Returns
    -------
        the combined directions, which is a list of steps for both transit and driving directions from the
    starting point to the end point.
    
    '''
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
        if final_driving_directions:
            combined_directions = driving_directions + final_driving_directions
        else:
            return "Error fetching final driving directions"
    else:
        combined_directions = driving_directions

    return combined_directions

def calculate_total_time(directions):
    '''The function calculates the total time based on the duration of each step in a list of directions.
    
    Parameters
    ----------
    directions
        The parameter "directions" is expected to be a list of dictionaries. Each dictionary represents a
    step in a set of directions and should contain a key "duration" which maps to another dictionary
    with a key "value" that represents the duration of the step in seconds.
    
    Returns
    -------
        the total time calculated from the given directions.
    
    '''
    total_time = 0
    for step in directions:
        if 'duration' in step:
            total_time += step['duration']['value']
    return total_time

def calculate_total_distance(directions):
    '''The function calculates the total distance from a list of directions.
    
    Parameters
    ----------
    directions
        The `directions` parameter is expected to be a list of dictionaries. Each dictionary represents a
    step in a set of directions and should contain a key called 'distance' which itself is a dictionary
    containing a key called 'value'. The 'value' key should have a numeric value representing the
    distance of
    
    Returns
    -------
        the total distance calculated from the given directions.
    
    '''
    total_distance = 0
    for step in directions:
        if 'distance' in step:
            total_distance += step['distance']['value']
    return total_distance

# Get driving directions for transit and final leg
def get_driving_directions_for_transit_steps(transit_steps, start_point):
    '''The function `get_driving_directions_for_transit_steps` takes a list of transit steps and a start
    point, and returns a list of driving directions for each transit step.
    
    Parameters
    ----------
    transit_steps
        The `transit_steps` parameter is a list of steps in a transit route. Each step is a dictionary that
    contains information about the step, such as the travel mode (e.g., TRANSIT, WALKING, DRIVING) and
    details about the transit (e.g., arrival stop name
    start_point
        The starting point for the driving directions. It could be an address, a landmark, or any location
    identifier.
    
    Returns
    -------
        a list of driving directions.
    
    '''
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
    '''The function `get_transit_stops` takes a list of transit steps and returns a list of the names of
    the transit stops.
    
    Parameters
    ----------
    transit_steps
        The parameter `transit_steps` is a list of dictionaries. Each dictionary represents a step in a
    transit route. Each step contains information about the mode of travel, such as walking, transit, or
    driving, and additional details about the step, such as the arrival stop for transit steps.
    
    Returns
    -------
        a list of transit stops.
    
    '''
    transit_stops = []
    for step in transit_steps:
        # travel_mode in step check handles an error where the steps are messed up if
        # GMaps can't find a good route and throws an error in get_transit_stops
        if 'travel_mode' in step and step['travel_mode'] == 'TRANSIT':
            transit_stops.append(step.get('transit_details', {}).get('arrival_stop', {}).get('name'))
    return transit_stops

def extract_transit_steps(directions):
    '''The function extracts transit steps from a directions object.
    
    Parameters
    ----------
    directions
        The `directions` parameter is expected to be a list containing a dictionary of directions. The
    dictionary should have a key called 'legs' which maps to a list of dictionaries representing the
    legs of the journey. Each leg should have a key called 'steps' which maps to a list of dictionaries
    representing
    
    Returns
    -------
        a list of transit steps from the given directions.
    
    '''

    #checks if the directions are in a format that means theres an error- usually happens if you're trying to map to a location and GMaps cannot find a path
    if isinstance(directions, str):
        return [{"error_message": directions}]  # Return an error message in a list

    transit_steps = []

    for step in directions[0]['legs'][0]['steps']:
        if step['travel_mode'] == 'TRANSIT':
            transit_steps.append(step)

    return transit_steps

def get_chosen_route_data(start, end):
    '''The function `get_chosen_route_data` calculates the chosen route between two locations, including
    mode of transportation, distance, time, departure and arrival times, directions, and transit stops.
    
    Parameters
    ----------
    start
        The starting location for the route.
    end
        The "end" parameter represents the destination or end point of the route.
    
    Returns
    -------
        a dictionary containing information about the chosen route. The dictionary includes the mode of
    transportation (either "Transit" or "Driving"), the distance and time of the chosen route, the
    departure and arrival times, the directions for the chosen route, and a list of transit stops along
    the route.
    
    '''
    transit_directions = get_transit_directions(start, end)
    driving_directions = get_driving_directions(start, end)

    # Check if transit_directions is a string (error message), usually happens when GMaps fails to route
    if isinstance(transit_directions, str):
        return {"error_message": transit_directions}

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
    '''The function `extract_polyline` takes a directions response and extracts the path as a string for a
    static map.
    
    Parameters
    ----------
    polyline_str
        The `polyline_str` parameter is a string representation of a polyline. A polyline is a compressed
    format for representing a series of geographic coordinates. It is commonly used in mapping
    applications to represent routes or paths.
    
    Returns
    -------
        The function `extract_polyline` returns a string representing the path for a static map.
    
    '''
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
