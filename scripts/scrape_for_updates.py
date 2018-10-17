# Web Scraper -- Check for updated bills & scrape them
# Republic of Ireland Oireachtas -- BILLS

############################################################

# import necessary packages for web scraping

import time
import datetime
import urllib.request, json
from urllib.request import urlopen
import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver # needed since site uses js to load content
from pyvirtualdisplay import Display

import pandas as pd
import pymongo

import pickle

# start time

start_time = time.time()

# set up MongoDB

from pymongo import MongoClient

# scrape PDFS

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO, BytesIO

def pdf_url_to_txt(url):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    f = urlopen(url).read()
    fp = BytesIO(f)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    
    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

# run

def run():
    
    client = MongoClient('mongodb://kate:5n43jkqg@localhost:27017/bill_db_ireland?authSource=bill_db_ireland')
    db = client['bill_db_ireland']
    bill_collection = db['bill_collection']
    updated_bill_collection = db['updated_bill_collection']

    now = (datetime.datetime.now() - datetime.timedelta(days=10)).strftime("%Y-%m-%d")

    url_head = "https://www.oireachtas.ie/en/bills/"
    update_links_list = []

    with urllib.request.urlopen("https://api.oireachtas.ie/v1/legislation?bill_status=Current&bill_source=Government,Private%20Member&date_start=" + now + "&date_end=2099-01-01&limit=50&chamber_id=&lang=en") as url:
        data = json.loads(url.read().decode())

        if data["head"]["counts"]["billCount"] > 0:
            for i in range(0,len(data["results"])):
                updated_bill_title = data["results"][i]["bill"]["shortTitleEn"]
                for j in range(11,15):
                    if data["results"][i]["bill"]["uri"][-j:][0] == 'b':
                        updated_bill_url = url_head + str(data["results"][i]["bill"]["uri"][-j:])
                        break
                update_links_list.append(updated_bill_url)
                i += 1

    if len(update_links_list) > 0:
            previous_updates = pd.DataFrame(list(updated_bill_collection.find()))
            for row in previous_updates.itertuples():
                for link in update_links_list:
                    if row[11] == link:
                        update_links_list.remove(link)

    if len(update_links_list) > 0:
        db.drop_collection(updated_bill_collection)
        # load chromedriver to navigate bill pages
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome('./chromedriver',chrome_options=options)
        
        for url in update_links_list:
            driver.get(url)
            innerHTML = driver.execute_script("return document.body.innerHTML")
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            abstract = soup.find('a', attrs={"class":"share-trigger"}) # find description and bill title here
            bill_source = soup.find_all(class_="c-bill-intro__meta") # find bill sponsor, source & originating house here
            title = soup.find('h1').text.strip() # bill title
            description = soup.find('p', class_ = "c-bill-intro__long-title") # bill description
            date = soup.find('p', class_ = "c-bill-intro__date") # bill date updated
            if description is None:
                description = 'No description available.'
            else:
                description = description.text.strip()
            if date is None:
                date = ''
            else:
                date = date.text.strip()
            if len(bill_source) < 3:
                sponsor = 'Unavailable' # bill sponsor
                #source = '' #bill source
                origin = 'Unavailable' # originating house
            else:
                sponsor = bill_source[0].get_text().strip() #bill sponsor
                #source = bill_source[1].get_text().strip() # bill source
                origin = bill_source[2].get_text().strip() # originating house
            try:
                stage_div = soup.find('div',class_ = "-current") # div enclosing bill stage
                stage = stage_div.find('h3',class_ = "c-bill-tracker-tooltip__heading").text.strip()
                bill_history = stage
                stage_info = stage_div.find('p',class_ = "c-bill-tracker-tooltip__content").text.strip()
            except:
                stage = 'Unavailable'
                bill_history = stage
                stage_info = 'Unavailable'
            try:
                bill_pdf_div = soup.find('div',class_ = "c-bill-versions-list__button") # div enclosing bill pdf
                bill_pdf = bill_pdf_div.find('a').get('href')
            except:
                bill_pdf = ''
            bill_info = {'title':title, 'description':description, 'date':date, 'bill_history':bill_history, 'sponsor':sponsor, 'origin':origin, 'stage':stage, 'stage_info':stage_info, 'bill_pdf':bill_pdf, 'url':url } # or [description[21:]]
            db.updated_bill_collection.insert_one(bill_info)

        driver.quit()

        updated_bill_collection = db.updated_bill_collection
        updated_tagged_bills = db.updated_tagged_bills

        bill_df = pd.DataFrame(list(updated_bill_collection.find()))
        db.drop_collection(updated_tagged_bills)

        #Dictionary of Categories

        pickle_in = open("/home/tags_dict.pickle","rb")
        cat_dict = pickle.load(pickle_in)


        tags_list = []
        i = 0

        for row in bill_df.itertuples():
            text0 = row[10].lower()
            text1 = row[5].lower()
            text_list = text0 + '-' + text1
            if 'bill entitled an act' in text_list:
                text_list = text_list.replace('bill entitled an act','').lstrip()
            i += 1
            tags_list.append([str(i)] + [text0])
            for key in cat_dict:
                for val in cat_dict[key]:
                    if val.lower() in text_list:
                        if key not in tags_list[i-1]:
                            tags_list[i-1].append(key)
            tags_dict = {'bill' : tags_list[i-1][0], 'title' : tags_list[i-1][1]}
            k = 1
            tags_dict['tags'] = {}
            for item in tags_list[i-1][2:]:
                tags_dict['tags']['tag ' + str(k)] = item
                k +=1
            db.updated_tagged_bills.insert_one(tags_dict)

        updated_tagged_bills = db.updated_tagged_bills
        final_updated_bills = db.final_updated_bills
        db.drop_collection(final_updated_bills)

        tagged_bill_df = pd.DataFrame(list(updated_tagged_bills.find()))

        if tagged_bill_df.empty == False:
            
            bill_df['title_lower'] = bill_df['title'].str.lower()
            
            result = pd.merge(bill_df,
                              tagged_bill_df[['title','tags']].drop_duplicates(subset=['title']),
                              left_on='title_lower',right_on='title',how='inner')
                
            result = result.drop(columns=['title_y'])
            result = result.rename(columns={'title_x' : 'title'})
            
            db.final_updated_bills.insert_many(result.to_dict('records'))

        bill_collection = db['final_updated_bills']

        bill_df = pd.DataFrame(list(bill_collection.find()))

        # run pdf

        links_list = []

        for row in bill_df.itertuples():
            links_list.append(row[3])

        bill_pdf_dict = {}

        for url in links_list:
            if url == '':
                pass
            else:
                try:
                    text = pdf_url_to_txt(url)
                    bill_pdf_dict[url] = text
                except:
                    pass

        bill_pdf_df = pd.DataFrame(list(bill_pdf_dict.items()), columns=['bill_pdf', 'text'])

        acts_dict = {}
        failed_start = []

        for row in bill_pdf_df.itertuples():
            text = row[2]
            acts = text.find("ACTS REFERRED TO")
            act = text.find("ACT REFERRED TO")
            if acts != -1:
                start = acts
                end = text.find('\n\n',text.find('\n\n',start)+1)
                acts_text = text[start:end]
                acts_list = []
                i = 0
                while i < len(acts_text):
                    next_i = acts_text.find('\n', i)
                    if next_i == -1:
                        acts_list.append(acts_text[i:len(acts_text)])
                        break
                    else:
                        acts_list.append(acts_text[i:next_i])
                        i = next_i + 1
                for item in acts_list:
                    if item == '':
                        acts_list.remove(item)
                    elif item == 'ACTS REFERRED TO':
                        acts_list.remove(item)
                    elif item == '\n':
                        acts_list.remove(item)
                acts_dict[row[1]] = acts_list
            elif act != -1:
                start = act
                end = text.find('\n\n',text.find('\n\n',start)+1)
                acts_text = text[start:end]
                acts_list = []
                i = 0
                while i < len(acts_text):
                    next_i = acts_text.find('\n', i)
                    if next_i == -1:
                        acts_list.append(acts_text[i:len(acts_text)])
                        break
                    else:
                        acts_list.append(acts_text[i:next_i])
                        i = next_i + 1
                for item in acts_list:
                    if item == '':
                        acts_list.remove(item)
                    elif item == 'ACT REFERRED TO':
                        acts_list.remove(item)
                    elif item == '\n':
                        acts_list.remove(item)
                acts_dict[row[1]] = acts_list
            else:
                failed_start.append(row[1])

        acts_df = pd.DataFrame(list(acts_dict.items()), columns=['bill_pdf', 'acts_list'])
        merge_acts_list = pd.merge(bill_pdf_df,acts_df,on='bill_pdf',how="left")

        final_updated_bills = db.final_updated_bills
        tagged_updated_bill_df = pd.DataFrame(list(final_updated_bills.find()))
        tagged_updated_bill_df = tagged_updated_bill_df.drop_duplicates(subset=['title'],keep='last')
        merge_all = pd.merge(tagged_updated_bill_df,merge_acts_list,on='bill_pdf',how="left")

        db.final_tagged_updated_bills.drop()
        db.final_tagged_updated_bills.insert_many(merge_all.to_dict('records'))
        db.updated_bills_complete.drop()

        updated_bills_w_acts = pd.DataFrame(list(db.final_tagged_updated_bills.find()))

        if tagged_updated_bill_df.empty == False:
            
            result = pd.merge(tagged_updated_bill_df,
                              updated_bills_w_acts[['title_lower','acts_list','text']],
                              left_on='title_lower',right_on='title_lower',how='inner')
        
            db.updated_bills_complete.insert_many(result.to_dict('records'))

