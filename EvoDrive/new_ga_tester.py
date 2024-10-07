import os
import xml.etree.ElementTree as ET
import time
import pygad
import numpy as np
from parameters import *
from utils import *
import psutil

process_name = 'Carla'
scenario_filepath = '/home/adarash/EvoDrive/EvoDrive/custom_scenarios/'
restarting_interval = 5
run_number = 0
carla_pid = []

def on_generation(ga_instance):
    print("\033[1m> HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\033[0m")
    if (run_number % restarting_interval):
        print("\033[1m> Restarting Carla Server\033[0m")
        for pid in carla_pid:
            os.system("kill -9 " + pid)
        os.system("./launch_carla.sh")
        time.sleep(10)
        carla_pid = []
        for proc in psutil.process_iter():
            if process_name  in proc.name():
                carla_pid.append(str(proc.pid))
    
    

class GaTester():

    
    def __init__(self, scenario_tested):
        self.scenario_tested = scenario_tested
        self._scenario_filepath = scenario_filepath + scenario_tested
        

        for proc in psutil.process_iter():
            if process_name in proc.name():
                carla_pid.append(str(proc.pid)) 
        print(carla_pid)
        

    def _fitness_func(self, ga_instance, solution, solution_idx):
        # write the parameters to file
        print('SCENARIO FILE NUMBER = ' + str(solution[0]))
        self._create_scenario(solution, self.scenario_tested)
        fitness  = float(self._run_simulation())
        return fitness
    
    def _run_simulation(self):
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
        print('Driving Score = ' + str(driving_score ))
        return driving_score
    
    def run_ga(self, num_genes):
        # get gene space and num_genes automatically

        gene_space = self._prelims_ga()

        # Genetic Algorithm Parameters
        ga_instance = pygad.GA(
            num_generations=100,  # Number of generations
            num_parents_mating=5,  # Number of solutions selected as parents in each generation
            fitness_func=self._fitness_func,  # Custom fitness function
            sol_per_pop=20,  # Population size
            num_genes=num_genes,  # Number of variables (genes)
            gene_type=float,  # Type of gene (int or float)
            gene_space=gene_space,  # Range for each gene
            on_generation=on_generation,
            crossover_type="single_point",  # Crossover type
            mutation_type="random",  # Mutation type
            mutation_percent_genes=10,  # Percentage of genes to mutate
            save_solutions=False,
            stop_criteria="saturate_3" 
        )

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

    def _prelims_ga(self):
        # variables needed for RandomTester
        n_var = 10 # + variables required for the scenario
        gene_space = []
        # calculate the number of variables required for the scenario
        n_var = n_var + len(SCENARIO_TYPES[self.scenario_tested])
        # type and range for variable 0
        
        gene_space.append({'low': 1, 'high': len(os.listdir(scenario_filepath)), 'step': 1})

        # type and range for 8 weather variables
        for parameter in WEATHERS:
            gene_space.append({'low': WEATHERS[parameter][0], 'high': WEATHERS[parameter][1], 'step': 0.5})

        # type and range for scenario variables
        for parameter in SCENARIO_TYPES[self.scenario_tested]:
            if parameter[1] == 'value':
                gene_space.append({'low': parameter[2][0], 'high': parameter[2][1], 'step': 0.5})
                
            elif parameter[1] == 'choice':
                gene_space.append({'low': 0, 'high': len(parameter[2]), 'step': 1})
                
            else:
                print('There is something wrong with the SCENARIO_TYPES variable')
        
        return gene_space
    
    
    def _create_scenario(self, x, scenario_tested):
        filepath = '/home/adarash/EvoDrive/EvoDrive/leaderboard/data/custom_route.xml'
        n = 0
        new_scenario_filepath = self._scenario_filepath +'/' + str(int(x[0])) + '.xml'
        n = n+1
        os.system('cp ' + new_scenario_filepath + ' ' + filepath)

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
