from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.selection.rnd import RandomSelection
from pymoo.operators.crossover.sbx import SBX

from pymoo.operators.mutation.pm import PolynomialMutation
from pymoo.operators.mutation.bitflip import BitflipMutation

from pymoo.visualization.scatter import Scatter
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize
from pymoo.termination import get_termination

import pygad
import numpy as np

import os
import numpy as np
import random
import time
import json
import math
import carla
import psutil
import xml.etree.ElementTree as ET
from agents.navigation.global_route_planner import GlobalRoutePlanner
from parameters import *
from utils import generate_xml
from utils import save_route_data

process_name = 'Carla'


def run_simulation(x):
    
    start = x[9]
    end = x[10]
    print("\033[1m> Loading map for {}\033[0m".format(town))
    # carla connection
    client = carla.Client('localhost', 2000)
    client.set_timeout(50)
    client.load_world(town) 
    world = client.get_world()
    tmap = world.get_map()  
    
    print("\033[1m> Generating route\033[0m")
    all_spawn_points = tmap.get_spawn_points()
    start_index = int(round((start * (len(all_spawn_points)-1))/100))
    end_index = int(round((end * (len(all_spawn_points)-1))/100))
    print('start = ' + str(start_index) + ' and  end = ' + str(end_index))
    if (start_index == end_index):
        print('changed the indexessssss')
        if(start_index == (len(all_spawn_points) - 1)):
            end_index = end_index - 1
        else:
            end_index = end_index + 1    
        
    start_wp = all_spawn_points[start_index]
    end_wp = all_spawn_points[end_index]
    grp = GlobalRoutePlanner(tmap, 1.0)
    route = grp.trace_route(start_wp.location, end_wp.location)
    
    print("\033[1m> Generating weather\033[0m")
    weather_values = list(np.around(np.array(x[0:10]),1)) 
    weather_values.insert(0, 100.0)
    weather_settings = []
    n = 0
    for key, value in WEATHERS.items():
        weather_value =  weather_values[n]
        weather_settings.append((str(key), weather_value))  
        n = n + 1

    #print("\033[1m> Generating scenario\033[0m")
    scen_type = None
    scenario_attributes = None
    
    print("\033[1m> Writing parameters to file\033[0m")
    #save xml
    generate_xml(town, route, dict(weather_settings), scen_type, scenario_attributes, sim_n, routes_filepath)
    
    driving_score = 1000
    
    try:
        #run sim
        os.system("./leaderboard/run_leaderboard.sh")            
        #read json average driving score
        with open(leaderboard_results_filepath) as f:
            data = json.load(f)
        driving_score = data["values"][0]
        
    except Exception as e:
        print(e)
        
    print("\033[1m> Average driving score = {}\033[0m".format(driving_score))
    
    return driving_score

# random tester
def run_random(max_evals):
    global sim_n
    
    while True:
        # generate random values
        x = []
        for key, value in WEATHERS.items():
            x.append(random.uniform(value[0], value[1]))
        x.append(random.uniform(0,100))
        x.append(random.uniform(0,100))
            
        print("\n")
        print("\n\033[1m========= Generating Scene_eval_n_{} =========\033[0m".format(sim_n))
        run_simulation(x)
    
        # save data to csv file
        save_route_data(sim_n)
        
        if(sim_n == max_evals):
            print("\033[1m> Ending Testing\033[0m")
            break
        
        # restart carla every 'restart_interval' evaluations
        if sim_n%restart_interval == 0:
            global carla_pid
            print("\033[1m> Restarting Carla Server\033[0m")
            for pid in carla_pid:
                os.system("kill -9 " + pid)
            os.system("./launch_carla.sh")
            carla_pid = []
            for proc in psutil.process_iter():
                if process_name in proc.name():
                    carla_pid.append(str(proc.pid)) 
    
            print(carla_pid)
                    
        sim_n = sim_n + 1  
        
weather_parameters_list = ['cloudiness', 'fog_density', 'precipitation', 'precipitation_deposits', 
                        'sun_altitude_angle', 'sun_azimuth_angle', 'wetness', 'wind_intensity']

scenario_parameters_list = ['distance', 'blocker_model', 'crossing_angle']


def get_all_data():
    list_of_all_scenarios = os.listdir('/home/adarash/EvoDrive/EvoDrive/custom_scenarios/')

    for scenario in list_of_all_scenarios:

        print('\n\n' + scenario)

        scenes = os.listdir('/home/adarash/EvoDrive/EvoDrive/custom_scenarios/' + str(scenario))
        number_of_parameters = len(SCENARIO_TYPES[scenario])
        s_n = 0
        scenario_parameters_list = []

        for parameter in SCENARIO_TYPES[scenario]:
            scenario_parameters_list.append(parameter[0])

        if scenario_parameters_list == []:
            print('no parameters, skipping')
            continue

        print(scenario_parameters_list)

        list_of_parameters = []

        for scene in scenes:
            filepath = '/home/adarash/EvoDrive/EvoDrive/custom_scenarios/' + str(scenario) + '/' + str(scene)
            tree = ET.parse(filepath)    
            root = tree.getroot()
            route = root[0]
            scenarios = route.find('scenarios')
            scenario_in_file = scenarios.find('scenario')
            p_n = 0
            list_of_values = []
            for parameters in scenario_parameters_list:
                parameter = scenario_in_file.find(parameters)
                if parameter is not None:
                    list_of_values.append(parameter.get('value'))
                else:
                    list_of_values.append(0)
                p_n = p_n+1
            
            list_of_parameters.append(list_of_values)
            s_n = s_n + 1
            
        #print(list_of_parameters)
        mylist = list(map(list, zip(*list_of_parameters)))
        #print(mylist)
        mylist2 = []
        for field in mylist:
            mylist2.append(set(field))
        print(mylist2)

# Define the fitness function.
    def fitness_func(solution, solution_idx):
        # Extracting variables from the solution
        x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14 = solution

        # Example fitness function: This is a simple arbitrary function
        # that combines integers and floats. You should replace this with
        # your actual function.
        fitness = (
            x1 * np.sin(x2) +
            np.sqrt(x3 * x4) +
            np.log1p(x5) +
            x6**2 +
            5 * x7 +
            np.cos(x8) +
            x9 / (x10 + 1) +
            x11 * x12 - x13 +
            x14**3
        )

        # If your objective is to minimize, you can return -fitness.
        return fitness



if __name__ == '__main__':
    get_all_data()
    exit()
    
    global town
    
    #town = input('Town to test: ')
    town = 'Town01'
    max_evals = 500
    #tester = input('Tester to run[GA, RANDOM]: ')
    
    tester = 'RANDOM'
    
    # get carla pid
    for proc in psutil.process_iter():
        if process_name in proc.name():
            carla_pid.append(str(proc.pid)) 
    
    print(carla_pid)
    
    # run tester
    if tester == 'GA':
        #run_ga(max_evals)
        pass
    elif tester == 'RANDOM':
        run_random(max_evals)
