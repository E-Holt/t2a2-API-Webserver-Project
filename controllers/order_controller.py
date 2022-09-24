from flask import Blueprint, jsonify, request
from main import db
from models.beans import Bean
from models.orders import Order
from models.users import User
from models.roasters import Roaster
from schemas.bean_schema import bean_schema, beans_schema
from schemas.order_schema import order_schema, orders_schema
from schemas.roaster_schema import roaster_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date

order = Blueprint("order", __name__, url_prefix="/order")

# Show all current orders
@order.route("/", methods=["GET"])
@jwt_required()
def get_order():
    roaster_id = get_jwt_identity()
    roaster = Roaster.query.get(roaster_id)
    # it is not enough with a token, the identity needs to be a librarian
    if not roaster:
        return {"error": "You don't have the permission to do this"}, 401
    # get all the bean from the database
    order_list = Order.query.all()
    result = orders_schema.dump(order_list)
    return jsonify(result)

# Post a new order
@order.route("/<int:id>", methods=["POST"])
@jwt_required()
def new_order(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    # it is not enough with a token, the identity needs to be a user
    if not user:
        return {"error": "You don't have the permission to do this"}, 401
    #find the book in the database
    bean = Bean.query.get(id)
    #check if book exist in the database
    if not bean:
        return {"error": "That bean variety isn't currently available"} 
    order_fields = order_schema.load(request.json)
    order = Order(
        order_date = order_fields["order_date"],
        amount = order_fields["amount"],
        grind = order_fields["grind"],
        price = order_fields["price"],
        user_id = order_fields["user_id"],
        bean_id = order_fields["bean_id"]
    )

    db.session.add(order)
    db.session.commit()

    return jsonify(order_schema.dump(order))