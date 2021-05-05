import os
from flask import Flask, render_template, request, redirect
import db_func
import classes
from werkzeug.utils import secure_filename
import base64
from PIL import Image
import os, binascii
from bson.objectid import ObjectId

UPLOAD_FOLDER = os.getcwd()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

global currentUser # the username of the user currently logged in
currentUser = 'Tester'


@app.route('/')
def displayIndex():
    return render_template('index.html')
    
@app.route('/logout')
def logout():
    global currentUser
    currentUser = ''
    return redirect('/')

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
    if request.method == 'POST': # user clicks add to cart
        cartItem = request.form['objectID']
        if currentUser == '':
            return redirect('/login')
        db_func.addToCart(cartItem, currentUser)
        user = db_func.findUser(currentUser)
        return render_template('cart.html', cart=user['Cart'])

    item = db_func.pullID(_id)
    return render_template('itemView.html', item = item)

@app.route('/sell/post', methods = ['GET', 'POST'])
def postItem():
    global currentUser
    if currentUser == '':
        return redirect('/login')
    err = False
    typ = '' # placeholder
    if request.method == 'POST':
        typ = request.form['type']
    return render_template('postItem.html', typ = typ, err = err, user = currentUser)

@app.route('/sell/post/confirmation', methods = ['GET', 'POST'])
def confirm():
    str_res = ''
    if request.method == 'POST':
        prodTyp = request.form['prodTyp']
        name = request.form['name']
        desc = request.form['desc']
        price = request.form['price']
        seller = request.form['seller']
        
        prod = classes.product(name, price, desc, prodTyp, seller)
        
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
        return render_template("postItem.html", typ = prodTyp, err = err, user=db_func.findUser(currentUser))
    

@app.route('/login', methods = ['GET', 'POST'])
def login():
    global currentUser
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        check = db_func.checkPassword(username, password)
        if check:
            currentUser = username
            return redirect('/')
    return render_template('login.html')

@app.route('/account', methods = ['GET', 'POST'])
def viewAccount():
    global currentUser
    if currentUser == '':
        return redirect('/login')
    user = db_func.findUser(currentUser)
    return render_template('account.html', user = user)

@app.route('/create', methods = ['GET', 'POST'])
def create():
    global currentUser
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        displayName = request.form['displayName']
        db_func.createUser(username, password, displayName)
        currentUser = request.form['username']
        return redirect('/')
    return render_template('create.html')

@app.route('/cart', methods = ['GET', 'POST'])
def cart():
    global currentUser
    if currentUser == '':
        return redirect('/login')
    user = db_func.findUser(currentUser)
    if request.method == 'POST':
        itemID = request.form['itemID']
        cart = db_func.removeFromCart(itemID, currentUser)
        return render_template('cart.html', cart=cart)
    return render_template('cart.html', cart=user['Cart'])

"""@app.route('/r', methods = ['GET', 'POST'])
def remove():
    if request.method == 'POST':
        db_func.removeListingPicture(request.form['itemID'])
        return render_template('index.html')"""

@app.route('/checkout', methods=['GET','POST'])
def checkout():
    global currentUser # buyer POV
    user = db_func.findUser(currentUser)
    if request.method == 'POST':
        cart = request.form['cart']
        dictList = list(eval(cart))
        for d in dictList:
            sellerName = db_func.getSellerName(str(d['_id']))
            db_func.sendNotification(str(d['_id']), currentUser, sellerName)
            db_func.removeFromCart(str(d['_id']), currentUser)
            db_func.removeFromListings(str(d['_id']), sellerName)
            db_func.removeListing(d)
        return render_template('order.html')
    return render_template('cart.html', cart = user['Cart'], err = True)

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)