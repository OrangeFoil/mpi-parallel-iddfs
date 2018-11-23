#!/bin/python3

from mpi4py import MPI

size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()


def do_some_task(n: int):
    if n == 42:
        return (True, n, "I am #42")
    else:
        return (False, n, None)

# distribute tasks
if rank == 0:
    n = [i + 40 for i in range(size)]
else:
    n = None
n = MPI.COMM_WORLD.scatter(n, root=0)

# compute results
if rank == 0:
    data = None
else:
    data = do_some_task(n)

# collect results
data = MPI.COMM_WORLD.gather(data, root=0)
if rank == 0:
    for i in range(1, size):
        if data[i][0]:
            print("Node", i, "found a solution for n =",
                  data[i][1], "=>", data[i][2])
        else:
            print("Node", i, "did not find a solution for n =", data[i][1])
else:
    assert data is None
