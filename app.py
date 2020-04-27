from flask import Flask, request, jsonify
from flask_restplus import Resource, Api, fields
from database import db_session
from models import BlogPost,Item,ItemCategory,Year,Color,Postitem,Carbon
import json
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
        print(data)
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
        post=Postitem(post_id=data['post_id'],item_id=data['item_id'],type_id=data['type_id'],color_id=data['color_id'],year_id=data['year_id'],latitude=data['latitude'],longitude=data['longitude'],status=1)
        db_session.add(post)
        db_session.commit()
        return {'Message':'Success'}

@api.route('/allinone')
class Allinone(Resource):
    def get(self, **kwargs):
        item=list(map(lambda it: it.serialize(), Item.query.all()))
        types=list(map(lambda ty: ty.serialize(), ItemCategory.query.all()))
        colors=list(map(lambda cl: cl.serialize(), Color.query.all()))
        years=list(map(lambda yr: yr.serialize(), Year.query.all()))
        valuedict={}
        valuedict["Item"]=item
        valuedict["ItemCategory"]=types
        valuedict["Color"]=colors
        valuedict['Year']=years
        

        return jsonify(valuedict)

@api.route('/posteditems')
class Postitems(Resource):
   
    def get(self, **kwargs):

        fetchedvalues=(db_session.query(Postitem,Item,ItemCategory,Color,Year).join(Item).join(ItemCategory).join(Color).join(Year)).filter(Postitem.status==1).all()
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
        fetchedvalues=(db_session.query(Postitem,Item,ItemCategory,Color,Year).join(Item).join(ItemCategory).join(Color).join(Year)).filter(Item.item_name==data['item_name'],Postitem.status==1).all()
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
        print(data)
        # datatoupdate={BlogPost.post:data['post']}
        postdata=Postitem.query.filter_by(post_id=data['post_id']).first()
        postdata.status = 0
        db_session.commit()
        return {'Message':'Success'}

@api.route('/allposteditems')
class Postitems(Resource):
   
    def get(self, **kwargs):

        fetchedvalues=(db_session.query(Postitem,Item,ItemCategory,Color,Year).join(Item).join(ItemCategory).join(Color).join(Year)).all()
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


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    application.run(debug=True)
