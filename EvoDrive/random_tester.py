import carla
import random
import math
import xml.etree.ElementTree as ET
import time
import psutil
import os
import json

#from agents.navigation.global_route_planner import GlobalRoutePlanner
#from agents.navigation.local_planner import RoadOption

from parameters import *
from utils import generate_xml
from utils import generate_scenario
from utils import save_route_data
debug_time = 15
min_route_distance = 100
max_route_distance = 800

min_number_of_scenarios = 1
max_number_of_scenarios = 3
min_distance_between_scenarios = 50




WORKING_SCENARIOS = {}

class RandomTester():  
    

    __filepath = './leaderboard/data/custom_route.xml'
    __map = None
    __world = None
    __client = None
    __town = ''
    __route_distance = 0
    __number_of_scenarios = 0
    __sim_n = 1
    
    def __init__(self, town):
        self.__client = carla.Client('localhost', 2000)
        self.__client.set_timeout(50)
        self.__town = town
    
        
    ##################################################################
    ########  MAIN ###################################################
    
    def reload(self):
        self.__client = carla.Client('localhost', 2000)
        self.__client.set_timeout(50)
    
    def generate_scene(self):
        
        
        print("\n\033[1m========= Generating Random Scene_{} =========\033[0m".format(self.__sim_n))
        
        print("\033[1m> Loading map for {}\033[0m".format(self.__town))
        self.__client.load_world(str(self.__town)) 
        self.__world = self.__client.get_world()
        self.__map = self.__world.get_map()
        
        print("\033[1m> Generating route\033[0m")
        route = self.__generate_route()
        
        print("\033[1m> Generating scenario\033[0m")
        #scen_type = str(random.choice(SCENARIO_TYPES).key)
        #scen_type = 'YieldToEmergencyVehicle'
        #scenario_attributes = generate_scenario(route, scen_type, self.__map, self.__town)
        scen_type = None
        scenario_attributes = None
        
        print("\033[1m> Generating weather\033[0m")
        weather = self.__generate_weather()
        
        print("\033[1m> Writing parameters to file\033[0m")
        generate_xml(self.__town, route, weather, scen_type, scenario_attributes, self.__sim_n, routes_filepath)    
        
        self.__sim_n = self.__sim_n + 1
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
           
            if distance > min_route_distance:
                correct = True
          
          
        self.__number_of_scenarios = math.floor(distance / min_distance_between_scenarios)
        
        ######################################
        # For debugging
        #for point in route:
        #    debug.draw_string(point[0].transform.location, 'o', draw_shadow=False, color=carla.Color(r=0, g=128, b=0), life_time=debug_time, persistent_lines=True)
        #debug.draw_string(start.transform.location, 'o', draw_shadow=False, color=carla.Color(r=255, g=0, b=0), life_time=debug_time, persistent_lines=True)
        #debug.draw_string(end.transform.location, 'o', draw_shadow=False, color=carla.Color(r=0, g=0, b=255), life_time=debug_time, persistent_lines=True)
        #print('\t Distance is ' + str(distance))
        #print('\t Number of points in route is ' + str(len(route)))
        #spectator = self.__world.get_spectator()
        #spectator.set_transform(carla.Transform(carla.Location((start.transform.location.x - end.transform.location.x), (start.transform.location.y - end.transform.location.y),350), carla.Rotation(268,0,0)))
        #time.sleep(debug_time)
        #######################################
        
        
        return route   
    
    
    def __generate_weather(self):
        weather = []
        for key, value in WEATHERS.items():
            weather_value =  random.randint(value[0], value[1])
            weather.append((str(key), weather_value))
        
        return dict(weather)
                                
        
if __name__ == '__main__':
    
    
    print('\n\n\n\n')
    client = carla.Client('localhost', 2000)
    client.set_timeout(50)
    client.load_world('Town05') 
    world = client.get_world()
    tmap = world.get_map()  
    
    all_spawn_points = tmap.get_spawn_points()
    
    print(all_spawn_points)
    
    
    
    
    # carla_pid = []
    
    # for proc in psutil.process_iter():
    #     if 'Carla' in proc.name():
    #         carla_pid.append(str(proc.pid))
    
    # #town = input('Town to test: ')
    # town = 'Town05'
    # tester = RandomTester(town)
    # print('this is to kill: ' + str(carla_pid))
    # sim_n = 1
    
    # while True:
    
    #     tester.generate_scene()
    #     os.system("./leaderboard/scripts/run_evaluation.sh")
        
        
    #     print('simulation is ')
    #     #read json average driving score
    #     with open(leaderboard_results_filepath) as f:
    #         data = json.load(f)
    #     driving_score = data["values"][0]
    #     print("\033[1m> Average driving score = {}\033[0m".format(driving_score))
        
    #     # save data to csv file
    #     save_route_data(sim_n)
        
    #     sim_n = sim_n + 1
        
    #     if sim_n%3 == 0:
    #         print("\033[1m> Restarting Carla Server\033[0m")
    #         for pid in carla_pid:
    #             os.system("kill -9 " + pid)
    #         os.system("./launch_carla.sh")
    #         carla_pid = []
    #         for proc in psutil.process_iter():
    #             if process_name in proc.name():
    #                 carla_pid.append(str(proc.pid))
    #         tester.reload()
                
    #     if (sim_n == 1001):
    #         break
        
        
    # print('Finished testing: reached 1000 evals')