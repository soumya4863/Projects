from sql_connection import get_sql_connection

def get_all_products(connection):
    cursor = connection.cursor()
    query = ("select products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name, products.qty from products inner join uom on products.uom_id=uom.uom_id")
    cursor.execute(query)
    response = []
    for (product_id, name, uom_id, price_per_unit, uom_name,qty) in cursor:
        response.append({
            'product_id': product_id,
            'name': name,
            'uom_id': uom_id,
            'price_per_unit': price_per_unit,
            'uom_name': uom_name,
            'qty' : qty
        })
    return response

def insert_new_product(connection, product):
    cursor = connection.cursor()
    if int(product['price_per_unit'])<0:
        return -1;
    query = ("INSERT INTO products "
             "(name, uom_id, price_per_unit)"
             "VALUES (%s, %s, %s)")
    data = (product['product_name'], product['uom_id'], product['price_per_unit'])

    cursor.execute(query, data)
    connection.commit()
    return cursor.lastrowid

def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = ("DELETE FROM products where product_id=" + str(product_id))
    cursor.execute(query)
    connection.commit()

    return cursor.lastrowid

def update_product(connection,product):
    cursor=connection.cursor()
    sql_update_query = """Update products set name = %s,price_per_unit=%s where name = %s"""
    input_data = (product['new_product_name'],product['price_per_unit'],product['old_product_name'])
    cursor.execute(sql_update_query, input_data)
    connection.commit()
    
    return cursor.lastrowid

if __name__ == '__main__':
    connection = get_sql_connection()
    

    