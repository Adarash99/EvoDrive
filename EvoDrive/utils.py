import xml.etree.ElementTree as ET
import csv
import json
from parameters import *
import random
import carla




def get_waypoints_before_junctions(route):
        viable_wp = []
        
        for x in range(20,(len(route)-5)):
            if (route[x][1] != RoadOption.LANEFOLLOW and route[x-1][1] != RoadOption.LANEFOLLOW):
                if(route[x-2][1] == RoadOption.LANEFOLLOW):
                    viable_wp.append(route[x-2][0])         
        
        #print('we have ' + str(len(viable_wp)) + ' viable waypoints!!!')
        return viable_wp


def generate_scenario(route, scen_type, tmap, town):
     
    
    
    wp = random.choice(route)[0]
    
    # choose trigger point accordingly
    if scen_type == 'PedestrianCrossing':  # near junctions
        pass 
    elif scen_type == 'HardBreakRoute':   #anywhere
        pass
    
    trigger_point = (
        str(round(wp.transform.location.x, 1)),
        str(round(wp.transform.location.y, 1)),
        str(round(wp.transform.location.z, 1)),
        str(round(wp.transform.rotation.yaw, 1))
    )
    
    
    
    
    # set all the attributes for the chosen scenario
    
    attribute_list = SCENARIO_TYPES[scen_type]
    scenario_attributes = [['trigger_point', 'transform', trigger_point]]
    for attribute in attribute_list:
        a_name, a_type = attribute
        
        # transform attribute
        if a_type == 'transform':
            a_data = get_transform_data(a_name, scen_type, tmap, world, spectator)
            
        # location attribute
        elif 'location' in a_type:
            if "sidewalk" in a_type:
                lane_type = carla.LaneType.Sidewalk
            elif "bicycle" in a_type:
                lane_type = carla.LaneType.Biking
            elif "driving" in a_type:
                lane_type = carla.LaneType.Driving
            else:
                lane_type = carla.LaneType.Driving

            wp = tmap.get_waypoint(random.choice(route)[0].transform.location, lane_type=lane_type)

            a_data =  (
                    str(round(wp.transform.location.x, 1)),
                    str(round(wp.transform.location.y, 1)),
                    str(round(wp.transform.location.z, 1))
                )

            if "probability" in a_type:
                p = input(f"\033[1m> Enter the '{a_name}' probability \033[0m")
                a_data += (p,)
        
        # value, choice, bool attribute
        elif a_type == 'value':
            a_data = str(random.randint(20,150))
        
        elif a_type == 'choice':
            a_data = get_value_data(a_name)
            
        elif a_type == 'bool':
            a_data = get_value_data(a_name)
            
        # interval attribute
        elif a_type == 'interval':
            a_data = get_interval_data(a_name)
            
        # not used
        else:
            raise ValueError("Unknown attribute type")
        
        
        
        if a_data:  # Ignore the attributes that use default values
            scenario_attributes.append([a_name, a_type, a_data])
            
    print(scenario_attributes)
    
    return scenario_attributes



def generate_xml(town, route_list, weather_settings, scen_type, scenario_attributes, sim_n, routes_filepath):
        
        positions = []
        for point in route_list:    
            position = [point[0].transform.location.x, point[0].transform.location.y, (point[0].transform.location.z+1)]
            positions.append(position)
            
        root = ET.Element('routes')
        route = ET.SubElement(root, 'route')
        route.set('id', '0')
        route.set('town', str(town))
        
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
                
        ################################### 
        # # scenario definition
        if scen_type:
            new_scenario = ET.SubElement(scenarios, "scenario")
            new_scenario.set("name", scen_type + "_1")
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
        tree.write(leaderboard_input_file)
        #tree.write(routes_filepath + '/route' + str(sim_n) + '.xml')
        
        
def save_route_data(sim_n):
    
    # Write route data from xml file
    
    tree = ET.parse(leaderboard_input_file)
    root = tree.getroot()
    
    csv_line = [] 
    
    weather_settings = root[0][0][0].attrib
    start_point = root[0][1][0].attrib
    end_point = root[0][1][1].attrib
    #scenario = root[0][2][0].attrib
    
    csv_line.append(str(sim_n))
    
    for item in weather_settings:
        csv_line.append(weather_settings[item])  
    for item in start_point:
        csv_line.append(start_point[item])   
    for item in end_point:
        csv_line.append(end_point[item])
    
    #csv_line.append(scenario['type'])
    
    # Write route results from json file
    with open(leaderboard_results_filepath) as f:
        results = json.load(f)
        for item in results['values']:   
            csv_line.append(item)
    
    # Write to CSV file
    
    # with open("data/data.csv",'a+', newline='') as write_obj:
    #     csv_writer = csv.writer(write_obj)
    #     csv_writer.writerow(csv_line)
       