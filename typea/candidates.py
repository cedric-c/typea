#!/usr/local/bin/python3.7
# /**
 # * @author Cédric Clément <cclem054@uottawa.ca>
 # * @version 1.0
 # * (c) Copyright 2018 Cédric Clément.
 # */

import os
from os import listdir
from os.path import isfile, join
import PyPDF2

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
    
    def meta(self, directory = os.getcwd()):
        """(Candidates, str) -> dictionary of str"""
        path = os.path.expanduser(directory)
        meta = {}
        for filename in self.list(directory):
            pdf_object = open(filename, 'rb')
            reader = PyPDF2.PdfFileReader(pdf_object)
            meta[filename] = reader.documentInfo
            # meta.append(reader.documentInfo)
        return meta


if __name__ == "__main__":
    c = Candidates()
    # print(os.getcwd())
    test = c.list(os.getcwd())
    
    meta = c.meta()
    print(meta)