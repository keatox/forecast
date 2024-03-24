import praw
import string
from collections import Counter
from preprocess import Preprocess

KEY = "m3cPpLyaVlE0JxcZBkIFaA"
SECRET = "Fvk4PgPavpfb8TR4wnKMMz5nF5a8HA"

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
with open("sentiment/english.txt", "r") as my_file:
    for line in my_file:
        stopword.append(line.strip())

terms = [term for term in terms if term.lower() not in stopword]
counter.update(terms)
print(counter.most_common(50))