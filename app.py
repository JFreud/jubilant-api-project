from flask import Flask

app = Flask(__name__)

@app.route('/')
def root():
	return "what"

if __name__ == '__main__':
	app.debug = True
	app.run()        #runs the app

print "what"
