import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buy')
def displayBuyerTab():
    return render_template('buyerTab.html')

if __name__ == '__main__':
    app.run(debug=True)