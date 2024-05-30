from flask import Flask, render_template, request
# from datascraping import Datascraping
# from predict import Predict

# #add error handling for unknown stock
# stock = 'AAPL'
# scraper = Datascraping()
# model = Predict()

# scraper.scrape(stock)

app = Flask(__name__,template_folder='../frontend/templates',static_folder='../frontend/static')

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    app.run(debug=True)