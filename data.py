import mysql.connector

	mysql.connector.connect(
	    host="localhost",
	    user="YOUR_USERNAME",
	    password="YOUR_PASSWORD",
	    database="YOUR_DATABASE"
	)


mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM your_table")

for row in mycursor.fetchall():
    print(row)
