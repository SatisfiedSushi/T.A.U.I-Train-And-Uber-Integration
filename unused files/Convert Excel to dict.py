from pandas import *

import pprint
df = read_excel('CTA train addresses.xlsx')
google_maps_place_IDs = df['gmaps place id'].tolist()
cta_station_IDs = df['cta station id'].tolist()

# convert to dict
cta_to_gmaps_ID_mapping = dict(zip(google_maps_place_IDs, cta_station_IDs))
pprint.pprint(cta_to_gmaps_ID_mapping)
