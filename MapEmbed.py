import googlemaps
import polyline


# Replace with your own API key
api_key = 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM'

# Initialize the Google Maps client
gmaps = googlemaps.Client(api_key)

# Function to decode polyline points
def decode_polyline(polyline_str):
    return polyline.decode(polyline_str)
def map_inputs(start, end):
    start, end = start, end

    # Get directions
    directions = gmaps.directions(start, end)

    # Extract the path from the directions response
    path = []
    for step in directions[0]['legs'][0]['steps']:
        path.extend(decode_polyline(step['polyline']['points']))

    # Generate the path as a string for the static map
    path_color = '0x0000ff'
    path_weight = 5
    path_string = f'color:{path_color}|weight:{path_weight}|'
    path_string += '|'.join([f"{lat},{lng}" for lat, lng in path])


    # Get coordinates of start and end locations
    start_location = directions[0]['legs'][0]['start_location']
    end_location = directions[0]['legs'][0]['end_location']

    # Generate markers for start and end locations
    start_label = 'S'
    end_label = 'E'
    start_marker_color = 'green'
    end_marker_color = 'red'
    markers = f'markers=color:{start_marker_color}|label:{start_label}|{start_location["lat"]},{start_location["lng"]}&'
    markers += f'markers=color:{end_marker_color}|label:{end_label}|{end_location["lat"]},{end_location["lng"]}'

    return start, end, path_string, markers

