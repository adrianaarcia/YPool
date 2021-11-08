import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from greedy import dynamic_greedy_matching, greedy_matching, greedy_util


def test_greedy_util1():
	inp = None
	with pytest.raises(TypeError):
		greedy_util(inp)

def test_greedy_util2():
	inp = 1
	with pytest.raises(TypeError):
		greedy_util(inp)

def test_greedy_util3():
	inp = 1,2
	with pytest.raises(TypeError):
		greedy_util(inp)

def test_greedy_util4():
	inp = [1]
	out1, out2 = greedy_util(inp)
	assert out1 == 0 and out2 == []

def test_greedy_util5():
	inp = [1,2]
	with pytest.raises(TypeError):
		greedy_util(inp)

def test_greedy_util6():
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'}
	]
	val, out = greedy_util(inp)
	assert len(out) == 0

def test_greedy_util7():
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'}
	]
	val, out = greedy_util(inp)
	out == []

def test_greedy_util8():
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'}
	]
	val, out = greedy_util(inp)
	assert val == 0

def test_greedy_util9():
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'}
	]
	val, out = greedy_util(inp)
	assert out == []

def test_greedy_util10():
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'}
	]
	val, out = greedy_util(inp)
	assert val > 0 and val <= 1

def test_greedy_util11():
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'}
	]
	val, out = greedy_util(inp)
	assert len(out) == 3

def test_greedy_util12():
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'}
	]
	val, out = greedy_util(inp)
	out == ['abc1', 'abc2', 'abc0']

def test_greedy_util13():
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'}
	]
	out, lst = greedy_util(inp)
	assert out == 1

def test_greedy_util14():
	# 1 week apart
	inp = [
	{'netId': 'abc0', 'date': '2021-04-16', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc2', 'date': '2021-04-30', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'}
	]
	out, lst = greedy_util(inp)
	assert out == 0.500000000001424

def test_greedy_matching1():
	inp = None
	with pytest.raises(TypeError):
		greedy_matching(inp)

def test_greedy_matching2():
	inp = 1
	with pytest.raises(TypeError):
		greedy_matching(inp)

def test_greedy_matching3():
	inp = 1,2
	with pytest.raises(TypeError):
		greedy_matching(inp)

def test_greedy_matching4():
	inp = [1]
	with pytest.raises(TypeError):
		greedy_matching(inp)

def test_greedy_matching5():
	inp = [1,2]
	with pytest.raises(TypeError):
		greedy_matching(inp)

def test_greedy_matching6():
	thres = 0.935
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'}
	]
	out = greedy_matching(inp, thres)
	assert len(out) == len(inp)

def test_greedy_matching7():
	thres = 0.935
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'}
	]
	out = greedy_matching(inp, thres)
	assert out[0]['matched'] == False

def test_greedy_matching8():
	thres = 0.935
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'}
	]
	out = greedy_matching(inp, thres)
	assert out[0]['matched'] == True

def test_greedy_matching9():
	# 1 item a day apart
	thres = 0.935
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-22', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'}
	]
	out = greedy_matching(inp, thres)
	assert out[0]['matched'] == False

def test_greedy_matching10():
	# Same day, different times, want different group sizes
	thres = 0.935
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'}
	]
	out = greedy_matching(inp, thres)
	assert out[0]['matched'] == False

def test_greedy_matching11():
	# Same day, within 5 hours of each other, want different group sizes
	thres = 0.935
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '06:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '11:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '16:48'}
	]
	out = greedy_matching(inp, thres)
	assert out[0]['matched'] == False

def test_greedy_matching12():
	# Same day, within 4 hours of each other, want different group sizes
	thres = 0.935
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '06:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '14:48'}
	]
	out = greedy_matching(inp, thres)
	no_true = 0
	for i in out:
		if i['matched'] == True:
			no_true += 1
	assert no_true == 3

