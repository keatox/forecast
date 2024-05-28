from datascraping import Datascraping
from predict import Predict

#add error handling for unknown stock
stock = 'AAPL'
scraper = Datascraping()
model = Predict()

scraper.scrape(stock)




