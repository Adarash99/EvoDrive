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

import os
import numpy as np
import random
import time
import json
import math
import carla
import psutil

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



class MyProblem(ElementwiseProblem):
    
    def __init__(self, n_var, n_obj, n_ieq_constr, n_eq_constr, xl, xu):
        self.n_var = n_var
        self.n_obj = n_obj
        self.n_ieq_constr = n_ieq_constr
        self.n_eq_constr = n_eq_constr
        self.xl = xl
        self.xu = xu
        super().__init__(n_var=self.n_var, n_obj=self.n_obj, n_ieq_constr=self.n_ieq_constr, n_eq_constr=self.n_eq_constr, xl=self.xl, xu=self.xu)
        
    def _evaluate(self, x, out, *args, **kwargs):
        global sim_n
        
        print("\n")
        print("\n\033[1m========= Generating Scene_eval_n_{} =========\033[0m".format(sim_n))
        out["F"] = run_simulation(x)
        #out["G"] = x[9]-x[10]-5
        #out["H"] = x[10]-x[11]
        
        # save data to csv file
        save_route_data(sim_n)
        
        # restart carla every 'restart_interval' evaluations
        if sim_n%restart_interval == 0:
            global carla_pid
            print("\033[1m> Restarting Carla Server\033[0m")
            for pid in carla_pid:
                os.system("kill -9 " + pid)
            os.system("./launch_carla.sh")
            carla_pid = []
            for proc in psutil.process_iter():
                if 'Carla'  in proc.name():
                    carla_pid.append(str(proc.pid))
                    
        sim_n = sim_n + 1

def run_ga(max_evals):
    
    n_var = 11
    
    # -> cloudiness [0,100]
    # -> fog_density [0,100]
    # -> fog_distance [0,100]
    # -> precipitation [0,100] 
    # -> precipitation_deposits [0,100] 
    # -> sun_altitude_angle [-90,90] 
    # -> sun_azimuth_angle [0,360] 
    # -> wetness [0,100] 
    # -> wind_intensity [0,100]

    # -> initial_waypoint [depends on town] -> map (0,100) to (0, len(all_spawn_points))
    # -> final_waypoint   [depends on town]
    
    # -> scenario NOT FIXED YET
    
    n_obj = 1
    xl = np.array([0,0,0,0,0,-90,0,0,0,0,0])
    xu = np.array([100,100,100,100,100,90,360,100,100,100,100])
    
    # termination criteria:
    #     n_eval 
    #     n_gen
    #     time

    # operators not used yet
    sampling = FloatRandomSampling()
    selection = RandomSelection()
    crossover = SBX()
    mutation = PolynomialMutation(prob=1.0, eta=10)
    
    algorithm = GA(pop_size,
                   eliminate_duplicates = True)
    
    problem = MyProblem(n_var, n_obj, 0, 0, xl, xu)
    termination = get_termination("n_eval", max_evals)
    
    res = minimize(problem,
                   algorithm,
                   termination,
                   seed = 1,
                   verbose=True,
                   save_history=True)
    
    
    print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))
    
    print("\033[1m> Ending Testing\033[0m")

    #F = problem.pareto_front()
    #Scatter().add(F).show()


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
        
        
        
        
if __name__ == '__main__':
    global town
    
    #town = input('Town to test: ')
    town = 'Town01'
    max_evals = 500
    tester = input('Tester to run[GA, RANDOM]: ')
    
    #tester = 'RANDOM'
    
    # get carla pid
    for proc in psutil.process_iter():
        if process_name in proc.name():
            carla_pid.append(str(proc.pid)) 
    
    print(carla_pid)
    
    # run tester
    if tester == 'GA':
        run_ga(max_evals)
    elif tester == 'RANDOM':
        run_random(max_evals)
