#! /bin/bash

xhost +

docker run -it --rm \
    -v $(pwd)/EvoDrive/:/EvoDrive \
    -v $(pwd)/Carla/:/Carla \
    --env="QT_X11_NO_MITSHM=1" \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e SDL_VIDEODRIVER=x11 \
    -e DISPLAY=$DISPLAY \
    --net=host \
    --runtime=nvidia \
    --privileged \
    --gpus all \
    ctester:v1 bash
