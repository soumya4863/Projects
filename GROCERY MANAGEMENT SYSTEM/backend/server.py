from urllib import response
from flask import Flask, request, jsonify
from importlib_metadata import method_cache
from sql_connection import get_sql_connection
import mysql.connector
import json

import products_dao
import orders_dao
import uom_dao

app = Flask(__name__)

connection = get_sql_connection()

@app.route('/getReport',methods=['GET'])
def get_report():
    response=orders_dao.getReport(connection)
    response=jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getyearReport',methods=['GET'])
def get_year_report():
    response=orders_dao.getyearReport(connection)
    response=jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getProducts', methods=['GET'])
def get_products():
    response = products_dao.get_all_products(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    if product_id==-1:
        print('failed to insert order')
        return 'Error in price per item'
    else:
        response = jsonify({
            'product_id': product_id
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload)
    if order_id==-2:
        return 'Transaction failed due to insufficient products'
    if order_id==-1:
        return 'Unsuccessful Transaction'
    else:
        response = jsonify({
            'order_id': order_id
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


#@app.route('/updateProduct',methods=['POST'])
#def update_product():
#    request_payload = json.loads(request.form['data'])
#    product_id = products_dao.update_product(connection,request_payload)
#    response = jsonify({
#        'product_id': product_id
#    })
#    response.headers.add('Access-Control-Allow-Origin', '*')
#    return response 



if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(port=5000)