def test_greedy_matching13():
	# Same day, within 4 hours of each other, want different group sizes, mode =5, expect 4 matching
	thres = 0.935
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '06:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '14:48'},
	{'netId': 'abc3', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-3', 'request_time': '2021-04-23 02:41:19', 'time': '12:48'},
	{'netId': 'abc4', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-4', 'request_time': '2021-04-23 02:41:19', 'time': '08:48'}
	]
	out = greedy_matching(inp, thres)
	no_true = 0
	for i in out:
		if i['matched'] == True:
			no_true += 1
	assert no_true == 4

def test_greedy_matching14():
	# Same day, within 4 hours of each other, want different group sizes, 2 fours, 2 fives, 1 3 expect 4matching
	thres = 0.935
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '06:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '14:48'},
	{'netId': 'abc3', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '12:48'},
	{'netId': 'abc4', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '08:48'}
	]
	out = greedy_matching(inp, thres)
	no_true = 0
	for i in out:
		if i['matched'] == True:
			no_true += 1
	assert no_true == 4

def test_greedy_matching15():
	#Important
	# Same day, within 4 hours of each other, want different group sizes expect a matching of 5
	thres = 0.935
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '06:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '14:48'},
	{'netId': 'abc3', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-3', 'request_time': '2021-04-23 02:41:19', 'time': '12:48'},
	{'netId': 'abc4', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-4', 'request_time': '2021-04-23 02:41:19', 'time': '08:48'}
	]
	out = greedy_matching(inp, thres)
	no_true = 0
	for i in out:
		if i['matched'] == True:
			no_true += 1
	assert no_true == 3

def test_greedy_matching16():
	#Important
	# Same day, within 4 hours of each other, 5 people, all want 4, expect 4
	thres = 0.935
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '06:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '14:48'},
	{'netId': 'abc3', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-3', 'request_time': '2021-04-23 02:41:19', 'time': '12:48'},
	{'netId': 'abc4', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-4', 'request_time': '2021-04-23 02:41:19', 'time': '08:48'}
	]
	out = greedy_matching(inp, thres)
	no_true = 0
	for i in out:
		if i['matched'] == True:
			no_true += 1
	assert no_true == 4

def test_greedy_matching17():
	# Same day, within 4 hours of each other, want different group sizes, mode =5, expect 5 matching
	thres = 0.935
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '06:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '14:48'},
	{'netId': 'abc3', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-3', 'request_time': '2021-04-23 02:41:19', 'time': '12:48'},
	{'netId': 'abc4', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-4', 'request_time': '2021-04-23 02:41:19', 'time': '08:48'}
	]
	out = greedy_matching(inp, thres)
	no_true = 0
	for i in out:
		if i['matched'] == True:
			no_true += 1
	assert no_true == 5

def test_greedy_matching18():
	# Same day, within 4 hours of each other, want different group sizes, mode =5, expect 5 matching
	thres = 0.935
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '06:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '14:48'},
	{'netId': 'abc3', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-3', 'request_time': '2021-04-23 02:41:19', 'time': '12:48'},
	{'netId': 'abc4', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-4', 'request_time': '2021-04-23 02:41:19', 'time': '08:48'}
	]
	out = greedy_matching(inp, thres)
	no_true = 0
	for i in out:
		if i['matched'] == True:
			no_true += 1
	assert no_true == 5


def test_dynamic_greedy_matching18():
	# Same day, within 4 hours of each other, want different group sizes, mode =5, expect 5 matching
	thres = 0.935
	inp = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '06:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '14:48'},
	{'netId': 'abc3', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-3', 'request_time': '2021-04-23 02:41:19', 'time': '12:48'},
	{'netId': 'abc4', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-4', 'request_time': '2021-04-23 02:41:19', 'time': '08:48'}
	]
	out1 = greedy_matching(inp, thres)
	out2 = dynamic_greedy_matching([inp])
	for i in range(len(out1)):
		assert out1[i]['matched'] == out2[i]['matched']


