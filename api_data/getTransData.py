"""
a script for getting materials from Old Bailey Online
"""
# Imports
from itertools import count
from operator import concat
import string
import xml.etree.ElementTree as ET  # for parsing XML
from io import StringIO
import pandas as pd 
import requests 

#Trail IDs
trialIDs = [
#1790's
"t17811017-41",
"t17820220-47",
"t17820703-44",
"t17820911-38",
"t17820911-51",
#1800's 
"t17900915-4",
"t17900915-30",
"t17900915-33",
"t17900915-34",
"t17900915-51",
#1810's
"t18000917-17",
"t18000917-74",
"t18000917-99",
"t18000917-105",
#1820's
"t18190113-6",
"t18190113-94",
"t18190113-122",
"t18190113-126",
"t18190113-127",
#1830's
"t18300218-11",
"t18300218-30",
"t18300218-49",
"t18300218-54",
"t18300218-98",
#1840's
"t18400106-437",
"t18400106-455",
"t18400106-495",
"t18400106-507",
"t18400106-535"
] 

# List to store URLs for each trial
request_urls = []

# Loop through 
for trials in trialIDs:

    # Request URL
    request_url = "https://www.oldbaileyonline.org/obapi/text?div=" + trials

    # Append to list
    request_urls.append(request_url)

# view the request URLs
print(request_urls)

# Lists for trial text, Crime date & Name
allTrialText = []
crimeDate_list = []
defendantName_list = []

# Loop through URLS
for request_url in request_urls:
    r = requests.get(request_url)
    root = ET.fromstring(r.content)

#get all trial text 
    for p in root.iter('div1'):
        # Get all inner text 
        alltext = " ".join(t for t in p.itertext())
        #append to list
        allTrialText.append(alltext)

#Crime Date
    # for crimeDateText in root.iter('rs'):
    #     if crimeDateText.get('type') == 'crimeDate':
    #         crimeDate_list.append(crimeDateText.text)

 #Crime Date
    for crimeYearText in root.iter(tag = 'interp'):
        if crimeYearText.get('type') == 'year':
            year = crimeYearText.attrib.get("value")
            crimeDate_list.append(year)

#Defendant Name
    for convictName in root.iter('persName'):
        if convictName.get('type') == 'defendantName':
            defendantName_list.append(convictName.text)
            #I only want the first defendantName that appears, hence the break
            break
        

# Eliminates whitespace from database
def remove_whitespace(x):
    try:
        # remove spaces inside and outside of string
        x = " ".join(x.split())
    except:
        pass
    return x

#White space solution from 
#https://stackoverflow.com/questions/33788913/pythonic-efficient-way-to-strip-whitespace-from-every-pandas-data-frame-cell-tha


trialDict = {"crimeDate":crimeDate_list ,"trialText":allTrialText ,"defendantName":defendantName_list}

#Create database from dictionary 
df = pd.DataFrame.from_dict(trialDict, orient='index')

#Remove whitespace
df = df.applymap(remove_whitespace)

#Transpose
df = df.transpose()
df\

#Export to CSV file 
df.to_csv('trasportedConvicts.csv')




