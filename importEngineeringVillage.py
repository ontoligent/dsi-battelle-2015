# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 12:14:48 2015

@author: juan
"""
import pandas as pd
import os

# get the files
path = '/home/juan/workspace/Battelle/EngineeringVillage'

files = os.listdir(path)

dat = pd.DataFrame()
for file in files:
    print("Processing " + str(file))
    frame = pd.read_excel(os.path.join(path,file), encoding = 'utf-8')
    frame.columns = frame.columns.str.lower()
    frame.columns = frame.columns.str.replace("[^A-Za-z0-9]","_")
    dat = dat.append(frame, ignore_index = True)
dat.to_csv('EngineeringVillage.csv',encoding = 'utf-8')
