from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize
from pymoo.termination import get_termination
import os
import numpy as np
import xml.etree.ElementTree as ET
import json

WEATHERS = {'route_percentage': [100,100],
                 'cloudiness': [0,100], 
                 'fog_density': [0,10],  #[0,100]
                 'fog_distance': [0,10], #[0,100]
                 'precipitation': [0,100], 
                 'precipitation_deposits': [0,100], 
                 'sun_altitude_angle': [-90,90], 
                 'sun_azimuth_angle': [0,360], 
                 'wetness': [0,100], 
                 'wind_intensity': [0,100]
                 }

def run_simulation(x):
    
    weather_values = list(np.around(np.array(x),1)) 
    weather_values.insert(0, 100.0)
    weather_settings = []
    n = 0
    for key, value in WEATHERS.items():
        weather_value =  weather_values[n]
        weather_settings.append((str(key), weather_value))  
        n = n + 1

    route = []
    scen_type_list = []
    scenario_attributes_list = []
    
    #save xml
    generate_xml(route, dict(weather_settings), scen_type_list, scenario_attributes_list)
    
    #run sim
    os.system("./leaderboard/scripts/run_evaluation.sh")
    
    #read json average driving score
    with open('leaderboard/results.json') as f:
        data = json.load(f)
        
    driving_score = data["values"][0]
    
    return driving_score



def generate_xml(route, weather_settings, scen_type_list, scenario_attributes_list):
        #positions = []
        #positions = self.__get_list_of_positions(route)
        root = ET.Element('routes')
        route = ET.SubElement(root, 'route')
       
        route.set('id', '0')
        route.set('town', 'Town05')
        
        weathers = ET.SubElement(route, 'weathers')
        weather = ET.SubElement(weathers, 'weather')

        for key, value in weather_settings.items():
            weather.set(str(key), str(value))
        
        waypoints = ET.SubElement(route, 'waypoints')
        
        # start point
        waypoint = ET.SubElement(waypoints, 'position')
        waypoint.set('x', '189.7')
        waypoint.set('y', '-11.0')
        waypoint.set('z', '1.0')
        # end point
        waypoint = ET.SubElement(waypoints, 'position')
        waypoint.set('x', '155.0')
        waypoint.set('y', '169.1')
        waypoint.set('z', '0.0')

        scenarios = ET.SubElement(route, 'scenarios')        
                
        ########################### scenario definition
        
        for n in range(0, len(scen_type_list)):
        
            scen_type = scen_type_list[n]
            scenario_attributes = scenario_attributes_list[n]
            
            new_scenario = ET.SubElement(scenarios, "scenario")
            new_scenario.set("name", scen_type + "_" + str(n))
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
        tree.write('leaderboard/data/custom_route.xml')
        
        
        

class MyProblem(ElementwiseProblem):
    def __init__(self, n_var, n_obj, xl, xu):
        self.n_var = n_var
        self.n_obj = n_obj
        self.xl = xl
        self.xu = xu
        super().__init__(n_var=self.n_var, n_obj=self.n_obj, xl=self.xl, xu=self.xu)
        
    def _evaluate(self, x, out, *args, **kwargs):
        
        #print(x)
        out["F"] = run_simulation(x)
        


def run_ga():
    
    n_var = 9
    n_obj = 1
    xl = np.array([0,0,0,0,0,-90,0,0,0])
    xu = np.array([100,100,100,100,100,90,360,100,100])
    
    # termination criteria:
    #     n_eval 
    #     n_gen
    #     time


    algorithm = GA(pop_size=10)
    problem = MyProblem(n_var, n_obj, xl, xu)
    #termination = get_termination("time", "00:00:30")

    result = minimize(problem, algorithm, seed = 2, verbose=True)




if __name__ == '__main__':
    
    run_ga()