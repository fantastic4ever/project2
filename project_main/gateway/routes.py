from project_main.gateway import app
from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify, Response
from sqlalchemy.sql import func
import urllib
import logging
import json
import boto3
from pymongo import MongoClient
from project_main import mongo_credentials

mongo_url = 'mongodb://%s:%s@ds033915.mongolab.com:33915/project2' % (mongo_credentials.DB_USERNAME, mongo_credentials.DB_PASSWORD)
mongo = MongoClient(mongo_url)
response_queue_url = {}  # map from client_id(which is also the id of response queue) to queueUrl
response_cache = {}
# sqs = boto3.resource('sqs', region_name='us-east-1')
sqs = boto3.client('sqs', region_name='us-east-1')

def init():
    get_response_queue_url_from_db()

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
    client_id = str(args.get("client_id", ""))  # client_id is also the id of response queue
    request_id = str(args.get("request_id", ""))  # if request_id is None, then return the first one in queue
    if not client_id:
        return Response("client_id is empty", status=400)
    this_cache = response_cache.setdefault(client_id, {})
    if request_id:  # only request_id is empty
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
    queueUrl = "https://sqs.us-east-1.amazonaws.com/308367428478/test"
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
                raise Exception('Invalid response')
            # logging.info(receiptHandle)
            # logging.info(this_request_id)
            # logging.info(result)
        except Exception, e:
            return Response("The response is not valid", status=500)
        response_cache[client_id][this_request_id] = result  # add it to cache
        write_response_to_db(client_id, this_request_id, result)  # add it to db
        # sqs.delete_message(QueueUrl=queueUrl, ReceiptHandle=receiptHandle)
        logging.info("read request_id %s from sqs"%this_request_id)
        if not request_id or request_id==this_request_id:  # if match or doest not provide request_id, return
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
