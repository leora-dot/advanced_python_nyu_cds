import numpy as np
import random

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = MPI.COMM_WORLD.Get_rank()

def slice_data(arr, num_partitions):

    val_min = min(arr)
    val_max = max(arr)

    pivot_vals = list(np.linspace(val_min, val_max , num=num_partitions))
    pivot_vals.insert(0, val_min - 1)
    pivot_vals.append(val_max + 1)

    arr_splits = []
    for i in range(num_partitions):
        arr_split = [x for x in arr if pivot_vals[i]<x<= pivot_vals[i+1] ]
        arr_splits.append(arr_split)

    return arr_splits

def bubble_sort(arr):
    n = len(arr)

    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

    return arr

##GENERATE ARRAY IN ROOT
if rank == 0:
    num_partitions = comm.Get_size()
    #arr = [3, 5, 7, 4, 6, 7, 11, 9, 2, 8, 3, 2]
    arr = [random.randint(1, 500) for i in range(num_elements)]
    arr_sliced = slice_data(arr, num_partitions)
else:
    arr_sliced = None

#SCATTER ARRAY TO ALL PROCESSES & SORT
arr = comm.scatter(arr_sliced, root=0)
arr_sort = bubble_sort(arr)
sorted = comm.gather(arr_sort, root=0)

#PRINT SORTED ARRAY
if rank == 0:
    flattened = [val for sublist in sorted for val in sublist]
    print(flattened)

#RUN COMMAND: mpiexec -n 4 python parallel_sorter.py
