"""
a script for getting materials from Old Bailey Online
"""
# Imports
from itertools import count
from operator import concat
import string
from unicodedata import name
import xml.etree.ElementTree as ET  # for parsing XML
from io import StringIO
import pandas as pd 
import requests 

#Trail IDs
trialIDs = [
#1780's
"t17820220-62", 
"t17820220-83", 
"t17820220-84", 
#1790's
"t17900113-66",
"t17900224-47",
"t17900224-68",
"t17900707-24",
#1800's 
"t18000115-78",
"t18000219-81",
"t18000219-83",
"t18000402-17",
#1810's
"t18110918-17",
"t18111030-48",
"t18121202-39",
"t18121202-84",
"t18130714-89",
#1820's
"t18210718-88",
"t18220911-203",
"t18230219-136",
"t18231022-130",
"t18231022-131",
#1830's
"t18330214-129",
"t18390408-1361",
"t18390916-2433",
#1840's
"t18400302-870",
"t18400406-1272",
"t18410510-1403",
"t18420704-2141",
"t18421128-220",
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

# #Crime Date
#     for crimeDateText in root.iter('rs'):
#         if crimeDateText.get('type') == 'crimeDate':
#             crimeDate_list.append(crimeDateText.text)
 
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

# Export to CSV file 
df.to_csv('corporalConvicts.csv')




