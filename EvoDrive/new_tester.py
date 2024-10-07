import carla
import os
import time
from agents.navigation.global_route_planner import GlobalRoutePlanner
import random
import xml.etree.ElementTree as ET
import pygad
import numpy as np
from parameters import *
from utils import *
from new_ga_tester import *
from new_ga_tester import GaTester

weather_parameters_list = ['cloudiness', 'fog_density', 'fog_distance' 'precipitation', 'precipitation_deposits', 
                        'sun_altitude_angle', 'sun_azimuth_angle', 'wetness', 'wind_intensity']

scenario_list = ['StaticCutIn', 'VehicleTurningRoutePedestrian', 'ConstructionObstacle', 'HazardAtSideLane', 'EnterActorFlowV2', 'DynamicObjectCrossing', 'MergerIntoSlowTraffic', 'HighwayExit', 'VehicleOpensDoorTwoWays', 'Accident', 'ParkingCutIn', 'HighwayCutIn', 'ConstructionObstacleTwoWays', 'HardBreakRoute', 'InterurbanAdvancedActorFlow', 'SignalizedJunctionRightTurn', 'YieldToEmergencyVehicle', 'CrossingBicycleFlow', 'VehicleTurningRoute', 'EnterActorFlow', 'ParkedObstacleTwoWays', 'SignalizedJunctionLeftTurn', 'AccidentTwoWays', 'ControlLoss', 'OppositeVehicleTakingPriority', 'InvadingTurn', 'PriorityAtJunction', 'OppositeVehicleRunningRedLight', 'ParkedObstacle', 'BlockedIntersection', 'PedestrianCrossing', 'InterurbanActorFlow', 'ParkingCrossingPedestrian', 'NonSignalizedJunctionLeftTurn', 'NonSignalizedJunctionRightTurn', 'HazardAtSideLaneTwoWays']

scenario_tested = 'PedestrianCrossing'
scenario_filepath = '/home/adarash/EvoDrive/EvoDrive/custom_scenarios/'
scenario_filepath = scenario_filepath + scenario_tested


class RandomTester():  
    def __init__(self, n_var, v_type, v_ranges):
        print('Initializing Random Tester')
        self.n_var = n_var
        self.v_ranges = v_ranges
        self.v_type = v_type
        #self.x = []

    def get_parameters(self):
        n = 0
        x = []
        for v_range in self.v_ranges:
            if self.v_type[n] == 'int':
                x.append(random.randint(v_range[0], v_range[1]))
            elif self.v_type[n] == 'float':
                x.append(random.uniform(v_range[0], v_range[1]))
            else:
                print('Variable type not valid -> ' + str(self.v_type[n]))
            n = n + 1
        return x


def main():
    scores = []

    # tester = GaTester(scenario_tested)
    # num_genes = 13
    # tester.run_ga(num_genes)

    for scenario_tested in scenario_list:
        print("\033[1m> SCENARIO TESTED = {}\033[0m".format(scenario_tested))
        n_var, v_type, v_ranges = prelims(scenario_tested)
        tester = RandomTester(n_var, v_type, v_ranges)
        x = tester.get_parameters()
        print("\033[1m> File number = {}\033[0m".format(x[0]))
        create_scenario(x, scenario_tested)
        driving_score = run_simulation()
        scores.append(driving_score)
        print("\033[1m> Average driving score = {}\033[0m".format(driving_score))
        time.sleep(10)


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
    v_type = []
    v_ranges = []
    # calculate the number of variables required for the scenario
    n_var = n_var + len(SCENARIO_TYPES[scenario_tested])
    # type and range for variable 0
    
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

def create_scenario(x, scenario_tested):
    scenario_filepath = '/home/adarash/EvoDrive/EvoDrive/custom_scenarios/'
    scenario_filepath = scenario_filepath + scenario_tested
    filepath = '/home/adarash/EvoDrive/EvoDrive/leaderboard/data/custom_route.xml'
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

def run_simulation():
    
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

    return driving_score

if __name__ == '__main__':
    main()