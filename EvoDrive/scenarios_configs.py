import xml.etree.ElementTree as ET
import carla
import time

debug_time = 50

client = carla.Client('localhost', 2000)
client.load_world('Town05')
world = client.get_world()
tmap = world.get_map()
debug = world.debug

time.sleep(3)
print('connected to the simuator')

# read the xml

filename = './leaderboard/data/custom_route.xml'

tree = ET.parse(filename)
root = tree.getroot()
 
waypoints = root[0][1]

for point in waypoints:
    
    location = carla.Location(x = float(point.get('x')), y = float(point.get('y')), z = float(point.get('z')))
    debug.draw_string(location, 'o', draw_shadow=False, color=carla.Color(r=0, g=128, b=0), life_time=debug_time, persistent_lines=True)



