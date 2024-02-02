leaderboard_results_filepath = 'leaderboard/results.json'
leaderboard_input_file = 'leaderboard/data/custom_route.xml'

results_filepath = 'data/results/'
routes_filepath = 'data/routes'

process_name = "Carla"
carla_pid = []

### Genetic Algorithm variables ####

restart_interval = 5
pop_size = 15
#n_max_gen = 30 #not used
max_time = "19:00:00"
sim_n = 1

####################################

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


SCENARIO_TYPES ={

    # Junction scenarios
    "SignalizedJunctionLeftTurn": [
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "SignalizedJunctionRightTurn": [
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "OppositeVehicleRunningRedLight": [
        ["direction", "choice"],
    ],
    "NonSignalizedJunctionLeftTurn": [
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "NonSignalizedJunctionRightTurn": [
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "OppositeVehicleTakingPriority": [
        ["direction", "choice"],
    ],

    # Crossing actors
    "DynamicObjectCrossing": [
        ["distance", "value"],
        ["direction", "value"],
        ["blocker_model", "value"],
        ["crossing_angle", "value"]
    ],
    "ParkingCrossingPedestrian": [
        ["distance", "value"],
        ["direction", "choice"],
        ["crossing_angle", "value"],
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
        ["start_actor_flow", "location driving"],
        ["end_actor_flow", "location driving"],
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "EnterActorFlowV2": [
        ["start_actor_flow", "location driving"],
        ["end_actor_flow", "location driving"],
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "InterurbanActorFlow": [
        ["start_actor_flow", "location driving"],
        ["end_actor_flow", "location driving"],
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "InterurbanAdvancedActorFlow": [
        ["start_actor_flow", "location driving"],
        ["end_actor_flow", "location driving"],
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "HighwayExit": [
        ["start_actor_flow", "location driving"],
        ["end_actor_flow", "location driving"],
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "MergerIntoSlowTraffic": [
        ["start_actor_flow", "location driving"],
        ["end_actor_flow", "location driving"],
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "MergerIntoSlowTrafficV2": [
        ["start_actor_flow", "location driving"],
        ["end_actor_flow", "location driving"],
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],
    "CrossingBicycleFlow": [
        ["start_actor_flow", "location bicycle"],
        ["flow_speed", "value"],
        ["source_dist_interval", "interval"],
    ],

    # Route obstacles
    "ConstructionObstacle": [
        ["distance", "value"],
        ["direction", "value"],
        ["speed", "value"],
    ],
    "ConstructionObstacleTwoWays": [
        ["distance", "value"],
        ["frequency", "interval"],
    ],
    "Accident": [
        ["distance", "value"],
        ["direction", "value"],
        ["speed", "value"],
    ],
    "AccidentTwoWays": [
        ["distance", "value"],
        ["frequency", "interval"],
    ],
    "ParkedObstacle": [
        ["distance", "value"],
        ["direction", "value"],
        ["speed", "value"],
    ],
    "ParkedObstacleTwoWays": [
        ["distance", "value"],
        ["frequency", "interval"],
    ],
    "VehicleOpensDoorTwoWays": [
        ["distance", "value"],
        ["frequency", "interval"],
    ],
    "HazardAtSideLane": [
        ["distance", "value"],
        ["speed", "value"],
        ["bicycle_drive_distance", "value"],
        ["bicycle_speed", "value"],
    ],
    "HazardAtSideLaneTwoWays": [
        ["distance", "value"],
        ["frequency", "value"],
        ["bicycle_drive_distance", "value"],
        ["bicycle_speed", "value"],
    ],
    "InvadingTurn": [
        ["distance", "value"],
        ["offset", "value"],
    ],

    # Cut ins
    "HighwayCutIn": [
        ["other_actor_location", "location driving"],
    ],
    "ParkingCutIn": [
        ["direction", "choice"],
    ],
    "StaticCutIn": [
        ["distance", "value"],
        ["direction", "choice"],
    ],

    # Others
    "ControlLoss": [
    ],
    "HardBreakRoute": [
    ],
    "ParkingExit": [
        ["direction", "choice"],
        ["front_vehicle_distance", "value"],
        ["behind_vehicle_distance", "value"],
    ],
    "YieldToEmergencyVehicle": [
        ["distance", "value"],
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