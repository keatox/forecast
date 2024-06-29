from flask import Flask, render_template, request, jsonify
from flask_compress import Compress
from datascraping import Datascraping
from database import Database
from predict import Predict

scraper = Datascraping()
model = Predict()
db = Database()
app = Flask(__name__,template_folder='../frontend/templates',static_folder='../frontend/static')
Compress(app)

@app.route('/',methods=['GET','POST'])
def main():
    if request.method == 'POST':
        query = request.form
        # checks which search bar is being used
        if query.get('landingsearch'):
            stock = query.get('landingsearch').upper().split()[-1].replace('(','').replace(')','')
            if db.is_valid_stock(stock):
                return dashboard(True)
            else:
                return landing(True)
        else:
            stock = query.get('dashsearch').upper().split()[-1].replace('(','').replace(')','')
            boolean = db.is_valid_stock(stock)
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
        scraper.scrape(db.stock)
        model.predict_prices(db.stock)
    return render_template('dashboard.html',
                           error=error,
                           ticker=db.stock,
                           data=scraper.data,
                           pred=model.info)
    
@app.route('/help')
def help():
    return render_template('help.html')

# gets query from frontend and returns top results
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '').strip()
    if query:
        try:
            cursor = db.conn.cursor()
            cursor.execute("""SELECT * FROM Stocks 
                            WHERE ticker ILIKE %s
                            OR name ILIKE %s
                            LIMIT 5;""",(query + '%',query + '%'))
            results = cursor.fetchall()
            cursor.close()
            return jsonify([result[1] + " ("+ result[0] +")" for result in results])
        except:
            print("Can't connect to server.")
    return jsonify([])

# opens a connection upon page load
@app.route('/create_conn',methods=['POST'])
def create_conn():
    db.conn = db.connect_db()
    return jsonify({"status": "success"}), 200

# closes connection upon exiting page
@app.route('/cleanup',methods=['POST'])
def cleanup():
    db.conn.close()
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    # app.run(debug=True)