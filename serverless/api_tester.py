import json 
import requests

DEBUG=False
base_url = "https://yalepool.com/" if not DEBUG else "http://localhost:5000/"


def print_data(response):
	response_dict = json.loads(response.text)
	tok = None 
	if isinstance(response_dict, list):
		for i in response_dict:
			print(type(i))
			print(i)
			
	elif isinstance(response_dict, dict):
		for i in response_dict:
			print(i, ":", response_dict[i])
	else:
		print(response_dict)
        
### Example of registering a user
# url = base_url+'users'
api_key = 'a333b39d-6ff7-4e54-9488-b8ec66d7a39d' 
header = {'api-key' : api_key}
# data = {'netId': 'abc12334', "first_name":"Jared", "last_name":"yoyo","email":"testt123@yale.edu"}
# print(requests.post(url, headers=header, json=data))

### Example of getting the destinations
# url = base_url+'destinations'
# print_data(requests.get(url))

### Example of submitting requests 
# url = base_url+'ride-request'
# data = {'netId': 'ds2496', "date":"2021-06-10", "time":"14:30", "origin":"Yale", "destination": "Airport-JFK", "preferred_car_type":"XL", "preferred_group_size":"4"}
# print_data(requests.post(url, json=data))
# data = {'netId': 'jgt37', "date":"2021-06-10", "time":"14:30", "origin":"Yale", "destination": "Airport-JFK", "preferred_car_type":"XL", "preferred_group_size":"4"}
# print_data(requests.post(url, json=data))
# data = {'netId': 'ds2496', "date":"2021-06-10", "time":"14:30", "origin":"Yale", "destination": "Airport-JFK", "preferred_car_type":"XL", "preferred_group_size":"4"}
# print_data(requests.post(url, json=data))
# data = {'netId': 'jgt37', "date":"2021-06-10", "time":"14:30", "origin":"Yale", "destination": "Airport-JFK", "preferred_car_type":"XL", "preferred_group_size":"4"}
# print_data(requests.post(url, json=data))
# data = {'netId': 'oka5', "date":"2021-06-10", "time":"14:30", "origin":"Yale", "destination": "Airport-JFK", "preferred_car_type":"XL", "preferred_group_size":"4"}
# print_data(requests.post(url, json=data))
# data = {'netId': 'ds2496', "date":"2021-06-10", "time":"14:30", "origin":"Yale", "destination": "Airport-JFK", "preferred_car_type":"XL", "preferred_group_size":"4"}
# print_data(requests.post(url, json=data))
# data = {'netId': 'jgt37', "date":"2021-06-10", "time":"14:30", "origin":"Yale", "destination": "Airport-JFK", "preferred_car_type":"XL", "preferred_group_size":"4"}
# print_data(requests.post(url, headers=header, json=data))
# data = {'netId': 'oka5', "date":"2021-06-10", "time":"14:30", "origin":"Yale", "destination": "Airport-JFK", "preferred_car_type":"XL", "preferred_group_size":"4"}
# print_data(requests.post(url, json=data))

### Example of getting request status for given user 
# url = base_url+'get-request-status'
# header = {'api-key' : 'a333b39d-6ff7-4e54-9488-b8ec66d7a39d'}
# data = {'netId': 'ds2496'}
# print_data(requests.post(url, headers=header, json=data))


### Example of running match algo
# url = base_url+'run-algo'
# header = {'api-key' : '8d6dadde-3d6f-450d-bb5d-df8fa6005982'}
# print(requests.get(url, headers=header))

### Example of checking if a user is registered 
# url = base_url+'is-registered'
# header = {'api-key' : 'a333b39d-6ff7-4e54-9488-b8ec66d7a39d'}
# data = {'netId': 'oka5'}
# print_data(requests.post(url, headers=header, json=data))

### Example of confirming a match
# url = base_url+'confirm-match'
# header = {'api-key' : 'a333b39d-6ff7-4e54-9488-b8ec66d7a39d'}
# data = {'netId': 'ds2496', 'requestId': '12305403-418f-4121-a2cd-f49a69ff0c50'}
# print_data(requests.post(url, headers=header, json=data))

### Example of declining a match
# url = base_url+'decline-match'
# header = {'api-key' : 'a333b39d-6ff7-4e54-9488-b8ec66d7a39d'}
# data = {'netId': 'jgt37', 'requestId': '490bc3b6-e68b-41a7-bac3-c513955bfb3e'}
# print_data(requests.post(url, headers=header, json=data))

## Example of canceling a request
url = base_url+'cancel-request'
header = {'api-key' : 'a333b39d-6ff7-4e54-9488-b8ec66d7a39d'}
data = {'netId': 'jgt37', 'requestId': '18342f81-9bf7-4141-a05b-725645997b0d'}
print_data(requests.post(url, headers=header, json=data))

### Example of getting group info
# url = base_url+'get-group-info'
# header = {'api-key' : 'a333b39d-6ff7-4e54-9488-b8ec66d7a39d'}
# data = {'groupId': '123'}
# print_data(requests.post(url, headers=header, json=data))