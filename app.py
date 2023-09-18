from flask import Flask, render_template, request
from MapEmbed import map_inputs
import UberDeepLink

api_key = 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM'

app = Flask(__name__)

@app.route('/handle_post', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        start_lat, start_long, end_lat, end_long, origin, destination = UberDeepLink.addy_to_lat_long(start, end)
        url = f"https://m.uber.com/ul/?client_id=<CLIENT_ID>&action=setPickup&pickup[latitude]={start_lat}&pickup[longitude]={start_long}&pickup[formatted_address]={origin}&dropoff[latitude]={end_lat}&dropoff[longitude]={end_long}&dropoff[formatted_address]={destination}"
        return render_template('input.html', start=start, end=end, api_key=api_key), url


if __name__ == '__main__':
    app.run(debug=True)
