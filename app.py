import os
from flask import Flask, render_template

app = Flask(__name__)



@app.route('/')
def displayIndex():
    return render_template('index.html')

@app.route('/buy')
def displayBuyerTab():
    return render_template('buyerTab.html')

@app.route('/sell')
def displaySellerTab():
    return render_template('sellerTab.html')


if __name__ == '__main__':
    app.run(debug=True)