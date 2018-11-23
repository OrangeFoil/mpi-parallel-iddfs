#!/bin/python3

from mpi4py import MPI

size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()

#data = (rank + 1)**2
data = "I am process {} of {} on {}".format(rank, size, name)
data = MPI.COMM_WORLD.gather(data, root=0)
if rank == 0:
    print("Got data", data)
else:
    assert data is None
