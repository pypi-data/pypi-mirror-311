import sys
import os 
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

from nucdens import access

# open database using the mirror on datapub  
densdb=access.database(workdir=os.environ["HOME"]+"/work/densdb/",webbase="https://datapub.fz-juelich.de/anogga/files/densindx/")

# print all entries of the database (this looks best in a Jupyter notebook)
print(densdb.pddf.to_markdown()) 

# print all entries but restrict tto limited number of columns

colsel=["kind","Z","N","MODENN","orderNN","LambdaNN","tnforder","c1","c3","c4","cd","ce","cE1","cE3","lambdaSRGNN","srgwf","relcalc","omega","theta","qmom","uniquefilename"]

print(densdb.pddf[colsel].sort_values(by=["kind","Z","N","MODENN","LambdaNN","cE1","cE3","cd","lambdaSRGNN","omega","theta"]).to_markdown())

# then get a specific wave function 
# it is essential that the kind is specified (either two or one) 
# rest of labels can be omitted. The results needs to be unique though. 
# the file is downloaded 
denslabels={"kind":"two","MODENN":"chsms", "Z":2, "N":2 , "orderNN":"n4lo+","LambdaNN":450.0,"tnforder":"n2lo","ce":-0.38595,"omega":80,"theta":45}
hashname,uniquefilename=densdb.get_file(**denslabels)
print("hashname",hashname)
print("uniquefilename",uniquefilename)

# then finally, do the opposite: get infos for a specific hashname
# there is only one entry possible 
# directly transfer to a dictionary
properties_dict=densdb.pddf[densdb.pddf.hashname=="dd9d0a1bcd01525bfbb99e3957d8af13efe5c73c442ebeb397b51377951c15fa"][colsel].to_dict('records')
# this is all info 
print(properties_dict[0])
# but one could also look at specific entries
print("omega,theta: ", properties_dict[0]["omega"],properties_dict[0]["theta"])
print("uniquefilename", properties_dict[0]["uniquefilename"])
