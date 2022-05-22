import datetime
import mysql.connector

cnx = None

def get_sql_connection():
  print("Opening mysql connection")
  global cnx

  if cnx is None:
    cnx = mysql.connector.connect(user='root', password='Soumya_123', database='ksgrocerystore')

  return cnx