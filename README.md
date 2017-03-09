GeoNames REST API
------------------
This small project implements Connexion and Swagger(OpenApi) based REST endpoints to find cities 
based on keyword and finding k nearest cities for given city. Connexion is built on top of Flask 
and it handles HTTP based REST api's. The OpenApi based specification for api's is defind in yaml file. 
The handler for each end point is mapped to python function in yaml file. The handler for the REST 
endpoint is invoked when user accesses the endpoint using different means. Swagger also provides a very 
nice user interface for accessing the api endpoints.

The data for this project has been taken from 'cities1000.txt' from geonames website. Parsing the 
'cities1000.txt' is the easiest part since the data is well structured and each line has 19 tab 
separated fields. Once the location(longitude, latitude) is parsed, KDTree is used for finding k 
nearest neighbors. 

KDTree is a binary tree where every node has k elements(or dimensions). It has average search time of 
O(log n). KDTree stores k dimensional points by dividing plane into two parts. In this particular case 
since we are inserting (latitude, longitude) into KDTree 2D plane is formed. Each point is inserted 
based on splitting axis for ex. if 'x' or latitude is chosen as splitting axis, the value x from point 
to be inserted is compared against current node and all points with value less that current node will 
be inserted to left subtree and points with larger values of x will be inserted into the right subtree. 
The KDTree suffers from unbalanced subtrees similar to binary tree.

Install pip requirements & run server:
---------------------------------------
1. ```mkvirtualenv geonamesenv```
1. ```pip install -r requirements.txt```
2. ```python geonames_api_server.py```

Results:
---------
The Swagger UI can be accessed using using http://localhost:8080/v1.0/ui/. The nearest_neighbors api 
only accepts country code for ex. IN, US etc.

```
rkadam@rkadam-vbox:~/github/geonames_analysis$ curl -X GET "http://0.0.0.0:8080/v1.0/cities/bangalore"
[
  {
    "city": "Bengaluru",
    "country_code": "IN"
  }
]
```
```
rkadam@rkadam-vbox:~/github/geonames_analysis$ curl -X GET "http://0.0.0.0:8080/v1.0/cities/New%20york"
[
  {
    "city": "New York Mills",
    "country_code": "US"
  },
  {
    "city": "West New York",
    "country_code": "US"
  },
  {
    "city": "Albany",
    "country_code": "US"
  },
  {
    "city": "Amsterdam",
    "country_code": "US"
  },
  {
    "city": "Binghamton",
    "country_code": "US"
  },
  {
    "city": "Buffalo",
    "country_code": "US"
  },
  {
    "city": "East New York",
    "country_code": "US"
  },
  {
    "city": "New York City",
    "country_code": "US"
  },
  {
    "city": "New York Mills",
    "country_code": "US"
  },
  {
    "city": "Potsdam",
    "country_code": "US"
  },
  {
    "city": "Syracuse",
    "country_code": "US"
  }
]
```
```
rkadam@rkadam-vbox:~/github/geonames_analysis$ curl -X GET "http://0.0.0.0:8080/v1.0/cities/Syracuse"
[
  {
    "city": "Siracusa",
    "country_code": "IT"
  },
  {
    "city": "Syracuse",
    "country_code": "US"
  },
  {
    "city": "Syracuse",
    "country_code": "US"
  },
  {
    "city": "East Syracuse",
    "country_code": "US"
  },
  {
    "city": "North Syracuse",
    "country_code": "US"
  },
  {
    "city": "Syracuse",
    "country_code": "US"
  },
  {
    "city": "Syracuse",
    "country_code": "US"
  },
  {
    "city": "Syracuse",
    "country_code": "US"
  }
]
```
```
rkadam@rkadam-vbox:~/github/geonames_analysis$ curl -X GET "http://0.0.0.0:8080/v1.0/nearest_cities?city=bangalore&k=10&country=IN"
[
  {
    "city": "Bengaluru",
    "country_code": "IN"
  },
  {
    "city": "Yelahanka",
    "country_code": "IN"
  },
  {
    "city": "Hoskote",
    "country_code": "IN"
  },
  {
    "city": "Nelamangala",
    "country_code": "IN"
  },
  {
    "city": "Dasarahalli",
    "country_code": "IN"
  },
  {
    "city": "Anekal",
    "country_code": "IN"
  },
  {
    "city": "Devanhalli",
    "country_code": "IN"
  },
  {
    "city": "Dod Ball\u0101pur",
    "country_code": "IN"
  },
  {
    "city": "Hos\u016br",
    "country_code": "IN"
  },
  {
    "city": "M\u0101l\u016br",
    "country_code": "IN"
  },
  {
    "city": "M\u0101gadi",
    "country_code": "IN"
  }
]
```
```
rkadam@rkadam-vbox:~/github/geonames_analysis$ curl -X GET "http://0.0.0.0:8080/v1.0/nearest_cities?city=New%20york&k=10&country=US"
[
  {
    "city": "New York Mills",
    "country_code": "US"
  },
  {
    "city": "Perham",
    "country_code": "US"
  },
  {
    "city": "Wadena",
    "country_code": "US"
  },
  {
    "city": "Menahga",
    "country_code": "US"
  },
  {
    "city": "Parkers Prairie",
    "country_code": "US"
  },
  {
    "city": "Frazee",
    "country_code": "US"
  },
  {
    "city": "Park Rapids",
    "country_code": "US"
  },
  {
    "city": "Detroit Lakes",
    "country_code": "US"
  },
  {
    "city": "Staples",
    "country_code": "US"
  },
  {
    "city": "Alexandria",
    "country_code": "US"
  },
  {
    "city": "Osakis",
    "country_code": "US"
  }
]
```

Enhancements:
--------------
1. Instead of parsing the geonames text file every time the server launches, the parsed data
can be stored in database. Also redis can be used to cache the location data and result of queries
2. KDTree in scipy.spatial module is single threaded. It can be modified to make use of multiple cores
3. Instead of having functions in genonames module as REST endpoint handlers, it is better
to have the handlers in class GeoNames as methods. This would be much cleaner way of implementing REST handlers
4. Having KDTree for each country greatly improves the query time since KDTree is built per tree.
But the tradeoff is this approach requires more memory
5. Improve the nearest_neighbors api to handle country name
6. Enhance the api's to return more fields in result which should be trivial
