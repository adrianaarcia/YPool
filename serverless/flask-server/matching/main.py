from matching.matching import find_matches
from matching.sample_inputs import gen_sample_input
#from utility import print_results

import datetime as dt
import json
import requests

def main():
	sample_input = gen_sample_input(50, dt.date(2021,4,30), dt.date(2021,4,30), orig="Yale", dest="Airport-JFK", matched=0)
	results = find_matches(sample_input)

	base_url = "https://yalepool.com/"
	api_key = 'a333b39d-6ff7-4e54-9488-b8ec66d7a39d' 
	header = {'api-key' : api_key} 
	
	
	for req in results:
		#register user
		url = base_url+'users'
		data = {'netId': req['netId'], "first_name":"Test", "last_name":"Account","email":"test.123@yale.edu"} #register user
		print(requests.post(url, headers=header, json=data))
		
		#submit requests
		url = base_url+'ride-request'
		print(requests.post(url, headers=header, json=req))

		pass

if __name__ == '__main__':
    main()
