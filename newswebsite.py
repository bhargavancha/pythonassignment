import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
import sys
import re

# reading url as ennvironment variable
url_value = sys.argv[1]

# reading page and importing through beautiful soup
response = requests.get(url_value)
doc = BeautifulSoup(response.text, 'html.parser')

# getting all the tags with h3
headlines = doc.find_all('h3')
stories_list = []

#getting headline,url and summary
stories = doc.find_all('div', { 'class': 'gs-c-promo' })
for story in stories:
    headline = story.find('h3')
    link = story.find('a')
    summary = story.find('p')
    # Does our story have a summary?
    if summary:
        # Build a dict that has a summary
        story_dict = {
            'headline': headline.text,
            'url': link['href'],
            'summary': summary.text
        }
    else:
        # Build a dict that does not have a summary
        story_dict = {
            'headline': headline.text,
            'url': link['href'],
        }    
    # Add the dict to our list
    stories_list.append(story_dict)

#print(stories_list)

#creating dataframe using pandas 

df = pd.DataFrame(stories_list)

# Connecting to MongoDB
client =  MongoClient("mongodb://bhargavmongo:bhargavmongodb@ac-1hywkig-shard-00-00.i63ycxq.mongodb.net:27017,ac-1hywkig-shard-00-01.i63ycxq.mongodb.net:27017,ac-1hywkig-shard-00-02.i63ycxq.mongodb.net:27017/?ssl=true&replicaSet=atlas-trgwvk-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client['bhargavmongo']
collection = db['artifactdata']
collection.insert_many(df.to_dict("records"))

#reading Data from Mongodb 

#enter keyword to search article details
keyword = sys.argv[2]
search_string = re.compile(keyword)

#getting article details

for x in collection.find({"headline": search_string}):
 
  print(x)
      
        
    


