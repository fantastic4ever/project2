from project_main.gateway import app
from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify, Response
from sqlalchemy.sql import func
import urllib
import logging
import json
import boto3

response_queue_url = {}  # map from client_id(which is also the id of response queue) to queueUrl
response_cache = {}
# sqs = boto3.resource('sqs', region_name='us-east-1')
sqs = boto3.client('sqs', region_name='us-east-1')

def init():
    get_response_queue_url_from_db()
    get_response_cache_from_db()

### get a list of all available rest api ###
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
    queueUrl = "https://sqs.us-east-1.amazonaws.com/308367428478/test"
    for msg in sqs.receive_messages(QueueUrl = queueUrl, MessageAttributeNames=["All"]):  # TODO: should keep polling until request_id match
        print msg.body
        for k,v in msg.message_attributes.items():
            print k,v
    return "200"
        # if msg.message_attributes:
        #     client_id = msg.message_attributes.get('client_id')
        #     result = msg.message_attributes.get('result')
        #     response_cache[client_id][request_id] = result
        #     write_response_to_db(client_id, request_id, result)

def write_response_to_db(client_id, request_id, result):
    pass

def get_response_cache_from_db():
    pass


if __name__ == '__main__':
    init()
