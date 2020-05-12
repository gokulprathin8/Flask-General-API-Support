from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import identity, authenticate
import uuid

app = Flask(__name__)
app.secret_key = 'secret'
api = Api(app)

jwt = JWT(app, authenticate, identity)

home = [
    {
        'body': 'API built with Flask. Flask depends on the Jinja template engine and the Werkzeug WSGI toolkit.',
        'contact': 'Contact your network administrator for assistance.',
        'contact-detials': 'gokulprathin8@gmail.com'
    }
]

items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {'item': None}, 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be left Blank!"
        )
        data = parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return items

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        get_name = request.args.get('name')
        item = next(filter(lambda x: x['name'] == name,items), None)
        if item is None:
            item = {'name': name, 'price': get_name}
            items.append(item)
        else:
            item.update(get_name)
        return item

class ItemList(Resource):
    @jwt_required()
    def get(self):
        return items

class Home(Resource):
    def get(self):
        return home

class Student(Resource):
    def get(self, name):
        return {'student': name}

api.add_resource(Home, '/')
api.add_resource(ItemList, '/itemList')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Student, '/student/<string:name>')

app.run(port=5000, debug=True )
