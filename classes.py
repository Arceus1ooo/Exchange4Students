class product():
    def __init__(self, name, price, description, typ):
        self.name = name
        self.price = price
        self.desc = description
        self.typ = typ

class furntiture():
    def __init__(self, typ, color, l, w, h, lbs):
        self.typ = typ
        self.color = color
        self.dim = (l, w, h)
        self.weight = lbs

class book():
    def __init__(self, title, ed, course):
        self.title = title
        self.ed = ed
        self.course = course

class electronic():
    def __init__(self, typ, mod, l, w, h, lbs):
        self.typ = typ
        self.mod = mod
        self.dim = (l, w, h)
        self.weight = lbs        

class clothing():
    def __init__(self, typ, color, sz):
        self.typ = typ
        self.color = color
        self.size = sz
        
class sports_gear():
    def __init__(self, typ, lbs):
        self.kind = typ
        self.weight = lbs
