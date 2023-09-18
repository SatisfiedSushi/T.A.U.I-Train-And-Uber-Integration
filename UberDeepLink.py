import GoogleMapsAPIs as gmaps
import requests

request = requests.post("http://taui.pythonanywhere.com/")

def addy_to_lat_long(start, end):

    origin = start
    destination = end

    start_long_lat = gmaps.get_lat_lng_from_address(origin, 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM')
    start_long_lat = start_long_lat.split(",")
    start_long = start_long_lat[1]
    start_lat = start_long_lat[0]

    end_long_lat = gmaps.get_lat_lng_from_address(destination, 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM')
    end_long_lat = end_long_lat.split(",")
    end_long = end_long_lat[1]
    end_lat = end_long_lat[0]

    return start_lat, start_long, end_lat, end_long, origin, destination