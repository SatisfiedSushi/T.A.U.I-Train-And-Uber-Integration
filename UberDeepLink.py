import googlemaps

def addy_to_lat_long(start, end, api_key):
    # Initialize the Google Maps client
    gmaps = googlemaps.Client(api_key)

    # Geocode the start and end addresses
    start_geocode = gmaps.geocode(start)
    end_geocode = gmaps.geocode(end)

    # Extract latitude and longitude from the geocode results
    start_lat = start_geocode[0]['geometry']['location']['lat']
    start_lng = start_geocode[0]['geometry']['location']['lng']
    end_lat = end_geocode[0]['geometry']['location']['lat']
    end_lng = end_geocode[0]['geometry']['location']['lng']

    return start_lat, start_lng, end_lat, end_lng