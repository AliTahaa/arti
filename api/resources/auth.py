#!/usr/bin/python3
""" Authentication resources """

from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import db

class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        name = data['name']
        email = data['email']
        password = generate_password_hash(data['password'])

        cursor = db.connection.cursor()
        cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', (name, email, password))
        db.connection.commit()

        return jsonify(message="User registered successfully")

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']

        cursor = db.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            access_token = create_access_token(identity={'id': user[0], 'email': user[2]})
            return jsonify(access_token=access_token)
        else:
            return jsonify(message="Invalid credentials"), 401
