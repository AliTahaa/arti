#!/usr/bin/python3
""" Order resources """

from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.db import db

class OrderList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()['id']
        cursor = db.connection.cursor()
        cursor.execute('SELECT * FROM orders WHERE user_id = %s', (user_id,))
        orders = cursor.fetchall()
        return jsonify(orders)

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()['id']
        data = request.get_json()
        total = data['total']
        items = data['items']

        cursor = db.connection.cursor()
        cursor.execute('INSERT INTO orders (user_id, total) VALUES (%s, %s)', (user_id, total))
        order_id = cursor.lastrowid

        # Insert items into order_items table
        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            price = item['price']
            cursor.execute('INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)', (order_id, product_id, quantity, price))
        
        db.connection.commit()

        return jsonify(message="Order created", order_id=order_id)

class Order(Resource):
    @jwt_required()
    def get(self, order_id):
        user_id = get_jwt_identity()['id']
        cursor = db.connection.cursor()
        cursor.execute('SELECT * FROM orders WHERE id = %s AND user_id = %s', (order_id, user_id))
        order = cursor.fetchone()

        if not order:
            return jsonify(message="Order not found"), 404

        # Fetch order items
        cursor.execute('SELECT * FROM order_items WHERE order_id = %s', (order_id,))
        items = cursor.fetchall()

        return jsonify(order=order, items=items)

    @jwt_required()
    def delete(self, order_id):
        user_id = get_jwt_identity()['id']
        cursor = db.connection.cursor()
        
        # Check if the order exists
        cursor.execute('SELECT * FROM orders WHERE id = %s AND user_id = %s', (order_id, user_id))
        order = cursor.fetchone()

        if not order:
            return jsonify(message="Order not found"), 404

        # Delete order items
        cursor.execute('DELETE FROM order_items WHERE order_id = %s', (order_id,))
        # Delete order
        cursor.execute('DELETE FROM orders WHERE id = %s', (order_id,))
        
        db.connection.commit()

        return jsonify(message="Order deleted successfully")
