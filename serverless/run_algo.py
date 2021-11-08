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


url = base_url+'run-algo'
header = {'api-key' : '8d6dadde-3d6f-450d-bb5d-df8fa6005982'}
print(requests.get(url, headers=header))