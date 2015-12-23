**Router Service**
----------
### GET **/public/k12**


Map the public url to private url, create response queues for new clients and send the request message to the k12's request queue.


**Sample Request**

GET {ServerPath}/public/k12

Headers:{
    client_id: 1
}

**Sample Success Response**

```json
{
    "_status": "SUCCESS",
    "_success": {
        "message": {
            "MD5OfMessageBody": "6686853da3491a56c98917cc5c4ddea2",
            "MD5OfMessageAttributes": "569e011fc3b0998ca53ef0e24fd931e3",
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
                "RequestId": "0304b39f-95c6-50b3-851e-fd6a930ffb49"
            },
            "MessageId": "73529d39-2c41-45a8-80f9-3451333e4757"
        },
        "request_id": "6f2c7be27ea872be017d04a8c1740664509b1cd2",
        "code": 200
    }
}
```

**Possible Error Response**  
* 404 Resource not found  
* 500 Internal Server Error

---


### GET **/public/k12/studentid/\<studentid\>**

Map the public url to private url, create response queues for new clients and send the request message to the k12's request queue.

**Sample Request**

GET {ServerPath}/public/k12/studentid/qs2147

Headers:{
    client_id: 1
}

**Sample Success Response**

```json
{
    "_status": "SUCCESS",
    "_success": {
        "message": {
            "MD5OfMessageBody": "6686853da3491a56c98917cc5c4ddea2",
            "MD5OfMessageAttributes": "9a092abb122eb948adf7392608cc9df4",
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
                "RequestId": "6436a567-3629-5162-b11f-eb9231e84782"
            },
            "MessageId": "11742668-50df-4350-9bc9-6834ccbf6f35"
        },
        "request_id": "1a156d482b2336098766beb1df1c8c5f4dedd4f6",
        "code": 200
    }
}
```

**Possible Error Response**  
* 500 Internal Server Error


---
### GET **/public/k12/studentid/\<studentid\>/schoolid/\<schoolid\>**

Map the public url to private url, create response queues for new clients and send the request message to the k12's request queue.

**Sample Request**

GET {ServerPath}/public/k12/studentid/qs2147/schoolid/NJU

Headers:{
    client_id: 1
}

**Sample Success Response**

```json
{
    "_status": "SUCCESS",
    "_success": {
        "message": {
            "MD5OfMessageBody": "6686853da3491a56c98917cc5c4ddea2",
            "MD5OfMessageAttributes": "4fe2c0da13f4f9266724dd9e43a263f2",
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
                "RequestId": "99300ab8-548a-5a67-b5d4-444d5ca7fb86"
            },
            "MessageId": "e9628ed5-4581-470c-a1b8-e6a1e51d9b20"
        },
        "request_id": "8a4c8256d00ae1b5e087c6be88f637b2176380dd",
        "code": 200
    }
}
```

**Possible Error Response**  
* 500 Internal Server Error


---
### POST **/public/k12**

Map the public url to private url, create response queues for new clients and send the request message to the k12's request queue.

**Sample Request**

POST {ServerPath}/public/k12

Headers:{
    Content-Type: application/json
    client_id: 1
}

*HTTP Body*
```json
{
    "studentid":"ab1234", 
    "schoolid":"Columbia", 
    "firstname":"foo", 
    "lastname":"bar", 
    "hobby":"coding"
}
```

**Sample Success Response**

*HTTP Body*
```json
{
    "_status": "SUCCESS",
    "_success": {
        "message": {
            "MD5OfMessageBody": "6686853da3491a56c98917cc5c4ddea2",
            "MD5OfMessageAttributes": "c61fc314a368e1b1a2d1e0957643080e",
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
                "RequestId": "766d72e3-49a7-5847-8cb6-3c1641d4b23c"
            },
            "MessageId": "51f65119-fbc0-4bb1-843e-7c4c338d9e7c"
        },
        "request_id": "a0f8d4e7f908334939bc70813bb8d2120f078935",
        "code": 200
    }
}
```

**Possible Error Response**  
* 404 Resource not found  
* 500 Internal Server Error


---
### PUT **/public/k12/studentid/\<studentid\>/schoolid/\<schoolid\>**

Map the public url to private url, create response queues for new clients and send the request message to the k12's request queue.

**Sample Request**

PUT {ServerPath}/public/k12/studentid/qs2147/schoolid/ColumbiaUniversity

Headers:{
    Content-Type: application/json
    client_id: 1
}

*HTTP Body*
```json
{
    "firstname":"yangqiu", 
    "lastname":"shen",
    "major":"computer engineering",
    "age":23
}
```

**Sample Success Response**

```json
{
    "_status": "SUCCESS",
    "_success": {
        "message": {
            "MD5OfMessageBody": "6686853da3491a56c98917cc5c4ddea2",
            "MD5OfMessageAttributes": "808a8a68ce6a5ed46699419098f2d02c",
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
                "RequestId": "df907b38-c3b8-5c33-b063-35cdcb0d5b13"
            },
            "MessageId": "91e1825a-88c0-454e-aa2f-863b80010276"
        },
        "request_id": "c5206a0c8be7b18fcc968a2402f4ddae39149dd2",
        "code": 200
    }
}
```

**Possible Error Response**
* 404 Resource not found
* 500 Internal Server Error

---
### DELETE **/public/k12/studentid/\<studentid\>/schoolid/\<schoolid\>**

Map the public url to private url, create response queues for new clients and send the request message to the k12's request queue.

**Sample Request**

DELETE {ServerPath}/public/k12/studentid/qs2147/schoolid/NJU

Headers:{
    client_id: 1
}

**Sample Success Response**

```json
{
    "_status": "SUCCESS",
    "_success": {
        "message": {
            "MD5OfMessageBody": "6686853da3491a56c98917cc5c4ddea2",
            "MD5OfMessageAttributes": "3febec40a0e164b3804537811fb1880a",
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
                "RequestId": "459c5efd-dd04-549e-9894-1008d5eca3be"
            },
            "MessageId": "8e2aaca1-d386-4df9-a2eb-1baf40b3ac73"
        },
        "request_id": "6086fa6b38d9a7da6cbe86949d5a541ccc6474e7",
        "code": 200
    }
}
```

**Possible Error Response**
* 404 Resource not found
* 500 Internal Server Error





