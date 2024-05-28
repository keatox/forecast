import praw
import os         
from dotenv import load_dotenv, find_dotenv
from preprocess import Preprocess
from sentimodel import Sentimodel

class Datascraping:
    def __init__(self):
        # you will need to create your own .env file and Reddit API app
        load_dotenv(find_dotenv())
        KEY = os.getenv("REDDIT_API_KEY")
        SECRET = os.getenv("REDDIT_API_SECRET")

        self.__model = Sentimodel()
        self.__process = Preprocess()
        self.__reddit = praw.Reddit(client_id=KEY,
                            client_secret=SECRET,
                            user_agent='Sentiment analysis')

    def scrape(self,stock):
        terms = []                                                                   # change limit to determine number of posts to scrape
        for post in self.__reddit.subreddit('wallstreetbets').search(stock,sort="relevance",limit=100):
            terms.append([post.selftext])
        terms = [term for term in terms if term[0] != "" and len(term[0].split()) >= 15]  # removes empty terms to mitigate false negatives

        # processing and prediction
        tokens = [self.__process.preprocess(term)[0] for term in terms]
        counts = self.__model.vectorize(tokens)
        predictions = self.__model.prediction(counts)

        # prints each term and respective prediction
        [print(terms[i][0],[predictions[i].upper()]) for i in range(len(predictions))]
        
        # prints sentiment score out of 10
        sum = 0
        for i in range(len(predictions)):
            if predictions[i] == 'positive':
                sum += 1
        print("%.2f" % (10 * sum/len(predictions)))

    # hardcoded stock for now
scraper = Datascraping()
stock = 'DOGE'
scraper.scrape(stock)