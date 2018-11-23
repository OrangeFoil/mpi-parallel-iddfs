#!/bin/bash
NODES=8

echo "Creating Docker network"
docker network create mpi-net

echo "Starting master"
docker run -d --rm --hostname=mpi-master --memory=1g --name=mpi-master --network=mpi-net mpi-parallel-iddfs

echo "Starting $NODES nodes"
i=0
hosts=mpi-master
while [ $i -lt $NODES ]; do
    docker run -d --rm --hostname="mpi-node$i" --memory=1g --name="mpi-node$i" --network=mpi-net mpi-parallel-iddfs
    hosts=$hosts,mpi-node$i
    ((i++))
done

echo "Familiarize the master with its nodes" # this is necessary to populate '.ssh/known_hosts'
i=0
while [ $i -lt $NODES ]; do
    docker exec mpi-master ssh -o'StrictHostKeyChecking=no' root@mpi-node$i echo -n
    ((i++))
done

echo "Executing mpirun on the master"
echo "--------------------------------------------------------------"
docker exec mpi-master mpirun --allow-run-as-root --host $hosts python3 main.py
echo "--------------------------------------------------------------"

echo "Stopping master"
docker stop mpi-master

echo "Stopping worker nodes"
i=0
while [ $i -lt $NODES ]; do
    docker stop mpi-node$i
    ((i++))
done

echo "Deleting Docker network"
docker network rm mpi-net
