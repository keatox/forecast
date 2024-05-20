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
    for post in reddit.subreddit('wallstreetbets').search(stock,sort="relevance",limit=100):
        terms.append([post.selftext])
    terms = [term for term in terms if term[0] != "" and len(term[0].split()) >= 15]  # removes empty terms to mitigate false negatives

    tokens = [process.preprocess(term)[0] for term in terms]
    counts = model.vectorize(tokens)
    predictions = model.prediction(counts)

    [print(terms[i][0],[predictions[i].upper()]) for i in range(len(predictions))]
    sum = 0
    for i in range(len(predictions)):
        if predictions[i] == 'positive':
            sum += 1
    print(sum/len(predictions))

stock = 'DOGE'
scrape(stock)