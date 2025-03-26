import xml.etree.ElementTree as ET
import math
import os



training_file_path = "/home/adarash/EvoDrive/EvoDrive/leaderboard/data/all_routes.xml"
tree = ET.parse(training_file_path)
root = tree.getroot()

file_number = 0

for route in root:
    
    for scenario in route[2].findall('scenario'):
        print('file number === ' + str(file_number))

        # create basic xml structure
        new_root = ET.Element(root.tag)
        new_route = ET.SubElement(new_root, route.tag, attrib={'id':'0', 'town':'Town12'})
        for elem in route:
            ET.SubElement(new_route, elem.tag, elem.attrib)

        new_weathers = new_route.find('weathers')
        new_waypoints = new_route.find('waypoints')
        new_scenarios = new_route.find('scenarios')
        # transfer the scenario over
        new_scenario = ET.SubElement(new_scenarios, 'scenario')
        new_scenario.set('name', scenario.get('name'))
        new_scenario.set('type', scenario.get('type'))
        scenario_name = scenario.get('type')
        # set parameters
        for parameter in scenario:
            ET.SubElement(new_scenario, parameter.tag, parameter.attrib)
        
        # get correct waypoints
        location = new_scenario.find('trigger_point')
        waypoints = route[1]
        point_n = 0
        min_distance = 100000
        for waypoint in waypoints:
            distance = math.sqrt((float(location.get('x')) - float(waypoint.get('x'))) ** 2 + (float(location.get('y')) - float(waypoint.get('y'))) ** 2)
            if distance < min_distance:
                closest_point = point_n
                min_distance = distance
            point_n = point_n + 1
        #print('closest point = ' + str(closest_point))
        if closest_point == 0:
            ET.SubElement(new_waypoints, waypoints[closest_point].tag, waypoints[closest_point].attrib)
            ET.SubElement(new_waypoints, waypoints[closest_point+1].tag, waypoints[closest_point+1].attrib)

        elif closest_point == point_n-1:
            ET.SubElement(new_waypoints, waypoints[closest_point-1].tag, waypoints[closest_point-1].attrib)
            ET.SubElement(new_waypoints, waypoints[closest_point].tag, waypoints[closest_point].attrib)
        else:
            ET.SubElement(new_waypoints, waypoints[closest_point-1].tag, waypoints[closest_point-1].attrib)
            ET.SubElement(new_waypoints, waypoints[closest_point].tag, waypoints[closest_point].attrib)
            ET.SubElement(new_waypoints, waypoints[closest_point+1].tag, waypoints[closest_point+1].attrib)

        #set weather
        weather = route[0][1]
        ET.SubElement(new_weathers,weather.tag, weather.attrib)

        # write to file
        new_tree = ET.ElementTree(new_root)
        filepath = '/home/adarash/EvoDrive/EvoDrive/custom_scenarios/' + scenario_name
        number = 0
        if os.path.exists(filepath):
            file_list = os.listdir(filepath)
            max_number = max([eval(i[:-4]) for i in file_list])
            number = max_number+1
        else:
            os.makedirs(filepath)
        filepath = filepath + '/' + str(number) + '.xml'
        new_tree.write(filepath, encoding='unicode')
        
        file_number = file_number + 1