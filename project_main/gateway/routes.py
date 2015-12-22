from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify, Response
from sqlalchemy.sql import func
import urllib
import logging
import json
import boto3
import sys
import os.path
from pymongo import MongoClient
import hashlib
import time
import simplejson as json

sys.path.append(os.path.abspath(__file__ + '../../..'))
import mongo_credentials
mongo_url = 'mongodb://%s:%s@ds033915.mongolab.com:33915/project2' % (mongo_credentials.DB_USERNAME, mongo_credentials.DB_PASSWORD)
mongo = MongoClient(mongo_url)
response_queue_url = {}  # map from client_id(which is also the id of response queue) to queueUrl
response_cache = {}
sqs = boto3.client('sqs')
app = Flask(__name__)
queue_finance_name = 'finance'
queue_k12_name = 'k12'
db = mongo.get_default_database()
response_queues = db.response_queues

def create_request_queues():
    queue_finance = sqs.create_queue(QueueName = queue_finance_name)
    queue_k12 = sqs.create_queue(QueueName = queue_k12_name)

def delete_request_queues():
    response = sqs.delete_queue(QueueUrl = 'https://queue.amazonaws.com/031864143155/' + queue_finance_name)
    response = sqs.delete_queue(QueueUrl = 'https://queue.amazonaws.com/031864143155/' + queue_k12_name)

def create_response_queue(client_id):
    queue = sqs.create_queue(QueueName = client_id)
    try:
        sqs.add_permission(QueueUrl = queue['QueueUrl'], Label = 'AllOp', AWSAccountIds = ['559115960312'], Actions = ['*'])
    except Error as e:
        print e
    response_queues.insert_one({'client_id': client_id, 'url': queue['QueueUrl']})
    return queue['QueueUrl']

def create_request_id():
    hash = hashlib.sha1()
    hash.update(str(time.time()))
    return hash.hexdigest()

def get_response_queue_url(client_id):
    queue_info = response_queues.find_one({'client_id': client_id})
    url = ''
    if queue_info:
        url =  queue_info['url']
    else:
        url = create_response_queue(client_id)
    return url

def send_to_request_queue(qName, op, response_queue_url, body, service_url):
    request_id = create_request_id()
    queue = sqs.get_queue_url(QueueName = qName)
    response = sqs.send_message(QueueUrl = queue['QueueUrl'], MessageBody = 'boto3', MessageAttributes = {
            'op': {
                'StringValue': op,
                'DataType': 'String'
            },
            'response_queue_url': {
                'StringValue': response_queue_url,
                'DataType': 'String'
            },
            'request_id': {
                'StringValue': request_id,
                'DataType': 'String'
            },
            'body': {
                'StringValue': body,
                'DataType': 'String'
            },
            'service_url': {
                'StringValue': service_url,
                'DataType': 'String'
            }
        })
    return response

def init():
    print 'init'
    #create_request_queues()
    queue_finance = sqs.get_queue_url(QueueName = queue_finance_name)
    queue_k12 = sqs.get_queue_url(QueueName = queue_k12_name)
    print queue_finance['QueueUrl']
    print queue_k12['QueueUrl']

### put the finance microservice request into corresponding sqs
@app.route('/public/finance', methods = ['GET'])
def get_finance_info():
    client_id = request.headers.get('client_id')
    url = get_response_queue_url(client_id)
    response = send_to_request_queue(queue_finance_name, 'GET', url, 'None', '/private/finance')
    return Response('{"_status": "SUCCESS", "_success": {"message":' + json.dumps(response) + ', "code": 200}', mimetype='application/json', status=200)

@app.route('/public/finance/<studentid>', methods = ['GET'])
def get_finance_info_by_studentid(studentid):
    client_id = request.headers.get('client_id')
    url = get_response_queue_url(client_id)
    response = send_to_request_queue(queue_finance_name, 'GET', url, 'None', '/private/finance/' + studentid)
    return Response('{"_status": "SUCCESS", "_success": {"message":' + json.dumps(response) + ', "code": 200}', mimetype='application/json', status=200)


@app.route("/public/finance", methods = ['POST'])
def post_finance_info():
    client_id = request.headers.get('client_id')
    url = get_response_queue_url(client_id)
    content = request.get_json(force = True)
    str_json = json.dumps(content)
    response = send_to_request_queue(queue_finance_name, 'POST', url, str_json, '/private/finance')
    return Response('{"_status": "SUCCESS", "_success": {"message":' + json.dumps(response) + ', "code": 200}', mimetype='application/json', status=200)

