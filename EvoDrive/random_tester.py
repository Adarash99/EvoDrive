import carla
import random
import math
import xml.etree.ElementTree as ET
import time

from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.navigation.local_planner import RoadOption


debug_time = 15
min_route_distance = 300
max_route_distance = 800

min_number_of_scenarios = 1
max_number_of_scenarios = 3
min_distance_between_scenarios = 50


SCENARIO_TYPES ={

    # Junction scenarios
    "SignalizedJunctionLeftTurn": [
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "SignalizedJunctionRightTurn": [
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "OppositeVehicleRunningRedLight": [
        ["direction", "choice"],
    ],
    "NonSignalizedJunctionLeftTurn": [
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "NonSignalizedJunctionRightTurn": [
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "OppositeVehicleTakingPriority": [
        ["direction", "choice"],
    ],

    # Crossing actors
    "DynamicObjectCrossing": [
        ["distance", "value"],
        ["direction", "value"],
        ["blocker_model", "value"],
        ["crossing_angle", "value"]
    ],
    "ParkingCrossingPedestrian": [
        ["distance", "value"],
        ["direction", "choice"],
        ["crossing_angle", "value"],
    ],
    "PedestrianCrossing": [
    ],
    "VehicleTurningRoute": [
    ],
    "VehicleTurningRoutePedestrian": [
    ],
    "BlockedIntersection": [
    ],

    # Actor flows
    "EnterActorFlow": [
        ["start_actor_flow", "location driving"],
        ["end_actor_flow", "location driving"],
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "EnterActorFlowV2": [
        ["start_actor_flow", "location driving"],
        ["end_actor_flow", "location driving"],
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "InterurbanActorFlow": [
        ["start_actor_flow", "location driving"],
        ["end_actor_flow", "location driving"],
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "InterurbanAdvancedActorFlow": [
        ["start_actor_flow", "location driving"],
        ["end_actor_flow", "location driving"],
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "HighwayExit": [
        ["start_actor_flow", "location driving"],
        ["end_actor_flow", "location driving"],
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "MergerIntoSlowTraffic": [
        ["start_actor_flow", "location driving"],
        ["end_actor_flow", "location driving"],
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "MergerIntoSlowTrafficV2": [
        ["start_actor_flow", "location driving"],
        ["end_actor_flow", "location driving"],
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "CrossingBicycleFlow": [
        ["start_actor_flow", "location bicycle"],
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],

    # Route obstacles
    "ConstructionObstacle": [
        ["distance", "value"],
        ["direction", "value"],
        ["speed", "value"],
    ],
    "ConstructionObstacleTwoWays": [
        ["distance", "value"],
        ["frequency", "interval"],
    ],
    "Accident": [
        ["distance", "value"],
        ["direction", "value"],
        ["speed", "value"],
    ],
    "AccidentTwoWays": [
        ["distance", "value"],
        ["frequency", "interval"],
    ],
    "ParkedObstacle": [
        ["distance", "value"],
        ["direction", "value"],
        ["speed", "value"],
    ],
    "ParkedObstacleTwoWays": [
        ["distance", "value"],
        ["frequency", "interval"],
    ],
    "VehicleOpensDoorTwoWays": [
        ["distance", "value"],
        ["frequency", "interval"],
    ],
    "HazardAtSideLane": [
        ["distance", "value"],
        ["speed", "value"],
        ["bicycle_drive_distance", "value"],
        ["bicycle_speed", "value"],
    ],
    "HazardAtSideLaneTwoWays": [
        ["distance", "value"],
        ["frequency", "value"],
        ["bicycle_drive_distance", "value"],
        ["bicycle_speed", "value"],
    ],
    "InvadingTurn": [
        ["distance", "value"],
        ["offset", "value"],
    ],

    # Cut ins
    "HighwayCutIn": [
        ["other_actor_location", "location driving"],
    ],
    "ParkingCutIn": [
        ["direction", "choice"],
    ],
    "StaticCutIn": [
        ["distance", "value"],
        ["direction", "choice"],
    ],

    # Others
    "ControlLoss": [
    ],
    "HardBreakRoute": [
    ],
    "ParkingExit": [
        ["direction", "choice"],
        ["front_vehicle_distance", "value"],
        ["behind_vehicle_distance", "value"],
    ],
    "YieldToEmergencyVehicle": [
        ["distance", "value"],
    ],

    # Special ones
    "BackgroundActivityParametrizer": [
        ["num_front_vehicles", "value"],
        ["num_back_vehicles", "value"],
        ["road_spawn_dist", "value"],
        ["opposite_source_dist", "value"],
        ["opposite_max_actors", "value"],
        ["opposite_spawn_dist", "value"],
        ["opposite_active", "bool"],
        ["junction_source_dist", "value"],
        ["junction_max_actors", "value"],
        ["junction_spawn_dist", "value"],
        ["junction_source_perc", "value"],
    ],
    "PriorityAtJunction": [
    ],
}


WEATHERS = {'route_percentage': [100,100],
                 'cloudiness': [0,100], 
                 'fog_density': [0,10],  #[0,100]
                 'fog_distance': [0,10], #[0,100]
                 'precipitation': [0,100], 
                 'precipitation_deposits': [0,100], 
                 'sun_altitude_angle': [-90,90], 
                 'sun_azimuth_angle': [0,360], 
                 'wetness': [0,100], 
                 'wind_intensity': [0,100]
                 }

TOWNS = ['Town01', 
         'Town02', 
         'Town03', 
         'Town04', 
         'Town05', 
         'Town06', 
         'Town07', 
         'Town10HD', 
         'Town12']

WORKING_SCENARIOS = {}

class RandomTester():  
    

    __filepath = './leaderboard/data/custom_route.xml'
    __map = None
    __world = None
    __client = None
    __town = ''
    __route_distance = 0
    __number_of_scenarios = 0
    
    def __init__(self, port=2000):
        self.__client = carla.Client('localhost', port)
        self.__client.set_timeout(50)
    
        
    ##################################################################
    ########  MAIN ###################################################
    
    def generate_scene(self):
        
        # choose map
        self.__town = random.choice(TOWNS)
        print("\033[1m> Loading map for {}\033[0m".format(self.__town))
        self.__client.load_world(str(self.__town)) 
        self.__world = self.__client.get_world()
        self.__map = self.__world.get_map()
        
        print("\033[1m> Generating route\033[0m")
        route = self.__generate_route()
        
        print("\033[1m> Generating scenario\033[0m")
        scen_type_list, scenario_attributes_list = self.__generate_scenarios(route)
        
        print("\033[1m> Generating weather\033[0m")
        weather = self.__generate_weather()
        
        print("\033[1m> Writing parameters to file\033[0m")
        self.__generate_xml(route, weather, scen_type_list, scenario_attributes_list)
        
    ##################################################################
    ##################################################################
    
    def __calculate_route(self, start, end, grp):

        added_distance = 0
        route = []
        route = grp.trace_route(start.transform.location, end.transform.location)
        for j in range(len(route) - 1):
            wp, option = route[j]
            wp_next = route[j + 1][0]
            added_distance += wp.transform.location.distance(wp_next.transform.location)
        
        return added_distance, route 
        
    
    # returns list of tuples (waypoints, road options)
    def __generate_route(self):    
        all_spawn_points = self.__map.get_spawn_points()
        grp = GlobalRoutePlanner(self.__map, 1.0)
        correct = False
        distance = 0
        start = None
        end = None
        
        debug = self.__world.debug
        
        start  = self.__map.get_waypoint(random.choice(all_spawn_points).location, project_to_road=True, lane_type=carla.LaneType.Driving)
        end = self.__map.get_waypoint(random.choice(all_spawn_points).location, project_to_road=True, lane_type=carla.LaneType.Driving)
        distance = 0
        route = []
        distance, route = self.__calculate_route(start, end, grp)
    
        while not correct:
            start  = self.__map.get_waypoint(random.choice(all_spawn_points).location, project_to_road=True, lane_type=carla.LaneType.Driving)
            end = self.__map.get_waypoint(random.choice(all_spawn_points).location, project_to_road=True, lane_type=carla.LaneType.Driving)        
            distance, route = self.__calculate_route(start, end, grp)
           
            if distance > min_route_distance and distance < max_route_distance :
                correct = True
          
          
        self.__number_of_scenarios = math.floor(distance / min_distance_between_scenarios)
        
        ######################################
        # For debugging
        for point in route:
            debug.draw_string(point[0].transform.location, 'o', draw_shadow=False, color=carla.Color(r=0, g=128, b=0), life_time=debug_time, persistent_lines=True)
        debug.draw_string(start.transform.location, 'o', draw_shadow=False, color=carla.Color(r=255, g=0, b=0), life_time=debug_time, persistent_lines=True)
        debug.draw_string(end.transform.location, 'o', draw_shadow=False, color=carla.Color(r=0, g=0, b=255), life_time=debug_time, persistent_lines=True)
        print('\t Distance is ' + str(distance))
        print('\t Number of points in route is ' + str(len(route)))
        spectator = self.__world.get_spectator()
        spectator.set_transform(carla.Transform(carla.Location((start.transform.location.x - end.transform.location.x), (start.transform.location.y - end.transform.location.y),350), carla.Rotation(268,0,0)))
        time.sleep(debug_time)
        #######################################
        
        
        return route
    
    
    def get_waypoints_before_junctions(self, route):
        viable_wp = []
        
        for x in range(20,(len(route)-5)):
            if (route[x][1] != RoadOption.LANEFOLLOW and route[x-1][1] != RoadOption.LANEFOLLOW):
                if(route[x-2][1] == RoadOption.LANEFOLLOW):
                    viable_wp.append(route[x-2][0])         
        
        #print('we have ' + str(len(viable_wp)) + ' viable waypoints!!!')
        return viable_wp

    #TODO
    def __generate_scenarios(self, route):
        
        # select scenario type from the list
        
        #viable_wp = self.get_waypoints_before_junctions(route)
        
        scen_type_list = []
        scenario_attributes_list = []
        
        for n in range(0,1):
                   
            scen_type = 'HardBreakRoute'
            #wp = viable_wp[n]
            wp = random.choice(route)[0]
    
            trigger_point = (
                str(round(wp.transform.location.x, 1)),
                str(round(wp.transform.location.y, 1)),
                str(round(wp.transform.location.z, 1)),
                str(round(wp.transform.rotation.yaw, 1))
            )
            
            # set all the attributes for the scenario
            
            attribute_list = SCENARIO_TYPES[scen_type]
            scenario_attributes = [['trigger_point', 'transform', trigger_point]]
            for attribute in attribute_list:
                a_name, a_type = attribute
                if a_type == 'transform':
                    a_data = get_transform_data(a_name, scen_type, tmap, world, spectator)
                elif 'location' in a_type:
                    a_data = get_location_data(a_name, scen_type, tmap, world, spectator, a_type)
                elif a_type in ('value', 'choice', 'bool'):
                    a_data = get_value_data(a_name)
                elif a_type == 'interval':
                    a_data = get_interval_data(a_name)
                else:
                    raise ValueError("Unknown attribute type")

                if a_data:  # Ignore the attributes that use default values
                    scenario_attributes.append([a_name, a_type, a_data])
                    
            scen_type_list.append(scen_type)
            scenario_attributes_list.append(scenario_attributes)
        
        
        return scen_type_list, scenario_attributes_list      
    
    
    def __generate_weather(self):
        weather = []
        for key, value in WEATHERS.items():
            weather_value =  random.randint(value[0], value[1])
            weather.append((str(key), weather_value))
        
        return dict(weather)
                    
                    
        
    # getting waypoints into writable xml format positions
    def __get_list_of_positions(self, route):
        positions = []
        debug = self.__world.debug
        for point in route:    
            position = [point[0].transform.location.x, point[0].transform.location.y, (point[0].transform.location.z+1)]
            positions.append(position) 
        return positions
    

    
    # writing the xml file specifying the scene
    def __generate_xml(self, route, weather_settings, scen_type_list, scenario_attributes_list):
        positions = []
        positions = self.__get_list_of_positions(route)
        root = ET.Element('routes')
        route = ET.SubElement(root, 'route')
       
        route.set('id', '0')
        route.set('town', self.__town)
        
        weathers = ET.SubElement(route, 'weathers')
        weather = ET.SubElement(weathers, 'weather')

        for key, value in weather_settings.items():
            weather.set(str(key), str(value))
        
        waypoints = ET.SubElement(route, 'waypoints')
        
        # start point
        waypoint = ET.SubElement(waypoints, 'position')
        waypoint.set('x', str(round(positions[0][0], 1)))
        waypoint.set('y', str(round(positions[0][1], 1)))
        waypoint.set('z', str(round(positions[0][2], 1)))
        # end point
        waypoint = ET.SubElement(waypoints, 'position')
        waypoint.set('x', str(round(positions[-1][0], 1)))
        waypoint.set('y', str(round(positions[-1][1], 1)))
        waypoint.set('z', str(round(positions[-1][2], 1)))

        scenarios = ET.SubElement(route, 'scenarios')        
                
        ########################### scenario definition
        
        for n in range(0, len(scen_type_list)):
        
            scen_type = scen_type_list[n]
            scenario_attributes = scenario_attributes_list[n]
            
            new_scenario = ET.SubElement(scenarios, "scenario")
            new_scenario.set("name", scen_type + "_" + str(n))
            new_scenario.set("type", scen_type)
            
            for a_name, a_type, a_value in scenario_attributes:
                data = ET.SubElement(new_scenario, a_name)
                if a_type == 'transform':
                    data.set("x", a_value[0])
                    data.set("y", a_value[1])
                    data.set("z", a_value[2])
                    data.set("yaw", a_value[3])
                elif 'location' in a_type:
                    data.set("x", a_value[0])
                    data.set("y", a_value[1])
                    data.set("z", a_value[2])
                    if 'probability' in a_type:
                        data.set("p", a_value[3])
                elif a_type in ('value', 'choice', 'bool'):
                    data.set("value", a_value)
                elif a_type == 'interval':
                    data.set("from", a_value[0])
                    data.set("to", a_value[1])           
            
        ##################################
        
        
        
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