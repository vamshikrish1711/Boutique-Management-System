import mysql.connector

mydb = mysql.connector.connect(
host="localhost",
user="Dharani",
password="22eg112c12",
database="sboutique"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM your_table")

for row in mycursor.fetchall():
    print(row)
