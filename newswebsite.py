import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient

response = requests.get('https://www.bbc.com/news')
doc = BeautifulSoup(response.text, 'html.parser')

headlines = doc.find_all('h3')
stories_list = []
stories = doc.find_all('div', { 'class': 'gs-c-promo' })
for story in stories:
    headline = story.find('h3')
    link = story.find('a')
    summary = story.find('p')
    # Does our story have a summary?
    if summary:
        # Build a dict that HAS a summary
        story_dict = {
            'headline': headline.text,
            'url': link['href'],
            'summary': summary.text
        }
    else:
        # Build a dict that does NOT have a summary
        story_dict = {
            'headline': headline.text,
            'url': link['href'],
        }    
    # Add the dict to our list
    stories_list.append(story_dict)

#print(stories_list)

df = pd.DataFrame(stories_list)

# Connect to MongoDB
client =  MongoClient("mongodb://bhargavmongo:bhargavmongodb@ac-1hywkig-shard-00-00.i63ycxq.mongodb.net:27017,ac-1hywkig-shard-00-01.i63ycxq.mongodb.net:27017,ac-1hywkig-shard-00-02.i63ycxq.mongodb.net:27017/?ssl=true&replicaSet=atlas-trgwvk-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client['bhargavmongo']
collection = db['artifactdata']
df.reset_index(inplace=True)
data_dict = df.to_dict("records")
collection.insert_one({"index":"Sensex","data":data_dict})


