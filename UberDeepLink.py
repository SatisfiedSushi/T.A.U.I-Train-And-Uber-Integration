import GoogleMapsAPIs as gmaps
import app
import requests

request = requests.post("http://taui.pythonanywhere.com/")

def addy_to_lat_long(start, end):

    origin = start
    destination = end

    start_long_lat = gmaps.get_lat_lng_from_address(origin, gmaps.api_key)
    start_long_lat = start_long_lat.split(",")
    start_long = start_long_lat[1]
    start_lat = start_long_lat[0]

    end_long_lat = gmaps.get_lat_lng_from_address(destination, gmaps.api_key)
    end_long_lat = end_long_lat.split(",")
    end_long = end_long_lat[1]
    end_lat = end_long_lat[0]

    return start_lat, start_long, end_lat, end_long, origin, destination
uber_url = f"https://m.uber.com/ul/?client_id=<CLIENT_ID>&action=setPickup&pickup[latitude]={start_lat}&pickup[longitude]={start_long}&pickup[formatted_address]={origin}&dropoff[latitude]={end_lat}&dropoff[longitude]={end_long}&dropoff[formatted_address]={destination}"

