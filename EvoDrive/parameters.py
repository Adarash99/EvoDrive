


weathers_list = {'cloudiness': [0,100], 
                 'fog_density': [0,100], 
                 'fog_distance': [0,100], 
                 'precipitation': [0,100], 
                 'precipitation_deposits': [0,100], 
                 'sun_altitude_angle': [-90,90], 
                 'sun_azimuth_angle': [0,360], 
                 'wetness': [0,100], 
                 'wind_intensity': [0,100]
                 }

scenarios_list = {}

junction_scenarios = {}

available_maps = None


def get_all_avilable_maps():
    client = carla.Client('localhost', port)
    client.set_timeout(15)
    available_maps = client.get_available_maps()