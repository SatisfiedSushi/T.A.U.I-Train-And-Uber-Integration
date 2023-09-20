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

        # Get path of route
        directions = route_data["directions"]

        # Get locations and markers for each location
        stop_lat = []
        stop_long = []
        for stop in route_data["transit_stops"]:
            stop_lat.append(stop['location']['lat'])
            stop_long.append(stop['location']['lng'])
        start_location = directions[0]['legs'][0]['start_location']
        end_location = directions[0]['legs'][0]['end_location']
        end_lat, end_long = end_location['lat'], end_location['lng']
        start_lat, start_long = start_location['lat'], start_location['lng']

        # Get first and last station lat and long
        stop1_lat = stop_lat[0]
        stop1_long = stop_long[0]
        stop1_address = get_address_from_lat_lng(stop1_lat, stop1_long, api_key)
        stop2_lat = stop_lat[-1]
        stop2_long = stop_long[-1]
        stop2_address = get_address_from_lat_lng(stop2_lat, stop2_long, api_key)
        return render_template('index.html', start=start, end=end, api_key=api_key,
                               start_lat=start_lat, start_long=start_long, end_lat=end_lat, end_long=end_long,
                               stop1_lat=stop1_lat, stop1_long=stop1_long, stop1_address=stop1_address,
                               stop2_lat=stop2_lat, stop2_long=stop2_long, stop2_address=stop2_address)
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
