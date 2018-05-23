import requests 
import json
import os
from flask import Flask
from flask import request
from flask import make_response
import sqlite3
app = Flask(__name__)

@app.route('/webhook',methods=['POST'])

def webhook():
	req = request.get_json(silent = True , force = True)
	print ("Request: ")
	print (json.dumps(req,indent = 4))
	res = collectFromFirebase(req)
	res = json.dumps(res , indent = 4 )
	print (res)
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r

def collectFromFirebase(req):
	
	result = req.get("queryResult")
	query = result.get("fulfillmentText")
	parameters = result.get("parameters")
	student_name = parameters.get("given-name")
	student_name = student_name.capitalize()
	query = result.get("fulfillmentText")
	print (query)
	conn = sqlite3.connect('student_db')
	c = conn.cursor()
	c.execute(query)
	data = list(c.fetchone())
	output = "Mr %s is from %s currently pursuing %s  . His 10 th percentage is %s " %(student_name , str(data[5]) , str(data[3] ) , str(data[6]) )
	speech = "This is from my sys buddy"
	return {
	"fulfillmentText": output,
	}


if __name__ == '__main__': 
	port = int(os.getenv('PORT',8000))
	print ("Starting app on port %d" %(port) )
	app.run(debug = True , port = port , host = '0.0.0.0')









 
