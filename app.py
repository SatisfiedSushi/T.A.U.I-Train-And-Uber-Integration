from flask import Flask, render_template, request
from GetDirections import *

api_key = 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM'

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    '''The `index()` function retrieves route data based on user input, extracts relevant information from
    the data, and renders an HTML template with the extracted information.

    Returns
    -------
        The function `index()` returns a rendered template called 'index.html' with various variables
    passed to it. The variables include `start`, `end`, `api_key`, `start_lat`, `start_long`, `end_lat`,
    `end_long`, `stop1_lat`, `stop1_long`, `stop1_address`, `stop2_lat`, `stop2_long`, and
    `stop2_address

    '''
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        # Get the route data
        route_data = get_chosen_route_data(start, end)

        # Check if 'directions' key exists in route_data
        if 'directions' in route_data:
            directions = route_data["directions"]
        else:
            directions = "No directions available"

        # Check if directions is a string (indicating an error)
        if isinstance(directions, str):
            return render_template('index.html', start=(start + " ERROR- invalid route"), end=(end + " ERROR- invalid route"), api_key=api_key)  # Pass an error message to the template

        # Get locations and markers for each location
        stop_lat = []
        stop_long = []
        transit_stops = route_data.get("transit_stops", [])  # Default to an empty list if missing
        for stop in transit_stops:
            stop_lat.append(stop['location']['lat'])
            stop_long.append(stop['location']['lng'])
        start_location = directions[0]['legs'][0]['start_location']
        end_location = directions[0]['legs'][0]['end_location']
        end_lat, end_long = end_location['lat'], end_location['lng']
        start_lat, start_long = start_location['lat'], start_location['lng']

        # Get first and last station lat and long
        stop1_lat = stop_lat[0] if stop_lat else 0
        stop1_long = stop_long[0] if stop_long else 0
        stop1_address = get_address_from_lat_lng(stop1_lat, stop1_long, api_key) if stop_lat else ""
        stop2_lat = stop_lat[-1] if stop_lat else 0
        stop2_long = stop_long[-1] if stop_long else 0
        stop2_address = get_address_from_lat_lng(stop2_lat, stop2_long, api_key) if stop_lat else ""

        return render_template('index.html', start=start, end=end, api_key=api_key,
                               start_lat=start_lat, start_long=start_long, end_lat=end_lat, end_long=end_long,
                               stop1_lat=stop1_lat, stop1_long=stop1_long, stop1_address=stop1_address,
                               stop2_lat=stop2_lat, stop2_long=stop2_long, stop2_address=stop2_address,
                               directions=directions)
    return render_template('index.html', start='', end='', api_key=api_key)


@app.route('/receive_location_data', methods=['GET'])
def receive_location_data():
    '''The function receives latitude and longitude data of the user, uses an API key to get the corresponding address,
    and returns the address.

    Returns
    -------
        The address of the current location of the user corresponding to the latitude and longitude provided.
    
    '''
    lat = request.args.get('latitude')
    long = request.args.get('longitude')
    address = get_address_from_lat_lng(lat, long, api_key)
    return address


if __name__ == '__main__':
    app.run(debug=True)
