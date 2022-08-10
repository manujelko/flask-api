import sqlite3

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field cannot be left blank")
    parser.add_argument("name", type=str, required=False)

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': row[0], 'price': row[1]}
        return {'message': 'Item not found'}, 404


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
