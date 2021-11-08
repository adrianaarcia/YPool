import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utility import sort_by_clusters, mode, group_by_cluster, sort_by_group, match_score, group_score, get_stats, print_stats, print_groups, print_results, combine_dt

def test_group_by_cluster1():
	inp = None
	with pytest.raises(TypeError):
		group_by_cluster(inp, inp, inp)

def test_group_by_cluster2():
	inp = 1
	with pytest.raises(TypeError):
		group_by_cluster(inp, inp , inp)

def test_group_by_cluster3():
	inp = [1]
	with pytest.raises(TypeError):
		group_by_cluster(inp, inp , inp)

def test_group_by_cluster4():
	data = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'}
	]

	clusters = [1]
	no_clusters = 2
	d = group_by_cluster(data, clusters , no_clusters)
	assert d[0] == [] and d[1] == [{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'}]

def test_group_by_cluster5():
	data = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'}
	]

	clusters = [1,3]
	no_clusters = 2
	with pytest.raises(IndexError):
		group_by_cluster(data, clusters , no_clusters)

def test_group_by_cluster6():
	data = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'}
	]

	clusters = [1,0,1]
	no_clusters = 2
	d = group_by_cluster(data, clusters , no_clusters)
	assert data[0] in d[1] and data[1] in d[0] and data[2] in d[1]

def test_group_match_score1():
	inp = None
	with pytest.raises(TypeError):
		match_score(inp)

def test_group_match_score2():
	inp = None
	with pytest.raises(TypeError):
		match_score(inp, inp)

def test_group_match_score3():
	inp = 1
	with pytest.raises(TypeError):
		match_score(inp)

def test_group_match_score4():
	inp = 1
	with pytest.raises(TypeError):
		match_score(inp, inp)

def test_group_match_score5():
	data = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'}
	]

	d1 = match_score(data[0], data[1])
	d2 = match_score(data[0], data[2])
	d3 = match_score(data[1], data[2])
	assert d1 == 0.8829024057541068
	assert d2 == 0.9124131944445166
	assert d3 == 0.9343656994048268
	

def test_group_score1():
	inp = None
	with pytest.raises(TypeError):
		group_score(inp)

def test_match_score2():
	inp = 1
	with pytest.raises(TypeError):
		group_score(inp)


def test_match_score3():
	inp = [1]
	out = group_score(inp)
	assert out == 0

def test_match_score4():
	inp = [1,2]
	with pytest.raises(TypeError):
		group_score(inp)
		
def test_group_score5():
	data = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'}
	]

	d = group_score(data)
	assert d == 0.9098937665344834

def test_get_stats1():
	inp = None
	with pytest.raises(TypeError):
		get_stats(inp)

def test_get_stats2():
	inp = 1
	with pytest.raises(TypeError):
		get_stats(inp)

def test_get_stats3():
	data = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'}
	]
	out = get_stats(data)
	assert out == {'No. matched': 0, 'No. groups': 0, 'Avg. group score': '0%', 'Avg. group size': 0, 'Match rate': 0}

def test_get_stats4():
	data = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'}
	]
	out = get_stats(data)
	assert out == {'No. matched': 1, 'No. groups': 1, 'Avg. group score': '0.0%', 'Avg. group size': 1.0, 'Match rate': 33.33333333333333}

def test_get_stats5():
	data = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': False, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'}
	]
	out = get_stats(data)
	assert out == {'No. matched': 2, 'No. groups': 1, 'Avg. group score': '91.24%', 'Avg. group size': 2.0, 'Match rate': 66.66666666666666}

def test_get_stats6():
	data = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'}
	]
	out = get_stats(data)
	assert out == {'No. matched': 3, 'No. groups': 1, 'Avg. group score': '90.99%', 'Avg. group size': 3.0, 'Match rate': 100.0}

def test_print_stats1():
	inp = None
	with pytest.raises(TypeError):
		print_stats(inp)

def test_print_stats2():
	inp = 1
	with pytest.raises(TypeError):
		print_stats(inp)

