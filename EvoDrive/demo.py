import carla
from random import randint
import random
import os
import sys
import time
import xml.etree.ElementTree as ET

from random_tester import RandomTester
from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.navigation.local_planner import RoadOption

####################
# PARAMETERS

debug_time = 5

LIFE_TIME = debug_time

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


def draw_point(world, wp, option):
    if option == RoadOption.LEFT:  # Yellow
        color = carla.Color(128, 128, 0)
    elif option == RoadOption.RIGHT:  # Cyan
        color = carla.Color(0, 128, 128)
    elif option == RoadOption.CHANGELANELEFT:  # Orange
        color = carla.Color(128, 32, 0)
    elif option == RoadOption.CHANGELANERIGHT:  # Dark Cyan
        color = carla.Color(0, 32, 128)
    elif option == RoadOption.STRAIGHT:  # Gray
        color = carla.Color(0, 0, 0)
    else:  # LANEFOLLOW
        color = carla.Color(0, 128, 0)  # Green

    world.debug.draw_point(wp.transform.location + carla.Location(z=0.2), size=0.05, color=color, life_time=LIFE_TIME)


def add_data(start, tmap, world, end, grp):

    #draw_keypoint(world, end.transform.location)
    added_distance = 0
    route = grp.trace_route(start.transform.location, end.transform.location)
    for j in range(len(route) - 1):
        wp, option = route[j]
        wp_next = route[j + 1][0]
        #draw_point(world, wp, option)
        added_distance += wp.transform.location.distance(wp_next.transform.location)
    
    return added_distance, route



def main_function(n):
    print("\n\033[1m========= Generating Random Scene_{} =========\033[0m".format(n))
    try:
        tester = RandomTester(2000)
        tester.generate_scene()
        os.system("./leaderboard/scripts/run_evaluation.sh")
        n = n + 1
        main_function(n)
    except Exception as e:
        print(e)
        print('TRYING TO RESTART CARLA')
        n = n - 1 
        os.system("./launch_carla.sh")
        time.sleep(30)
        main_function(n)

    

main_function(1)
