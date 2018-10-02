#scripts/update_bills.py

from datetime import date
import pickle

import pandas as pd
import pymongo
from pymongo import MongoClient

import csv
from bill.models import Bill, Category, Origin, Sponsor, Stage

def run():
    #check old bills
    today = date.today()

    for item in Bill.objects.filter(updated = True):
        if today - item.updated_at > 6:
            item.updated = False
    
    client = MongoClient('localhost', 27017)
    db = client.bill_db_ireland
    final_updated_bills = db.final_updated_bills
    
    #open all updated tagged bills from mongodb as dataframe
    bill_df = pd.DataFrame(list(final_updated_bills.find()))
    
    if bill_df.empty == False:
        for row in bill_df.itertuples():
            if Bill.objects.all().filter(title = row[9]).count() == 1:
                bill = Bill.objects.get(title = row[9])
                bill.save()
                bill.updated = True
                bill.save()
                bill.updated_at = today
                bill.save()
                updated_stage = Stage(stage = row[6],stage_info = row[7])
                updated_stage.save()
                bill.stage.add(updated_stage)
                bill.save()
            elif Bill.objects.all().filter(title = row[9]).count() == 0:
                o = Origin(origin = row[4][19:]) #set origin
                o.save()
                st = Stage(stage = row[6],stage_info = row[7]) # forgot to actually collect stage..
                st.save()
                sponsor_list = row[5][14:].split(';')
                a = Bill(title = row[9],description = row[3],origin = o,stage = st) #add all elements to Bill
                a.save()
                for name in sponsor_list:
                    name = name.strip()
                    if Sponsor.objects.all().filter(sponsor=name).count() == 1:
                        sp_existing = Sponsor.objects.get(sponsor=name)
                        sp_existing.save()
                        a.sponsor.add(sp_existing)
                        a.save()
                    else:
                        sp = Sponsor(sponsor = name)
                        sp.save()
                        a.sponsor.add(sp) #add all sponsors to Bill
                        a.save()
                for i in row[8]:
                    c = Category(category = row[8][i])
                    if Category.objects.all().filter(category=c).count() == 1:
                        c_existing = Category.objects.get(category=row[8][i])
                        c_existing.save()
                        a.category.add(c_existing)
                        a.save()
                    else:
                        c.save()
                        a.category.add(c) #add all categories to Bill
                        a.save()


