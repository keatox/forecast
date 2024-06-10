from flask import Flask, render_template, request
from datascraping import Datascraping
from predict import Predict

scraper = Datascraping()
model = Predict()
app = Flask(__name__,template_folder='../frontend/templates',static_folder='../frontend/static')

stock=''
data = {}
pred = {}
new_data = False

@app.route('/',methods=['GET','POST'])
def main():
    global stock
    global new_data
    if request.method == 'POST':
        query = request.form
        if query.get('landingsearch'):
            stock = query.get('landingsearch').upper()
            if scraper.is_valid_stock(stock):
                new_data = True
                return dashboard()
            else:
                return render_template('landing.html',error="unknown stock ticker")
        elif query.get('dashsearch'):
            temp = query.get('dashsearch').upper()
            if scraper.is_valid_stock(temp):
                stock = temp
                new_data = True
                return dashboard()
            else:
                return render_template('dashboard.html',
                                       error="unknown stock ticker",
                                       ticker=stock,
                                       score=data['score'],
                                       positive=data['positive'],
                                       negative=data['negative'])
    else:
        return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    global data
    global pred
    global new_data
    if new_data:
        data = scraper.scrape(stock)
        pred = model.predict_prices(stock)
        new_data = False
    return render_template('dashboard.html',
                           ticker=stock,
                           score=data['score'],
                           positive=data['positive'],
                           negative=data['negative'],
                           chart=pred['chart'])

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    app.run(debug=True)