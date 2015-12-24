# **Student Finance Microservice**

---
### GET **/private/finance** 
List all student finance information.

**Sample Request**  
GET {ServerPath}/private/finance

**Sample Success Response**
```json
{
  "_items": [
    {
      "_updated": "Wed, 23 Dec 2015 04:01:13 GMT",
      "student_id": "yl9999",
      "tuition": 0,
      "_links": {
        "self": {
          "href": "finance/567a1c893fc0e7259cea5d00",
          "title": "Finance"
        }
      },
      "_created": "Wed, 23 Dec 2015 04:01:13 GMT",
      "_id": "567a1c893fc0e7259cea5d00",
      "_etag": "a8833212098ffc9dd5208134e436d902b3fa7027"
    },
    {
      "_updated": "Wed, 23 Dec 2015 20:52:17 GMT",
      "course_list": [
        {
          "course_id": 22345,
          "credit": 3,
          "unit_price": 1200
        },
        {
          "course_id": 33333,
          "credit": 3,
          "unit_price": 1200
        }
      ],
      "student_id": "yl3179",
      "tuition": 3600,
      "_links": {
        "self": {
          "href": "finance/567b095c38086db673bacd39",
          "title": "Finance"
        }
      },
      "_created": "Wed, 23 Dec 2015 20:51:40 GMT",
      "_id": "567b095c38086db673bacd39",
      "_etag": "e1b751fe20724212ce62c93a68bf4d6f07ebb817"
    }
  ],
  "_links": {
    "self": {
      "href": "finance",
      "title": "finance"
    },
    "parent": {
      "href": "/",
      "title": "home"
    }
  },
  "_meta": {
    "max_results": 25,
    "total": 2,
    "page": 1
  }
}
```

**Possible Error Response**  
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error



---
### GET **/private/finance/_<student_id_>**  
Retrieve a specific student's finance information by his/her student_id, where student_id should follow the exact format of two lower case alphabets followed by four digits.

**Sample Request**  
GET {ServerPath}/private/finance/yl3179

**Sample Success Response**
```json
{
  "_updated": "Wed, 23 Dec 2015 20:52:17 GMT",
  "course_list": [
    {
      "course_id": 22345,
      "credit": 3,
      "unit_price": 1200
    },
    {
      "course_id": 33333,
      "credit": 3,
      "unit_price": 1200
    }
  ],
  "student_id": "yl3179",
  "tuition": 3600,
  "_links": {
    "self": {
      "href": "finance/567b095c38086db673bacd39",
      "title": "Finance"
    },
    "collection": {
      "href": "finance",
      "title": "finance"
    },
    "parent": {
      "href": "/",
      "title": "home"
    }
  },
  "_created": "Wed, 23 Dec 2015 20:51:40 GMT",
  "_id": "567b095c38086db673bacd39",
  "_etag": "e1b751fe20724212ce62c93a68bf4d6f07ebb817"
}
```

**Possible Error Response**  
* 404 Resource not found  
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error



---
### POST **/private/finance**  
Add student finance information to the collection.

**Sample Request**  
POST {ServerPath}/private/finance
###### *HTTP Body* 
```json
{
    "student_id": "yl3999",
    "course_list": [{
        "course_id": 12345,
        "credit": 3,
        "unit_price": 1200
    }]
}
```

**Sample Success Response**
```json
{
  "_updated": "Thu, 24 Dec 2015 02:13:35 GMT",
  "_links": {
    "self": {
      "href": "finance/567b54cf3fc0e73f74ca210c",
      "title": "Finance"
    }
  },
  "_created": "Thu, 24 Dec 2015 02:13:35 GMT",
  "_status": "OK",
  "_id": "567b54cf3fc0e73f74ca210c",
  "_etag": "0f1d17a1b40d3568458bc3c72d55648db6757d90"
}
```

**Possible Error Response**
* 403 Bad request
* 422 student_id not unique
* 422 invalid data type
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error



---
### PUT **/private/finance/_<student_id_>**  
Update columns/attributes of existing student finance information.

**Sample Request**  
PUT {ServerPath}/private/finance/yl3179
###### *HTTP Head* 
```
If-Match = e1b751fe20724212ce62c93a68bf4d6f07ebb817
```
###### *HTTP Body* 
```json
{
    "student_id": "yl3179",
    "course_list": [{
        "course_id": 22345,
        "credit": 3,
        "unit_price": 1200
    }]
}
```

**Sample Success Response**
```json
{
  "_updated": "Thu, 24 Dec 2015 02:21:58 GMT",
  "_links": {
    "self": {
      "href": "finance/567b095c38086db673bacd39",
      "title": "Finance"
    }
  },
  "_created": "Wed, 23 Dec 2015 20:51:40 GMT",
  "_status": "OK",
  "_id": "567b095c38086db673bacd39",
  "_etag": "8b8d9c212f3f471b313e75cac977d8531aea5b3f"
}
```

**Possible Error Response**
* 403 Bad request
* 403 An etag must be provided to edit a document
* 412 Client and server etags don't match
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error



---
### DELETE **/private/finance**  
Delete all finance information in the collection.

**Sample Request**  
DELETE {ServerPath}/private/finance

**Sample Success Response**
```json
Status 204 NO CONTENT
No response received
```

**Possible Error Response**
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error



---
### DELETE **/private/finance/_<student_id_>**  
Delete the finance information of student with specified student_id.

**Sample Request**  
DELETE {ServerPath}/private/finance/yl9999
###### *HTTP Head* 
```
If-Match = a8833212098ffc9dd5208134e436d902b3fa7027
```

**Sample Success Response**
```json
Status 204 NO CONTENT
No response received
```

**Possible Error Response**
* 403 Bad request
* 403 An etag must be provided to edit a document
* 404 Resource not found
* 412 Client and server etags don't match
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error
