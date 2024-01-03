import carla
import random
import xml.etree.ElementTree as ET
import time
#from parameters import *

weathers_list = {'route_percentage': [100,100],
                 'cloudiness': [0,100], 
                 'fog_density': [0,50],  #[0,100]
                 'fog_distance': [0,50], #[0,100]
                 'precipitation': [0,100], 
                 'precipitation_deposits': [0,100], 
                 'sun_altitude_angle': [-90,90], 
                 'sun_azimuth_angle': [0,360], 
                 'wetness': [0,100], 
                 'wind_intensity': [0,100]
                 }


class RandomTester():  
    
    __route_distance = 500
    __filepath = './leaderboard/data/custom_route.xml'
    __map = None
    __world = None
    
    def __init__(self, port=2000):
        client = carla.Client('localhost', port)
        client.set_timeout(15)
        
        # TODO
        # harcoding Town05 for now
        client.load_world('Town05') 
        
        world = client.get_world()
        self.__world = world
        self.__map = world.get_map()
        
    ########  MAIN #########
    
    def generate_scene(self):
        route = self.__generate_route()
        ## for debugging
        #self.debug_route(route)
        scenarios_list = self.__generate_scenarios()
        weather = self.__generate_weather()
        self.__generate_xml(route, scenarios_list, weather)
        
    ########################    
        
    
    # returns list of waypoints
    def __generate_route(self):
        all_spawn_points = self.__map.get_spawn_points()
        start_point = random.choice(all_spawn_points)
        route = []
        start_waypoint = self.__map.get_waypoint(start_point.location, project_to_road=True, lane_type=carla.LaneType.Driving)
        route.append(start_waypoint)
        last_waypoint = start_waypoint
        for n in range(round(self.__route_distance/10)):
            next_waypoint = last_waypoint.next(10.0)[-1]
            route.append(next_waypoint)
            last_waypoint = next_waypoint
        return route

    #TODO
    def __generate_scenarios(self):
        pass
    
    
    def __generate_weather(self):
        weather = []
        for key, value in weathers_list.items():
            weather_value =  random.randint(value[0], value[1])
            weather.append((str(key), weather_value))
        
        return dict(weather)
                    
                    
        
    # getting waypoints into writable xml format positions
    def __get_list_of_positions(self, route):
        positions = []
        for point in route:    
            position = [str(point.transform.location.x), str(point.transform.location.y), str(point.transform.location.z)]
            positions.append(position) 
        return positions
    
    
    # writing the xml file specifying the scene
    def __generate_xml(self, route, scenarios_list, weather_settings):
        positions = self.__get_list_of_positions(route)
        root = ET.Element('routes')
        route = ET.SubElement(root, 'route')
        route.set('id', '0')
        route.set('town', 'Town05')
        weathers = ET.SubElement(route, 'weathers')
        weather = ET.SubElement(weathers, 'weather')

        for key, value in weather_settings.items():
            weather.set(str(key), str(value))
                        
        waypoints = ET.SubElement(route, 'waypoints')

        for position in positions:
            waypoint = ET.SubElement(waypoints, 'position')
            waypoint.set('x', position[0])
            waypoint.set('y', position[1])
            waypoint.set('z', position[2])

        scenarios = ET.SubElement(route, 'scenarios')
        #TODO
        tree = ET.ElementTree(root)
        # Write XML file
        tree.write(self.__filepath)
        
    
    #function to print a route to screen
    def debug_route(self, route):
        debug = self.__world.debug
        spectator = self.__world.get_spectator()
        c = 0
        for point in route:
            debug.draw_string(point.transform.location, 'o', draw_shadow=False, color=carla.Color(r=c, g=c, b=c), life_time=10, persistent_lines=True)
            c = c + 5
        #show the route 
        spectator.set_transform(carla.Transform(carla.Location(-5,0,350), carla.Rotation(268,0,0)))
        time.sleep(10)
        
        

# unit test
if __name__ == '__main__':
    while True:
        tester = RandomTester(2000)
        tester.generate_scene()