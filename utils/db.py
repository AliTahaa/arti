#!/usr/bin/python3
""" Database configuration """

from flask_mysqldb import MySQL

db = MySQL()

def init_db(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'your_password'
    app.config['MYSQL_DB'] = 'arti_store'
    db.init_app(app)
