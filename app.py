from flask import Flask, render_template, request, jsonify
from MapEmbed import map_inputs
from UberDeepLink import addy_to_lat_long
from GetLocation import get_current_location

api_key = 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM'

app = Flask(__name__)


@app.route('/' """, methods=['GET', 'POST']""")
def index():
    """
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        start_lat, start_long, end_lat, end_long = addy_to_lat_long(start, end, api_key)
        return render_template('input.html', start=start, end=end, api_key=api_key, start_lat=start_lat, start_long=start_long, end_lat=end_lat, end_long=end_long)
    return render_template('input.html', start='', end='', api_key=api_key)
    """

app = Flask(__name__)

@app.route('/receive_location_data', methods=['POST'])
def receive_location_data():
    data = request.get_json()
    if data and 'latitude' in data and 'longitude' in data:
        latitude = data['latitude']
        longitude = data['longitude']
        # Process the received location data (e.g., store it in a database)
        print(f"Received location data - Latitude: {latitude}, Longitude: {longitude}")
        return render_template('input.html'), jsonify({'message': 'Location data received successfully'}), 200
    else:
        return render_template('input.html'), jsonify({'error': 'Invalid location data'}), 400


if __name__ == '__main__':
    app.run(debug=True)
