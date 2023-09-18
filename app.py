from flask import Flask, render_template, request
from MapEmbed import map_inputs
from UberDeepLink import addy_to_lat_long

api_key = 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM'

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def handle_post():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        start_lat, start_long, end_lat, end_long = addy_to_lat_long(start, end, api_key)
        return render_template('input.html', start=start, end=end, api_key=api_key, start_lat=start_lat, start_long=start_long, end_lat=end_lat, end_long=end_long)
    return render_template('input.html', start='', end='', api_key=api_key)

if __name__ == '__main__':
    app.run(debug=True)
