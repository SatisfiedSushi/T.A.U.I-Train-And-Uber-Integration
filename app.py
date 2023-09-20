from flask import Flask, Response, render_template, request, send_from_directory
import json
from MapEmbed import map_inputs
from UberDeepLink import addy_to_lat_long
from GoogleMapsAPIs import *

api_key = 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM'

app = Flask(__name__)


@app.route('/' , methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        start_lat, start_long, end_lat, end_long = addy_to_lat_long(start, end, api_key)
        return render_template('input.html', start=start, end=end, api_key=api_key, start_lat=start_lat, start_long=start_long, end_lat=end_lat, end_long=end_long)
    return render_template('input.html', start='', end='', api_key=api_key)


@app.route('/receive_location_data', methods=['GET'])
def receive_location_data():
    lat = request.args.get('latitude')
    long = request.args.get('longitude')
    accuracy = request.args.get('accuracy')
    print(lat, long, accuracy)
    address = get_address_from_lat_lng(lat, long, api_key)
    return address


if __name__ == '__main__':
    app.run(debug=True)
