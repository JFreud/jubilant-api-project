from flask import Flask, render_template, request, session, redirect, url_for, flash
from utils import database, api
import os, sqlite3, hashlib, requests

app = Flask(__name__)
app.secret_key="PlaceHolderKey"
database.createTable()


@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home')
def home():
        return render_template('home.html')




@app.route('/output',methods = ['GET','POST'])
def output():
		requestedUser =  str(request.form['lastfm']).strip('[]')
		#input new data if the user+lastfm combo doesn't already exist
		if (database.isStringInTableCol(session['user'],"userSongs","username")==False or database.isStringInTableCol(requestedUser,"userSongs","lastFMuser")==False):
			requestedUser =  str(request.form['lastfm']).strip('[]')
			database.insertIntoUserSongs(session['user'],requestedUser,api.buildDictForDB(requestedUser))
		return render_template('output.html',songList=database.songsWithMatchingTone(session['user'],requestedUser,request.form['feeling']))

@app.route('/makeaccount',methods = ['GET','POST'])
def makeaccount():
	username = request.form['username']
	password = hashlib.md5(request.form['password'].encode()).hexdigest()
	confirmPassword = hashlib.md5(request.form['confirmPassword'].encode()).hexdigest()

	#check if username already exists
	if (database.isStringInTableCol(username,'login','username')==True):
		"""return render_template('accountErrorPage.html',linkString='/register',buttonString='Username already exists, click here to go back')"""
		flash("Username already exists.")
		return redirect(url_for('register'))
		#check if passwords are the same
	elif(password != confirmPassword):
		"""return render_template('accountErrorPage.html',linkString='/register',buttonString='Passwords do not match, click here to try again')"""
		flash("Passwords do not match")
		return redirect(url_for('register'))
	#all seems good, add to DB
	else:
		database.insertIntoLoginTable(username,password)
		return render_template('login.html')


@app.route('/logout')
def logout():
        return null

@app.route('/login',methods=['GET','Post'])
def login():
	print session.has_key("user")
	if session.has_key("user") == False:
		return render_template('login.html')
	return redirect(url_for('userWelcome'))

@app.route('/register',methods=['GET','Post'])
def register():
	print bool(session)
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
			print session
			if (database.isMatchUserAndPass(username,password)==True):	#check if user login is correct
				print "wot"
				session['user']=username
				return render_template('input.html')
			elif (database.isStringInTableCol(username,'login','username') == False):
				flash("User does not exist.")
				return redirect(url_for('login'))
			else:
				flash("Wrong Password.")
				return redirect(url_for('login'))

	except:
		print bool(session)


	return render_template('accountErrorPage.html',linkString="/login",buttonString="something is very wrong, click here to login again")




if __name__ == '__main__':
	app.debug = True
	app.run()        #runs the app
