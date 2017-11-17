from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

@app.route('/')
def root():
	return render_template('home.html')

if __name__ == '__main__':
	app.debug = True
	app.run()        #runs the app

print "what"
