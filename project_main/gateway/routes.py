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

sys.path.append(os.path.abspath(__file__ + '../../..'))
import mongo_credentials

response_queue_address = {}  # map from client_id(which is also the id of response queue) to queueUrl
response_cache = {}
sqs = boto3.client('sqs')
app = Flask(__name__)
queue_finance_name = 'finance'
queue_k12_name = 'k12'

mongo_url = 'mongodb://%s:%s@ds033915.mongolab.com:33915/project2' % (mongo_credentials.DB_USERNAME, mongo_credentials.DB_PASSWORD)
client = MongoClient(mongo_url)
db = client.get_default_database()
response_queues = db.response_queues


def create_request_queues():
    queue_finance = sqs.create_queue(QueueName = queue_finance_name)
    queue_k12 = sqs.create_queue(QueueName = queue_k12_name)

def delete_request_queues():
    response = sqs.delete_queue(QueueUrl = 'https://queue.amazonaws.com/031864143155/' + queue_finance_name)
    response = sqs.delete_queue(QueueUrl = 'https://queue.amazonaws.com/031864143155/' + queue_k12_name)

def create_response_queue(client_id):
    queue = sqs.create_queue(QueueName = client_id)
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
    print 'get response queue url'
    print url
    return url

def init():
    print 'init'
    create_request_queues()
    queue_finance = sqs.get_queue_url(QueueName = queue_finance_name)
    queue_k12 = sqs.get_queue_url(QueueName = queue_k12_name)
    print queue_finance['QueueUrl']
    print queue_k12['QueueUrl']
    '''
    response = sqs.receive_message(QueueUrl = queue_finance['QueueUrl'], MessageAttributeNames=["All"], MaxNumberOfMessages = 10)
    print 'get message from finance queue'
    print response
    print 'print each request'
    for message in response['Messages']:
        print '....'
        print message['MessageAttributes']
    '''
    get_response_queue_address_from_db()
    get_response_cache_from_db()

### put the finance microservice request into corresponding sqs
@app.route('/public/finance', methods = ['GET'])
def get_finance_info():
    client_id = request.headers.get('client_id')
    request_id = create_request_id()
    url = get_response_queue_url(client_id)
    queue_finance = sqs.get_queue_url(QueueName = queue_finance_name)
    response = sqs.send_message(QueueUrl = queue_finance['QueueUrl'], MessageBody = 'boto3', MessageAttributes = {
            'op': {
                'StringValue': 'GET',
                'DataType': 'String'
            },
            'response_queue_url': {
                'StringValue': url,
                'DataType': 'String'
            },
            'request_id': {
                'StringValue': request_id,
                'DataType': 'String'
            },
            'resource_id': {
                'StringValue': 'ALL',
                'DataType': 'String'
            },
            'service_url': {
                'StringValue': '/private/finance',
                'DataType': 'String'
            }
        })
    print response
    return Response('{"_status": "SUCCESS", "_success": {"message": "Put the request into finance queue", "code": 200}}', mimetype='application/json', status=200)


@app.route('/public/finance/<studentid>', methods = ['GET'])
def get_finance_info_by_uni(studentid):
    client_id = request.headers.get('client_id')
    request_id = create_request_id()
    url = get_response_queue_url(client_id)
    queue_finance = sqs.get_queue_url(QueueName = queue_finance_name)
    response = sqs.send_message(QueueUrl = queue_finance['QueueUrl'], MessageBody = 'boto3', MessageAttributes = {
            'op': {
                'StringValue': 'GET',
                'DataType': 'String'
            },
            'response_queue_url': {
                'StringValue': url,
                'DataType': 'String'
            },
            'request_id': {
                'StringValue': request_id,
                'DataType': 'String'
            },
            'resource_id': {
                'StringValue': studentid,
                'DataType': 'String'
            },
            'service_url': {
                'StringValue': '/private/finance/' + studentid,
                'DataType': 'String'
            }
        })
    return Response('{"_status": "SUCCESS", "_success": {"message": "Put the request into finance queue", "code": 200}}', mimetype='application/json', status=200)


### put the k12 microservice request into corresponding sqs
@app.route('/public/k12', methods = ['GET'])
def get_k12_info():
    client_id = request.headers.get('client_id')
    request_id = create_request_id()
    url = get_response_queue_url(client_id)
    queue_k12 = sqs.get_queue_url(QueueName = queue_k12_name)
    try:
        response = sqs.send_message(QueueUrl = queue_k12['QueueUrl'], MessageBody = 'boto3', MessageAttributes = {
                'op': {
                    'StringValue': 'GET',
                    'DataType': 'String'
                },
                'response_queue_url': {
                    'StringValue': url,
                    'DataType': 'String'
                },
                'request_id': {
                    'StringValue': request_id,
                    'DataType': 'String'
                },
                'resource_id': {
                    'StringValue': 'ALL',
                    'DataType': 'String'
                },
                'service_url': {
                    'StringValue': '/private/k12',
                    'DataType': 'String'
                }
            })
    except Error as e:
        print e
    print 'response'
    print response
    return Response('{"_status": "SUCCESS", "_success": {"message": "Put the request into k12 queue", "code": 200}}', mimetype='application/json', status=200)

@app.route('/public/k12/studentid/<studentid>', methods = ['GET'])
def get_k12_info_by_studentid(studentid):
    client_id = request.headers.get('client_id')
    request_id = create_request_id()
    url = get_response_queue_url(client_id)
    queue_k12 = sqs.get_queue_url(QueueName = queue_k12_name)
    try:
        response = sqs.send_message(QueueUrl = queue_k12['QueueUrl'], MessageBody = 'boto3', MessageAttributes = {
                'op': {
                    'StringValue': 'GET',
                    'DataType': 'String'
                },
                'response_queue_url': {
                    'StringValue': url,
                    'DataType': 'String'
                },
                'request_id': {
                    'StringValue': request_id,
                    'DataType': 'String'
                },
                'resource_id': {
                    'StringValue': 'ALL',
                    'DataType': 'String'
                },
                'service_url': {
                    'StringValue': '/private/k12/studentid/' + studentid,
                    'DataType': 'String'
                }
            })
    except Error as e:
        print e
    print 'response'
    print response
    return Response('{"_status": "SUCCESS", "_success": {"message": "Put the request into k12 queue", "code": 200}}', mimetype='application/json', status=200)


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

""" get queue info from database and update response_queue_address """
@app.route('/response_queue_address', methods=['GET'])
def get_response_queue_address_from_db():
    pass

@app.route('/response', methods=['GET'])
def get_response():
    args = request.args
    client_id = args.get("client_id", "")  # client_id is also the id of response queue
    request_id = args.get("request_id", "")  # if request_id is None, then return the first one in queue
    this_cache = response_cache.setdefault(client_id, {})
    if request_id in this_cache:
        return Response(this_cache[request_id], mimetype='application/json', status=200)
    # else retrieve from sqs and put into cache and db
    queueUrl = ""
    for msg in sqs.receive_message(QueueUrl= queueUrl):  # TODO: should keep polling until request_id match
        if msg.message_attributes:
            client_id = msg.message_attributes.get('client_id')
            result = msg.message_attributes.get('result')
            response_cache[client_id][request_id] = result
            write_response_to_db(client_id, request_id, result)

def write_response_to_db(client_id, request_id, result):
    pass

def get_response_cache_from_db():
    pass


if __name__ == '__main__':
    init()
    app.run(host = '127.0.0.1', port = 3000)
