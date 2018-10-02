# -*- coding: utf-8 -*-

#scripts/add_tds.py

import csv
from bill.models import Deputy, Senator, Constituency, Party, Panel

def run():
    #open all deputy & senator information from csv
    with open('/home/TD_data.csv','r',encoding='latin-1') as inp:
        reader = csv.reader(inp)
        con_list = []
        party_list = []
        for j,row in enumerate(reader):
            if (j == 0):
                pass
            else:
                td = Deputy(name = row[0], email = row[5], phone = row[6], photo = row[7], url = row[8]) #set td model fields
                td.save()
                con_list.append(row[2])
                party_list.append(row[3])
        con_list = list(set(con_list))
        party_list = list(set(party_list))
        for k,item in enumerate(con_list):
            con = Constituency(name = item, con_id = k)
            con.save()
        for l,item in enumerate(party_list):
            party = Party(name = item, party_id = 1)
            party.save()
    #open all deputy & senator information from csv
    with open('/home/senator_list.csv','r',encoding='latin-1') as inp:
        reader = csv.reader(inp)
        panel_list = []
        for k,row in enumerate(reader):
            if (k == 0):
                pass
            else:
                senator = Senator(name = row[0], email = row[5], phone = row[6]) #set senator model fields
                senator.save()
                panel_list.append(row[3])
        panel_list = list(set(panel_list))
        for m, item in enumerate(panel_list):
            pan = Panel(name = item, panel_id = m)
            pan.save()

