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

def flatten_list(list_of_lists):
    return [val for sublist in list_of_lists for val in sublist]

num_elements = 10000

#Root generates an array & created partitions based on values
if rank == 0:
    num_partitions = comm.Get_size()
    #arr = [3, 5, 7, 4, 6, 7, 11, 9, 2, 8, 3, 2]
    arr = [random.randint(1, 500) for i in range(num_elements)]
    print("Array Generated. Generating {} partitions...".format(num_partitions))
    arr_sliced = slice_data(arr, num_partitions)
    print("Partions generated. Sorting...")

else:
    arr_sliced = None

#Partitioned array is scattered & all processes perform bubble sort
arr = comm.scatter(arr_sliced, root=0)
arr_sort = bubble_sort(arr)

#Process output is gathered to create a list of sorted arrays
sorted = comm.gather(arr_sort, root=0)

#Root flattens list & sorts array
if rank == 0:
    print("Array Sorted.")
    sorted = flatten_list(sorted)
    print(sorted)

#RUN COMMAND: mpiexec -n 4 python parallel_sorter.py
