import json, logging, boto3, decimal
import httplib
import urllib
from boto3.dynamodb.conditions import Key, Attr

global table
global connection


def pull_message():
    sqs_client = boto3.client('sqs')
    request_queue_url = 'https://queue.amazonaws.com/031864143155/k12'
    while True:
        response = sqs_client.receive_message(
            QueueUrl = request_queue_url,
            AttributeNames=['ReceiveMessageWaitTimeSeconds'], 
            MessageAttributeNames=['All'], 
            MaxNumberOfMessages=10, 
            VisibilityTimeout=60, 
            WaitTimeSeconds=20)
        if 'Messages' in response.keys() and len(response['Messages']) > 0:
            for message in response['Messages']:
                print(message['MessageAttributes'])
                message_attr = message['MessageAttributes']
                header = {'Content-type': 'application/json', 'Response-url':message_attr['response_queue_url']['StringValue']}
                conn.request(method=message_attr['op']['StringValue'], 
                    url=message_attr['service_url']['StringValue'],
                    body=message_attr['body']['StringValue'],
                    headers=header)
                response = conn.getresponse()
                print response.read()
                sqs_client.delete_message(QueueUrl=request_queue_url,
                    ReceiptHandle=message['ReceiptHandle'])

if __name__ == "__main__":
    conn = httplib.HTTPConnection('%s:%s' % ('localhost', '9000'))
    pull_message()