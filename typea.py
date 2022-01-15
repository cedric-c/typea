#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-

import os, shutil, ntpath
from typea.candidates import Candidates
from copy import copy

articles = Candidates()
print("Attempting to rename", len(articles.pdfs), "files")

skipped = 0
renamed = 0
# print(articles.infos)
# quit()
for file in articles.pdfs:
    authors, title, date = articles.name(file)
    original_name = ntpath.basename(file)

    if (date != None):
        date = date[2:6]

    date = date if date != None else ''

    if (authors == title == None or title == None or authors == title == '' or title == ''):
        print("Skipping file (missing attributes):", file)
        skipped += 1
        articles.clone(filepath=file, new_name=original_name, add_ext=False)
        continue

    if (authors == None or authors == ''):
        print("Warning: No author(s) in meta")
        renamed += 1
        articles.clone(filepath=file, new_name=title)
        continue

    if (len(authors.split(" ")) == 1):
        print("Broken authors")
        skipped += 1
        articles.clone(filepath=file, new_name=original_name, add_ext=False)
        continue

    firstAuthor = authors.split(" ")[1]

    articles.clone(filepath=file, new_name=date + " - " + firstAuthor + " - " + title)
    renamed += 1

print("Renamed", renamed, "files, skipped", skipped)
