import praw
import os         
from dotenv import load_dotenv, find_dotenv
from preprocess import Preprocess
from sentimodel import Sentimodel

# you will need to create your own .env file and Reddit API app
load_dotenv(find_dotenv())
KEY = os.getenv("REDDIT_API_KEY")
SECRET = os.getenv("REDDIT_API_SECRET")

model = Sentimodel()
process = Preprocess()
reddit = praw.Reddit(client_id=KEY,
                     client_secret=SECRET,
                     user_agent='Sentiment analysis')

def scrape(stock):
    terms = []
    for post in reddit.subreddit('wallstreetbets').search(stock,sort="relevance",limit=5):
        terms.append(process.preprocess(post.title))
        terms.append(process.preprocess(post.selftext))
        for i in range(1,5):
            terms.append(process.preprocess(post.comments[i].body))

    terms = process.remove_stopwords(terms,stock)

    terms = model.vectorize(terms)
    print(terms.shape)

stock = 'AAPL'
scrape(stock)