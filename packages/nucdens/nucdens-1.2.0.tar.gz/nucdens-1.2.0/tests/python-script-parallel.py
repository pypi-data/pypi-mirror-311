#!/usr/bin/env python
from mpi4py import MPI
import torch
import os 

cudaflag=torch.cuda.is_available()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

try:
  cuda_devices=os.environ['CUDA_VISIBLE_DEVICES']
except:
  cuda_devices=""
  
nodename=os.environ['HOSTNAME']

print("rank {0:d} on node {1:s} sees devices: {2:s}".format(rank,nodename,cuda_devices))

print("rank {0:d} running from {1:d} processes!".format(rank,size))

if cudaflag:
  numgpu = torch.cuda.device_count()
  for id in range(numgpu):
    print("GPU on task {0:d} with id {1:d}: {2:s}".format(rank,id,torch.cuda.get_device_name(id)))
else:
  print("No cuda found on task {0:d}".format(rank))

MPI.Finalize()

        
      


      
