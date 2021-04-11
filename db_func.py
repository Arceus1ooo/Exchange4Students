import pymongo
import classes

client = pymongo.MongoClient("mongodb+srv://dbAdmin:dbAdminPASS@cluster0.ih0la.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.Exchange4Students

def post(prod):
    
    item = {"Name" : prod.name,
            "Price" : prod.price,
            "Description" : prod.desc,
            "Type" : "",
            "Product Details" : {}}
    
    if hasattr(prod.typ, 'title'):
        item['Type'] = "Book"
        item['Product Details']['Title'] = prod.typ.title
        item['Product Details']['Edition'] = prod.typ.ed
        item['Product Details']['Course'] = prod.typ.course
        
    elif hasattr(prod.typ, 'size'):
        item['Type'] = "Clothing"
        item['Product Details']['Type'] = prod.typ.typ
        item['Product Details']['Color'] = prod.typ.color
        item['Product Details']['Size'] = prod.typ.size
        
    elif hasattr(prod.typ, 'kind'):
        item['Type'] = "Sports Gear"
        item['Product Details']['Type'] = prod.typ.kind
        item['Product Details']['Weight'] = prod.typ.weight
        
    elif hasattr(prod.typ, 'model'):
        item['Type'] = "Electronic"
        item['Product Details']['Type'] = prod.typ.typ
        item['Product Details']['Model'] = prod.typ.mod
        item['Product Details']['Dimensions']['Length'] = prod.typ.dim.l
        item['Product Details']['Dimensions']['Width'] = prod.typ.dim.w
        item['Product Details']['Dimensions']['Height'] = prod.typ.dim.h
        item['Product Details']['Weight'] = prod.typ.weight

    else:
        item['Type'] = "Furniture"
        item['Product Details']['Type'] = prod.typ.typ
        item['Product Details']['Color'] = prod.typ.color
        item['Product Details']['Dimensions']['Length'] = prod.typ.dim.l
        item['Product Details']['Dimensions']['Width'] = prod.typ.dim.w
        item['Product Details']['Dimensions']['Height'] = prod.typ.dim.h
        item['Product Details']['Weight'] = prod.typ.weight
    
    res = db.Listings.insert_one(item)
    return res
    


def pull(typ, keyword):
    
    if typ != '':
        result = db.Listings.find({'Type' : typ})
    elif keyword != '':
        result = db.Listings.find({'Description' : 
                                   {'$regex' : keyword, '$options' : 'i'}})
    
    return result


client.close()
