from flask import Blueprint, jsonify, request
from a_cupcakes.helpers import token_required
from a_cupcakes.models import db, Item, item_schema, items_schema

api = Blueprint('api',__name__,url_prefix='/api')

@api.route('/getdata')
@token_required
def get_data(current_user_token):
    return { 'some' : 'value'}

# Menu Items Endpoint
@api.route('/menu-items', methods =['POST'])
@token_required
def create_menu_item(current_user_token):
    type = request.json['type']
    description = request.json['description']
    price = request.json['price']
    user_token = current_user_token.token

    item = Item(type, description, price, user_token)
    db.session.add(item)
    db.session.commit()

    response = item_schema.dump(item)
    return jsonify(response)

# Retrieve all items endpoint
@api.route('/menu-items', methods=['GET'])
@token_required
def get_menu_items(current_user_token):
    owner = current_user_token.token
    items = Item.Query.filer_by(user_token=owner).all()
    response = items_schema.dump(items)
    return jsonify(response)

# Retrieve one item endpoint
@api.route('/menu-items/<id>', methods = ['GET'])
@token_required
def get_menu_item(current_user_token, id):
    owner = current_user_token
    item = Item.query.get(id)
    response = item_schema.dump(item)
    return jsonify(response)

# Update chracter endpoint
@api.route('/menu-items/<id>', methods = ['POST', 'PUT'])
@token_required
def update_menu_item(current_user_token, id):
    item = Item.query.get(id)

    item.type = request.json['type']
    item.description = request.json['description']
    item.price = request.json['price']

    db.session.commit()
    response = item_schema.dump(item)
    return jsonify(response)

# Delete drone endpoint
@api.route('/menu-items/<id>', methods = ['DELETE'])
@token_required
def delete_menu_item(current_user_token, id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()

    response = item_schema.dump(item)
    return jsonify(response)