import mysql.connector


mycon = mysql.connector.connect(host="localhost",user="root",passwd = "******",database = "lms")

if mycon.is_connected():
    print('successfully connected to mysql database')

# cursor = mycon.cursor()
# # cursor.execute("select * from books")
# data = cursor.fetchall()
# count = cursor.rowcount

# for row in data:
#     print(row)

