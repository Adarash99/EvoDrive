import carla
import os
import time
import random
import xml.etree.ElementTree as ET
import pygad
import json
import numpy as np
from parameters import *
from utils import *

import warnings
#warnings.filterwarnings("ignore")

weather_parameters_list = ['cloudiness', 'fog_density', 'fog_distance' 'precipitation', 'precipitation_deposits', 
                        'sun_altitude_angle', 'sun_azimuth_angle', 'wetness', 'wind_intensity']

scenario_list_all = ['StaticCutIn', 'VehicleTurningRoutePedestrian', 'ConstructionObstacle', 'HazardAtSideLane', 'EnterActorFlowV2', 'DynamicObjectCrossing', 'MergerIntoSlowTraffic', 'HighwayExit', 'VehicleOpensDoorTwoWays', 'Accident', 'ParkingCutIn', 'HighwayCutIn', 'ConstructionObstacleTwoWays', 'HardBreakRoute', 'InterurbanAdvancedActorFlow', 'SignalizedJunctionRightTurn', 'YieldToEmergencyVehicle', 'CrossingBicycleFlow', 'VehicleTurningRoute', 'EnterActorFlow', 'ParkedObstacleTwoWays', 'SignalizedJunctionLeftTurn', 'AccidentTwoWays', 'ControlLoss', 'OppositeVehicleTakingPriority', 'InvadingTurn', 'PriorityAtJunction', 'OppositeVehicleRunningRedLight', 'ParkedObstacle', 'BlockedIntersection', 'PedestrianCrossing', 'InterurbanActorFlow', 'ParkingCrossingPedestrian', 'NonSignalizedJunctionLeftTurn', 'NonSignalizedJunctionRightTurn', 'HazardAtSideLaneTwoWays']

scenario_list = ['VehicleTurningRoutePedestrian', 'EnterActorFlowV2', 'DynamicObjectCrossing', 'HardBreakRoute', 'InterurbanAdvancedActorFlow', 'SignalizedJunctionRightTurn', 'CrossingBicycleFlow', 'VehicleTurningRoute', 'EnterActorFlow', 'ParkedObstacleTwoWays', 'SignalizedJunctionLeftTurn', 'OppositeVehicleTakingPriority', 'InvadingTurn', 'PriorityAtJunction', 'OppositeVehicleRunningRedLight', 'PedestrianCrossing', 'InterurbanActorFlow', 'ParkingCrossingPedestrian', 'NonSignalizedJunctionLeftTurn', 'NonSignalizedJunctionRightTurn', 'HazardAtSideLaneTwoWays']

min_values = []
max_values = []


pwd = os.getcwd()
scenario_tested = 'DynamicObjectCrossing'
scenario_filepath = pwd + '/custom_scenarios/'
scenario_filepath = scenario_filepath + scenario_tested

sim_n = 0
number_of_tests = 0

restarting_interval = 4
process_name = 'Carla'

'''
############## Random Tester ##############
'''
def random_tester():
    test_number = 0
    file_number_list = []
    #scenario_tested = 'VehicleTurningRoutePedestrian' #random.choice(scenario_list)
    print("\033[1m> SCENARIO TESTED = {}\033[0m".format(scenario_tested))
    start = time.time()
    
    for i in range(100):
        restart(i)
        print("\033[1m> TEST NUMBER = {}\033[0m".format(test_number))
        
        n_var, v_type, v_ranges = prelims(scenario_tested)
       
        x = random_sampler(n_var, v_type, v_ranges)
        print("\033[1m> File number = {}\033[0m".format(x[0]))
        file_number_list.append(x[0])
        create_scenario(x, scenario_tested)
        driving_score = run_simulation()
        print("\033[1m> Average driving score = {}\033[0m".format(driving_score))
        time.sleep(3)
        save_route_data(test_number, x[0])
        test_number = test_number + 1
        print(file_number_list)

    print("\033[1m> TEST NUMBER = {}\033[0m".format(test_number))
    

    end = time.time()
    print(f"Time taken to run the code was {end-start} seconds")