@app.route("/public/finance/<studentid>", methods = ['PUT'])
def update_finance_info(studentid):
    client_id = request.headers.get('client_id')
    url = get_response_queue_url(client_id)
    content = request.get_json(force = True)
    str_json = json.dumps(content)
    response = send_to_request_queue(queue_finance_name, 'POST', url, str_json, '/private/finance/' + studentid)
    return Response('{"_status": "SUCCESS", "_success": {"message":' + json.dumps(response) + ', "code": 200}', mimetype='application/json', status=200)

@app.route('/public/finance', methods=['DELETE'])
def delete_finance_info():
    client_id = request.headers.get('client_id')
    url = get_response_queue_url(client_id)
    response = send_to_request_queue(queue_finance_name, 'DELETE', url, 'None', '/private/finance')
    return Response('{"_status": "SUCCESS", "_success": {"message":' + json.dumps(response) + ', "code": 200}', mimetype='application/json', status=200)

@app.route('/public/finance/<studentid>', methods=['DELETE'])
def delete_finance_info_by_studentid(studentid):
    client_id = request.headers.get('client_id')
    url = get_response_queue_url(client_id)
    response = send_to_request_queue(queue_k12_name, 'DELETE', url, 'None', '/private/finance/studentid/' + studentid)
    return Response('{"_status": "SUCCESS", "_success": {"message":' + json.dumps(response) + ', "code": 200}', mimetype='application/json', status=200)

### put the k12 microservice request into corresponding sqs
@app.route('/public/k12', methods = ['GET'])
def get_k12_info():
    client_id = request.headers.get('client_id')
    url = get_response_queue_url(client_id)
    response = send_to_request_queue(queue_k12_name, 'GET', url, 'None', '/private/k12')
    print response
    return Response('{"_status": "SUCCESS", "_success": {"message":' + json.dumps(response) + ', "code": 200}', mimetype='application/json', status=200)

@app.route('/public/k12/studentid/<studentid>', methods = ['GET'])
def get_k12_info_by_studentid(studentid):
    client_id = request.headers.get('client_id')
    url = get_response_queue_url(client_id)
    response = send_to_request_queue(queue_k12_name, 'GET', url, 'None', '/private/k12/studentid/' + studentid)
    return Response('{"_status": "SUCCESS", "_success": {"message":' + json.dumps(response) + ', "code": 200}', mimetype='application/json', status=200)

@app.route('/public/k12/studentid/<studentid>/schoolid/<schoolid>', methods=['GET'])
def get_k12_info_by_studentid_schoolid(studentid, schoolid):
    client_id = request.headers.get('client_id')
    url = get_response_queue_url(client_id)
    response = send_to_request_queue(queue_k12_name, 'GET', url, 'None', '/private/k12/studentid/' + studentid + '/schoolid/' + schoolid)
    return Response('{"_status": "SUCCESS", "_success": {"message":' + json.dumps(response) + ', "code": 200}', mimetype='application/json', status=200)

@app.route('/public/k12', methods = ['POST'])
def post_k12_info():
    client_id = request.headers.get('client_id')
    url = get_response_queue_url(client_id)
    content = request.get_json(force = True)
    str_json = json.dumps(content)
    response = send_to_request_queue(queue_k12_name, 'POST', url, str_json, '/private/k12')
    return Response('{"_status": "SUCCESS", "_success": {"message":' + json.dumps(response) + ', "code": 200}', mimetype='application/json', status=200)

@app.route('/public/k12/studentid/<studentid>/schoolid/<schoolid>', methods=['PUT'])
def update_k12_info(studentid, schoolid):
    client_id = request.headers.get('client_id')
    url = get_response_queue_url(client_id)
    content = request.get_json(force = True)
    str_json = json.dumps(content)
    response = send_to_request_queue(queue_k12_name, 'PUT', url, str_json, '/private/k12/studentid/' + studentid + '/schoolid/' + schoolid)
    return Response('{"_status": "SUCCESS", "_success": {"message":' + json.dumps(response) + ', "code": 200}', mimetype='application/json', status=200)

@app.route('/public/k12', methods=['DELETE'])
def delete_k12_info():
    client_id = request.headers.get('client_id')
    url = get_response_queue_url(client_id)
    response = send_to_request_queue(queue_k12_name, 'DELETE', url, 'None', '/private/k12')
    return Response('{"_status": "SUCCESS", "_success": {"message":' + json.dumps(response) + ', "code": 200}', mimetype='application/json', status=200)

