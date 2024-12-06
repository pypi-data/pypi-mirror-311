#!/usr/bin/env python
#SBATCH --nodes=2
#SBATCH --ntasks=128
#SBATCH --ntasks-per-node=64
#SBATCH --cpus-per-task=2
#SBATCH --output=test.out
#SBATCH --error=test.out
#SBATCH --time=00:10:00
#SBATCH --partition=dc-gpu-devel
#SBATCH --gres=gpu:4
#SBATCH --job-name=pyt
#SBATCH --mail-user=a.nogga@fz-juelich.de
#SBATCH --account=ias-4
#SBATCH --mail-type=ALL
#SBATCH --export=ALL

import subprocess   # to call shell 
import os

homedir=os.environ['HOME']

outfile=open(homedir+"/netbeans-jureca/nucdensity/tests/test.out", 'a')

# check enviroment

subprocess.call(["bash", "-c", "ml"],
      stdin=None, 
      stdout=outfile, 
      stderr=outfile)

os.environ['CUDA_VISIBLE_DEVICES']="0,1,2,3"

subprocess.call(["srun","--account","jikp03","python",homedir+"/netbeans-jureca/nucdensity/tests/python-script-parallel.py"],
      stdin=None, 
      stdout=outfile, 
      stderr=outfile)

outfile.close()

                
