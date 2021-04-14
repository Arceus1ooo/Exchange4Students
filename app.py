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

@app.route('/sell', methods= ['GET', 'POST'])
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
    return render_template('itemList.html', lst = lst, typ = typ, keyword = keyword)

@app.route('/itemList/<string:_id>', methods = ['GET', 'POST'])
def displayItem(_id):
    item = db_func.pullID(_id)
    return render_template('itemView.html', item = item)

@app.route('/sell/post', methods = ['GET', 'POST'])
def postItem():
    if request.method == 'POST':
        typ = request.form['type']
    return render_template('postItem.html', typ = typ)

@app.route('/sell/post/confirmation', methods = ['GET', 'POST'])
def confirm():
    if request.method == 'POST':
        prodTyp = request.form['prodTyp']
        name = request.form['name']
        desc = request.form['desc']
        price = request.form['price']
        
        prod = classes.product(name, price, desc, prodTyp)
        
        if prodTyp == 'Book':
            setattr(prod, 'title', request.form['title'])
            setattr(prod, 'ed', request.form['ed'])
            setattr(prod, 'course', request.form['course'])
        elif prodTyp == 'Clothing':
            setattr(prod, 'typ', request.form['type'])
            setattr(prod, 'color', request.form['color'])
            setattr(prod, 'sz', request.form['sz'])
        elif prodTyp == 'Sports Gear':
            setattr(prod, 'kind', request.form['kind'])
            setattr(prod, 'weight', request.form['weight'])
        elif prodTyp == 'Electronic':
            setattr(prod, 'typ', request.form['type'])
            setattr(prod, 'mod', request.form['model'])
            setattr(prod, 'l', request.form['l'])
            setattr(prod, 'w', request.form['w'])
            setattr(prod, 'h', request.form['h'])
            setattr(prod, 'weight', request.form['weight'])
        elif prodTyp == 'Furniture':
            setattr(prod, 'typ', request.form['type'])
            setattr(prod, 'color', request.form['color'])
            setattr(prod, 'l', request.form['l'])
            setattr(prod, 'w', request.form['w'])
            setattr(prod, 'h', request.form['h'])
            setattr(prod, 'weight', request.form['weight'])
        
        res = db_func.post(prod)
        str_res = str(res)
            
    return render_template('confirmation.html', str_res = str_res)


if __name__ == '__main__':
    app.run(debug=True)