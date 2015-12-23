from eve import Eve
from flask import Response, request
from pymongo import MongoClient
import requests, json, sys



#####################
# Eve Configuration #
#####################
# Schema
schema = {
    "student_id": {
        "type": "string",
        "minlength": 6,
        "maxlength": 6,
        "required": True,
        "unique": True
    },
    "course_list": {
        "type": "list"
    },
    "tuition": {
    	"type": "float",
    	"min": 0,
    	"default": 0
    }
}

# Settings
settings = {
	# Use db hosted on MongoLab
	'MONGO_HOST': 'ds033915.mongolab.com',
	'MONGO_PORT': 33915,
	'MONGO_USERNAME': 'admin',
	'MONGO_PASSWORD': 'admin',
	'MONGO_DBNAME': 'project2',

	# URL prefix
	'URL_PREFIX': 'private',

	# Data schema
	'DOMAIN': {
		'finance': {
			'additional_lookup': {
				 'url': 'regex("[a-z]{2}[0-9]{4}$")', #("[\w]+")',
				 'field': 'student_id',
			 },
			'schema': schema
		}
	},
	
	'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],
	'ITEM_METHODS': ['GET', 'PUT', 'DELETE']
}

# App Initialization
app = Eve(settings=settings)


# Main
if __name__ == '__main__':
	if len(sys.argv) == 3:
		app.run(host = sys.argv[1], port = int(sys.argv[2]))
	else:
		app.run()