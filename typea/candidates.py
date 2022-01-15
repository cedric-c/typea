#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-

import os
import shutil
from os import listdir
from os.path import isfile, join

import PyPDF2

TARGET_EXTENSION = ".pdf"
OUTPUT_DIRECTORY = "renamed_articles"

ARTICLE_CREATOR = '/Creator'
ARTICLE_PRODUCER = '/Producer'
ARTICLE_AUTHOR = '/Author'
ARTICLE_TITLE = '/Title'
ARTICLE_SUBJECT = '/Subject'
ARTICLE_DATE = '/CreationDate'
IEEE_ARTICLE_ID = '/IEEE#20Issue#20ID'  # IEEE


# ARTICLE_PUBLICATION_ID = '/IEEE#20Publication#20ID' # IEEE

class Candidates:
    """This is a potential candidate for renaming"""

    def __init__(self, directory=os.getcwd()):
        """(Candidates, str) -> NoneType"""
        self.directory = directory
        self.pdfs = self.list(self.directory)
        self.infos = self.meta(self.directory)

    def list(self, directory=None):
        """(Candidates, str) -> dictionary of str
        Lists the files in the provided directory which have a pdf extension.        
        """

        if (directory == None):
            directory = self.directory

        filenames = []
        path = os.path.expanduser(directory)
        for file in listdir(path):
            qualified_name = join(path, file)
            if isfile(qualified_name):
                name = join(path, file)
                _, extension = os.path.splitext(name)
                if extension == TARGET_EXTENSION:
                    # if(self.readable(name)):
                    filenames.append(name)

        return filenames

    def meta(self, directory=None):
        """(Candidates) -> dictionary of str
        Returns the files and their metadata as a dictionary indexed on the filenames of the files.
        """

        if (directory == None):
            directory = self.directory

        meta = {}
        for filename in self.pdfs:
            if (self.readable(filename)):
                pdf_object = open(filename, 'rb')
                reader = PyPDF2.PdfFileReader(pdf_object)
                meta[filename] = reader.getDocumentInfo()

        return meta

    def readable(self, filename):
        """(Candidates) -> str
        Returns True if PyPDF can read the PDF and/or parse the attributes.
        """
        try:
            pdf_object = open(filename, 'rb')
            reader = PyPDF2.PdfFileReader(pdf_object)
            return True
        except:
            return False

    def clone(self, filepath, new_name=None, destination_dir=None, add_ext=True):
        """(Candidates) -> name of target file str, name of target destination_dir dir, str.
        Copies the file at the fully qualified filepath to destination_dir.
        If no destination_dir is provided, copies to OUTPUT_DIRECTORY.
        
        Creates the folder starting from the path first specified when creating the object.
        """

        if (destination_dir == None):
            destination_dir = OUTPUT_DIRECTORY

        if (not os.path.exists(destination_dir)):
            os.makedirs(destination_dir)

        new_dir = join(self.directory, destination_dir)
        new_path = new_name + TARGET_EXTENSION if add_ext else new_name
        shutil.copy(filepath, join(new_dir, new_path))

    def name(self, filepath):
        """(Candidates) -> name of target file str
        Returns the name of a file by searching through the metadata.
        """
        author = self.__getAuthor(filepath)
        title = self.__getTitle(filepath)
        date = self.__get(ARTICLE_DATE, filepath)
        return author, title, date

    def __getAuthor(self, filepath):
        """This is a WIP.
        """
        try:
            data = self.infos[filepath]
            return data[ARTICLE_AUTHOR]
        except:
            return None

    def __getTitle(self, filepath):
        """This is a WIP
        """
        try:
            data = self.infos[filepath]
            # print(data,"hello")
            return data[ARTICLE_TITLE]
        except:
            return None

    def __get(self, key, filepath):
        """This is a WIP.
        """
        try:
            data = self.infos[filepath]
            return data[key]
        except:
            return None


if __name__ == "__main__":
    c = Candidates()
    # print(os.getcwd())
    # test = c.list(os.getcwd())
    # meta = c.meta()
    # print(len(meta))
