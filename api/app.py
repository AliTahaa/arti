#!/usr/bin/python3
""" Main application file """

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_restful import Api
from config import Config
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db import db, init_db
from resources.auth import UserRegister, UserLogin
from resources.product import ProductList, Product
from resources.order import OrderList, Order

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Extensions
jwt = JWTManager(app)
CORS(app)
api = Api(app)
init_db(app)

# Routes
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(ProductList, '/products')
api.add_resource(Product, '/products/<int:product_id>')
api.add_resource(OrderList, '/orders')
api.add_resource(Order, '/orders/<int:order_id>')

if __name__ == '__main__':
    app.run(debug=True)
