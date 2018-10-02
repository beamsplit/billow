# -*- coding: utf-8 -*-

# scripts/map_models.py

import pandas as pd
import pymongo
from pymongo import MongoClient

import csv
from bill.models import Bill, Category, AssociatedAct, Origin, Sponsor, Stage, Deputy, Senator, Constituency, Party, Panel

def run():
    #open all deputy information from csv
    with open('/home/TD_data.csv','r',encoding='latin-1') as inp:
        reader = csv.reader(inp)
        for j,row in enumerate(reader):
            if (j == 0):
                pass
            else:
                td = Deputy.objects.get(name=row[0]) #set td model fields
                con = Constituency.objects.get(name=row[2])
                party = Party.objects.get(name=row[3])
                con.deputy_set.add(td)
                con.save()
                party.deputy_set.add(td)
                party.save()
    #open all senator information from csv
    with open('/home/senator_list.csv','r',encoding='latin-1') as inp:
        reader = csv.reader(inp)
        for j,row in enumerate(reader):
            if (j == 0):
                pass
            else:
                sen = Senator.objects.get(name=row[0]) #set td model fields
                panel = Panel.objects.get(name=row[3])
                panel.senator_set.add(sen)
                panel.save()


    
