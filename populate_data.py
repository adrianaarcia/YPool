import json 
import requests

base_url = "https://yalepool.com/" 


api_key = 'a333b39d-6ff7-4e54-9488-b8ec66d7a39d' 
header = {'api-key' : api_key}


### Example of submitting requests 
data = {'netId': 'ds2496', "date":"2021-06-10", "time":"14:30", "origin":"Yale", "destination": "Airport-JFK", "preferred_car_type":"XL", "preferred_group_size":"4"}
print(requests.post(url, headers=header, json=data))
data = {'netId': 'jgt37', "date":"2021-06-10", "time":"14:30", "origin":"Yale", "destination": "Airport-JFK", "preferred_car_type":"XL", "preferred_group_size":"4"}
print(requests.post(url, headers=header, json=data))

### Example of registering users 
url = base_url+'users'
data = {'netId': 'abc12334', "first_name":"Jared", "last_name":"yoyo","email":"testt123@yale.edu"}
print(requests.post(url, headers=header, json=data))