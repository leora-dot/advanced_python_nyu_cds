import numpy
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

randNum = numpy.zeros(1)

if rank == 1:
        randNum = numpy.random.random_sample(1)
        print("Process", rank, "drew the number", randNum[0])
        req = comm.Isend(randNum, dest=0) #COMMENT OUT TO DEMONSTRATE IMMEDIATE RETURN
        req.Wait() #COMMENT OUT TO DEMONSTRATE IMMEDIATE RETURN

if rank == 0:
        print("Process", rank, "before receiving has the number", randNum[0])
        req = comm.Irecv(randNum, source=1)
        req.Wait() #COMMENT OUT TO DEMONSTRATE IMMEDIATE RETURN
        print("Process", rank, "received the number", randNum[0])

#RUN COMMAND: mpiexec -n 2 python mpi5.py
