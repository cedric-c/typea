#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ntpath
import re

from typea.candidates import Candidates
from typea.utils import STOPWORDS


def extract_contents(articles: Candidates, to_remove: list) -> list:
    """

    @param articles:
    @param to_remove: list of tuples where
    @return:
    """
    data = []
    for title, content in articles.contents.items():
        for c in content:
            v = c
            for i, j in to_remove:
                v = re.sub(i, j, v)
            v = v.lower()
            data += v.split(' ')
    return data


def build_index(data: list, sort=False):
    index = {}
    for word in data:
        if word not in index:
            index[word] = 1
        else:
            index[word] += 1
    if sort:
        return sorted(index.items(), key=lambda x: x[1], reverse=True)
    else:
        return index


def main():
    articles = Candidates()
    # print(json.dumps(articles.contents, indent=4))

    # 2. build index
    # 1. filter words
    to_remove = [
        ("\n-\n", ''),
        ("\n\n", ' '),
        ("\n", ' '),
        (",", ' '),
        (r"\.|=", ''),
        (r'^[a-zA-Z]', ''),
        (r'^[\W]', '')
    ]
    data = extract_contents(articles, to_remove)
    index = build_index(data, sort=True)

    MINIMUM_OCCURENCE_COUNT = 5
    MINIMUM_WORD_LENGTH = 2

    # remove words that only occur once
    index = [(k, v) for (k, v) in index if v >= MINIMUM_OCCURENCE_COUNT]

    # remove stopwords
    index = [(k, v) for (k, v) in index if k not in STOPWORDS]

    # remove items of length <= 2
    index = [(k, v) for (k, v) in index if len(k) >= MINIMUM_WORD_LENGTH]

    print(index)
    print("Attempting to rename", len(articles.pdfs), "files")
    exit(1)

    skipped = 0
    renamed = 0

    for file in articles.pdfs:
        authors, title, date = articles.name(file)
        original_name = ntpath.basename(file)

        if date is not None:
            date = date[2:6]

        date = date if date is not None else ''

        if authors == title is None or title is None or authors == title == '' or title == '':
            print("Skipping file (missing attributes):", file)
            skipped += 1
            articles.clone(filepath=file, new_name=original_name, add_ext=False)
            continue

        if authors is None or authors == '':
            print("Warning: No author(s) in meta")
            renamed += 1
            articles.clone(filepath=file, new_name=title)
            continue

        if len(authors.split(" ")) == 1:
            print("Broken authors")
            skipped += 1
            articles.clone(filepath=file, new_name=original_name, add_ext=False)
            continue

        firstAuthor = authors.split(" ")[1]

        articles.clone(filepath=file, new_name=date + " - " + firstAuthor + " - " + title)
        renamed += 1

    print("Renamed", renamed, "files, skipped", skipped)


def insert_after_prefix(prefix: str, to_insert: str, content: str) -> str:
    """
    Inserts a value after a certain prefix
    @param prefix:
    @param to_insert:
    @param content:
    """
    matches = content.split(prefix, maxsplit=1)
    print(matches)


def string_manipulation_tutorial():
    myo1 = "My_document_with_myocarditis.txt"
    cmyo = "COVID_My_document_with_myocarditis.txt"
    doc2 = "COVID_COVID_My_myo_document_with_myocarditis.txt"

    patterns = [myo1, cmyo, doc2]
    for p in patterns:
        insert_after_prefix('COVID', 'myo', p)


if __name__ == "__main__":
    main()
    # string_manipulation_tutorial()
