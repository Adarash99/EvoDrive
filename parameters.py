leaderboard_results_filepath = 'leaderboard/results.json'
leaderboard_input_file = 'leaderboard/data/custom_route.xml'

results_filepath = 'data/results/'
routes_filepath = 'data/routes'


carla_pid = []

### Genetic Algorithm variables ####

restart_interval = 5
pop_size = 15
#n_max_gen = 30 #not used
max_time = "10:00:00"
sim_n = 1

####################################

WEATHERS = {     'cloudiness': [0,100], 
                 'fog_density': [0,100],  #[0,100]
                 'fog_distance': [0,100], #[0,100]
                 'precipitation': [0,100], 
                 'precipitation_deposits': [0,100], 
                 'route_percentage' : [0,100],
                 'sun_altitude_angle': [-90,90], 
                 'sun_azimuth_angle': [0,360], 
                 'wetness': [0,100], 
                 'wind_intensity': [0,100]
                 }

TOWNS = ['Town01', 
         'Town02', 
         'Town03', 
         'Town04', 
         'Town05', 
         'Town06', 
         'Town07', 
         'Town10HD', 
         'Town12']


SPAWN_POINTS = [
    
]

SCENARIOS = ['StaticCutIn', 'VehicleTurningRoutePedestrian', 'ConstructionObstacle', 'HazardAtSideLane', 'EnterActorFlowV2', 'DynamicObjectCrossing', 'MergerIntoSlowTraffic', 'HighwayExit', 'VehicleOpensDoorTwoWays', 'Accident', 'ParkingCutIn', 'HighwayCutIn', 'ConstructionObstacleTwoWays', 'HardBreakRoute', 'InterurbanAdvancedActorFlow', 'SignalizedJunctionRightTurn', 'YieldToEmergencyVehicle', 'CrossingBicycleFlow', 'VehicleTurningRoute', 'EnterActorFlow', 'ParkedObstacleTwoWays', 'ParkingExit', 'SignalizedJunctionLeftTurn', 'AccidentTwoWays', 'ControlLoss', 'OppositeVehicleTakingPriority', 'MergerIntoSlowTrafficV2', 'InvadingTurn', 'PriorityAtJunction', 'OppositeVehicleRunningRedLight', 'ParkedObstacle', 'BlockedIntersection', 'PedestrianCrossing', 'InterurbanActorFlow', 'ParkingCrossingPedestrian', 'NonSignalizedJunctionLeftTurn', 'NonSignalizedJunctionRightTurn', 'HazardAtSideLaneTwoWays']

SCENARIO_TYPES ={

    # Junction scenarios
    "SignalizedJunctionLeftTurn": [
        ["flow_speed", "value", [8, 20]]
    ],
    "SignalizedJunctionRightTurn": [
        ["flow_speed", "value", [8, 20]]
    ],
    "OppositeVehicleRunningRedLight": [
    ],
    "NonSignalizedJunctionLeftTurn": [
        ["flow_speed", "value", [8, 20]]
    ],
    "NonSignalizedJunctionRightTurn": [
        ["flow_speed", "value", [8, 20]]
    ],
    "OppositeVehicleTakingPriority": [
    ],

    # Crossing actors
    "DynamicObjectCrossing": [
        ["distance", "value", [10, 70]],
        ["blocker_model", "choice", ['static.prop.foodcart', 'static.prop.advertisement', 'static.prop.haybalelb', 
                                     'static.prop.busstoplb', 'static.prop.container']],
        ["crossing_angle", "value", [-10, 70]]
    ],


    "ParkingCrossingPedestrian": [
        ["distance", "value", [0, 50]],
        ["crossing_angle", "value", [0, 20]]
    ],
    "PedestrianCrossing": [
    ],
    "VehicleTurningRoute": [
    ],
    "VehicleTurningRoutePedestrian": [
    ],
    "BlockedIntersection": [
    ],

    # Actor flows
    "EnterActorFlow": [
        ["flow_speed", "value", [14, 21]]
    ],
    "EnterActorFlowV2": [
        ["flow_speed", "value", [14, 22]]
    ],
    "InterurbanActorFlow": [
        ["flow_speed", "value", [14, 20]]
    ],
    "InterurbanAdvancedActorFlow": [
        ["flow_speed", "value", [14, 18]]
    ],
    "HighwayExit": [
        ["flow_speed", "value", [9, 16]]
    ],
    "MergerIntoSlowTraffic": [
        ["flow_speed", "value", [8, 18]]
    ],
    "MergerIntoSlowTrafficV2": [            # no point, only has 3 scenes
        ["flow_speed", "value", [10]]
    ],
    "CrossingBicycleFlow": [
        ["flow_speed", "value", [4, 10]]
    ],

    # Route obstacles
    "ConstructionObstacle": [
        ["distance", "value", [0, 200]],
        ["speed", "value", [0, 60]],
    ],
    "ConstructionObstacleTwoWays": [
        ["distance", "value", [70, 250]]
    ],
    "Accident": [
        ["distance", "value", [0, 200]],
        ["speed", "value", [0, 70]],
    ],
    "AccidentTwoWays": [
        ["distance", "value", [70, 200]]
    ],
    "ParkedObstacle": [
        ["distance", "value", [0, 150]],
        ["speed", "value", [0, 70]],
    ],
    "ParkedObstacleTwoWays": [
        ["distance", "value", [0, 150]]
    ],
    "VehicleOpensDoorTwoWays": [
        ["distance", "value", [35, 70]]
    ],
    "HazardAtSideLane": [
        ["distance", "value", [50, 100]],
        ["speed", "value", [25, 65]],
        ["bicycle_drive_distance", "value", [60, 200]],
        ["bicycle_speed", "value", [5, 17]],
    ],
    "HazardAtSideLaneTwoWays": [
        ["distance", "value", [40, 110]],
        ["frequency", "value", [75, 140]],
        ["bicycle_drive_distance", "value", [40, 300]],
        ["bicycle_speed", "value", [5, 17]],
    ],
    "InvadingTurn": [
        ["distance", "value", [80, 180]],
        ["offset", "value", [0.2, 0.6]],
    ],

    # Cut ins
    "HighwayCutIn": [
    ],
    "ParkingCutIn": [
    ],
    "StaticCutIn": [
        ["distance", "value", [70, 200]]
    ],

    # Others
    "ControlLoss": [
    ],
    "HardBreakRoute": [
    ],
    "ParkingExit": [                # no point, ads not able
        ["direction", "choice"],
        ["front_vehicle_distance", "value"],
        ["behind_vehicle_distance", "value"],
    ],
    "YieldToEmergencyVehicle": [    # no point, ads not able
        ["distance", "value", [100, 150]],
    ],

    # Special ones
    "BackgroundActivityParametrizer": [
        ["num_front_vehicles", "value"],
        ["num_back_vehicles", "value"],
        ["road_spawn_dist", "value"],
        ["opposite_source_dist", "value"],
        ["opposite_max_actors", "value"],
        ["opposite_spawn_dist", "value"],
        ["opposite_active", "bool"],
        ["junction_source_dist", "value"],
        ["junction_max_actors", "value"],
        ["junction_spawn_dist", "value"],
        ["junction_source_perc", "value"],
    ],
    "PriorityAtJunction": [
    ],
}
