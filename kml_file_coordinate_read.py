# https://stackoverflow.com/questions/67454345/google-kml-file-to-python

# Reading KML file, from google my maps
from pykml import parser

with open('Fargo, ND.kml', 'r') as f:
    root = parser.parse(f).getroot()
namespace = {"kml": 'http://www.opengis.net/kml/2.2'}
pms = root.xpath(".//kml:Placemark[.//kml:Polygon]", namespaces=namespace)

# Grabbing polygon name and polygon locations from KML file 
coordinate_dict = dict()
for p in pms:
    coordinate_dict[p.name.text.strip()] = p.Polygon.outerBoundaryIs.LinearRing.coordinates
    

def coordinate_string_to_array(input_string: str):
    '''This function takes pykml parsed string of longitude, lattitude, z.
    Then returns numpy array of longitude, lattitude.
    Arguments:
        Input: 
              -78.8185249,42.9578562,0
              -78.8107143,42.9608398,0
              -78.8109289,42.9616878,0
              -78.8139759,42.9642002,0
              -78.8166795,42.964263,0
              -78.819469,42.9637919,0
              -78.8236747,42.9640746,0
              -78.8240181,42.9582959,0
              -78.8196407,42.9581702,0
              -78.8185249,42.9578562,0
        
        Returns:
            array([[-78.8186595,  42.9576485],
           [-78.8189814,  42.9578919],
           [-78.8195929,  42.9579704],
           [-78.8317809,  42.9581981],
           [-78.8296137,  42.9557718],
           [-78.8237772,  42.9531334],
           [-78.8186595,  42.9576485]])
    '''
    
    coodrinate_points_list = [i.strip() for i in str(input_string).strip().split('\n')] # Splits on new lines since each points in polygon are separated by newline characters.
    import pandas as pd
    coordinate_points_df =  pd.DataFrame(coodrinate_points_list) # Loading into dataframe for string manipulation
    coordinate_points_df = coordinate_points_df[0].str.split(',', expand=True)
    coordinate_points_df.columns = ['lat', 'lon', 'z']
    try:
        coordinate_points_array = coordinate_points_df[['lat', 'lon']].to_numpy().astype('float')
    except ValueError as e:
        print('ERROR:', e)
        print('Could not convert the to numpy array float:')
        print(coordinate_points_df[['lat', 'lon']])

    return coordinate_points_array

coordinate_dict_numpy_formatted = {k: coordinate_string_to_array(v) for (k,v) in coordinate_dict.items()}

print(coordinate_dict_numpy_formatted)
