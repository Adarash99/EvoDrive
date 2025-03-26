import time
import os
import psutil
import json
import csv
import xml.etree.ElementTree as ET
import numpy as np
import math
from parameters import * 

min_distance = 0.9
pwd = os.getcwd()
restarting_interval = 4
process_name = 'Carla'
scenario_tested = 'DynamicObjectCrossing'
scenario_filepath = pwd + '/custom_scenarios/'
scenario_filepath = scenario_filepath + scenario_tested

def create_scenario(x, scenario_tested):
    scenario_filepath = pwd + '/custom_scenarios/'
    scenario_filepath = scenario_filepath + scenario_tested
    filepath = pwd + '/leaderboard/data/custom_route.xml'
    n = 0
    scenario_filepath = scenario_filepath +'/' + str(int(x[0])) + '.xml'
    n = n+1
    os.system('cp ' + scenario_filepath + ' ' + filepath)

    time.sleep(1)

    tree = ET.parse(filepath)    
    root = tree.getroot()

    # set weather parameters
    route = root[0]
    weathers = route.find('weathers')
    weather = weathers.find('weather')
    
    for parameter in WEATHERS:
        weather.set(parameter, str(x[n]))
        n = n+1

    # set scenario parameters
    scenarios = route.find('scenarios')
    scenario = scenarios.find('scenario')

    scenario_parameters_list = []
    for parameters in SCENARIO_TYPES[scenario_tested]:
        scenario_parameters_list.append(parameters[0])

    y = 0
    for parameters in scenario_parameters_list:
        parameter = scenario.find(parameters)
        if parameter is None:
            print('Parameter "' + parameters + '" is not in the file!')
        else:
            if SCENARIO_TYPES[scenario_tested][y][1] == 'value':
                    parameter.set('value', str(x[n]))
                    n = n + 1
            elif SCENARIO_TYPES[scenario_tested][y][1] == 'choice':
                    parameter.set('value', str(SCENARIO_TYPES[scenario_tested][y][2][int(x[n])]))
                    n = n + 1
            else:
                print('There is something wrong with the SCENARIO_TYPES variable')
        y = y + 1

    # save modified xml
    new_tree = ET.ElementTree(root)
    new_tree.write(filepath, encoding='unicode')

