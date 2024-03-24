import praw
from preprocess import Preprocess

KEY = "m3cPpLyaVlE0JxcZBkIFaA"
SECRET = "Fvk4PgPavpfb8TR4wnKMMz5nF5a8HA"

reddit = praw.Reddit(client_id=KEY,
                     client_secret=SECRET,
                     user_agent='Sentiment analysis by u/P0PT4RT0')

stock = 'AAPL'

process = Preprocess()

for post in reddit.subreddit('wallstreetbets').search(stock,sort="relevance",limit=2):
    print(process.preprocess(post.title),process.preprocess(post.selftext))
    for i in range(4):
        print(process.preprocess(post.comments[i].body))

