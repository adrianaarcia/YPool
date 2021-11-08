import random
import datetime as dt
import copy
import numpy as np
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from matching.matching import find_matches
from sample_inputs import gen_sample_input

def test_find_matches():
    n = 50
    s = dt.date(2021, 1, 1)
    e = dt.date(2021, 12, 31)
    sparsity = dt.timedelta(weeks=random.randint(0,16))
    
    inputs = gen_sample_input(n, s, e, sparsity, matched=0)
    tmp = copy.deepcopy(inputs)

    results = find_matches(inputs)

    assert len(results) == len(inputs) #same number of entries
    assert np.array_equal(inputs, tmp) #dont alter original input list

    # check that matched entries are not changed
    inputs = gen_sample_input(n, s, e, sparsity)
    
    matched = [inp for inp in inputs if inp['matched']]
    unmatched = [inp for inp in inputs if not inp['matched']]
    
    r1 = matched + find_matches(unmatched)
    r2 = find_matches(inputs)

    assert len(r1) == len(r2)
    
    #sort by request time
    r1 = sorted(r1, key=lambda i: i['request_time']) 
    r2 = sorted(r2,  key=lambda i: i['request_time'])
    
    #check that only groupId and matched are changed
    for res1, res2 in zip(r1, r2):
        assert res1['netId'] == res2['netId']
        assert res1['date'] == res2['date']
        assert res1['origin'] == res2['origin']
        assert res1['destination'] == res2['destination']
        assert res1['preferred_car_type'] == res2['preferred_car_type']
        assert res1['preferred_group_size'] == res2['preferred_group_size']
        assert res1['requestId'] == res2['requestId']
        assert res1['request_time'] == res2['request_time']
        assert res1['time'] == res2['time']
