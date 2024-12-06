import os

import pandas as pd
from nucdens import access
import numpy as np
from pyperclip import copy


def main():
    # print all columns of the table with densities
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)

    # connect to database, choose working directory for downloading densities
    workdir = os.environ["HOME"]+"/"
    densdf = access.database(workdir=workdir)
    # select a specific set of densities, here the one and two body densities
    # for 3He with angle 59.98 deg
    # as of now there is only one density fulfilling this requirements
    print("Proceeding with workdir="+workdir)
    inputStr = "\nInput which nucleus\n1. 3H\n2. 3He\n3. 4He\n4. 6Li\n"
    num = int(input(inputStr))
    if num == 1:
        Z = 1
        N = 2
        name = "3H"
    elif num == 2:  # 3He
        Z = 2
        N = 1
        name = "3He"
    elif num == 3:  # 4He
        Z = 2
        N = 2
        name = "4He"
    elif num == 4:  # 6Li
        Z = 3
        N = 3
        name = "6Li"
    else:
        raise ValueError("Wrong number entered")
    # match int(num):
    #     case 1:  # 3H
    #         Z = 1
    #         N = 2
    #         name = "3H"
    #     case 2:  # 3He
    #         Z = 2
    #         N = 1
    #         name = "3He"
    #     case 3:  # 4He
    #         Z = 2
    #         N = 2
    #         name = "4He"
    #     case 4:  # 6Li
    #         Z = 3
    #         N = 3
    #         name = "6Li"
    #     case _:
    #         raise ValueError("Wrong number entered")

    numBodies = int(
        input("\nEnter 1 or 2\n1. Onebody density\n2. Twobody density\n"))
    if numBodies == 1:
        kind = "one"
        subfolder = "1Ndensities"
    elif numBodies == 2:
        kind = "two"
        subfolder = "2Ndensities"
    else:
        raise ValueError("Wrong number entered")
    # match numBodies:
    #     case 1:
    #         kind = "one"
    #         subfolder = "1Ndensities"
    #     case 2:
    #         kind = "two"
    #         subfolder = "2Ndensities"
    #     case _:
    #         raise ValueError("Wrong number entered")

    # angle = "ls"
    # while angle == "ls":
    #     orls = " or ls to print available densities: "
    #     angle = input("Enter desired angle in degrees"+orls)
        # if angle == "ls":
    s = ((densdf.pddf.Z == Z) & (
        densdf.pddf.kind == kind) & (
        densdf.pddf.N == N))

    printframe = densdf.pddf[s][["Z", "N", "theta"]
                                ].sort_values("theta")
    thetaValues = np.unique(printframe["theta"].to_numpy())
    print("Possible Angles Are")
    print("------------------------")
    for i in range(len(thetaValues)):
        print(i+1, ". ", thetaValues[i])
    i = int(input("Input integer for the angle desired: "))-1
    angle = thetaValues[i]
    print("Selected theta=", angle, "\n")
    #  print(printframe.to_string(index=False, header=True))

    # omega = "ls"
    # while omega == "ls":
    #     orls = " or ls to print available densities: "
    #     omega = input("Enter desired energy in MeV"+orls)
    #     if omega == "ls":
    s = ((
        densdf.pddf.Z == Z) & (
        densdf.pddf.kind == kind) & (
        densdf.pddf.theta == angle) & (
        densdf.pddf.N == N)
    )

    printframe = densdf.pddf[s][["Z", "N", "omega"]
                                ].sort_values("omega")

    omegaValues = np.unique(printframe["omega"].to_numpy())
    print("Possible Energy Values Are")
    print("------------------------")
    for i in range(len(omegaValues)):
        print(i+1, ". ", omegaValues[i], "MeV")
    i = int(input("Input integer for the energy desired: "))-1
    omega = omegaValues[i]
    print("Selected omega=", angle, "MeV")

    selection = ((
        densdf.pddf.Z == Z) & (
        densdf.pddf.N == N) & (
        densdf.pddf.theta == angle) & (
        densdf.pddf.kind == kind) & (
        densdf.pddf.omega == omega)
    )

    print(densdf.pddf[selection][["Z", "N", "theta", "omega", "hashname"]])

    if len(densdf.pddf[selection]) == 1:
        label = densdf.pddf[selection].to_dict("records")[0]
    elif len(densdf.pddf[selection]) == 0:
        os.remove("densities_table.h5")
        raise ValueError("No density of this type")
    else:
        selectList = ["kind", "Z", "N", "omega", "theta",
                      "uniquefilename", "addtime",
                      "moditime", "LambdaNN", "tnforder"]
        print(densdf.pddf[selection][selectList])

        print("\nMore than one entry selected. Printed all columns")
        row = int(input("Enter row (number in left) of file to use: "))
        #  TODO: check the row actually appears in selection
        label = densdf.pddf.to_dict("records")[row]

    # densName = name + "-"+str(angle)+"=theta-"+str(omega)\
    #     + "=MeV-"+kind+"body.gz"
    densName = name + "-"+str(angle)+"=theta-"+str(omega)\
        + "=MeV-"+kind+"body.h5"
    path = "densities-"+name+r"/"+subfolder+r"/"
    if not os.path.exists(path):
        print("Directory named\n"+path+"\nDoes not exist, creating one now")
        os.makedirs(path)

    fullPath = path+densName
    if os.path.isfile(fullPath):
        yesno = input("File already exists, okay to overwrite? y/n: ").lower()
        if yesno == "n":
            os.remove("densities_table.h5")
            return 0
    # full print uniquefilename
    hashname, uniquename = densdf.get_file(**label)
    assert(os.path.isfile(hashname))
    fileLocation = workdir+fullPath
    os.replace(hashname, fileLocation)
    print("Downloaded file to: " + fileLocation)
    os.remove(workdir+"densities_table.h5")
    copy("'"+fileLocation+"'")
    print("Copied file location to clipboard")


if __name__ == "__main__":
    main()
