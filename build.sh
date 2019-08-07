#!/bin/bash

# docker build script

set -e

cd $(dirname $0)

DOCKERFILE="Dockerfile"

if [ ! $(which docker) ]; then echo "*** missing docker, please install docker ***"; exit 1; fi
if [ ! -f $DOCKERFILE ]; then echo "*** missing $DOCKERFILE ***"; exit 1; fi

# get dockername
STR=$(cat $DOCKERFILE | grep LABEL | grep dockername) || { echo "failed"; exit 1; }
DOCKERNAME=$(echo "$STR" | cut -d '=' -f 2 | cut -d ' ' -f 3 | sed  's/"//g') || { echo "failed"; exit 1; }

# get dockertag
STR=$(cat $DOCKERFILE | grep LABEL | grep dockertag) || { echo "failed"; exit 1; }
DOCKERTAG=$(echo "$STR" | cut -d '=' -f 2 | cut -d ' ' -f 3 | sed  's/"//g') || { echo "failed"; exit 1; }

set -ex

# build image
docker build -t $DOCKERNAME:$DOCKERTAG .
docker tag $DOCKERNAME:$DOCKERTAG $DOCKERNAME:latest

# test image
#docker run --rm --entrypoint "/usr/local/bin/pytest" $DOCKERNAME:$DOCKERTAG "/hev/tests"
# big shm-size for chrome to work
docker run --rm --shm-size 2g --entrypoint "/usr/local/bin/pytest" $DOCKERNAME:$DOCKERTAG "/hev/tests"

# push image
REGISTRY="rancher.n7sa.com:5000"
docker tag $DOCKERNAME $REGISTRY/$DOCKERNAME:$DOCKERTAG
docker tag $DOCKERNAME $REGISTRY/$DOCKERNAME:latest
docker push $REGISTRY/$DOCKERNAME:$DOCKERTAG
docker push $REGISTRY/$DOCKERNAME:latest

# list image
docker images | grep $DOCKERNAME
