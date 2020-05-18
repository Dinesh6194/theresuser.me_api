from flask import Flask, request, jsonify
from flask_restplus import Resource, Api, fields
from database import db_session
from models import BlogPost,Item_details,Year,Color,Postitem,Carbon, UserActivity, UserDetails
from sqlalchemy import func, extract
import json
import numpy as np
import pandas as pd
import shapefile as shp
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import utm

application = Flask(__name__)
api = Api(application,
          version='0.1',
          title='Our sample API',
          description='This is our sample API',
)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@api.route('/blog_posts')
class BlogPosts(Resource):
    model = api.model('Model', {
        'id': fields.Integer,
        'title': fields.String,
        'post': fields.String,
    })
    @api.marshal_with(model, envelope='resource')
    def get(self, **kwargs):
        return BlogPost.query.all()

@api.route('/blog_posts_insert')
class PostMessage(Resource):
    def post(self):
        data=request.get_json()
        blogpost=BlogPost(id=data['id'],title=data['title'],post=data['post'])
        db_session.add(blogpost)
        db_session.commit()
        return {'Message':'Success'}

@api.route('/blog_posts_update')
class PutMessage(Resource):
    def put(self):
        data=request.get_json()
        
        # datatoupdate={BlogPost.post:data['post']}
        postdata=BlogPost.query.filter_by(title=data['title']).first()
        postdata.post = data['post']
        db_session.commit()
        return {'Message':'Success 1'}


@api.route('/items')
class Items(Resource):
    model = api.model('Model', {
        'item_id': fields.Integer,
        'item_name': fields.String,
    })
    @api.marshal_with(model, envelope='resource')
    def get(self, **kwargs):
        return Item.query.all()

@api.route('/items_types')
class ItemCategorys(Resource):
    model = api.model('Model', {
        'type_id': fields.Integer,
        'type_name': fields.String,
    })
    @api.marshal_with(model, envelope='resource')
    def get(self, **kwargs):
        return ItemCategory.query.all()

@api.route('/colors')
class Colors(Resource):
    model = api.model('Model', {
        'color_id': fields.Integer,
        'color_name': fields.String,
    })
    @api.marshal_with(model, envelope='resource')
    def get(self, **kwargs):
        return Color.query.all()

@api.route('/years')
class Years(Resource):
    model = api.model('Model', {
        'year_id': fields.Integer,
        'year_range': fields.String,
    })
    @api.marshal_with(model, envelope='resource')
    def get(self, **kwargs):
        return Year.query.all()
@api.route('/post_items')
class Postitems(Resource):
    def post(self):
        data=request.get_json()
        post=Postitem(post_id=data['post_id'],item_id=data['item_id'],color_id=data['color_id'],year_id=data['year_id'],latitude=data['latitude'],longitude=data['longitude'],status=1)
        db_session.add(post)
        db_session.commit()
        return {'Message':'Success'}

@api.route('/allinone')
class Allinone(Resource):
    def get(self, **kwargs):
        item=list(map(lambda it: it.serialize(), Item_details.query.all()))
        colors=list(map(lambda cl: cl.serialize(), Color.query.all()))
        years=list(map(lambda yr: yr.serialize(), Year.query.all()))
        valuedict={}
        valuedict["Item"]=item
        valuedict["Color"]=colors
        valuedict['Year']=years
        

        return jsonify(valuedict)

@api.route('/posteditems')
class Postitems(Resource):
   
    def get(self, **kwargs):

        fetchedvalues=(db_session.query(Postitem,Item_details,Color,Year).join(Item_details).join(Color).join(Year)).filter(Postitem.status==1).all()
        postlist=[]
        for listelement in fetchedvalues:
            valuedict={}
            for tupleelement in listelement:
                valuedict.update(tupleelement.serialize())
            postlist.append(valuedict)
       
        return jsonify(postlist)
        
@api.route('/posteditemssearch')
class Postitems(Resource):
   
    def post(self, **kwargs):
        data=request.get_json()
        fetchedvalues=(db_session.query(Postitem,Item_details,Color,Year).join(Item_details).join(Color).join(Year)).filter(Item_details.item_name==data['item_name'],Postitem.status==1).all()
        postlist=[]
        for listelement in fetchedvalues:
            valuedict={}
            for tupleelement in listelement:
                valuedict.update(tupleelement.serialize())
            postlist.append(valuedict)
       
        return jsonify(postlist)
@api.route('/pickitem')
class Pickitem(Resource):
    def post(self):
        data=request.get_json()
        
        # datatoupdate={BlogPost.post:data['post']}
        postdata=Postitem.query.filter_by(post_id=data['post_id']).first()
        postdata.status = 0
        db_session.commit()
        return {'Message':'Success'}

@api.route('/allposteditems')
class Postitems(Resource):
   
    def get(self, **kwargs):

        fetchedvalues=(db_session.query(Postitem,Item_details,Color,Year).join(Item_details).join(Color).join(Year)).all()
        postlist=[]
        for listelement in fetchedvalues:
            valuedict={}
            for tupleelement in listelement:
                valuedict.update(tupleelement.serialize())
            postlist.append(valuedict)
       
        return jsonify(postlist)

        
