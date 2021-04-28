import pymongo
import classes
import bson

client = pymongo.MongoClient("mongodb+srv://dbAdmin:dbAdminPASS@cluster0.ih0la.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.Exchange4Students

def post(prod):
    
    item = {"Name" : prod.name,
            "Price" : prod.price,
            "Description" : prod.desc,
            "Type" : prod.prodTyp,
            "Image" : prod.image,
            "Product Details" : {}}
    
    if prod.prodTyp == "Book":
        item['Product Details']['Title'] = prod.title
        item['Product Details']['Edition'] = prod.ed
        item['Product Details']['Course'] = prod.course
        
    elif prod.prodTyp == "Clothing":
        item['Product Details']['Type'] = prod.typ
        item['Product Details']['Color'] = prod.color
        item['Product Details']['Size'] = prod.sz
        
    elif prod.prodTyp == "Sports Gear":
        item['Product Details']['Type'] = prod.kind
        item['Product Details']['Weight'] = prod.weight
        
    elif prod.prodTyp == "Electronic":
        item['Product Details']['Type'] = prod.typ
        item['Product Details']['Model'] = prod.mod
        item['Product Details']['Dimensions'] = {}
        item['Product Details']['Dimensions']['Length'] = prod.l
        item['Product Details']['Dimensions']['Width'] = prod.w
        item['Product Details']['Dimensions']['Height'] = prod.h
        item['Product Details']['Weight'] = prod.weight

    elif prod.prodTyp == "Furniture":
        item['Product Details']['Type'] = prod.typ
        item['Product Details']['Color'] = prod.color
        item['Product Details']['Dimensions'] = {}
        item['Product Details']['Dimensions']['Length'] = prod.l
        item['Product Details']['Dimensions']['Width'] = prod.w
        item['Product Details']['Dimensions']['Height'] = prod.h
        item['Product Details']['Weight'] = prod.weight
    
    res = db.Listings.insert_one(item)
    return res
    


def pull(typ, keyword):

    def pullHelper(typ, keyword, search):
        if typ == 'Any' and keyword != '':
            result = db.Listings.find({search : 
                                    {'$regex' : keyword, '$options' : 'i'}})
        elif typ == 'Any' and keyword == '':
            result = db.Listings.find({})
        elif typ != '' and typ != 'Any' and keyword != '':
            result = db.Listings.find({'Type' : typ, search : 
                                    {'$regex' : keyword, '$options' : 'i'}})
        elif typ != '' and keyword == '':
            result = db.Listings.find({'Type' : typ})

        return result

    res = pullHelper(typ, keyword, 'Name')
    if res.count() == 0:
        res = pullHelper(typ, keyword, 'Description')
    
    return res

def pullID(itemID):
    '''returns item with specific itemID'''
    return db.Listings.find({'_id': bson.ObjectId(oid=str(itemID))})


def addToCart(itemID, username):
    '''adds item to user's cart'''
    item = pullID(itemID)
    user = searchUsers(username)

def searchUsers(username):
    '''searches for the user with the given username in the db'''
    user = db.Users.find_one({'Username': username})
    return user

def checkPassword(username, password):
    '''verifies password with username'''
    user = searchUsers(username)
    if user == None:
        return False

    if password == user['Password']:
        return True
    else:
        return False

def createUser(username, password, displayName):
    user = {"Username" : username,
            "Password" : password,
            "Display Name" : displayName,
            "Cart" : {},
            "Listings" : {}
            }

    db.Users.insert_one(user)

client.close()