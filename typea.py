#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018, Cédric Clément
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# * The name of the author may not be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os, shutil, ntpath
from typea.candidates import Candidates
from copy import copy

articles = Candidates()
print("Attempting to rename",len(articles.pdfs), "files")

skipped = 0
renamed = 0

for file in articles.pdfs:
    authors, title = articles.name(file)
    original_name = ntpath.basename(file)
    
    if(authors == title == None or title == None or authors == title == '' or title == ''):
        print("Skipping file (missing attributes):", file)
        skipped += 1
        articles.clone(filepath=file, new_name=original_name, add_ext=False)
        continue
    
    if(authors == None or authors == '' ):
        renamed += 1
        articles.clone(filepath=file, new_name=title)
        continue
    
    firstAuthor = authors.split(" ")[1]
    
    articles.clone(filepath=file, new_name=firstAuthor + " - " + title)
    renamed += 1
    
print("Renamed",renamed,"files, skipped",skipped)