@api.route('/carbon_intensity')
class Carbons(Resource):
   
    def post(self, **kwargs):
        data=request.get_json()
        fetchedvalues=list(map(lambda c: c.serialize(),db_session.query(Carbon).filter(Carbon.item_name==data['item_name']).all()))
        
        return jsonify(fetchedvalues)

@api.route('/postedactivities')
class UserActivities(Resource):
   
    def post(self, **kwargs):
        data=request.get_json()
        fetchedvalues=(db_session.query(UserActivity,Postitem,Item_details).filter(UserActivity.post_id==Postitem.post_id,Postitem.item_id==Item_details.item_id,UserActivity.user_email==data['user_email']).all())
        postlist=[]
        for listelement in fetchedvalues:
            valuedict={}                  
            for tupleelement in listelement:
                valuedict.update(tupleelement.serialize())
            postlist.append(valuedict)
       
        return jsonify(postlist)
@api.route('/post_useractivity')
class UserActivitys(Resource):
    def post(self):
        request_data=request.get_json()
        list_data=list(request_data)
        for data in list_data:
            useractivity=UserActivity(record_id=data['record_id'],user_email=data['user_email'],post_id=data['post_id'],contributed_date=data['contributed_date'],activity_category=data['activity_category'])
            db_session.add(useractivity)
            db_session.commit()
        return {'Message':'Success'}

@api.route('/post_user')
class UserDetails(Resource):
    def post(self):
        data=request.get_json()
        user=UserDetails(user_email=data['user_email'],user_name=data['user_name'])
        db_session.add(user)
        db_session.commit()
        return {'Message':'Success'}

@api.route('/user_name')
class UserDetailss(Resource):
   
    def post(self, **kwargs):
        data=request.get_json()
        fetchedvalues=list(map(lambda c: c.serialize(),db_session.query(UserDetails).filter(UserDetails.user_email==data['user_email']).all()))
        
        return jsonify(fetchedvalues)


@api.route('/post_items_list')
class Postitems(Resource):
    def post(self):
        data=request.get_json()
        list_data=list(data)
        for i in list_data:
            post=Postitem(post_id=i['post_id'],item_id=i['item_id'],color_id=i['color_id'],year_id=i['year_id'],latitude=i['latitude'],longitude=i['longitude'],status=1)
            db_session.add(post)
            db_session.commit()
        return {'Message':'Success'}

@api.route('/allactivity')
class UserActivityss(Resource):
    def get(self, **kwargs):
        user_activity=list(map(lambda it: it.serialize(), UserActivity.query.all()))     
        return jsonify(user_activity)

@api.route('/top_three')
class TopUserActivities(Resource):
   
    def post(self, **kwargs):
        data=request.get_json()
        fetchedvalues=db_session.query(UserActivity,Postitem,Item_details).filter(UserActivity.post_id==Postitem.post_id,Postitem.item_id==Item_details.item_id,extract('Month',UserActivity.contributed_date)==data['month']).group_by(UserActivity.user_email).with_entities(UserActivity.user_email,func.sum(Item_details.carbon_intensity*Item_details.kg),func.sum(Item_details.kg)).order_by(func.sum(Item_details.carbon_intensity*Item_details.kg).desc()).limit(3).all()
        fetcheduservalues=db_session.query(UserActivity,Postitem,Item_details).filter(UserActivity.post_id==Postitem.post_id,Postitem.item_id==Item_details.item_id,extract('Month',UserActivity.contributed_date)==data['month'],UserActivity.user_email==data['user_email']).group_by(UserActivity.user_email).with_entities(UserActivity.user_email,func.sum(Item_details.carbon_intensity*Item_details.kg),func.sum(Item_details.kg)).all()
        postlist=[]
        for valuelist in fetchedvalues:
            valuedict={}
            valuedict["user_email"]=valuelist[0]
            valuedict["total_ci"]=valuelist[1]
            valuedict["total_weight"]=valuelist[2]
            postlist.append(valuedict)
        for valuelist in fetcheduservalues:
            valuedict={}
            valuedict["user_email"]=valuelist[0]
            valuedict["total_ci"]=valuelist[1]
            valuedict["total_weight"]=valuelist[2]
            postlist.append(valuedict)
        return jsonify(postlist)

@api.route('/day') 
class Location(Resource):       
    def post(self,**kwargs):
        data=request.get_json()
        tests = utm.from_latlon(data['latitude'], data['longitude'])
        day='None'
        shp_path = 'domesticwastedays/DOMESTIC_WASTE_DAYS.shp'
        sf = shp.Reader(shp_path)
        point = Point(tests[0], tests[1])
        for i in range(0,len(sf.records())):
            polygon = Polygon(sf.shapeRecords()[i].shape.points[:])
            if(polygon.contains(point)):
                day=sf.records()[i][0]
        return {"day":day}


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    application.run(debug=True)