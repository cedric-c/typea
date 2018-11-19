#!/usr/local/bin/python3.7
# /**
 # * @author Cédric Clément <cclem054@uottawa.ca>
 # * @version 1.0
 # * (c) Copyright 2018 Cédric Clément.
 # */

import os, sys, xattr, subprocess, shutil
import tempfile, xml.etree.ElementTree as ElementTree
from importlib import util
from os.path import isfile, join
from os import listdir
from copy import copy
xattr_spec = util.find_spec('xattr')
found_xattr = xattr_spec is not None

LISTABLE = ['array', 'dict', 'plist']
SCALAR = ['date','string','integer','false','true','real','data']

KEY_TITLE = 'kMDItemTitle'
KEY_AUTHOR = 'kMDItemAuthors'
KEY_JOURNAL = 'kMDItemDescription'
KEY_FILENAME = 'kMDItemDisplayName'
KEY_PUBLISHER = 'kMDItemCreator'

OUTPUT_DIR = 'out'

# No parameter means files in current directory
RENAME_IN_CURRENT  = 0

# 1 parameter means files in a specific directory, create an output folder
COPY_FROM    = 1

# 2 parameters means files in directory param[1] are renamed(copied) into directory at param[2]
COPY_FROM_TO = 2

# grab current directory
currentDirectory = os.getcwd()
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
            name = join(path, file)
            _, extension = os.path.splitext(name)
            if extension == ".pdf":
                filenames.append(name)
    return filenames

#
from collections import defaultdict



def c1():
    print("case 1")
    files = get_target_files()
    print(files)
    tempFiles = []
    for filename in files:
        temporaryFile = tempfile.TemporaryFile();
        tempFiles.append(temporaryFile)
        print("\n")
        print(filename)

        name = str(temporaryFile.name)+".xml"
        proc = subprocess.check_output(['mdls','-plist', name, filename]).decode()

    newNames = []
    for file in tempFiles:
        name = str(file.name) + ".xml"
        tree = ElementTree.parse(name)

        nodes = list(tree.getroot()[0])
        vals = {}
        for (index, child) in enumerate(nodes[:-1]):
            currentNode, nextNode = child, nodes[index + 1]

            if (currentNode.tag == 'key'):
                # 
                if(nextNode.tag in LISTABLE):
                    # print(list(nextNode))
                    v = []
                    for n in list(nextNode):
                        v.append(n.text)
                    # print(list(nextNode.text))
                    vals[currentNode.text] = v
                else:
                    vals[currentNode.text] = nextNode.text
                    
        
        # print(vals)
        auth_ = vals.get(KEY_AUTHOR)
        title = vals.get(KEY_TITLE)
        pub = vals.get(KEY_PUBLISHER)
        journal = vals.get(KEY_JOURNAL)
        
        outputPath = join(currentDirectory, OUTPUT_DIR)
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
        
        if type(auth_) is list:
            auth = auth_[0]
        else:
            auth = 'NA'
            
        
        newName = join(OUTPUT_DIR,pub+'_'+title+'_'+auth+'.pdf')
        newNames.append(newName)
        
    
    for (index, file) in enumerate(files):
        try:
            shutil.copy(file, newNames[index])
        except:
            print(newNames[index]+" alreadt exists... skipping\n")
        
    # Close and remove files
    for t in tempFiles:
        t.close()
        f = str(t.name)+".xml"
        os.remove(f)

def c2(directoryFrom):
    print("NOT IMPLEMENTED")
    # print("case 2: "+directoryFrom)
    # files = get_target_files(directoryFrom)
    # print(files)

def c3(directoryFrom, directoryTo):
    print("NOT IMPLEMENTED")
    # print("case 3: "+directoryFrom+" - "+directoryTo)
    # files = get_target_files(directoryFrom)
    # print(files)
    

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

    