def create_csv_file(scenario_tested):
    
    csv_line = ['test_number', 'cloudiness', 'fog_density', 'fog_distance', 'precipitation', 'precipitation_deposits', 'route_percentage', 'sun_altitude_angle', 'sun_azimuth_angle', 'wetness', 'wind_intensity', 'scenario_tested', 'file_number']
    for i in range(len(SCENARIO_TYPES[scenario_tested])):
        csv_line.append(str(SCENARIO_TYPES[scenario_tested][i][0]))
    csv_line.extend([' ', ' ', 'driving_score', 'route_completion', 'infraction_penalty', 'pedestrian_collision', 'vehicle_collision', 'layout_collision', 'red_light', 'stop_sign', 'off_road', 'route_deviation', 'route_timeout', 'agent_blocked', 'yield_emergency_vehicle', 'scenario_timeout', 'min_speed'])
 
    # Write to CSV file
    with open(pwd + "/data/data.csv",'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(csv_line)


def save_route_data(sim_n, file_n):
    
    leaderboard_results_filepath = pwd + '/leaderboard/results.json'
    
    # Write route data from xml file
    
    tree = ET.parse(pwd + '/leaderboard/data/custom_route.xml')
    root = tree.getroot()
    csv_line = [] 
    weather_settings = root[0][0][0].attrib
    scenario = root[0][2][0].attrib 
    csv_line.append(str(sim_n))
    for item in weather_settings:
        csv_line.append(weather_settings[item])
    scenario = scenario['type']

    csv_line.append(str(scenario))
    # add scenario type here
    # add file number
    csv_line.append(str(file_n))

    for item in SCENARIO_TYPES[scenario]:
        try:
            if item[1] == 'value':
                csv_line.append(root[0][2][0].find(item[0]).attrib['value'])
            elif item[1] == 'choice':
                choice = root[0][2][0].find(item[0]).attrib['value']
                list = item[2]
                position = list.index(choice)
                csv_line.append(position)
            else:
                csv_line.append(' ')
        except Exception as e:
            csv_line.append(' ')
            print(str(e) + ' item = ' + str(item[0]))
            #print("Problem saving the data of the scenario")

    csv_line.append(' ')
    csv_line.append(' ')

    # Write route results from json file
    with open(leaderboard_results_filepath) as f:
        results = json.load(f)
        for item in results['values']:   
            csv_line.append(item)
    
    # Write to CSV file
    with open(pwd + "/data/data.csv",'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(csv_line)

def prelims(scenario_tested):
    # variables needed for RandomTester
    n_var = 10 # + variables required for the scenario
    v_type = []
    v_ranges = []
    # calculate the number of variables required for the scenario
    n_var = n_var + len(SCENARIO_TYPES[scenario_tested])
    # type and range for variable 0
    v_type.append('int')
    v_ranges.append([0, len(os.listdir(scenario_filepath))-1])
    # type and range for 8 weather variables
    for parameter in WEATHERS:
        v_type.append('float')
        v_ranges.append(WEATHERS[parameter])
    # type and range for scenario variables
    for parameter in SCENARIO_TYPES[scenario_tested]:
        if parameter[1] == 'value':
            v_type.append('float')
            v_ranges.append(parameter[2])
        elif parameter[1] == 'choice':
            v_type.append('int')
            v_ranges.append([0, len(parameter[2])-1])
        else:
            print('There is something wrong with the SCENARIO_TYPES variable')
    
    return n_var, v_type, v_ranges

def prelims_ga():
        # variables needed for RandomTester
        n_var = 10 # + variables required for the scenario
        gene_space = []
        # calculate the number of variables required for the scenario
        n_var = n_var + len(SCENARIO_TYPES[scenario_tested])
        # type and range for variable 0
        #print(len(os.listdir(scenario_filepath)))
        gene_space.append({'low': 1, 'high': len(os.listdir(scenario_filepath)), 'step': 1})

        # type and range for 8 weather variables
        for parameter in WEATHERS:
            gene_space.append({'low': WEATHERS[parameter][0], 'high': WEATHERS[parameter][1], 'step': 0.5})

        # type and range for scenario variables
        for parameter in SCENARIO_TYPES[scenario_tested]:
            if parameter[1] == 'value':
                gene_space.append({'low': parameter[2][0], 'high': parameter[2][1], 'step': 0.5})
                
            elif parameter[1] == 'choice':
                gene_space.append({'low': 0, 'high': len(parameter[2]), 'step': 1})
                
            else:
                print('There is something wrong with the SCENARIO_TYPES variable')
        
        return gene_space


def is_similar(x, y):
    sum = 0
    for i in range(0,len(x)):
        sum = sum + ((x[i] - y[i]) ** 2)
    distance = math.sqrt(sum)
    print("> DISTANCE = " + str(distance))
    if(distance < min_distance):
        return True
    
    return False

def calculate_diversity(new_generation, scenario, min_values, max_values):
    changed = False
    length = len(SCENARIO_TYPES[scenario]) + 13

    prev_tests = np.genfromtxt(pwd + '/data/data.csv', delimiter=',')
    if (len(prev_tests)==0):
        print('> NO PREVIOUS TESTS')
        return new_generation
    prev_tests = np.delete(prev_tests, 0, axis=0)
    prev_tests = np.delete(prev_tests[:, :length], [0, 11], axis=1)  
    #changing the file number column position
    cols = list(range(prev_tests.shape[1]))
    cols.remove(10)
    cols.insert(0, 10)
    prev_tests = prev_tests[:, cols]

    min_values = np.array(min_values)
    max_values = np.array(max_values)

    for n, new_test in enumerate(new_generation):
        new_test = np.array(new_test)
        # normalise new test
        new_test = (new_test - min_values) / (max_values - min_values)

        for p, prev_test in enumerate(prev_tests):
            prev_test = np.array(prev_test)
            # normalise first prev test
            prev_test = (prev_test - min_values) / (max_values - min_values)

            # check if the files are the same
            if(new_generation[n][0] == prev_tests[p][0]): ## if different test files
                print('> SAME FILE NUMBERS')
                # calculate distance here
                if(is_similar(new_test, prev_test)):
                    print('> TESTS ARE TOO SIMILAR')
                    #change the new test
                    changed_test = np.random.uniform(min_values, max_values)
                    new_generation[n] = changed_test.tolist()
                    changed = True
                    break
            else:
                print('> DIFFERENT FILE NUMBERS')
                    
    return new_generation, changed


def restart(i):
    if i==1:
        return
    if (i % restarting_interval) or (i==1000):
        carla_pid = []
        for proc in psutil.process_iter():
            if process_name  in proc.name():
                carla_pid.append(str(proc.pid))
        print("\033[1m> Restarting Carla Server\033[0m")
        for pid in carla_pid:
            os.system("kill -9 " + pid)
        os.system("./launch_carla.sh")
        time.sleep(10)

def kill_carla():
    carla_pid = []
    for proc in psutil.process_iter():
        if process_name  in proc.name():
            carla_pid.append(str(proc.pid))
    print("\033[1m> Restarting Carla Server\033[0m")
    for pid in carla_pid:
        os.system("kill -9 " + pid)