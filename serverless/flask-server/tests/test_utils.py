import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import (
    generate_pairs,
    sort_by_group,
)


def test_get_generate_pairs_many():
    location_list = ["JFK", "JFK", "BDL", "BDL", "Yale"]
    mappings = generate_pairs(location_list)
    assert mappings == [('JFK', 2), ('BDL', 2), ('Yale', 1)]


def test_get_generate_pairs_one():
    location_list = ["JFK"]
    mappings = generate_pairs(location_list)
    assert mappings == [('JFK', 1)]


def test_get_generate_pairs_empty():
    location_list = []
    mappings = generate_pairs(location_list)
    assert mappings == []


def test_sort_by_group_unmatched():
    sample_items = [
        {'netId': 'abc0', 'date': '2021-04-22', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '123', 'matched': False, 'preferred_car_type': 'regular',
            'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-19 13:16:33', 'time': '01:32'},
        {'netId': 'abc1', 'date': '2021-04-20', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '321', 'matched': False, 'preferred_car_type': 'XL',
            'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-20 10:59:47', 'time': '08:18'},
        {'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '123', 'matched': False, 'preferred_car_type': 'regular',
            'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-24 07:51:59', 'time': '11:52'},
        {'netId': 'abc3', 'date': '2021-04-22', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '321', 'matched': False, 'preferred_car_type': 'XL',
            'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-3', 'request_time': '2021-04-18 20:09:56', 'time': '02:19'},
        {'netId': 'abc4', 'date': '2021-04-22', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '123', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-4', 'request_time': '2021-04-19 04:22:44', 'time': '09:01'}]
    groups = sort_by_group(sample_items)
    assert groups == []


def test_sort_by_group_matched():
    sample_items = [
        {'netId': 'abc0', 'date': '2021-04-22', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '123', 'matched': True, 'preferred_car_type': 'regular',
            'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-19 13:16:33', 'time': '01:32'},
        {'netId': 'abc1', 'date': '2021-04-20', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '321', 'matched': True, 'preferred_car_type': 'XL',
            'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-20 10:59:47', 'time': '08:18'},
        {'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '123', 'matched': True, 'preferred_car_type': 'regular',
            'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-24 07:51:59', 'time': '11:52'},
        {'netId': 'abc3', 'date': '2021-04-22', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '321', 'matched': True, 'preferred_car_type': 'XL',
            'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-3', 'request_time': '2021-04-18 20:09:56', 'time': '02:19'},
        {'netId': 'abc4', 'date': '2021-04-22', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '123', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-4', 'request_time': '2021-04-19 04:22:44', 'time': '09:01'}]
    groups = sort_by_group(sample_items)
    assert groups == [['abc0', 'abc2', 'abc4'], ['abc1', 'abc3']]
