import datetime as dt
import random
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utility import combine_dt
from sample_inputs import gen_sample_input, gen_request, random_dt_in_range, gen_random_datetime, locs

@pytest.fixture
def req_format():
    example = {'netId': 'abc0', 'date': '2021-04-22', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-19 13:16:33', 'time': '01:32'}
    return example


# gen_random_datetime()
def test_gen_random_datetime():
    iter = 100
    for _ in range(iter):
        r = gen_random_datetime()
        assert type(r) is dt.datetime 
    

# random_dt_in_range()
# #src: https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
def test_random_dt_in_range():
    iter = 100
    for _ in range(iter):
        #generate random dates
        d1 = gen_random_datetime()
        d2 = gen_random_datetime()

        s = min(d1,d2) #start dt
        e = max(d1,d2) #end dt

        rdt = random_dt_in_range(s,e)

        #check type and that it is in range
        assert type(rdt) is dt.datetime
        assert rdt >= s
        assert rdt <= e


# check_format compares a request to the format as given by pytest fixture req_format
def check_format(req_format, req):
    #check type
    assert type(req) is dict

    #check keys
    assert req.keys() == req_format.keys()
    
    #check entries
    assert dt.datetime.strptime(req['date'], '%Y-%m-%d') #date
    assert dt.datetime.strptime(req['time'], '%H:%M') #time
    assert req['origin'] in locs and req['destination'] in locs and req['origin'] != req['destination']
    assert req['groupId'] == '' or req['groupId'] == 'TEST-UUID'
    assert req['matched'] is True or req['matched'] is False
    assert req['preferred_car_type'] in ['Regular', 'XL'] #car type
    assert req['preferred_group_size'] in ['2','3','4','5'] #group size
    assert dt.datetime.strptime(req['request_time'], '%Y-%m-%d %H:%M:%S') #request time

# gen_request()
def test_gen_request(req_format):
    req_id = random.randint(0, sys.maxsize)
    
    #generate random dates
    d1 = gen_random_datetime()
    d2 = gen_random_datetime()

    s = min(d1,d2) #start dt
    e = max(d1,d2) #end dt

    req = gen_request(req_id, s, e)

    check_format(req_format, req)
    assert req['requestId'] == f'this-is-a-test-req-id-{req_id}' #request id

# gen_sample_input()
def test_gen_sample_input(req_format):
    n = random.randrange(1, 200)
    s = dt.date(2021, 1, 1)
    e = dt.date(2021, 12, 31)

    sample = gen_sample_input(n, s, e)
    
    for req in sample:
        assert len(sample) == n
        check_format(req_format, req)
    
    # test sparsity
    sparsity = random.randrange(1, 52)
    sample = gen_sample_input(n,s,e,sparsity)
    dts = sorted([combine_dt(i['date'], i['time']) for i in sample])
    
    assert abs(dts[-1] - dts[0]) < dt.timedelta(weeks=sparsity)

    # test origin and destination
    sample = gen_sample_input(n, s, e, orig="Testing", dest="123")
    for req in sample: 
        assert req['origin'] == 'Testing'
        assert req['destination'] == '123'
    
    # test matched
    sample = gen_sample_input(n, s, e, matched=0)
    for req in sample:
        assert not req['matched']
    
    sample = gen_sample_input(n,s,e, matched=1)
    for req in sample:
        assert req['matched']

    
