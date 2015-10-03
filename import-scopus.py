#script for processing the scopus xls files and recording notes

import pandas as pd
import os
import re

os.chdir("/home/matt/Documents/Classes/DSI Capstone/Data/Scopus/")
filenames = sorted(os.listdir())

allData = pd.DataFrame()
notesRead = {}
notesSkipped = {}

for file in filenames:
    if (".xslx" in file) | (".xls" in file):
        data = pd.read_excel(file)
        rawColumns = data.columns.values
    elif ".csv" in file:
        data = pd.read_csv(file)
        rawColumns = data.columns.values

    #inspect contents        
    print("\n" + file)
    print(str(data.shape[0]) + " rows, " + str(data.shape[1]) + " columns.")
    print(rawColumns)

    #pause before concatenating, skip concatenation if bad file
    keystroke = input('Type "s" to skip this file, ' + 
              '"n" to add a note, "q" to quit, ' +
              'any other key to record and continue:')
    
    if "s" not in keystroke:
        data.columns = data.columns.str.replace("[^A-Za-z0-9]","_").str.lower()
        allData = pd.concat([allData,data],join = "outer")
        notesRead[file] = ""
        if "n" in keystroke:
            note = input("Input notes about file for future reference:")
            notesRead[file] = note
    else: #File was skipped
        #Input notes about the skipped file
        note = input("Input notes about skipped file for future reference:")
        notesSkipped[file] = note
    if("q" in keystroke):
        break

#Get a filename for output
outputFile = input('Where should the output be written?')
while True:
    if re.match("[-a-zA-z0-9_]+\.[a-zA-z0-9]{1,4}$",outputFile):
        break
    outputFile = input("Invalid filename. Where should the output be written?")

#write to the file
allData.to_csv(path_or_buf = outputFile,index_label = False)

#Write notes about files read
with open("notes-read.txt","a") as f:
    f.write(str(len(notesRead)) + " files read into " + outputFile + ":\n") 
    f.write("filename,notes\n")
for file in notesRead.keys():
    with open("notes-read.txt","a") as f:
        f.write('"' + file + '","' + notesRead[file] + '"\n')

#Write notes about files skipped
with open("notes-skipped.txt","a") as f:
    f.write(str(len(notesRead)) + " files skipped:\n") 
    f.write("filename,notes\n")
for file in notesSkipped.keys():
    with open("notes-skipped.txt","a") as f:
        f.write('"' + file + '","' + notesSkipped[file] + '"\n')
