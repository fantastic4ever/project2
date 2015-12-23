from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('k12')

response = table.put_item(
   Item={
        'studentid': 'qs2147',
        'schoolid': 'Columbia University',
        'info': {
            'DOB':'19910813',
            'firstname':'Qiuyang',
            'lastname':'Shen'
        }
    }
)

print("PutItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))