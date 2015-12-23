from __future__ import print_function # Python 2/3 compatibility
from flask import Flask, request, jsonify, Response
from pymongo import MongoClient
import urllib2, requests
import sys, subprocess, os, signal, time
import json, logging, boto3, decimal
from boto3.dynamodb.conditions import Key, Attr

global table
global sqs_client

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


app = Flask(__name__)
logging.basicConfig(filename="k12.log",
                    level=logging.INFO, format='%(asctime)s --- %(message)s')

@app.route('/private/k12', methods=['GET'])
def get_all_student():
    response = table.scan()
    return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response)


@app.route('/private/k12/studentid/<studentid>', methods=['GET'])
def get_student_all_school(studentid):
    response = table.query(KeyConditionExpression=Key('studentid').eq(studentid))
    return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response)

@app.route('/private/k12/studentid/<studentid>/schoolid/<schoolid>', methods=['GET'])
def get_student_and_school(studentid, schoolid):
    response = table.query(KeyConditionExpression=Key('studentid').eq(studentid) & Key('schoolid').eq(schoolid))
    return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response)


@app.route('/private/k12', methods=['POST'])
def add_student_and_school():
    student = {}
    request_json = request.get_json()
    student['studentid'] = request_json['studentid']
    student['schoolid'] = request_json['schoolid']
    request_json.pop('studentid', None)
    request_json.pop('schoolid', None)
    student['info'] = request_json
    response = table.put_item(Item=student)
    print(json.dumps(response, indent=4, cls=DecimalEncoder))
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response)
    return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response['ResponseMetadata'])

@app.route('/private/k12/studentid/<studentid>/schoolid/<schoolid>', methods=['PUT'])
def update_student_and_school(studentid, schoolid):
    student = request.get_json()
    if not student:
        return "Nothing to update"
    update_expression = 'set '
    expression_values = {}
    for key, value in student.iteritems():
        update_expression += 'info.' + key + ' = :' + key + ','
        expression_values[':' + key] = value
    update_expression = update_expression[:-1]
    try:
        response = table.update_item(
            Key={
                'studentid': studentid,
                'schoolid': schoolid
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ReturnValues="UPDATED_NEW"
        )
    except Error as e:
        print(e)
        return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), e)
    print(json.dumps(response, indent=4, cls=DecimalEncoder))
    return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response)


@app.route('/private/k12/studentid/<studentid>/schoolid/<schoolid>', methods=['DELETE'])
def delete_student_and_school(studentid, schoolid):
    try:
        response = table.delete_item(
            Key={
                'studentid': studentid,
                'schoolid': schoolid
            }
        )
    except Error as e:
        print(e)
        return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), e)
    return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response)

@app.route('/private/k12/schoolid/<schoolid>', methods=['GET'])
def get_school(schoolid):
    response = table.scan(
        FilterExpression=Key('schoolid').eq(schoolid)
    )
    return send_to_response_queue(request.headers.get('Response-url'), request.headers.get('Request-id'), response)

def send_to_response_queue(resp_queue_url, req_id, json_object):
    print(json_object)
    response = sqs_client.send_message(QueueUrl = resp_queue_url, MessageBody = 'boto3', MessageAttributes = {
                'ReturnValue': {
                    'StringValue': json.dumps(json_object, cls=DecimalEncoder),
                    'DataType': 'String'
                },
                'RequestID':{
                    'StringValue':req_id,
                    'DataType': 'String'
                }
            })
    return response['MD5OfMessageBody']

if __name__ == "__main__":
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
    table = dynamodb.Table('k12')
    sqs_client = boto3.client('sqs')
    app.run(host='localhost', port=9000)






