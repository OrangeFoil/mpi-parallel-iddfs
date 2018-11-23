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

# coordination
solution_found = False
if rank == 0:
    batch = 0

while not solution_found:
    # distribute tasks
    if rank == 0:
        num_worker_nodes = size - 1
        n = [batch * num_worker_nodes + i for i in range(size)]
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
                solution_found = True
            else:
                print("Node", i, "did not find a solution for n =", data[i][1])

    # distribute solution_found variable
    if rank == 0:
        solution_found = [solution_found for _ in range(size)]
        batch += 1
    solution_found = MPI.COMM_WORLD.scatter(solution_found, root=0)
