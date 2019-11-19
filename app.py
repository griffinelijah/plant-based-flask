from flask import Flask

DEBUG = True
PORT = 8000

#initialize instance of flask clasas
app = Flask(__name__)

#default route
@app.route('/')
def hello():
	return 'Hello'



if __name__ == '__main__':
	app.run(debug=DEBUG, port=PORT)


