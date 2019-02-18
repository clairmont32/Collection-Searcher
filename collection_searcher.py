import os
import re
import threading


def rename_folders_files(toplevel, target):
    os.chdir(toplevel)
    for top, dir, files in os.walk(target):
        os.chdir(target)
        for folder in dir:
            newFolderName = folder.replace(' ', '_')
            os.rename(folder, newFolderName)
            for top, Dir, file in os.walk(folder):
                os.chdir(folder)
                for i in file:
                    newName = i.replace(' ', '_').lower()
                    os.rename(i, newName)
                os.chdir('..')


def compile_regex():
    keywordList = []
    with open('keywords.txt', 'r') as infile:
        for keyword in infile:
            keywordList.append(keyword.replace('\n', '|'))
    keywords = ''.join(keywordList)
    regex = re.compile(keywords, re.IGNORECASE)
    return regex


def search_files(regex):
    os.chdir('/storage/')
    os.chdir('collection1/collection__#1_usa_combos')

    credsFound = []
    for top, dir, files in os.walk('.'):

        for file in files:
            print('Searching {!s}'.format(file))
            with open(file,'rt') as dumpFile:
                for line in dumpFile:
                    results = re.search(regex, line)
                    if results:
                        foundString = file + ': ' + line
                        credsFound.append(foundString)

    return credsFound


regex = compile_regex()
found = search_files(regex)

with open('~/PycharmProjects/collection1/Found.txt', 'wt') as outfile:
    for cred in found:
        outfile.write(cred)
