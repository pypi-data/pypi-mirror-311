# Python example script to prepare databases including a directory of
# precalculated densities

import os
from nucdens import access
import glob
import re 
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

input_dir="/p/scratch/cjikp03/jikp0340/He4_2Ndensity_N4LO_cut=550_N2LO3N_lambda=1.88"
work_dir=os.environ["SCRATCH"]+"/densdb/"
uploaddir=os.environ["SCRATCH"]+"/densupload"

comptondf=access.database(workdir=work_dir)

# cd/ce values for different cutoffs at N4LO+ 
# 400:   "cd":3.3278,  "ce":-0.45405
# 450:   "cd":0.8918,  "ce":-0.38595    
# 500:   "cd":-1.2788,  "ce":-0.38214  
# 550:   "cd":-3.6257,  "ce":-0.41022  

inter_label={"c1":-1.23, "c3":-4.65, "c4":3.28, "cd":-3.6257,  "ce":-0.41022, 
             "cE1":0.0, "cE2":0.0, "cE3":0.0, "cE4":0.0, "cE5":0.0, 
             "cE6":0.0, "cE7":0.0, "cE8":0.0, "cE9":0.0, "cE10":0.0,
             "lam3NF":550.0, "tnforder":"n2lo-combine",
             "benchnr":"none", "jobnr":"none", "jubedir":"none",
             "N":2,"Z":2,"MTtot":0,"Tmax":0,"Nmax":20,"OmegaHO":16.0,
             "nnsrg":True,"tnfsrg":True,"lambdaSRGNN":1.88,"lambdaSRG3N":1.88,
             "MODENN":"chsms", "orderNN":"n4lo+", "LambdaNN":550.0, "potnr":72,"empotnr":1,
             "relcalc":False, "j12max3nf":0, "j3max3nf":0, 
             "potbareNN":82, "potbareNNTNF":82, 
             "ostatSRGNN":5, "ostatSRGTNF":5,
             "cutnumSRGNN":4,"cutnumSRGTNF":4,"empotsrg":0,
             "srgwf":True,
             }


tolerance=1E-8 
printlevel=1


file_list=glob.glob(input_dir+"/compton*.h5")
print(file_list)

for file_name in file_list:
  print(file_name)
  if os.path.exists(file_name):

    dens2b=access.densfile2b(file_name) 
    file_label=dens2b.get_labels()
    compl_label={**file_label,**inter_label}
    del dens2b

    try:
           hashnamedens=comptondf.add_file(filename=file_name,**compl_label) 
           file_added=True
    except:
           hashnamedens=comptondf.add_file(filename=file_name,**compl_label) 
           file_added=False
    if file_added:  
           hashname_uncompressed=work_dir+hashnamedens+"_uncompressed"
           os.rename(work_dir+hashnamedens,hashname_uncompressed)
           dens2b=access.densfile2b(hashname_uncompressed)
           dens2b.compress(work_dir+hashnamedens,tolerance,printlevel=printlevel)

    
    
print(comptondf.pddf.to_latex())
# now create upload ready version 
comptondf.prep_upload(uploaddir)

