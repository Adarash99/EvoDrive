#!/bin/bash


##################################
#kill -9 -1
#pkill -9 Carla
#pkill -9 python
#xhost +

##################################


export ROOT=/home/adarash/EvoDrive/EvoDrive
export CARLA_ROOT=/home/adarash/EvoDrive/CARLA_Leaderboard
export LEADERBOARD_ROOT=/${ROOT}/leaderboard
export SCENARIO_RUNNER_ROOT=/${ROOT}/scenario_runner


##################################
#sudo chown -R carla ${LEADERBOARD_ROOT} ${SCENARIO_RUNNER_ROOT}
#sudo chown -R carla ${CARLA_ROOT}
##################################


export PORT=2000
export ROUTES=${LEADERBOARD_ROOT}/data/custom_route.xml
#export ROUTES=${LEADERBOARD_ROOT}/data/routes_training.xml
#export ROUTES=${ROOT}/custom_scenarios/DynamicObjectCrossing/1.xml
export ROUTES_SUBSET=0
export REPETITIONS=1
export DEBUG_CHALLENGE=1

#export TEAM_AGENT=${LEADERBOARD_ROOT}/leaderboard/autoagents/npc_agent_modified.py
#export TEAM_AGENT=${LEADERBOARD_ROOT}/leaderboard/autoagents/human_agent.py
export TEAM_AGENT=${LEADERBOARD_ROOT}/leaderboard/autoagents/npc_agent.py

#export TEAM_AGENT=${LEADERBOARD_ROOT}/team_code/interfuser_agent.py
#export TEAM_CONFIG=${LEADERBOARD_ROOT}/team_code/interfuser_config.py

#export TEAM_AGENT=${LEADERBOARD_ROOT}/team_code/tcp_agent.py
#export TEAM_CONFIG=${LEADERBOARD_ROOT}/team_code/tcp.ckpt


export CHECKPOINT_ENDPOINT=${LEADERBOARD_ROOT}/results.json
export CHALLENGE_TRACK_CODENAME=SENSORS

export PYTHONPATH="${SCENARIO_RUNNER_ROOT}":"${LEADERBOARD_ROOT}":"${CARLA_ROOT}/PythonAPI/carla":$PYTHONPATH
export PYTHONPATH="${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.14-py3.7-linux-x86_64.egg":$PYTHONPATH

# launch carla world
#$CARLA_ROOT/CarlaUE4.sh -quality-level=low -world-port=$PORT -RenderOffScreen &
#$CARLA_ROOT/CarlaUE4.sh -quality-level=low -world-port=$PORT -resx=800 -resy=600 &
#PID=$!
#echo "Carla PID=$PID"

#sleep 15

python ./new_tester.py
#./leaderboard/run_leaderboard.sh
#python3.7 ./ga_tester.py
#python3.7 ./random_tester.py
