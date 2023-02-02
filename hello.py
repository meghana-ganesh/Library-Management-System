import main
import mysql.connector
from flask import Flask, render_template,request, redirect, url_for, session
from flask_mysqldb import MySQL
import datetime
import MySQLdb.cursors
import re

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = ' key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '*******'
app.config['MYSQL_DB'] = 'lms'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM form WHERE username = %s AND password = %s', (username, password,))
            # Fetch one record and return result
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            # session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            # return 'Logged in successfully!'
            return render_template('menu.html')
        else:
            # Account doesnt exist or username/password incorrect
            return render_template('index.html', msg='Incorrect username/password!')       
    return render_template('index.html', msg='')

@app.route('/login/register',methods=['GET','POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'librarian' in request.form and 'mob' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        librarian = request.form['librarian']
        mob = request.form['mob']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM form WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email or not librarian or not mob:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO form VALUES (%s, %s, %s,%s,%s)', (username, password, email,librarian,mob))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!hi'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/bookmenu')
def bookmenu():
    return render_template('bookmenu.html')

@app.route('/addbooks',methods=['GET','POST'])
def addbooks():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'isbn' in request.form and 'title' in request.form and 'author' in request.form and 'aid' in request.form and 'dop' in request.form:
        # Create variables for easy access
        isbn = request.form['isbn']
        title = request.form['title']
        author = request.form['author']
        aid = request.form['aid']
        dop = request.form['dop']
        
        

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM books WHERE title = %s ', (title,))
        account = cursor.fetchone()

        cursor.execute('SELECT * FROM author WHERE aid = %s', (aid,))
        x = cursor.fetchone()
        
        if account:
            msg = 'Book already exists!'
            # If account exists show error and validation checks
        elif x:
            cursor.execute('INSERT INTO books VALUES (NULL,%s, %s, %s,%s)', (isbn,title,dop,aid))
            mysql.connection.commit()
            msg='Book has been added but aid exists.'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO author VALUES (%s, %s)', (aid,author))
            cursor.execute('INSERT INTO books VALUES (NULL,%s, %s, %s,%s)', (isbn,title,dop,aid))

            mysql.connection.commit()
            msg = 'Book has been added!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('addbooks.html', msg=msg)

@app.route('/studentmenu')
def studentmenu():
    return render_template('studentmenu.html')

@app.route('/addstudent',methods=['GET','POST'])
def addstudent():
    # Output message if something goes wrong...
    # print(request.form)

    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'sname' in request.form and 'mob1' in request.form and 'mob2' in request.form and 'dob' in request.form and 'sex' in request.form:
        # Create variables for easy access
        sname = request.form['sname']
        mob1 = request.form['mob1']
        mob2 = request.form['mob2']
        dob = request.form['dob']
        sex = request.form['sex']
        
        

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE sname = %s', (sname,))
        account = cursor.fetchone()

        
        if account:
            msg = 'Student already exists!'
            # If account exists show error and validation checks
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO student VALUES (NULL,%s, %s, %s,%s,%s)', (sname,mob1,mob2,dob,sex))
            mysql.connection.commit()
            msg = 'Student has been added!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('addstudent.html', msg=msg)

@app.route('/issue',methods=['GET','POST'])
def issue():
    # Output message if something goes wrong...
    # print(request.form)

    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'bid' in request.form and 'sid' in request.form and 'idate' in request.form:
        # Create variables for easy access
        bid = request.form['bid']
        sid = request.form['sid']
        date = request.form['idate']
        # date = request.form.get('date')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO issue_table (bid,sid,issue_date)  VALUES (%s, %s,%s)', (bid,sid,date))
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
        mysql.connection.commit()
        msg = 'Issue details have been added!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('issue.html', msg=msg)

if __name__=='__main__':
    app.run(debug = True)
