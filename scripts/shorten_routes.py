import carla
import os
import time
import xml.etree.ElementTree as ET

#from random_tester import RandomTester
from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.navigation.local_planner import RoadOption

#function to print a route to screen
def debug_route(route):
    debug = world.debug
    
    for point,x in route:
        debug.draw_string(point.transform.location, 'o', draw_shadow=False, color=carla.Color(r=255, g=0, b=0), life_time=10000, persistent_lines=True)
       
    #show the route 
    #spectator.set_transform(carla.Transform(carla.Location(-5,0,350), carla.Rotation(268,0,0)))


filepath = '/home/lunet/coak12/EvoDrive/EvoDrive/custom_scenarios'
folders_list = os.listdir(filepath)

client = carla.Client('localhost', 2000)
client.set_timeout(50000)
client.load_world('Town12')
world = client.get_world()
time.sleep(10)
#debug = world.debug
wmap = world.get_map()
grp = GlobalRoutePlanner(wmap, 1.0)

for folder in folders_list:
    filepath = '/home/lunet/coak12/EvoDrive/EvoDrive/custom_scenarios'
    filepath = filepath + '/' + folder
    file_list = os.listdir(filepath)

    for file in file_list:
        filepath = '/home/lunet/coak12/EvoDrive/EvoDrive/custom_scenarios/' + folder
        filepath = filepath + '/' + file

        tree = ET.parse(filepath)
        root = tree.getroot()
        waypoints = root[0][1]
        trigger_point = root[0][2][0][0]
        
        
        #spectator = world.get_spectator()
        #spectator.set_transform(carla.Transform(carla.Location(float(waypoints[0].attrib['x']), float(waypoints[0].attrib['y']), 500.0), carla.Rotation(270,0,0)))


        # for waypoint in waypoints:
        #     wp = waypoint.attrib
        #     point = carla.Location(x=float(wp['x']), y=float(wp['y']), z=float(wp['z']))
        #     debug.draw_string(point, 'o', draw_shadow=False, color=carla.Color(r=255, g=0, b=0), life_time=1000, persistent_lines=True)
        #     time.sleep(5)
        #     print(wp)

        wp = trigger_point.attrib
        tpoint = carla.Location(x=float(wp['x']), y=float(wp['y']), z=float(wp['z']))
        #debug.draw_string(tpoint, 'o', draw_shadow=False, color=carla.Color(r=0, g=0, b=255), life_time=1000, persistent_lines=True)
        wp = waypoints[0].attrib
        spoint = carla.Location(x=float(wp['x']), y=float(wp['y']), z=float(wp['z']))
        wp = waypoints[-1].attrib
        epoint = carla.Location(x=float(wp['x']), y=float(wp['y']), z=float(wp['z']))

        route = grp.trace_route(spoint, tpoint)
        #debug_route(route)

        if(len(route)>22):
            swpoint = route[-20][0]
            waypoints[0].set('x', str(round(swpoint.transform.location.x, 1)))
            waypoints[0].set('y', str(round(swpoint.transform.location.y, 1)))
            waypoints[0].set('z', str(round(swpoint.transform.location.z, 1)))

        route = grp.trace_route(tpoint, epoint)
        #debug_route(route)

        if(len(route)>5):
            ewpoint = route[int((len(route))/2)][0]
            waypoints[-1].set('x', str(round(ewpoint.transform.location.x, 1)))
            waypoints[-1].set('y', str(round(ewpoint.transform.location.y, 1)))
            waypoints[-1].set('z', str(round(ewpoint.transform.location.z, 1)))


        tree.write(filepath)

        # print(file + ' -- done')

    print(folder + '-- done')