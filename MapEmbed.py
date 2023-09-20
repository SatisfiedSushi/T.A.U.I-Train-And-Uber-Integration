import googlemaps


# Replace with your own API key
api_key = 'AIzaSyA6cXymaX959J3CYjXTcNhCTBFTt9qi6pM'

# Initialize the Google Maps client
gmaps = googlemaps.Client(api_key)

def map_inputs(lat, long):
    # Generate markers for location
    label = 'P'
    marker_color = 'green'
    marker = f'markers=color:{marker_color}|label:{label}|{lat},{long}&'

    return marker

