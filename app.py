#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, session, redirect, url_for
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os

from flaskext.mysql import MySQL

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'

app.config['MYSQL_DATABASE_PASSWORD'] = 'Payal@001'

app.config['MYSQL_DATABASE_PASSWORD'] = 'prabhatd'

app.config['MYSQL_DATABASE_DB'] = 'test_db2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def home():
	return render_template('pages/placeholder.home.html')


@app.route('/search',methods=['GET','POST'])
def search():

	if 'username' not in session:
		return redirect(url_for('login'))

	else:
		form=SearchForm(request.form)
		#print("Hello")
		if request.method=='GET':
			return render_template('forms/search.html',form=form)
		elif request.method=='POST':
			#print("Raula")
			query=request.form['query']
			print(query)
			connection = mysql.get_db()
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM shop WHERE name = '"+query+"'");
					

			for row in cursor.fetchall():
				print(row)

			#connection.commit()

			return "Hello"

@app.route('/about')
def about():
	return render_template('pages/placeholder.about.html')


@app.route('/cus_login', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	#return render_template('forms/cus_login.html', form=form)

	#if 'username' in session:
	#	return redirect(url_for('home'))
	if 'username' in session:
		return redirect(url_for('home'))
	
	if request.method == 'GET':
		return render_template('forms/cus_login.html', form=form)

	elif request.method == 'POST':
			#data = request.form
			#print (data)

		phone  = request.form['phone']
		connection = mysql.get_db()
		cursor = connection.cursor()
		cursor.execute("SELECT COUNT(1) FROM customer WHERE phone = {};"
					.format(phone))

		if not cursor.fetchone()[0]:
			print('Invalid Username')
			#raise ServerError('Invalid username')

		password = request.form['password']
			
		cursor.execute("SELECT password FROM customer WHERE phone = {};"
						.format(phone))

		for row in cursor.fetchall():
			print (row)
			if password == row[0]:
				session['username'] = request.form['phone']
				return render_template('pages/placeholder.about.html')
	

	return render_template('pages/placeholder.home.html')


@app.route('/shop_login',methods=['GET','POST'])
def login2():
	#form = LoginForm(request.form)
	#return render_template('forms/shop_login.html', form=form)
	form = LoginForm2(request.form)
	#return render_template('forms/cus_login.html', form=form)

	if 'username' in session:
		return redirect(url_for('home'))
	if request.method == 'GET':
		return render_template('forms/shop_login.html', form=form)

	elif request.method == 'POST':
		data = request.form
		print (data)
		phone  = request.form['phone']
 
		connection = mysql.get_db()
		cursor = connection.cursor()
		cursor.execute("SELECT COUNT(1) FROM shop WHERE phone = {};"
					.format(phone))

		if not cursor.fetchone()[0]:
			print('Invalid Username')
			#raise ServerError('Invalid username')

		password  = request.form['password']
			
		cursor.execute("SELECT password FROM shop WHERE phone = {};"
						.format(phone))

		for row in cursor.fetchall():
			print (row)
			if password == row[0]:
				session['username'] = request.form['phone']
				return render_template('pages/placeholder.about.html')
	

	return render_template('pages/placeholder.home.html')



@app.route('/add/',methods=['GET','POST'])
def add():
	if request.method == 'GET':
		return render_template('add.html')
	elif request.method == 'POST':
		#print"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
		data=request.form
		#print request.form
		#print data
		#print data['item']
		#print data['price']
	shop_id=15
	connection = mysql.get_db()
	cursor = connection.cursor()
	cursor.execute(
		"""INSERT INTO 
			menu (
				shop_id,
				item,
				price)
		VALUES (%s,%s,%s)""", (shop_id, data['item'], data['price']))
	connection.commit()
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 




# For customer signup
@app.route('/cus_register', methods=['GET', 'POST'])
def register():
	form = RegisterForm1(request.form)

	if request.method == 'GET':
		return render_template('forms/cus_regis.html', form=form)
	elif request.method == 'POST':
		
		
		data = request.form
		name = data['name']
		phone_num = data['email']
		password = data['password']
		print (data, name, phone_num, password)
		connection = mysql.get_db()
		cursor = connection.cursor()
		cursor.execute(
			"""INSERT INTO 
				customer (
					name,
					phone,
					password)
			VALUES (%s,%s,%s)""", (name, phone_num, password))
		connection.commit()

	return str(name)+str(phone_num)+str(password)



# For shopkeepers signup
@app.route('/shop_register',methods=['GET','POST'])
def register2():
	form = RegisterForm2(request.form)
	if request.method == 'GET':
		return render_template('forms/shop_regis.html', form=form)
	elif request.method == 'POST':
		data = request.form
		print(data)
	
		name = data['name']
		phone = data['phone']
		address = data['address']
		password = data['password']
		print (data, name, address,phone, password)
		connection = mysql.get_db()
		cursor = connection.cursor()
		cursor.execute(
			"""INSERT INTO 
				shop (
					name,
					password,
					phone,
					address)
			VALUES (%s,%s,%s,%s)""", (name,password,phone,address))
		connection.commit()
		

		#return str(name)+str(phone_num)+str(password)
		return "hello"

	
@app.route('/forgot')
def forgot():
	form = ForgotForm(request.form)
	return render_template('forms/forgot.html', form=form)

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
	#db_session.rollback()
	return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
	return render_template('errors/404.html'), 404

if not app.debug:
	file_handler = FileHandler('error.log')
	file_handler.setFormatter(
		Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
	)
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
	app.run(port=25350)

# Or specify port manual0ly:
'''
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
'''
