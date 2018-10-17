 #scripts/update_bills.py

import datetime
import pickle

import pandas as pd
import pymongo
from pymongo import MongoClient

import csv
from bill.models import Bill, Category, AssociatedAct, Origin, Sponsor, Stage

def run():
    #check old bills
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    date_format = "%Y-%m-%d"

    for item in Bill.objects.filter(updated = True):
        start_date = datetime.datetime.strptime(str(today), date_format)
        end_date = datetime.datetime.strptime(str(item.updated_at),date_format)
        delta = start_date - end_date
        if delta.days > 6:
            item.updated = False
    
    client = MongoClient('localhost', 27017)
    db = client.bill_db_ireland
    updated_bills_complete = db.updated_bills_complete
    
    #open all updated tagged bills from mongodb as dataframe
    bill_df = pd.DataFrame(list(updated_bills_complete.find()))
    
    if bill_df.empty == False:
        for row in bill_df.itertuples():
            if Bill.objects.all().filter(title = row[13]).count() == 1:
                bill = Bill.objects.get(title = row[13])
                bill.save()
                bill.updated = True
                bill.save()
                bill.updated_at = today
                bill.save()
                updated_stage = Stage(stage = row[9],stage_info = row[10])
                updated_stage.save()
                bill.stage = updated_stage
                bill.save()
            elif Bill.objects.all().filter(title = row[13]).count() == 0:
                o = Origin(origin = row[7][19:]) #set origin
                o.save()
                st = Stage(stage = row[9],stage_info = row[10]) # set stage
                st.save()
                sponsor_list = row[8][14:].split(';')
                try:
                    d = datetime.datetime.strptime(row[5][14:],'%d %b %Y').strftime('%Y-%m-%d')
                except:
                    d = datetime.datetime.now().strftime("%Y-%m-%d")
                a = Bill(title = row[13], description = row[6], origin = o, stage = st, bill_history = row[3], date = d, url = row[15]) #add all elements to Bill
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
                for i in row[11]:
                    c = Category(category = row[11][i])
                    if Category.objects.all().filter(category=c).count() == 1:
                        c_existing = Category.objects.get(category=c)
                        c_existing.save()
                        a.category.add(c_existing)
                        a.save()
                    else:
                        c.save()
                        a.category.add(c) #add all categories to Bill
                        a.save()
                for item in row[2]:
                    if item != '':
                        if item[-1] == ')':
                            item = item[:item[-10:].find('(')-10 +len(item)].strip()
                        act = AssociatedAct(associated_act = item)
                        if AssociatedAct.objects.all().filter(associated_act=act).count() == 1:
                            act_existing = AssociatedAct.objects.get(associated_act=item)
                            act_existing.save()
                            a.associated_act.add(act_existing)
                            a.save()
                        else:
                            act.save()
                            a.associated_act.add(act) #add all acts to Bill
                            a.save()


