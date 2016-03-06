import os

# Disable Deprecation Warnings
import warnings
warnings.simplefilter('ignore', DeprecationWarning)

# Flask
from flask import Flask, render_template, request, redirect

import pandas as pd

# Sci-kit learn libraries for Logistic Regression
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib

import csv
# Pymongo Libraries for MongoDB
#import pymongo
#from pymongo import MongoClient

# Database specification
#MONGO_URL = os.environ.get('MONGOHQ_URL')
#client = MongoClient(MONGO_URL)

# Specify MongoDB Database and Collection
#db = client.jarvis
#collection = db.data

# Initialize Flask
app =Flask(__name__)

data_log = 'datasets/data.csv'

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/dump",methods=['GET'])
def dump():
	#tups = collection.find()
    csvfile = open(data_log, 'rb')
    tups = csv.DictReader(csvfile)
    return render_template('index.html', tups=tups)

@app.route("/insert", methods=['GET'])
def post():		
    out_file = open(data_log,'a+')																													
    '''
    tup = 	{
	    		"light":request.args['light'],
	    		"motion":request.args['motion'],
	    		"temprature":request.args['temprature'], 
	    		"humidity":request.args['humidity'],
	    		"time":request.args['time'],
	    		"bulb1":request.args['bulb1'],
	    		"bulb2":request.args['bulb2'],
	    		"fan1":request.args['fan1']
    		}
    '''

    #tup_id = collection.insert(tup)
    out_file.write('\n'+request.args['light'] + ','
    			+ request.args['motion'] + ','
	    		+ request.args['temprature'] + ','
	    		+ request.args['humidity'] + ','
	    		+ request.args['time'] + ','
	    		+ request.args['bulb1'] + ','
	    		+ request.args['bulb2'] + ','
	    		+ request.args['fan1'])
    out_file.close()
    return '1'


@app.route("/predict", methods=['GET'])
def predict():
	# Bulding Features list
	if request.args['device'] == 'bulb1' or request.args['device'] == 'bulb2' :
		features_input = [
	    		float(request.args['light']),
	    		float(request.args['time']),
	    		float(request.args['motion'])
    		]
	elif request.args['device'] == 'fan1' :
		features_input = [
	    		float(request.args['temprature']),
	    		float(request.args['humidity']),
	    		float(request.args['motion'])
    		]
  	#	Prediction using Model
  	_model = joblib.load('models/' + request.args['device'] + '.pkl')
  	target_predicted = _model.predict(features_input)
  	return str(target_predicted) 


@app.route("/generate", methods=['GET'])
def generate():
	data = pd.read_csv(data_log)

	# setting target value
	_bulb1 = data['bulb1']
	target = _bulb1.values

	# setting features for prediction
	numerical_features = data[['light', 'time', 'motion']]

	# converting into numpy arrays
	features_array = numerical_features.values

	# performing logistic regression,creating model
	logreg = LogisticRegression(C=1)
	logreg.fit(features_array, target)

	# dump generated model to file
	joblib.dump(logreg, 'models/' +'bulb1.pkl', compress=3)

	# Generate Model for Bulb2
	_bulb2 = data['bulb2']
	target = _bulb2.values
	numerical_features = data[['light', 'time', 'motion']]
	features_array = numerical_features.values

	logreg = LogisticRegression(C=1)
	logreg.fit(features_array, target)
	joblib.dump(logreg, 'models/' +'bulb2.pkl', compress=3)

	# Generate Model for Fan1
	_fan1 = data['fan1']
	target = _fan1.values
	numerical_features = data[['temprature', 'humidity', 'motion']]
	features_array = numerical_features.values

	logreg = LogisticRegression(C=1)
	logreg.fit(features_array, target)
	joblib.dump(logreg, 'models/' +'fan1.pkl', compress=3)

	return 'Models Generated'


if __name__ == "__main__":
	app.debug = True
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
