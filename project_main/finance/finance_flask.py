from flask import Flask, request, Response
from eve.io.mongo import Validator
from pymongo import MongoClient
import finance_flask as ff
import urllib2, json, requests, boto3
import sys, subprocess, signal, time
import os
import re



#############
# Variables #
#############
global eve_process
global args
global sqs_client
app = Flask(__name__)
mongo_url = 'mongodb://admin:admin@ds033915.mongolab.com:33915/project2'
eve_base_url = ''
schema_course = {
	"course_id": {
        "type": "integer",
        'min': 10000,
        'max': 99999,
        "required": True
    },
    "credit": {
    	"type": "integer",
        'min': 0,
        'max': 5,
        "required": True
    },
    "unit_price": {
    	"type": "float",
        'min': 0,
        "required": True
    }
}

########################
# Custom Error Handler #
########################
class MongoDbUnavailable(Exception):
	pass

class StudentNotExists(Exception):
	pass

class EveUnavailable(Exception):
	pass

@app.errorhandler(MongoDbUnavailable)
def mongodb_failed_to_connect(error):
	# return Response('{"_status": "ERR", "_error": {"message": "Failed to connect to mongodb", "code": 500}}', mimetype='application/json', status=500)
	return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response.content)

@app.errorhandler(StudentNotExists)
def mongodb_configuration_unavailable(error):
	# return Response('{"_status": "ERR", "_error": {"message": "Student with specified uni does not have record", "code": 404}}', mimetype='application/json', status=404)
	return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response.content)

@app.errorhandler(EveUnavailable)
def mongodb_failed_to_connect(error):
	# return Response('{"_status": "ERR", "_error": {"message": "Failed to connect to eve service", "code": 500}}', mimetype='application/json', status=500)
	return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response.content)

@app.errorhandler(Exception)
def unexpected_failure(error):
	template = "An exception of type {0} occured. Arguments:\n{1!r}"
	message = template.format(type(error).__name__, error.args)
	print message
	# return Response('{"_status": "ERR", "_error": {"message": "Unexpected failure", "code": 500}}', mimetype='application/json', status=500)
	return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response.content)



###############
# API Mapping #
###############
@app.route("/private/finance", methods = ['GET'])
def finance_read_all():
	print 'Recieved GET finance request'
	try:
		response = requests.get(eve_base_url)
		# return Response(response.content, mimetype='application/json', status=response.status_code)
		return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response.content)
	except Exception as e:
		if type(e).__name__ == 'ConnectionError':
			print 'Error: Cannot connect to eve'
			raise EveUnavailable
		else:
			print 'Error: %s when read finance from eve' % (type(e).__name__)
			raise e

@app.route("/private/finance", methods = ['POST'])
def finance_create_student():
	print 'Recieved POST finance request'
	try:
		data = request.get_json(force = True)
		# Calculate and update tuition
		tuition = 0
		if 'tuition' in data:
			tuition = data['tuition']
		if 'course_list' in data:
			for course in data['course_list']:
				tuition += course['credit'] * course['unit_price']
		data.update({'tuition': tuition})

		# Forward request to eve
		headers = request.headers
		response = requests.post(eve_base_url, data = json.dumps(data), headers = headers)
		# return Response(response.content, mimetype='application/json', status=response.status_code)
		return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response.content)
	except Exception as e:
		if type(e).__name__ == 'ConnectionError':
			print 'Error: Cannot connect to eve'
			raise EveUnavailable
		else:
			print 'Error: %s when add student finance info to eve' % (type(e).__name__)
			raise e

@app.route("/private/finance", methods = ['DELETE'])
def finance_delete_all():
	print 'Recieved DELETE finance request'
	try:
		response = requests.delete(eve_base_url)
		# return Response(response.content, mimetype='application/json', status=response.status_code)
		return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response.content)
	except Exception as e:
		if type(e).__name__ == 'ConnectionError':
			print 'Error: Cannot connect to eve'
			raise EveUnavailable
		else:
			print 'Error: %s when read finance from eve' % (type(e).__name__)
			raise e

