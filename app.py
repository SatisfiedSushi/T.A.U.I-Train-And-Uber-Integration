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


@app.route('/')
def receive_location_data():
    """if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        accuracy = request.form['accuracy']
        print(f"latitude: {latitude}, longitude: {longitude}")
        print(f"accuracy : {accuracy}")
        return render_template('location.html')"""
    return render_template('location.html')


if __name__ == '__main__':
    app.run(debug=True)
