import praw
import string
import os         
from dotenv import load_dotenv, find_dotenv
from collections import Counter
from preprocess import Preprocess

# you will need to create your own .env file and Reddit API app
load_dotenv(find_dotenv())
KEY = os.getenv("REDDIT_API_KEY")
SECRET = os.getenv("REDDIT_API_SECRET")

process = Preprocess()
reddit = praw.Reddit(client_id=KEY,
                     client_secret=SECRET,
                     user_agent='Sentiment analysis')

def scrape(stock):
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

    counter = Counter()
    terms = [term for term in terms if term.lower() not in stopword]
    counter.update(terms)
    return(counter.most_common(50))

stock = 'AAPL'
print(scrape(stock))