from flask import Flask, render_template, request, session, redirect, url_for
from utils import database
import os, sqlite3, hashlib

app = Flask(__name__)
app.secret_key="PlaceHolderKey"
database.createTable()


@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home')
def home():
        return render_template('home.html')


@app.route('/output')
def output():
        return render_template('output.html')

@app.route('/login',methods = ['GET','POST'])
def login():
	if bool(session) != False:
		return redirect(url_for('userWelcome'))
        try:
            if request.form['submitType'] == "Sign up": #detects a register request
				username = request.form['username']
				password = hashlib.md5(request.form['password'].encode()).hexdigest()
				confirmPassword = hashlib.md5(request.form['confirmPassword'].encode()).hexdigest()
				
				#check if username already exists
				if (database.isStringInTableCol(username,'login','username')==True):
					return render_template('accountErrorPage.html',linkString='/register',buttonString='Username already exists, click here to go back')
				
				#check if passwords are the same
				elif(password != confirmPassword):
					return render_template('accountErrorPage.html',linkString='/register',buttonString='Passwords do not match, click here to try again')
					
				#all seems good, add to DB
				else:
					database.insertIntoLoginTable(username,password)

              


        except:
            print "no POST data found"
		
		
        return render_template('login.html')

@app.route('/logout')
def logout():
        return null

@app.route('/register',methods=['GET','Post'])
def register():
	if bool(session) != False:
		return redirect(url_for('userWelcome'))
        return render_template('register.html')


        
@app.route('/userWelcomePage',methods=['GET','POST'])
def userWelcome():

	if bool(session) != False:
		return render_template('input.html')
	for entry in request.form:
		print entry
		print request.form[entry]
	try:
		if request.form['submitType'] == "Sign In": #detects a sign in request
			username = request.form['username']
			password = hashlib.md5(request.form['password'].encode()).hexdigest()
			if (database.isMatchUserAndPass(username,password)==True):	#check if user login is correct
				session['user']=username
				return render_template('input.html')
			else:
				return render_template('accountErrorPage.html',linkString="/login",buttonString="username and/or password is incorrect, click here to try again")
				
	except:
		print "no post data"

		
	return render_template('accountErrorPage.html',linkString="/login",buttonString="something is very wrong, click here to login again")




if __name__ == '__main__':
	app.debug = True
	app.run()        #runs the app


