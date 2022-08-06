from flask import Flask
from flask_jwt import JWT, jwt_required
from flask_restful import Api, Resource, reqparse

from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)


items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field cannot be left blank")
    parser.add_argument("name", type=str, required=False)

    @jwt_required()
    def get(self, name):
        item = next((item for item in items if item["name"] == name), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next((item for item in items if item["name"] == name), None):
            return {'message': f"An item with name '{name}' already exists."}, 400

        data = Item.parser.parse_args()
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201
    
    def delete(self, name):
        global items
        items = [item for item in items if item["name"] != name]
        return {"message": "item deleted"}
    
    def put(self, name):
        data = Item.parser.parse_args()
        data["name"] = name
        item = next((item for item in items if item["name"] == name), None)
        if not item:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

app.run(port=5000)