@app.route("/private/finance/<student_id>", methods = ['GET'])
def finance_read_student(student_id):
	print 'Recieved GET student finance request'
	try:
		response = requests.get(eve_base_url + '/' + student_id)
		# return Response(response.content, mimetype='application/json', status=response.status_code)
		return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response.content)
	except Exception as e:
		if type(e).__name__ == 'ConnectionError':
			print 'Error: Cannot connect to eve'
			raise EveUnavailable
		else:
			print 'Error: %s when read student finance from eve' % (type(e).__name__)
			raise e

@app.route("/private/finance/<student_id>", methods = ['PUT'])
def finance_update_student(student_id):
	print 'Recieved PUT student finance request'
	try:
		response = requests.get(eve_base_url + '/' + student_id)
		response_content = json.loads(response.content)
		oid = response_content['_id']
		data = request.get_json(force = True)

		# Calculate and update tuition
		tuition = 0
		if 'tuition' in data:
			tuition = data['tuition']
		if 'course_list' in data:
			for course in data['course_list']:
				tuition += course['credit'] * course['unit_price']
		data.update({'tuition': tuition})

		# Forward request to eve
		headers = request.headers
		response = requests.put(eve_base_url + '/' + oid, data = json.dumps(data), headers = headers)
		# return Response(response.content, mimetype='application/json', status=response.status_code)
		print "nani"
		return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response.content)
	except Exception as e:
		if type(e).__name__ == 'ConnectionError':
			print 'Error: Cannot connect to eve'
			raise EveUnavailable
		else:
			print 'Error: %s when update student finance from eve' % (type(e).__name__)
			raise e

@app.route('/private/finance/<student_id>', methods=['DELETE'])
def finance_delete_student(student_id):
	print 'Recieved DELETE student finance request'
	try:
		response = requests.get(eve_base_url + '/' + student_id)
		response_content = json.loads(response.content)
		oid = response_content['_id']
		headers = request.headers
		response = requests.delete(eve_base_url + '/' + oid, headers = headers)
		# return Response(response.content, mimetype='application/json', status=response.status_code)
		return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response.content)
	except Exception as e:
		if type(e).__name__ == 'ConnectionError':
			print 'Error: Cannot connect to eve'
			raise EveUnavailable
		else:
			print 'Error: %s when delete student finance from eve' % (type(e).__name__)
			raise e

@app.route("/private/finance/<student_id>/courses", methods = ['POST'])
def add_to_course_list(student_id):
	print 'Recieved POST courses request'
	try:
		courses_to_update = request.get_json(force = True)
		print 'courses_to_update(type=%s) = %s' % (type(courses_to_update).__name__, courses_to_update)
		# If data is not array, do not process
		if type(courses_to_update).__name__ != 'list':
			# return Response('{"_status": "ERR", "_error": {"message": "Data must be provided as list", "code": 400}}', mimetype='application/json', status=400)
			response_msg = '{"_status": "ERR", "_error": {"message": "Data must be provided as list", "code": 400}}'
			return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), json.loads(response_msg))
	
		# Get current course list
		client = MongoClient(mongo_url)
		db = client.project2
		cursor = db.finance.find(
			{
				"student_id": student_id
			}
		)
		if cursor.count() < 1:
			print 'Abort: Student not exists'
			raise StudentNotExists
		course_id_list = []
		if 'course_list' in cursor[0]:
			for course in cursor[0]['course_list']:
				course_id_list.append(course['course_id']);
		print 'course_id_list = %s' % (course_id_list)
		

		# Process only new courses
		count_new_course = 0
		count_old_course = 0
		for course in courses_to_update:
			print "course = %s" % (course)
			# Validate course data format
			v = Validator(schema_course)
			if not v.validate(course):
				# return Response('{"_status": "ERR", "_error": {"message": "Invalid data format of course; Please check API", "code": 400}}', mimetype='application/json', status=400)
				response_msg = '{"_status": "ERR", "_error": {"message": "Invalid data format of course; Please check API", "code": 400}}'
				return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), json.loads(response_msg))
			# Process only new courses
			if course['course_id'] not in course_id_list:
				print "\tadd"
				result = db.finance.update(
					{
						"student_id": student_id
					},
				    {
				        "$push": {
				            "course_list": course
				        },
				        "$currentDate": {"lastModified": True}
				    }
				)
				count_new_course += 1
			else:
				count_old_course += 1
		client.close()
		# return Response('{"_status": "SUCCESS", "_success": {"message": "'+str(count_new_course)+' course(s) added, '+str(count_old_course)+' course(s) already exist(s)", "code": 200}}', mimetype='application/json', status=200)
		response_msg = '{"_status": "SUCCESS", "_success": {"message": "'+str(count_new_course)+' course(s) added, '+str(count_old_course)+' course(s) already exist(s)", "code": 200}}'
		return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), json.loads(response_msg))
	except Exception as e:
		if type(e).__name__ == 'ConnectionError':
			print 'Error: Cannot connect to mongodb'
			raise MongoDbUnavailable
		else:
			print 'Error: %s when adding course for %s' % (type(e).__name__, student_id)
			raise e

