#!/usr/local/bin/python3.7
# /**
 # * @author Cédric Clément <cclem054@uottawa.ca>
 # * @version 1.0
 # * (c) Copyright 2018 Cédric Clément.
 # */

import os
from os import listdir
from os.path import isfile, join

TARGET_EXTENSION = "pdf"

class Candidates:
    """This is a potential candidate for renaming"""
    
    def __init__(self, directory = os.getcwd()):
        """(Candidates, str) -> NoneType"""
        self.directory = directory
    
    def list(self, directory = os.getcwd()):
        """(Candidates, str) -> dictionary of str"""
        filenames = []
        path = os.path.expanduser(directory)
        for file in listdir(path):
            qualified_name = join(path, file)
            if isfile(qualified_name):
                name = join(path, file)
                _, extension = os.path.splitext(name)
                if extension == "." + TARGET_EXTENSION:
                    filenames.append(name)
        return filenames


if __name__ == "__main__":
    c = Candidates()
    # print(os.getcwd())
    test = c.list(os.getcwd())
    print(test)