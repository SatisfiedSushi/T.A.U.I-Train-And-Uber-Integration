from flask import Flask, Response, render_template, request, send_from_directory
import json

from MapEmbed import map_inputs
from GetDirections import *

# from GoogleMapsAPIs import *

api_key = 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM'

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        # Get the route data
        route_data = get_chosen_route_data(start, end)
        # Extract individual parts into variables
        mode = route_data["mode"]
        distance = route_data["distance"]
        time = route_data["time"]
        departure_time = route_data["departure_time"]
        arrival_time = route_data["arrival_time"]

        # Get path of route
        directions = route_data["directions"]
        path = extract_polyline(directions)

        # Get locations and markers for each location
        stop_lat = []
        stop_long = []
        markers = []
        for stop in route_data["transit_stops"]:
            stop_lat.append(stop['location']['lat'])
            stop_long.append(stop['location']['lng'])
            markers.append(map_inputs(stop['location']['lat'], stop['location']['lng']))
        start_location = directions[0]['legs'][0]['start_location']
        end_location = directions[0]['legs'][0]['end_location']
        end_lat, end_long = end_location['lat'], end_location['lng']
        start_lat, start_long = start_location['lat'], start_location['lng']
        markers.append(map_inputs(start_lat, start_long))
        markers.append(map_inputs(end_lat,end_long))

        # Get first and last station lat and long
        stop1_lat = stop_lat[0]
        stop1_long = stop_long[0]
        stop1_address = get_address_from_lat_lng(stop1_lat, stop1_long, api_key)
        stop2_lat = stop_lat[-1]
        stop2_long = stop_long[-1]
        stop2_address = get_address_from_lat_lng(stop2_lat, stop2_long, api_key)
        return render_template('index.html', start=start, end=end, api_key=api_key, markers=markers, mode=mode,
                               distance=distance, time=time, departure_time=departure_time, arrival_time=arrival_time,
                               start_lat=start_lat, start_long=start_long, end_lat=end_lat, end_long=end_long,
                               stop1_lat=stop1_lat, stop1_long=stop1_long, stop1_address=stop1_address, stop2_lat=stop2_lat, stop2_long=stop2_long, stop2_address=stop2_address, path=path)
    return render_template('index.html', start='', end='', api_key=api_key)


@app.route('/receive_location_data', methods=['GET'])
def receive_location_data():
    lat = request.args.get('latitude')
    long = request.args.get('longitude')
    address = get_address_from_lat_lng(lat, long, api_key)
    return address


if __name__ == '__main__':
    app.run(debug=True)
