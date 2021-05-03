import os
from flask import Flask, render_template, request
import db_func
import classes
from werkzeug.utils import secure_filename
import base64
from PIL import Image
import os, binascii

UPLOAD_FOLDER = os.getcwd()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

global currentUser # the username of the user currently logged in
currentUser = 'Tester'


@app.route('/')
def displayIndex():
    return render_template('index.html')

@app.route('/buy', methods = ['GET', 'POST'])
def displayBuyerTab():
    typ = 'Any'
    keyword = ''
    if request.method == 'POST':
        typ = request.form['type']
        keyword = request.form['choice']
    res = db_func.pull(typ, keyword)
    lst = []
    for x in res:
        lst.append(x)
    return render_template('buyerTab.html', lst = lst, typ = typ, keyword = keyword)

@app.route('/sell', methods= ['GET', 'POST'])
def displaySellerTab():
    return render_template('sellerTab.html')

'''@app.route('/itemlist', methods = ['GET', 'POST'])
def displayListings():
    typ = 'Any'
    keyword = ''
    if request.method == 'POST':
        typ = request.form['type']
        keyword = request.form['choice']
    res = db_func.pull(typ, keyword)
    lst = []
    for x in res:
        lst.append(x)
    return render_template('itemList.html', lst = lst, typ = typ, keyword = keyword)'''

@app.route('/buy/<string:_id>', methods = ['GET', 'POST'])
def displayItem(_id):
    global currentUser
    if request.method == 'POST':
        cartItem = request.form['objectID']
        db_func.addToCart(cartItem, currentUser)
        user = db_func.findUser(currentUser)
        return render_template('cart.html', cart=user['Cart'])
    item = db_func.pullID(_id)
    return render_template('itemView.html', item = item)

@app.route('/sell/post', methods = ['GET', 'POST'])
def postItem():
    err = False
    if request.method == 'POST':
        typ = request.form['type']
    return render_template('postItem.html', typ = typ, err = err)

@app.route('/sell/post/confirmation', methods = ['GET', 'POST'])
def confirm():
    str_res = ''
    if request.method == 'POST':
        prodTyp = request.form['prodTyp']
        name = request.form['name']
        desc = request.form['desc']
        price = request.form['price']
        
        prod = classes.product(name, price, desc, prodTyp)
        
        image = request.files['img']
        if image.filename != '':
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "rb") as img_file:
                img_string = base64.b64encode(img_file.read()).decode('utf-8')
                setattr(prod, 'image', img_string)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            setattr(prod, 'image', '')
        
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
        
        if prod.name == '' or prod.price == '':
            str_res = ''
        else:
            res = db_func.post(prod)
            str_res = str(res)
        
    if str_res != '':
        conf = binascii.b2a_hex(os.urandom(15))
        conf = str(conf)
        return render_template('confirmation.html', conf = conf)
    else:
        err = True
        return render_template("postItem.html", typ = prodTyp, err = err)
    

@app.route('/login', methods = ['GET', 'POST'])
def login():
    global currentUser
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        check = db_func.checkPassword(username, password)
        if check:
            currentUser = username
            return render_template('cart.html')
    return render_template('login.html')

@app.route('/create', methods = ['GET', 'POST'])
def create():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        displayName = request.form['displayName']
        db_func.createUser(username, password, displayName)
    return render_template('create.html')

@app.route('/cart', methods = ['GET', 'POST'])
def cart():
    global currentUser
    user = db_func.findUser(currentUser)
    if request.method == 'POST':
        itemID = request.form['itemID']
        cart = db_func.removeFromCart(itemID, currentUser)
        return render_template('cart.html', cart=cart)
    return render_template('cart.html', cart=user['Cart'])


if __name__ == '__main__':
    app.run(debug=True)