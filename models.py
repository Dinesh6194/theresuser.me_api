from sqlalchemy import Table, Column, Integer, Text, Float, ForeignKey
from sqlalchemy.orm import mapper
from database import metadata, db_session

class BlogPost(object):
    query = db_session.query_property()
    def __init__(self, id=None, title=None, post=None):
        self.id = id
        self.title = title
        self.post = post

blog_posts = Table('blog_posts', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', Text),
    Column('post', Text)
)

mapper(BlogPost, blog_posts)


class Item(object):
    query = db_session.query_property()
    def __init__(self, item_id=None, item_name=None):
        self.item_id = item_id
        self.item_name = item_name

    def serialize(self):
     	return {"item_id":self.item_id,"item_name":self.item_name}
        

items = Table('items', metadata,
    Column('item_id', Integer, primary_key=True),
    Column('item_name', Text)
    
)

mapper(Item, items)


class ItemCategory(object):
    query = db_session.query_property()
    def __init__(self, type_id=None, type_name=None):
        self.type_id = type_id
        self.type_name = type_name

    def serialize(self):
     	return {"type_id":self.type_id,"type_name":self.type_name}
        

item_category = Table('item_category', metadata,
    Column('type_id', Integer, primary_key=True),
    Column('type_name', Text)
    
)

mapper(ItemCategory, item_category)


class Color(object):
    query = db_session.query_property()
    def __init__(self, color_id=None, color_name=None):
        self.color_id = color_id
        self.color_name = color_name

    def serialize(self):
     	return {"color_id":self.color_id,"color_name":self.color_name}
        

colors = Table('colors', metadata,
    Column('color_id', Integer, primary_key=True),
    Column('color_name', Text)
    
)

mapper(Color, colors)


class Year(object):
    query = db_session.query_property()
    def __init__(self, year_id=None, year_range=None):
        self.year_id = year_id
        self.year_range = year_range


    def serialize(self):
     	return {"year_id":self.year_id,"year_range":self.year_range}
        

years = Table('years', metadata,
    Column('year_id', Integer, primary_key=True),
    Column('year_range', Text)
    
)

mapper(Year, years)

class Postitem(object):
    query = db_session.query_property()
    def __init__(self, post_id=None,item_id=None,type_id=None,color_id=None,year_id=None,latitude=None,longitude=None,status=None):
        self.post_id=post_id
        self.item_id=item_id
        self.type_id=type_id
        self.color_id=color_id
        self.year_id=year_id
        self.latitude=latitude
        self.longitude=longitude
        self.status=status

    def serialize(self):
     	return {"post_id":self.post_id,"item_id":self.item_id,"type_id":self.type_id,"color_id":self.color_id,"year_id":self.year_id,"latitude":self.latitude,"longitude":self.longitude,"status":self.status}
        

posts = Table('posts', metadata,
    Column('post_id', Integer, primary_key=True),
    Column('item_id', Integer, ForeignKey(Item.item_id)),
    Column('type_id', Integer,ForeignKey(ItemCategory.type_id)),
    Column('color_id', Integer,ForeignKey(Color.color_id)),
    Column('year_id', Integer,ForeignKey(Year.year_id)),
    Column('latitude', Float),
    Column('longitude', Float),
    Column('status', Integer),
    
)


mapper(Postitem, posts)

class Carbon(object):
    query = db_session.query_property()
    def __init__(self, record_id=None, item_name=None,carbon_intensity=None):
        self.record_id = record_id
        self.item_name = item_name
        self.carbon_intensity=carbon_intensity

    def serialize(self):
     	return {"record_id":self.record_id,"item_name":self.item_name,"carbon_intensity":self.carbon_intensity}
        

carbons = Table('carbonintensity', metadata,
    Column('record_id', Integer, primary_key=True),
    Column('item_name', Text),
    Column('carbon_intensity',Float)
    
)

mapper(Carbon, carbons)
