import praw
import string
from nltk.corpus import stopwords
import nltk
from preprocess import Preprocess
from collections import Counter

KEY = "m3cPpLyaVlE0JxcZBkIFaA"
SECRET = "Fvk4PgPavpfb8TR4wnKMMz5nF5a8HA"

process = Preprocess()
counter = Counter()
reddit = praw.Reddit(client_id=KEY,
                     client_secret=SECRET,
                     user_agent='Sentiment analysis by u/P0PT4RT0')

stock = 'AAPL'

for post in reddit.subreddit('wallstreetbets').search(stock,sort="relevance",limit=2):
    counter.update(process.preprocess(post.title))
    counter.update(process.preprocess(post.selftext))
    for i in range(1,5):
        counter.update(process.preprocess(post.comments[i].body))

print(counter.most_common(5))