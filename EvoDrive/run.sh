#!/bin/bash


##################################
kill -9 -1
xhost +

##################################


export ROOT=/EvoDrive
export CARLA_ROOT=/Carla
export LEADERBOARD_ROOT=/${ROOT}/leaderboard
export SCENARIO_RUNNER_ROOT=/${ROOT}/scenario_runner


##################################
sudo chown -R carla ${LEADERBOARD_ROOT} ${SCENARIO_RUNNER_ROOT}
#sudo chown -R carla ${CARLA_ROOT}
##################################


export PORT=2000
export ROUTES=${LEADERBOARD_ROOT}/data/custom_route.xml
#export ROUTES=${LEADERBOARD_ROOT}/data/routes_training.xml
export REPETITIONS=1
export DEBUG_CHALLENGE=1

#export TEAM_AGENT=${LEADERBOARD_ROOT}/leaderboard/autoagents/npc_agent_modified.py
#export TEAM_AGENT=${LEADERBOARD_ROOT}/leaderboard/autoagents/human_agent.py
#export TEAM_AGENT=${LEADERBOARD_ROOT}/leaderboard/autoagents/npc_agent.py

#export TEAM_AGENT=${LEADERBOARD_ROOT}/team_code/interfuser_agent.py
#export TEAM_CONFIG=${LEADERBOARD_ROOT}/team_code/interfuser_config.py

export TEAM_AGENT=${LEADERBOARD_ROOT}/team_code/tcp_agent.py
export TEAM_CONFIG=${LEADERBOARD_ROOT}/team_code/tcp.ckpt


export CHECKPOINT_ENDPOINT=${LEADERBOARD_ROOT}/results.json
export CHALLENGE_TRACK_CODENAME=SENSORS

export PYTHONPATH="${SCENARIO_RUNNER_ROOT}":"${LEADERBOARD_ROOT}":"${CARLA_ROOT}/PythonAPI/carla":$PYTHONPATH
export PYTHONPATH="${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.14-py3.7-linux-x86_64.egg":$PYTHONPATH

# launch carla world
$CARLA_ROOT/CarlaUE4.sh -quality-level=low -world-port=$PORT -RenderOffScreen &
#$CARLA_ROOT/CarlaUE4.sh -quality-level=low -world-port=$PORT -resx=800 -resy=600 &
PID=$!
echo "Carla PID=$PID"

sleep 10

#./leaderboard/scripts/run_evaluation.sh
python3.7 ./ga_tester.py
#python3.7 ./random_tester.py
