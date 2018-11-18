# /**
 # * @author Cédric Clément <cclem054@uottawa.ca>
 # * @version 1.0
 # * (c) Copyright 2018 Cédric Clément.
 # */

import os, sys
from os.path import isfile, join
from os import listdir



# No parameter means files in current directory
RENAME_IN_CURRENT  = 0

# 1 parameter means files in a specific directory, create an output folder
COPY_FROM    = 1

# 2 parameters means files in directory param[1] are renamed(copied) into directory at param[2]
COPY_FROM_TO = 2

# grab current directory
# currentDirectory = os.getcwd()
# print(currentDirectory) # /Users/ced/div/quickRename
# print(os.curdir) # .


def get_target_files(directory: str = os.getcwd()):
    ''' Returns a list of targets on which to perform renaming operations
    '''
    
    # We'll put the filenames in here
    filenames = []
    
    # Sometimes, special characters are used such as '~' which means
    #    the 'home directory'. We want to create fully qualified paths.
    #    That is, replace '~' with it's real representation of
    #    c:\Users\<YOUR NAME>\
    #    Note that '~' means home on Mac, but not necessarily on other platforms.
    path = os.path.expanduser(directory)

    # For each file in the list of files for the directory located at path
    for file in listdir(path):
        qualifiedFilename = join(path, file)
        if isfile(qualifiedFilename):
            
            # Add the fully qualified file to our list of files to return
            filenames.append(join(path, file))
    return filenames


def c1():
    print("case 1")
    files = get_target_files()
    print(files)

def c2(directoryFrom):
    print("case 2: "+directoryFrom)
    files = get_target_files(directoryFrom)
    print(files)

def c3(directoryFrom, directoryTo):
    print("case 3: "+directoryFrom+" - "+directoryTo)
    files = get_target_files(directoryFrom)
    print(files)
    

if __name__ == "__main__":
    parameterCount = len(sys.argv) - 1
    # print("paramcount: "+str(parameterCount))
    
    cases = {
        RENAME_IN_CURRENT: lambda: c1(),
        COPY_FROM: lambda: c2(sys.argv[1]),
        COPY_FROM_TO: lambda: c3(sys.argv[1], sys.argv[2])
    }
    
    func = cases.get(parameterCount)
    func()

    