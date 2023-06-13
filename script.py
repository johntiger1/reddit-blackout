import requests
from bs4 import BeautifulSoup
import datetime
import re
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
from tqdm import tqdm

# Input date as YYYY-MM-DD
date_str = '2022-01-01'
date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')

# Calculate UNIX timestamp for the given date
start_timestamp = int(date_obj.timestamp())
end_timestamp = int((date_obj + datetime.timedelta(days=1)).timestamp())

# Hacker News API URL
api_url = 'https://hacker-news.firebaseio.com/v0'

# Fetch the top 500 stories
top_stories = requests.get(f'{api_url}/topstories.json').json()

# Initialize some variables
posts_per_hour = [0] * 24
keywords = []
upvotes = []

# Loop through the top stories with a progress bar
for story_id in tqdm(top_stories, desc='Processing stories'):
    story = requests.get(f'{api_url}/item/{story_id}.json').json()
    story_time = story['time']

    # Check if story is within the given date range
    if start_timestamp <= story_time < end_timestamp:
        # Count posts per hour
        hour = datetime.datetime.fromtimestamp(story_time).hour
        posts_per_hour[hour] += 1

        # Extract keywords from the title
        title = story['title']
        words = re.findall(r'\w+', title)
        keywords.extend(words)

        # Count upvotes
        upvotes.append(story['score'])

# Plot the number of posts per hour
plt.bar(range(24), posts_per_hour)
plt.xlabel('Hour')
plt.ylabel('Number of Posts')
plt.title('Posts per Hour on Hacker News')
plt.show()

# Plot the keyword frequency as a WordCloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(keywords))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# Plot the distribution of upvotes
plt.hist(upvotes, bins=20)
plt.xlabel('Upvotes')
plt.ylabel('Number of Posts')
plt.title('Upvotes Distribution on Hacker News')
plt.show()