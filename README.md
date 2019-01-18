# MPI Project - Winter Semester 2018/2019
Builds a docker image for simulating a MPI cluster. 
The goal is to run a parallelized version of the iterative deepening depth-first search (IDDFS) algorithm.
The algorithm and formalizations tree search problems is loaded from [another git repository](https://github.com/OrangeFoil/artificial-intelligence-ws-18-19) via a git submodule.  

## Prerequisites
* Bash
* Docker

## Quickstart
Run `./build.sh` to build the docker image.  
Run `./run.sh` to fire up a MPI cluster and run the application.
