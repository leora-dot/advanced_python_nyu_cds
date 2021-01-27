from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = MPI.COMM_WORLD.Get_rank()

##ASSIGNMENT
    #Process 0 reads a value from the user and verifies that it is an integer less than 100.
    #Process 0 sends the value to process 1 which multiplies it by its rank.
    #Process 1 sends the new value to process 2 which multiplies it by its rank.
    #This continues for each process, such that process i sends the value to process i+1 which multiplies it by i+1.
    #The last process sends the value back to process 0, which prints the result.

rank_current = MPI.COMM_WORLD.Get_rank()
rank_previous = rank_current - 1
rank_subsequent = rank_current + 1

size = comm.Get_size()
rank_max = size - 1

def get_integer():
    user_input_str = input ("Enter an integer less than 100 \n")
    try:
        user_input_int = int(user_input_str)
    except ValueError:
        get_integer()
    if user_input_int > 100:
        get_integer()
    return user_input_int

if rank == 0:

    #STARTING PROCESS
    val= get_integer()
    print("Process 0 recieved user input = {}".format(val))
    comm.send(val, dest= rank_subsequent)

    ##PRINTING LAST VALUE
    val = comm.recv(source= rank_max)
    print("Process {} recieved input = {}".format(rank, val))

else:
    val = comm.recv(source= rank_previous)
    #print("Process {} recieved input = {}".format(rank, val))
    val = val * rank

    if rank < rank_max:
        comm.send(val, dest= rank_subsequent)
    else:
        comm.send(val, dest = 0)
