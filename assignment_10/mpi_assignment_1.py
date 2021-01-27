from mpi4py import MPI
rank = MPI.COMM_WORLD.Get_rank()

#PROCESS WITH EVEN RANKS PRINT HELLO
if rank % 2 == 0:
    print("Hello from process {}".format(rank))

#PROCESS WITH EVEN RANKS PRINT GOODBYE
else:
    print("Goodbye from process {}".format(rank))


#RUN COMMAND: mpiexec -n 5 python mpi_assignment_1.py