def random_sampler(n_var, v_type, v_ranges):
        n = 0
        x = []
        for v_range in v_ranges:
            if v_type[n] == 'int':
                x.append(random.randint(v_range[0], v_range[1]))
            elif v_type[n] == 'float':
                x.append(random.uniform(v_range[0], v_range[1]))
            else:
                print('Variable type not valid -> ' + str(v_type[n]))
            n = n + 1
        return x

'''
############## Genetic Algorithm Tester ##############
'''

def ga_tester():
    # get gene space and num_genes automatically
    gene_space = prelims_ga()

    # Calculate min and max values
    for parameter in gene_space:
        min_values.append(parameter['low'])
        max_values.append(parameter['high'])

    num_genes = len(gene_space)
    #load previous instance
    #load = input('Enter the filename or leave empty: ')
    load = ''
    if load:
        print("\033[1m> Loading existing GA instance")
        ga_instance = pygad.load(load)
    else:       
        print("\033[1m> Creating new GA instance")
        # Genetic Algorithm Parameters
        ga_instance = pygad.GA(
            num_generations=20,  # Number of generations
            num_parents_mating=3, #3  # Number of solutions selected as parents in each generation
            fitness_func=fitness_func,  # Custom fitness function
            sol_per_pop=5, #5  # Population size
            num_genes=num_genes,  # Number of variables (genes)
            gene_type=[float, 1],  # Type of gene (int or float)
            gene_space=gene_space,
            on_mutation=on_mutation,
            allow_duplicate_genes=False,  # Range for each gene
            crossover_type="single_point", #single_point  # Crossover type
            mutation_type="random",  # Mutation type
            mutation_percent_genes=30, #20  # Percentage of genes to mutate
            save_solutions=True
            #stop_criteria="saturate_3"
        )

    ga_instance.save("ga_instance")

    # Running the Genetic Algorithm
    ga_instance.run()

    # Plot the fitness history
    ga_instance.plot_fitness()
    ga_instance.plot_genes()
    ga_instance.plot_new_solution_rate()

    print(ga_instance.solutions)

    # Print the details of the best solution.
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print(f"Best solution: {solution}")
    print(f"Best solution fitness: {solution_fitness}")

    # Predicting using the best solution
    prediction = ga_instance.best_solution_generation()
    print(f"Prediction: {prediction}")

def on_mutation(ga_instance, x):
    ## CHECK FOR DIVERSITY HERE
    ga_instance.save("ga_instance")
    print("\033[1m> Diversity check")
    modified_test, changed = calculate_diversity(x, scenario_tested, min_values, max_values)

    #print(modified_test)
    #print(x)

    if(changed):
        print("\033[1m> Similarity detected! Population changed")
        ga_instance.last_generation_offspring_mutation[0] = modified_test[0]
    else:
        print("\033[1m> No similarity detected! Population unchanged")

def fitness_func(ga_instance, solution, solution_idx):
        global number_of_tests
        number_of_tests = number_of_tests + 1
        restart(number_of_tests)
        # write the parameters to file
        print('SCENARIO FILE NUMBER = ' + str(solution[0]))
        print("\033[1m> TEST NUMBER = {}\033[0m".format(number_of_tests))

        create_scenario(solution, scenario_tested)
        driving_score  = float(run_simulation())
        time.sleep(3)
        
        save_route_data(number_of_tests, solution[0])
        

        print("\033[1m> DRIVING SCORE = {}\033[0m".format(driving_score))
        fitness = 100 - driving_score
        return fitness
        #return driving_score

'''
############## Common Functions ##############
'''

def run_simulation():
    #driving_score = 1000
    driving_score = 1000
    try:
        #run sim
        os.system("./leaderboard/run_leaderboard.sh")            
        #read json average driving score
        with open(leaderboard_results_filepath) as f:
            data = json.load(f)
        driving_score = float(data["values"][2]) # this is to ignore route completion results

    except Exception as e:
        print(e)
        restart(1000)
        run_simulation()

    return driving_score*100

if __name__ == '__main__':

    create_csv_file(scenario_tested)

    #tester = input("RA or GA: ")
    tester = "GA"
    if tester=='RA':
        random_tester()
    elif tester=='GA':
        ga_tester()
    else:
        print('N/A')
        exit()
    print("---------------- Testing Completed ----------------")
    kill_carla()