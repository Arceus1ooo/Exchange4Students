import os
from flask import Flask, render_template, request
import db_func
import classes

app = Flask(__name__)



@app.route('/')
def displayIndex():
    return render_template('index.html')

@app.route('/buy', methods = ['GET', 'POST'])
def displayBuyerTab():
    return render_template('buyerTab.html')

@app.route('/sell')
def displaySellerTab():
    return render_template('sellerTab.html')

@app.route('/itemlist', methods = ['GET', 'POST'])
def displayListings():
    typ = ''
    keyword = ''
    if request.method == 'POST':
        typ = request.form['type']
        keyword = request.form['choice']
    res = db_func.pull(typ, keyword)
    lst = []
    for x in res:
        lst.append(x)
    return render_template('itemList.html', lst = lst)

@app.route('/itemList/<string:name>', methods = ['GET', 'POST'])
def displayItem(name):
    return 'works'



if __name__ == '__main__':
    app.run(debug=True)