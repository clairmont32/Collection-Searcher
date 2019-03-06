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
    credsFound = []
    for top, directory, files in os.walk('.'):
        for dir in directory:
            os.chdir(dir)
            print('Searching in {!s}'.format(dir))
            for top, dirtop, files in os.walk('.'):
                files.sort()
                for file in files:
                    if file.endswith('txt'):
                        print('Searching {!s}'.format(file))
                        with open(file, 'r') as dumpFile:
                            try:
                                for line in dumpFile:
                                    results = re.search(regex, line)
                            except:
                                pass

                            if results:
                                foundString = file + ': ' + line
                                credsFound.append(foundString)
                os.chdir('../')
    return credsFound


if __name__ == '__main__':
    home = '/usr/home/matt/PycharmProjects/Collection-Searcher'
    regex = compile_regex()
    collectionDir = '/storage/collection1'
    os.chdir(collectionDir)
    found = search_files(regex)

    with open(home + '/found.txt', 'wt') as outfile:
        for cred in found:
            outfile.write(cred)