@app.route("/private/finance/<student_id>/courses", methods = ['PUT'])
def update_course_list(student_id):
	print 'Recieved PUT courses request'
	try:
		courses_to_update = request.get_json(force = True)
		print 'courses_to_update(type=%s) = %s' % (type(courses_to_update).__name__, courses_to_update)
		# If data is not array, do not process
		if type(courses_to_update).__name__ != 'list':
			# return Response('{"_status": "ERR", "_error": {"message": "Data must be provided as list", "code": 400}}', mimetype='application/json', status=400)
			response_msg = '{"_status": "ERR", "_error": {"message": "Data must be provided as list", "code": 400}}'
			return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), json.loads(response_msg))
		# Get current course list
		client = MongoClient(mongo_url)
		db = client.project2
		cursor = db.finance.find(
			{
				"student_id": student_id
			}
		)
		if cursor.count() < 1:
			print 'Abort: Student not exists'
			raise StudentNotExists
		course_id_list = []
		print
		if 'course_list' in cursor[0]:
			for course in cursor[0]['course_list']:
				course_id_list.append(course['course_id']);
		print 'course_id_list = %s' % (course_id_list)
		

		# Process only existing courses
		count_new_course = 0
		count_old_course = 0
		for course in courses_to_update:
			print "course = %s" % (course)
			# Validate course data format
			v = Validator(schema_course)
			if not v.validate(course):
				# return Response('{"_status": "ERR", "_error": {"message": "Invalid data format of course; Please check API", "code": 400}}', mimetype='application/json', status=400)
				response_msg = '{"_status": "ERR", "_error": {"message": "Invalid data format of course; Please check API", "code": 400}}'
				return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), json.loads(response_msg))
			# Process only existing courses
			if course['course_id'] in course_id_list:
				print "\tupdate"
				result = db.finance.update(
					{
						"student_id": student_id,
						"course_list.course_id": course['course_id']
					},
				    {
				        "$set": {
				        	"course_list.$": course
				        },
				        "$currentDate": {"lastModified": True}
				    }
				)
				count_old_course += 1
			else:
				count_new_course += 1
		client.close()
		# return Response('{"_status": "SUCCESS", "_success": {"message": "'+str(count_old_course)+' course(s) updated, '+str(count_new_course)+' course(s) do(es) not exist", "code": 200}}', mimetype='application/json', status=200)
		response_msg = '{"_status": "SUCCESS", "_success": {"message": "'+str(count_old_course)+' course(s) updated, '+str(count_new_course)+' course(s) do(es) not exist", "code": 200}}'
		return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), json.loads(response_msg))
	except Exception as e:
		if type(e).__name__ == 'ConnectionError':
			print 'Error: Cannot connect to mongodb'
			raise MongoDbUnavailable
		else:
			print 'Error: %s when adding course for %s' % (type(e).__name__, student_id)
			raise e

