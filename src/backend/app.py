from flask import Flask, render_template, request
from datascraping import Datascraping
from predict import Predict

scraper = Datascraping()
model = Predict()
app = Flask(__name__,template_folder='../frontend/templates',static_folder='../frontend/static')

@app.route('/',methods=['GET','POST'])
def main():
    if request.method == 'POST':
        query = request.form
        # checks which search bar is being used
        if query.get('landingsearch'):
            stock = query.get('landingsearch').upper()
            if scraper.is_valid_stock(stock):
                return dashboard(True)
            else:
                return landing(True)
        else:
            stock = query.get('dashsearch').upper()
            boolean = scraper.is_valid_stock(stock)
            return dashboard(boolean, not boolean)
    # default landing
    else:
        return landing()
    
@app.route('/landing')
def landing(error=False):
    return render_template('landing.html',error=error)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
def dashboard(new_data=False,error=False):
    # generates new dash if new stock is inputted
    if new_data:
        scraper.scrape(scraper.stock)
        model.predict_prices(scraper.stock)
    return render_template('dashboard.html',
                           error=error,
                           ticker=scraper.stock,
                           data=scraper.data,
                           pred=model.info)
    
@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0')
    app.run(debug=True)