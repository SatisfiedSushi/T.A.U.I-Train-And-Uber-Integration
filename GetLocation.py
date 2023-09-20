"""
import googlemaps
from googlemaps import Client

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
api_key = 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM'


def get_current_location(api_key):
    gmaps = Client(api_key)

    try:
        # Request the geolocation information for the user's IP address
        geolocation = gmaps.geolocate()

        # Extract latitude and longitude from the geolocation response
        current_lat = geolocation['location']['lat']
        current_long = geolocation['location']['lng']

        return current_lat, current_long
    except Exception as e:
        print("Error fetching current location:", str(e))
        return None


current_location = get_current_location(api_key)
print(current_location)
"""

import requests
import json


api_key = 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM'


def get_current_location(api_key):
    # Define the request payload
    payload = {
        "considerIp": "true",  # Considers the IP address of the device
    }

    # Make the POST request to the Geolocation API
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}"
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = json.loads(response.text)
        location = data.get('location')
        accuracy = data.get('accuracy')
        print(f"Latitude: {location['lat']}, Longitude: {location['lng']}, Accuracy: {accuracy} meters")
        return location, accuracy
    else:
        print(f"Failed to fetch location. Status code: {response.status_code}")


current_location = get_current_location(api_key)
print(current_location)
