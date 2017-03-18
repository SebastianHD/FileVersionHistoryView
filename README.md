# FileVersionHistoryView

Visualize relationship of file version to see progression and forks. This can also help determine latest version of file if names were scrambled (such as when doing a disk recovery by dumping files found via grep)

Requirements:
This module makes use of the following modules: scipy, Levenshtein, glob, os, matplotlib, itertools

Usage:
>>>import main from main

>>>main(dirName,fileSearchName)

dirName is a string that contains the path to a particular folder on the directory. 

fileSearchName is a string that contains a substring to search for in all of the files in the dirName path (excludes backup files denoted with ~)

example:
main('/home/sebastian/Documents/','test')
looks for all files that contain the substring 'test' in the path '/home/sebastian/Documents/' and process them.

Project is current under GNU General Public License v3.0.
