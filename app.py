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
    
@app.route('/input')
def input():
        return render_template('input.html')

@app.route('/output')
def output():
        return render_template('output.html')

@app.route('/login',methods = ['GET','POST'])
def login():
        if request.form['submitType'] == "Sign up": #detects a register request
            username = request.form['username']
            password = hashlib.md5(request.form['password'].encode()).hexdigest()
            database.insertIntoLoginTable(username,password)
        return render_template('login.html')

@app.route('/logout')
def logout():
        return null

@app.route('/register',methods=['GET','Post'])
def register():
        return render_template('register.html')
        





if __name__ == '__main__':
	app.debug = True
	app.run()        #runs the app


