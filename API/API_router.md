**k12 Microservice**
----------
### GET **/k12**


Send a request to list all the student information. The response contains a request ID which is used to retrieve all student information.


**Sample Request**

GET {ServerPath}/private/k12

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
            "MD5OfMessageAttributes": "aea417815355f8b5d413556be79c3dd1",
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
                "RequestId": "6cb573b5-208e-5239-acdb-3d410136588e"
            },
            "MessageId": "587645f8-df0a-4446-b954-dc44907ce944"
        },
        "request_id": "45585d6e0b898769e51eafb1ed35d5b374f1452f",
        "code": 200
    }
}
```

**Possible Error Response**  
* 404 Resource not found  
* 500 Internal Server Error

---
### GET **/response**


Fetch result from previous request. Here corresponds to the request of: 
GET {ServerPath}/private/k12

**Sample Request**

GET {ServerPath}/response?client_id=1&RequestID=45585d6e0b898769e51eafb1ed35d5b374f1452f

**Sample Success Response**

```json
{
    "Count": 5,
    "Items": [
        {
            "info": {
                "DOB": "19920813",
                "lastname": "yang",
                "firstname": "yang"
            },
            "schoolid": "CMU",
            "studentid": "yy1234"
        },
        {
            "info": {
                "lastname": "sss",
                "firstname": "sss"
            },
            "schoolid": "CU",
            "studentid": "ss3231"
        },
        {
            "info": {
                "DOB": "19910813",
                "lastname": "shen",
                "firstname": "qiuyang"
            },
            "schoolid": "ColumbiaUniversity",
            "studentid": "qs2147"
        },
        {
            "info": {
                "lastname": "Sun",
                "firstname": "Yun"
            },
            "schoolid": "CU",
            "studentid": "ys2816"
        },
        {
            "info": {
                "DOB": "19920813",
                "lastname": "du",
                "firstname": "cheng"
            },
            "schoolid": "CMU",
            "studentid": "cd2789"
        }
    ],
    "ScannedCount": 5,
    "ResponseMetadata": {
        "HTTPStatusCode": 200,
        "RequestId": "d00bac87-6c68-478f-a847-71e9d0c75dad"
    }
}
```

**Possible Error Response**  
* 404 Resource not found  
* 500 Internal Server Error

---


### GET **/private/k12/studentid/\<studentid\>**

Send a request to list student information by studentid. It contains information of all schools of which the student has record. The response contains the request ID which is used to retrieve the student information

**Sample Request**

GET {ServerPath}/private/k12/studentid/qs2147

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
            "MD5OfMessageAttributes": "3494565c8575f98b0da7042682798c4b",
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
                "RequestId": "1bca4173-75b4-5f20-ad47-0f8750dae5ce"
            },
            "MessageId": "8d8fbfe2-8624-432e-ae0c-f96bc5f41642"
        },
        "request_id": "967927cbac720cf50a34aeade6730ec5ee54f643",
        "code": 200
    }
}
```

**Possible Error Response**  
* 500 Internal Server Error


---
### GET **/response**

Fetch result from previous request. Here corresponds to the request of: 
GET {ServerPath}/private/k12/studentid/qs2147

**Sample Request**

GET {ServerPath}/response?client_id=1&RequestID=967927cbac720cf50a34aeade6730ec5ee54f643

**Sample Success Response**

```json
{
    "Count": 2,
    "Items": [
        {
            "info": {
                "DOB": "19910813",
                "lastname": "shen",
                "firstname": "qiuyang"
            },
            "schoolid": "ColumbiaUniversity",
            "studentid": "qs2147"
        },
        {
            "info": {
                "lastname": "shen",
                "firstname": "qiuyang",
                "hobby": "dota2"
            },
            "schoolid": "NJU",
            "studentid": "qs2147"
        }
    ],
    "ScannedCount": 2,
    "ResponseMetadata": {
        "HTTPStatusCode": 200,
        "RequestId": "3456c4c8-23af-45ce-880c-49733404b66e"
    }
}
```

**Possible Error Response**  
* 404 Resource not found  
* 500 Internal Server Error

---
### GET **/private/k12/studentid/\<studentid\>/schoolid/\<schoolid\>**

Send a request to list student information by studentid and schoolid. The response contains the request ID which is used to retrieve the student information

**Sample Request**

