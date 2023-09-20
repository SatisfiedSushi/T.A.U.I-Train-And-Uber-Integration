from flask import Flask, Response, render_template, request, send_from_directory
import json
from MapEmbed import map_inputs
from UberDeepLink import addy_to_lat_long

api_key = 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM'

app = Flask(__name__)

"""
@app.route('/' , methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        start_lat, start_long, end_lat, end_long = addy_to_lat_long(start, end, api_key)
        return render_template('input.html', start=start, end=end, api_key=api_key, start_lat=start_lat, start_long=start_long, end_lat=end_lat, end_long=end_long)
    return render_template('input.html', start='', end='', api_key=api_key)



@app.route('/')
def receive_location_data():
    #Code to receive json data
    None
"""
@app.route('/', methods=['GET'])
def send_js():
    json_file = open('data.json')
    data = json.load(json_file)
    name1 = data['employees'][0]['firstName']
    name2 = data['employees'][1]['firstName']
    name3 = data['employees'][2]['firstName']
    return render_template('index.html', name1=name1, name2=name2, name3=name3)




if __name__ == '__main__':
    app.run(debug=True)