@app.route("/private/finance/<student_id>/courses", methods = ['DELETE'])
def delete_from_course_list(student_id):
	print 'Recieved DELETE courses request'
	try:
		courses_to_update = request.get_json(force = True)
		print 'courses_to_update(type=%s) = %s' % (type(courses_to_update).__name__, courses_to_update)
		# If data is not array, do not process
		if type(courses_to_update).__name__ != 'list':
			# return Response('{"_status": "ERR", "_error": {"message": "Data must be provided as list", "code": 400}}', mimetype='application/json', status=400)
			response_msg = '{"_status": "ERR", "_error": {"message": "Data must be provided as list", "code": 400}}'
			return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), json.loads(response_msg))
		# Get current course list
		client = MongoClient(mongo_url)
		db = client.project2
		cursor = db.finance.find(
			{
				"student_id": student_id
			}
		)
		if cursor.count() < 1:
			print 'Abort: Student not exists'
			raise StudentNotExists
		course_id_list = []
		print
		if 'course_list' in cursor[0]:
			for course in cursor[0]['course_list']:
				course_id_list.append(course['course_id']);
		print 'course_id_list = %s' % (course_id_list)
		

		# Process only existing courses
		count_new_course = 0
		count_old_course = 0
		for course_id in courses_to_update:
			print "course_id = %s" % (course_id)
			# Process only existing courses
			if course_id in course_id_list:
				print "\tremove"
				result = db.finance.update(
					{
						"student_id": student_id,
						"course_list.course_id": course_id
					},
				    {
				        "$unset": {
				        	"course_list.$": ""
				        },
				        "$currentDate": {"lastModified": True}
				    }
				)
				count_old_course += 1
			else:
				count_new_course += 1
		client.close()
		# return Response('{"_status": "SUCCESS", "_success": {"message": "'+str(count_old_course)+' course(s) updated, '+str(count_new_course)+' course(s) do(es) not exist", "code": 200}}', mimetype='application/json', status=200)
		response_msg = '{"_status": "SUCCESS", "_success": {"message": "'+str(count_old_course)+' course(s) removed, '+str(count_new_course)+' course(s) do(es) not exist", "code": 200}}'
		return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), json.loads(response_msg))
	except Exception as e:
		if type(e).__name__ == 'ConnectionError':
			print 'Error: Cannot connect to mongodb'
			raise MongoDbUnavailable
		else:
			print 'Error: %s when adding course for %s' % (type(e).__name__, student_id)
			raise e



def send_to_response_queue(resp_queue_url, req_id, json_object):
    print(resp_queue_url)
    response = sqs_client.send_message(QueueUrl = resp_queue_url, MessageBody = 'boto3', MessageAttributes = {
        'ReturnValue': {
            'StringValue': json.dumps(json_object),
            'DataType': 'String'
        },
        'RequestID':{
            'StringValue':req_id,
            'DataType': 'String'
        }
    })
    return response['MD5OfMessageBody']

def start_eve_process(args):
	print "starting finance eve process..."
	ff.eve_process = subprocess.Popen(args)

def stop_eve_process(args):
	print "stopping finance eve process..."
	os.kill(ff.eve_process.pid, signal.SIGTERM)

if __name__ == "__main__":
		if(len(sys.argv) >= 3):
			sqs_client = boto3.client('sqs')

			host = sys.argv[1]
			eve_port = str((int(sys.argv[2]) + 10000))
			args = ['python', 'finance_eve.py', host, eve_port]
			start_eve_process(args)
			eve_base_url = 'http://' + host + ':' + eve_port + '/private/finance'
			app.run(host=host, port=int(sys.argv[2]))

