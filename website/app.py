# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import textwrap
from datetime import datetime

config = {
    "DEBUG": True  # run app in debug mode
}

app = Flask(__name__)


app.secret_key = 'your secret key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Oatmeal_007'
app.config['MYSQL_DB'] = 'techDetect'

date = datetime.now()
dateString = str(date)
todayDate = (textwrap.shorten(dateString, 11, placeholder = ''))
todayDate = todayDate.replace("-","_")

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'organization' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		organization = request.form['organization']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'name must contain only characters and numbers !'
		else:
			cursor.execute('INSERT INTO accounts(username, password, email, organization) VALUES  (% s, % s, % s, % s)', (username, password, email, organization, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

@app.route("/index")
def index():
	if 'loggedin' in session:
		return render_template("index.html")
	return redirect(url_for('login'))


@app.route("/display")
def display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE id = % s', (session['id'], ))
		account = cursor.fetchone()	
		return render_template("display.html", account = account)
	return redirect(url_for('login'))

@app.route("/update", methods =['GET', 'POST'])
def update():
	msg = ''
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE id = % s', (session['id'], ))
		account = cursor.fetchone()	
		if request.method == 'POST' and 'password' in request.form and 'email' in request.form and 'organization' in request.form:
			password = request.form['password']
			email = request.form['email']
			organization = request.form['organization']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM accounts WHERE username = % s', (session['username'], ))
			account = cursor.fetchone()
			if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				msg = 'Invalid email address !'
			elif account:
				cursor.execute('UPDATE accounts SET password =% s, email =% s, organization =% s WHERE id =% s', (password, email, organization, (session['id'], ), ))
				mysql.connection.commit()
				msg = 'You have successfully updated !'
		elif request.method == 'POST':
			msg = 'Please fill out the form !'
		return render_template("update.html", msg = msg, account = account)
	return redirect(url_for('login'))

@app.route("/students")
def pets():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM students')
        pet_records = cursor.fetchall()
        return render_template("students.html", pet_records = pet_records)
    return redirect(url_for('login'))

@app.route("/attendance")
def pet	():
	global todayDate
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM attendance_'+todayDate+'')
		attendance_records = cursor.fetchall()
		return render_template("attendance.html", attendance_records = attendance_records)
	return redirect(url_for('login'))	

if __name__ == "__main__":
	app.run(host ="localhost", debug = True, port = int("5000"))