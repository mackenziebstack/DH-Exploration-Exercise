# Part Four Log 

Tools: 
1. Python
2. ElementTree for parsing XML data 
3. Panadas libaray 
4. RStudio 
    * library(tidyverse)
    * library(tidytext)
5. R for data cleanup
6. Topicmodels for data visulization


Tutorials used:
1. Cleaning and manipulating data: https://craftingdh.netlify.app/tutorials/clean-data-r/
2. Excel and R: https://craftingdh.netlify.app/tutorials/excel/
3. APIS: https://craftingdh.netlify.app/tutorials/apis/
4. Topic Models: https://craftingdh.netlify.app/tutorials/topic-models/

## Log for Part Four

Date: June 17th 2022

Name: Mackenzie Stack


### Determine What Data

* Navigated to old bailey website and used search function to find trial ID's for women convicts in the 1780s and 1850s that resulted in transportation and corporal punishments

* Trial ID's for Corporal punishment :

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

Trial ID's for 

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

### Get Data 
* import relevant tools:
    * itertools import count
    * operator import concat
    * xml.etree.ElementTree as ET
    * io import StringIO
    * pandas as pd 
    * requests 

* Defined trials ID's in dict 
* Created empty list to hold request URLS 
* Looped through trial ids, concatonated with baseURL 
    * appened to list 
* Printed URLs for safety
### Manipulate Data 

* Created empty lists to store, database varaibles 
    * allTrialText = []
    * crimeDate_list = []
    * defendantName_list = []
* Looped through URLS and retrieved content
* Added Nested loops in URL loop to parse XML data 
    * For Loop; 
        * Get all trial data
        * Get crime date 
        * Get Defendent name
            * issue with reading more then one name on file
                * added break point after first instance 
* Created trial dictionary for database outline
    * {"crimeDate":crimeDate_list ,"trialText":allTrialText ,"defendantName":defendantName_list}

## Create a dataframe 

* Created dataframe: df = pd.DataFrame.from_dict(trialDict, orient='index')
* Issue with whitespace destorting data, employed solution from https://stackoverflow.com/questions/33788913/pythonic-efficient-way-to-strip-whitespace-from-every-pandas-data-frame-cell-tha
    * made comment to cite the solution in code
* transposed dataframe

## Export to csv file 

* exported df to CSV file
    * df.to_csv('trasportedConvicts.csv')

* Repeated all steps for second data set. 
# Topic Models 

* Imported libraries:
    * library(tidyverse)
    * library(tidytext)
    * library("dplyr")
    * library(tm)
    * library(topicmodels)
    * Library("reshape2")
    * library("ggplot2")
    * library("pals")

* added csv files to the project and the read them using:
    * cc  <- read_csv('corporalConvicts.csv')
* Attempted to manipulate df with cc_df <- cc_df %>% mutate(id = row_number()), to add an ID 
    * ended up changing the idex to id, and manually added a column 
* Added cc_df <- tibble(id = cc$id, text = (str_remove_all(cc$trialText, "[0-9]")), date = cc$crimeDate)
* Added stop word code. 
    * tidy_cc <- cc_df %>% unnest_tokens(word, text)
    * data(stop_words)
    *tidy_cc <- tidy_cc %>% anti_join(stop_words)
* tidied data
* added topic models, and added it to the import libraries 
* added parameters for visulization 
* issues with warnings, resaved files as UT8 for excel and no further problem.
* Bam, visulizations! 




    




