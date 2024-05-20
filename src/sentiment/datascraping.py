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
        terms.append([post.title])
        terms.append([post.selftext])
        for i in range(1,5):
            terms.append([post.comments[i].body])
    tokens = [process.preprocess(term)[0] for term in terms]

    #remove vectorized terms with 0 counts all around?
    tokens = model.vectorize(tokens)
    predictions = model.prediction(tokens)

    [print(terms[i][0],[predictions[i].upper()]) for i in range(len(predictions))]

    sum = 0
    for pred in predictions:
        if pred == 'positive':
            sum += 1
    print(sum/len(predictions))

stock = 'AAPL'
scrape(stock)