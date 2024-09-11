#!/usr/bin/python3
""" Product resources """

from flask_restful import Resource
from flask import request, jsonify
from utils.db import db

class ProductList(Resource):
    def get(self):
        cursor = db.connection.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        return jsonify(products)

    def post(self):
        data = request.get_json()
        name = data['name']
        description = data['description']
        price = data['price']
        image_url = data['image_url']
        category_id = data['category_id']

        cursor = db.connection.cursor()
        cursor.execute('INSERT INTO products (name, description, price, image_url, category_id) VALUES (%s, %s, %s, %s, %s)', (name, description, price, image_url, category_id))
        db.connection.commit()

        return jsonify(message="Product added successfully")

class Product(Resource):
    def get(self, product_id):
        cursor = db.connection.cursor()
        cursor.execute('SELECT * FROM products WHERE id = %s', (product_id,))
        product = cursor.fetchone()
        return jsonify(product)