def test_print_stats3(capfd):
	data = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'}
	]
	out = get_stats(data)
	print_stats(out)
	out1, err = capfd.readouterr()
	assert out1 == "\nNo. matched: 3\nNo. groups: 1\nAvg. group score: 90.99%\nAvg. group size: 3.0\nMatch rate: 100.0%\n"

def test_print_groups1():
	inp = None
	with pytest.raises(TypeError):
		print_groups(inp)

def test_print_groups2():
	inp = 1
	with pytest.raises(TypeError):
		print_groups(inp)

def test_print_groups3(capfd):
	data = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '2', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '2', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '2', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'}
	]
	print_groups(data)
	out1, err = capfd.readouterr()
	assert out1 == "Group ID: 2\nGroup score: 90.99%\nnet ID: abc0, date/time: 2021-04-23 00:48, origin: Yale, destination: Airport-JFK, pref. group size: 3, pref. car type: regular\nnet ID: abc1, date/time: 2021-04-23 19:48, origin: Yale, destination: Airport-JFK, pref. group size: 4, pref. car type: regular\nnet ID: abc2, date/time: 2021-04-23 10:48, origin: Yale, destination: Airport-JFK, pref. group size: 5, pref. car type: regular\n\n\n"

def test_print_results1(capfd):
	inp = None
	with pytest.raises(TypeError):
		print_results(inp)
	out1, err = capfd.readouterr()
	assert out1 == "Summary:\n--------------------------------"


def test_print_groups2(capfd):
	inp = 1
	with pytest.raises(TypeError):
		print_results(inp)
	out1, err = capfd.readouterr()
	assert out1 == "Summary:\n--------------------------------"

def test_print_results3(capfd):
	data = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '2', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'},
	{'netId': 'abc1', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '2', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '4', 'requestId': 'this-is-a-test-req-id-1', 'request_time': '2021-04-23 02:41:19', 'time': '19:48'},
	{'netId': 'abc2', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '2', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '5', 'requestId': 'this-is-a-test-req-id-2', 'request_time': '2021-04-23 02:41:19', 'time': '10:48'}
	]
	print_results(data)
	out1, err = capfd.readouterr()
	assert out1 == "Summary:\n--------------------------------\nNo. matched: 3\nNo. groups: 1\nAvg. group score: 90.99%\nAvg. group size: 3.0\nMatch rate: 100.0%\n\nGroups\n--------------------------------\nGroup ID: 2\nGroup score: 90.99%\nnet ID: abc0, date/time: 2021-04-23 00:48, origin: Yale, destination: Airport-JFK, pref. group size: 3, pref. car type: regular\nnet ID: abc1, date/time: 2021-04-23 19:48, origin: Yale, destination: Airport-JFK, pref. group size: 4, pref. car type: regular\nnet ID: abc2, date/time: 2021-04-23 10:48, origin: Yale, destination: Airport-JFK, pref. group size: 5, pref. car type: regular\n\n\n--------------------------------\n"
	
def test_combine_dt1():
	inp = None
	with pytest.raises(TypeError):
		combine_dt(inp)

def test_combine_dt2():
	inp = 1
	with pytest.raises(TypeError):
		combine_dt(inp)

def test_combine_dt3():
	data = [
	{'netId': 'abc0', 'date': '2021-04-23', 'origin': 'Yale', 'destination': 'Airport-JFK', 'groupId': '2', 'matched': True, 'preferred_car_type': 'regular', 'preferred_group_size': '3', 'requestId': 'this-is-a-test-req-id-0', 'request_time': '2021-04-23 02:41:19', 'time': '00:48'}]
	d1 = combine_dt(data[0]['date'], data[0]['time'])
	assert str(d1) == "2021-04-23 00:48:00"

def test_mode1():
	inp = None
	with pytest.raises(TypeError):
		mode(inp)

def test_mode2():
	inp = 1
	with pytest.raises(TypeError):
		mode(inp)

def test_mode3():
	inp = 1,2
	d = mode(inp)
	assert d == 1

def test_mode4():
	inp = 1,2,2
	d = mode(inp)
	assert d == 2


#test sort by clusters







