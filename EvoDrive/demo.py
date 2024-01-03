import carla
from random import randint
import random
import os
import sys
import time
import xml.etree.ElementTree as ET

from random_tester import RandomTester

####################
# PARAMETERS

debug_time = 5

##############################


#function to print a route to screen
def debug_route(route):
    debug = world.debug
    c = 0
    for point in route:
        debug.draw_string(point.transform.location, 'o', draw_shadow=False, color=carla.Color(r=c, g=c, b=c), life_time=debug_time, persistent_lines=True)
        c = c + 5
    #show the route 
    spectator.set_transform(carla.Transform(carla.Location(-5,0,350), carla.Rotation(268,0,0)))

##########################

while True:        
    #junction_ids = set([])
    
    # for point in route:
    #     if point.is_junction:
    #         junction_ids.add(point.junction_id)
    #         print('JUNCTION: ', point.junction_id)
            
    #debug_route(route)
    #print('Total number of junctions = ', len(junction_ids))
    
    tester = RandomTester(2000)
    tester.generate_scene()
    os.system("./leaderboard/scripts/run_evaluation.sh")
    time.sleep(5)

