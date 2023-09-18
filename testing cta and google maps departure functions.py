from google.transit import gtfs_realtime_pb2
import urllib.request

feed = gtfs_realtime_pb2.FeedMessage()
response = urllib.request.urlopen('https://www.transitchicago.com/downloads/sch_data/')
feed.ParseFromString(response.read())
for entity in feed.entity:
    if entity.HasField('trip_update'):
        print(entity.trip_update)