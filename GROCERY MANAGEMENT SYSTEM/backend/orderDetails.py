
#SELECT order_details.order_id,  order_details.quantity, order_details.total_price, products.name, orders.customer_name
#FROM (ksgrocerystore.order_details inner join ksgrocerystore.products inner join ksgrocerystore.orders)
#where order_details.product_id=products.product_id and order_details.order_id=orders.order_id;
from sympy import product
from sql_connection import get_sql_connection
def get_all_products(connection):
    cursor = connection.cursor()
    query = ("select products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name from products inner join uom on products.uom_id=uom.uom_id")
    cursor.execute(query)
    response = []
    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append({
            'product_id': product_id,
            'name': name,
            'uom_id': uom_id,
            'price_per_unit': price_per_unit,
            'uom_name': uom_name
        })
    print(response)
def update_product(connection,product):
    cursor=connection.cursor()
    sql_update_query = """Update products set name = %s,price_per_unit=%s where name = %s"""
    input_data = (product['new'],product['price'],product['old'])
    cursor.execute(sql_update_query, input_data)
    connection.commit()
    
    print(cursor.lastrowid)

def getReport(connection):
    cursor=connection.cursor()
    query="""select date_format(orders.datetime, '%M %Y') as Time,sum(total) as Total_Bill from ksgrocerystore.orders group by year(orders.datetime),month(orders.datetime)"""
    cursor.execute(query)
    response=[]
    for(Time,Total_Bill) in cursor:
        response.append({
            'time' : Time,
            'total' : Total_Bill
        })
    print(response)

def getyearReport(connection):
    cursor=connection.cursor()
    query="""select date_format(orders.datetime, '%Y') as Time,sum(total) as Total_Bill from ksgrocerystore.orders group by year(orders.datetime);"""
    cursor.execute(query)
    response=[]
    for(Time,Total_Bill) in cursor:
        response.append({
            'time' : Time,
            'total' : Total_Bill
        })
    print(response)

if __name__ == '__main__':
    connection = get_sql_connection()
    #get_all_products(connection)
    getyearReport(connection)
    

