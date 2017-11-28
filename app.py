from flask import Flask, render_template, request, session, redirect, url_for, flash
from utils import database, api
import os, sqlite3, hashlib, requests, json

app = Flask(__name__)
app.secret_key="PlaceHolderKey"
database.createTable()


key_obj = open("keys.txt")
keys = key_obj.readline().replace("\n", "").split(",")
key_obj.close()
#print keys
LASTFM_KEY = keys[0]
MUSIXMATCH_KEY = keys[1]
WATSON_KEY = keys[2]
YOUTUBE_KEY = keys[3]


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
    url = "http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user=" + requestedUser + "&api_key=%s&format=json" % (MUSIXMATCH_KEY)
    lastfm = requests.get(url)
    dL = json.loads(lastfm.text)
    try:
        if dL["message"] == "User not found":
            flash("last fm user does not exist")
            return redirect(url_for("userWelcome"))
    except KeyError:#message is only in dL if user not found
        pass
    #print "ENTERED OUTPUT\n"
    print "\nChecking this user: %s\n" % (requestedUser)
    print database.isStringInTable(session['user'], requestedUser, "username", "lastFMuser", "userSongs")
    print "====="
    print request.form
    if not database.isStringInTable(session['user'], requestedUser, "username", "lastFMuser", "userSongs") or 'update' in request.form:
        requestedUser =  str(request.form['lastfm']).strip('[]')
        #print "API DICT BUILT:"
        song_dict = api.buildDictForDB(requestedUser)
        #print "\n======SONG DICT: ==========\n"
        #print song_dict
        print "NEW"
        if (not song_dict):
            print "SHOULD REDIRECT:\n"
            flash("User has no loved songs")
            return redirect(url_for("userWelcome"))
        database.insertIntoUserSongs(session['user'],requestedUser,song_dict)
    songList=database.songsWithMatchingTone(session['user'],requestedUser,request.form['feeling'])
    print "HERE THE SONGLIST"
    print songList
    if not songList:
        flash("User does not love this tone")
        return redirect(url_for("userWelcome"))
    return render_template('output.html',songList=songList)

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
    print "USERNAME"
    print session['user']
    print session
    username = session.pop('user')
    msg = "Successfully logged out " + username
    flash(msg)
    return redirect(url_for('login'))

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
