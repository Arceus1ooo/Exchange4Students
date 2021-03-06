import pymongo
import classes
import bson
from datetime import datetime, date

client = pymongo.MongoClient("mongodb+srv://dbAdmin:dbAdminPASS@cluster0.ih0la.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.Exchange4Students

def post(prod):
    
    item = {"Seller" : prod.seller,
            "Name" : prod.name,
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
    addToListings(item['_id'], item['Seller'])
    return res
    
"""def removeListingPicture(itemID):
    '''Removes a listing's picture from listings db'''
    db.Listings.update_one({"_id": bson.ObjectId(oid=str(itemID))}, {"$set":{"Image": ""}})"""

def removeListing(item):
    '''removes listing from listing db'''
    db.Listings.remove(item)
    

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
    '''returns the item with specific itemID FROM LISTINGS DB, general POV'''
    return db.Listings.find_one({'_id': bson.ObjectId(oid=str(itemID))})

def pullIDCart(itemID, username):
    '''returns the item with specific itemID from user's cart, buyer POV'''
    user = findUser(username)
    cart = user['Cart']
    for item in cart:
        if str(item['_id']) == itemID:
            return item

def pullIDListing(itemID, username):
    '''returns the item with specific itemID from user's listings, seller POV'''
    user = findUser(username)
    listings = user['Listings']
    for item in listings:
        if str(item['_id']) == itemID:
            return item
    

def findUser(username):
    '''searches for the user with the given username in the db'''
    user = db.Users.find_one({'Username': username})
    return user

def createUser(username, password, displayName):
    user = {"Username" : username,
            "Password" : password,
            "Display Name" : displayName,
            "Cart" : [],
            "Listings" : [],
            "Notifications": []
            }

    db.Users.insert_one(user)

def checkPassword(username, password):
    '''verifies password with username'''
    user = findUser(username)
    if user == None:
        return False

    if password == user['Password']:
        return True
    else:
        return False

def buildCart(username):
    '''used for building user cart'''
    user = findUser(username)
    items = []
    for i in user['Cart']:
        items.append(i)
    return items

def buildListings(username):
    '''used for building user listings'''
    user = findUser(username)
    items = []
    for i in user['Listings']:
        items.append(i)
    return items

def addToListings(itemID, username):
    '''adds item to user's listings'''
    items = buildListings(username)
    items.append(pullID(itemID))
    db.Users.update_one({"Username": username}, {"$set":{"Listings": items}})

def addToCart(itemID, username):
    '''adds item to user's cart'''
    items = buildCart(username)
    if pullID(itemID) not in items:
        items.append(pullID(itemID))
    db.Users.update_one({"Username": username}, {"$set":{"Cart": items}})

def removeFromListings(itemID, username):
    '''removes item from user's listings'''
    items = buildListings(username)
    if pullIDListing(itemID, username) in items:
        items.remove(pullIDListing(itemID, username))
    db.Users.update_one({"Username": username}, {"$set":{"Listings": items}})
    #return items

def removeFromCart(itemID, username):
    '''removes item from user's cart'''
    items = buildCart(username)
    if pullIDCart(itemID, username) in items:
        items.remove(pullIDCart(itemID, username))
    db.Users.update_one({"Username": username}, {"$set":{"Cart": items}})
    return items

def getSellerName(itemID):
    '''returns the seller name object given item id, used with buyer POV'''
    item = pullID(itemID)
    sellerName = item['Seller']
    return sellerName

def getNotifications(username):
    '''builds the user's notification list'''
    user = findUser(username)
    n = []
    for note in user['Notifications']:
        n.append(note)
    return n

def sendNotification(itemID, buyerName, sellerName):
    '''sends a notification to seller that buyer bought item from seller'''
    item = pullIDListing(itemID, sellerName)

    n = getNotifications(sellerName)

    now = datetime.now()
    now_str = now.strftime('%d/%m/%Y %H:%M:%S')

    notif = {'Timestamp': now_str, 
            'Message': f"{buyerName} has bought item: {item['Name']} from you"}

    n.append(notif)
    db.Users.update_one({"Username": sellerName}, {"$set": {"Notifications": n}})

def removeNotifications(notif, sellerName):
    '''removes a notification from a seller's inbox'''
    n = getNotifications(sellerName)
    if notif in n:
        n.remove(notif)
    db.Users.update_one({"Username": sellerName}, {"$set": {"Notifications": n}})



client.close()