from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


items = []


class Item(Resource):
    def get(self, name):
        item = next((item for item in items if item["name"] == name), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next((item for item in items if item["name"] == name), None):
            return {'message': f"An item with name '{name}' already exists."}, 400

        data = request.get_json()
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

app.run(port=5000)