@app.route('/public/k12/studentid/<studentid>/schoolid/<schoolid>', methods=['DELETE'])
def delete_k12_info_by_studentid_schoolid(studentid, schoolid):
    client_id = request.headers.get('client_id')
    url = get_response_queue_url(client_id)
    response = send_to_request_queue(queue_k12_name, 'DELETE', url, 'None', '/private/k12/studentid/' + studentid + '/schoolid/' + schoolid)
    return Response('{"_status": "SUCCESS", "_success": {"message":' + json.dumps(response) + ', "code": 200}', mimetype='application/json', status=200)

@app.route('/', methods=['GET'])
def list_api():
    output = []
    html = "<!DOCTYPE html><html><head><title>Page Title</title></head><body><p>%s</p></body></html>"
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("<b>%s</b><br>%s<br>%s<br>"%(rule.endpoint, methods, url))
        output.append(line)

    return html%"</p><p>".join(sorted(output))

""" get queue info from database and update response_queue_url """
@app.route('/response_queue_url', methods=['GET'])
def get_response_queue_url_from_db():
    mongo_res = mongo.project2.response_queues.find()
    for res in mongo_res:
        url = res.get("url")
        client_id = res.get("client_id")
        if url and client_id:
            response_queue_url[client_id] = url
    return Response("update response_queue_url", status=200)

@app.route('/response', methods=['GET'])
def get_response():
    args = request.args
    client_id = str(args.get("client_id", ""))  # client_id is also the id of response queue
    request_id = str(args.get("request_id", ""))  # if request_id is None, then return the first one in queue
    if not client_id:
        return Response("client_id is empty", status=400)

    # queueUrl = "https://sqs.us-east-1.amazonaws.com/308367428478/test"
    queueUrl = response_queue_url.get(client_id)
    if not queueUrl:
        return Response("This client_id has not been registered yet", status=400)

    this_cache = response_cache.setdefault(client_id, {})
    if request_id:  # iff request_id is not empty
        # 1. if it's in cache
        if request_id in this_cache:
            logging.info("read from cache")
            return Response(this_cache[request_id], status=200)
        
        # 2. else if it's in db
        mongo_res = mongo.project2.response_cache.find_one(
            {
                "client_id": client_id,
                "request_id": request_id
            }
        )
        if mongo_res and mongo_res.get("result"):
            response_cache[client_id][request_id] = mongo_res["result"]  # add it to cache
            logging.info("read from mongo")
            return Response(mongo_res["result"], status=200)
    
    # 3. else retrieve from sqs and put into cache and db
    sqs_response = sqs.receive_message(QueueUrl=queueUrl, MessageAttributeNames=["All"])
    message = sqs_response.get("Messages", list())
    while message:
        try:
            message = message[0]  # only one message in list
            receiptHandle = message["ReceiptHandle"]
            message_attributes = message["MessageAttributes"]
            this_request_id = str(message_attributes["request_id"]["StringValue"])
            result = message_attributes["result"]["StringValue"]
            if not (receiptHandle and this_request_id and result):
                logging.error("receiptHandle: ", receiptHandle)
                logging.error("this_request_id: ", this_request_id)
                logging.error("result: ", result)
                raise Exception('Invalid response')
        except Exception, e:
            logging.error("message: ", str(message))
            return Response("The response is not valid", status=500)
        response_cache[client_id][this_request_id] = result  # add it to cache
        write_response_to_db(client_id, this_request_id, result)  # add it to db
        # sqs.delete_message(QueueUrl=queueUrl, ReceiptHandle=receiptHandle)
        logging.info("read request_id %s from sqs"%this_request_id)
        if not request_id or request_id==this_request_id:  # if match or does not provide request_id, return
            return Response(result, status=200)
        else:  # else keep polling
            sqs_response = sqs.receive_message(QueueUrl=queueUrl, MessageAttributeNames=["All"])
            message = sqs_response.get("Messages", list())

    # exit loop means message is empty
    logging.info("No result")
    return Response("There no results for the request at this time. Please try again later", status=404)

def write_response_to_db(client_id, request_id, result):
    mongo.project2.response_cache.insert_one(
        {
            "client_id": client_id,
            "request_id": request_id,
            "result": result
        }
    )


if __name__ == '__main__':
    init()
    app.run(host = '127.0.0.1', port = 3000)