GET {ServerPath}/private/k12/studentid/qs2147/NJU

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
            "MD5OfMessageAttributes": "1a6be77f0a49caa3f8978cf8007b5149",
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
                "RequestId": "6a9a1fd8-9cd3-5944-b83a-512cba85db04"
            },
            "MessageId": "9e43d2e4-b32c-45cd-a791-0f331ea1a2fa"
        },
        "request_id": "96aab8d5b51b90f4e0d52a6cae63b3235391b374",
        "code": 200
    }
}
```

**Possible Error Response**  
* 500 Internal Server Error

---
### GET **/response**

Fetch result from previous request. Here corresponds to the request of: 
GET {ServerPath}/private/k12/studentid/qs2147/NJU

**Sample Request**

GET {ServerPath}/response?client_id=1&RequestID=96aab8d5b51b90f4e0d52a6cae63b3235391b374

**Sample Success Response**

```json
{
    "Count": 1,
    "Items": [
        {
            "info": {
                "lastname": "shen",
                "firstname": "qiuyang",
                "hobby": "dota2"
            },
            "schoolid": "NJU",
            "studentid": "qs2147"
        }
    ],
    "ScannedCount": 1,
    "ResponseMetadata": {
        "HTTPStatusCode": 200,
        "RequestId": "a2e8f73d-469f-459c-91bc-bdeb00ae9536"
    }
}
```

**Possible Error Response**  
* 404 Resource not found  
* 500 Internal Server Error

---
### POST **/private/k12**

send a request to create new student with specifying schoolid and JSON body. The response contains the request ID which is used to retrieve the POST status information

**Sample Request**

POST {ServerPath}/private/k12

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
            "MD5OfMessageAttributes": "e5bd9fd7b23d77a23f0e8a43b9adccfa",
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
                "RequestId": "52187e50-d8c5-5b2c-b0d5-30a4ffd358dc"
            },
            "MessageId": "2553a910-4c4b-449b-af1d-4f2f6a407be0"
        },
        "request_id": "6628811e04ca022d925e7c9385fe5aed9a6f5796",
        "code": 200
    }
}
```

**Possible Error Response**  
* 404 Resource not found  
* 500 Internal Server Error


---
### GET **/response**

Fetch result from previous request. Here corresponds to the request of: 
POST {ServerPath}/private/k12

**Sample Request**

GET {ServerPath}/response?client_id=1&RequestID=6628811e04ca022d925e7c9385fe5aed9a6f5796

**Sample Success Response**

```json
{
    "ResponseMetadata": {
        "HTTPStatusCode": 200,
        "RequestId": "12f8de20-063b-4cf8-8468-22a0531b5deb"
    }
}
```

**Possible Error Response**  
* 404 Resource not found  
* 500 Internal Server Error

---
### PUT **/private/k12/studentid/\<studentid\>/schoolid/\<schoolid\>**

Send a request to update student info with specifying schoolid and JSON body. The response contains the request ID which is used to retrieve the PUT status information. 

**Sample Request**

PUT {ServerPath}/private/k12/studentid/qs2147/schoolid/ColumbiaUniversity

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
            "MD5OfMessageAttributes": "3d4027b0b919b6f1d8332bfbd74adea5",
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
                "RequestId": "22955ec0-312c-58db-a561-103419a1078d"
            },
            "MessageId": "197ee777-2314-403b-8a60-63516eee012c"
        },
        "request_id": "00d0cbf0143432cfffb68aab22466183b492537f",
        "code": 200
    }
}
```

**Possible Error Response**
* 404 Resource not found
* 500 Internal Server Error

---
### GET **/response**

Fetch result from previous request. Here corresponds to the request of: 
PUT {ServerPath}/private/k12/studentid/qs2147/schoolid/ColumbiaUniversity

**Sample Request**

GET {ServerPath}/response?client_id=1&RequestID=00d0cbf0143432cfffb68aab22466183b492537f

**Sample Success Response**

```json
{
    "Attributes": {
        "info": {
            "DOB": "19910813",
            "lastname": "shen",
            "major": "computer engineering",
            "age": 23,
            "firstname": "yangqiu"
        }
    },
    "ResponseMetadata": {
        "HTTPStatusCode": 200,
        "RequestId": "4b870476-651e-4a91-81d2-241e8af47876"
    }
}
```

**Possible Error Response**  
* 404 Resource not found  
* 500 Internal Server Error

---
### DELETE **/private/k12/studentid/\<studentid\>/schoolid/\<schoolid\>**

Send a request to delete student by studentid and schoolid. The response contains the request ID which is used to retrieve the DELETE status information

**Sample Request**

DELETE {ServerPath}/private/k12/studentid/qs2147/schoolid/NJU

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
            "MD5OfMessageAttributes": "e0be297f6eb1fe1d24dccb3472960b8c",
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
                "RequestId": "3fac353a-c059-55f1-8111-7bcee9dc63d3"
            },
            "MessageId": "0c9b5100-660f-4363-81bd-40f0ee5dff54"
        },
        "request_id": "c72e76c2cdc8ac51827d9b9af71669b4604bfb61",
        "code": 200
    }
}
```

**Possible Error Response**
* 404 Resource not found
* 500 Internal Server Error

---
### GET **/response**

Fetch result from previous request. Here corresponds to the request of: 
DELETE {ServerPath}/private/k12/studentid/qs2147/schoolid/NJU

**Sample Request**

GET {ServerPath}/response?client_id=1&RequestID=c72e76c2cdc8ac51827d9b9af71669b4604bfb61

**Sample Success Response**

```json
{
    "ResponseMetadata": {
        "HTTPStatusCode": 200,
        "RequestId": "08db7512-3b59-4e12-831d-0c7d0e6434d4"
    }
}
```

**Possible Error Response**  
* 404 Resource not found  
* 500 Internal Server Error





