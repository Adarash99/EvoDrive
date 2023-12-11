#import carla
from random import randint
#import time
#from PIL import Image
import os
import sys
import time
import xml.etree.ElementTree as ET
#import leaderboard.leaderboard.leaderboard_evaluator
#from leaderboard.leaderboard.utils.statistics_manager import StatisticsManager, FAILURE_MESSAGES


# variables for xml creation

weathers_list = ['route_percentage', 'cloudiness', 'fog_density', 'fog_distance', 'precipitation', 'precipitation_deposits', 'sun_altitude_angle', 'sun_azimuth_angle', 'wetness', 'wind_intensity']
weather_values = [100, 0, 0, 0, 0, 0, 0, 0, 0, 0]

positions = [['56.449505', '205.120041', '0.953773'],['185.469559', '160.977905', '0.930790']]


def generate_xml():
    routes = ET.Element('routes')
    route = ET.SubElement(routes, 'route')
    route.set('id', '0')
    route.set('town', 'Town05')
    weathers = ET.SubElement(route, 'weathers')
    weather = ET.SubElement(weathers, 'weather')

    for weather_element, weather_value in zip(weathers_list, weather_values):
        weather.set(weather_element, str(weather_value))
    waypoints = ET.SubElement(route, 'waypoints')

    for position in positions:
        waypoint = ET.SubElement(waypoints, 'position')
        waypoint.set('x', position[0])
        waypoint.set('y', position[1])
        waypoint.set('z', position[2])

    scenarios = ET.SubElement(route, 'scenarios')
    tree = ET.ElementTree(routes)
    # Write XML file
    tree.write('./leaderboard/data/custom_route.xml')
    print(ET.tostring(routes, encoding='utf8'))

# generate 10 random weathers
for i in range (10):
    for x in range(len(weather_values)):
        if(x>0):
            weather_values[x] = randint(0, 100)
    print(weather_values)
    generate_xml()
    #os.system("./leaderboard/scripts/run_evaluation.sh")

# generate_xml()
# os.system("./leaderboard/scripts/run_evaluation.sh")