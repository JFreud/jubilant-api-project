from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

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

@app.route('/login')
def login():
        return render_template('login.html')

@app.route('/logout')
def logout():
        return null

@app.route('/register')
def register():
        return render_template('register.html')
        





if __name__ == '__main__':
	app.debug = True
	app.run()        #runs the app


