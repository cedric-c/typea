# /**
 # * @author Cédric Clément <cclem054@uottawa.ca>
 # * @version 1.0
 # * (c) Copyright 2018 Cédric Clément.
 # */

import os, sys, xattr, subprocess, json
import tempfile, xml.etree.ElementTree as ElementTree
from importlib import util
from os.path import isfile, join
from os import listdir
from copy import copy
xattr_spec = util.find_spec('xattr')
found_xattr = xattr_spec is not None

TEMP_FILE_NAME = ".temp_quickrn"

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



def write_to_temp_file(content):
    descriptor, path = mkstemp()
    with open(path, 'w') as file:
        file.write(content)
    os.close(fd)
    return path

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

def parseXmlToJson(xml):
  response = {}

  for child in list(xml):
    if len(list(child)) > 0:
      response[child.tag] = parseXmlToJson(child)
    else:
      response[child.tag] = child.text or ''

    # one-liner equivalent
    # response[child.tag] = parseXmlToJson(child) if len(list(child)) > 0 else child.text or ''

  return response

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
        # print(proc)
        # print(temporaryFile.seek(0))
        # print(temporaryFile.read())

    for file in tempFiles:
        name = str(file.name) + ".xml"
        tree = ElementTree.parse(name)
        parsed = parseXmlToJson(tree.getroot().iter())
        print(parsed)
        # print(tree.getroot().getchildren())
        # for n in tree.iter():
            # print(dir(n))
        # print(dir(tree))
        # jsonTree = json.dumps(tree)
        # parsed = parseXmlToJson(tree)
        # print(parsed)
        print(tree.find("kMDItemCreator"))
        for child in list(tree.getroot()):
            children = list(child)
            # print(child.getchildren())
            # for c in children:
                # print(c.text)

    for file in tempFiles:
        with open(str(file.name)+".xml", 'r') as content:
            xml = content.read()
            # parsed = parseXmlToJson(xml)
            # v = dictify(xml)
            # print(v)


    
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

    