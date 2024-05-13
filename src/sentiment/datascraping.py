import praw
import string
import os         
from dotenv import load_dotenv, find_dotenv
from collections import Counter
from preprocess import Preprocess

load_dotenv(find_dotenv())
KEY = os.getenv("REDDIT_API_KEY")
SECRET = os.getenv("REDDIT_API_SECRET")

#array? https://oxylabs.io/blog/how-to-make-web-scraping-faster  multiprocessing


process = Preprocess()
counter = Counter()
reddit = praw.Reddit(client_id=KEY,
                     client_secret=SECRET,
                     user_agent='Sentiment analysis by u/P0PT4RT0')

stock = 'AAPL'

terms = []
for post in reddit.subreddit('wallstreetbets').search(stock,sort="relevance",limit=5):
    terms.extend(word for word in process.preprocess(post.title))
    terms.extend(word for word in process.preprocess(post.selftext))
    for i in range(1,5):
        terms.extend(word for word in process.preprocess(post.comments[i].body))

stopword = list(string.punctuation) + [stock.lower(),'“','”']
with open("res/english.txt", "r") as my_file:
    for line in my_file:
        stopword.append(line.strip())

terms = [term for term in terms if term.lower() not in stopword]
counter.update(terms)
print(counter.most_common(50))